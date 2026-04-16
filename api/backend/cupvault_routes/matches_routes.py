from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for match routes
matches = Blueprint("matches", __name__)


# GET /matches — all matches, optional filters [Andrew-3]
@matches.route("/matches", methods=["GET"])
def get_matches():
    cursor = get_db().cursor(dictionary=True)
    try:
        team_id = request.args.get("team_id")
        tournament_id = request.args.get("tournament_id")

        query = """
            SELECT m.match_id, tr.year, m.stage, m.match_date,
                   home.team_name AS home_team, m.home_score,
                   m.away_score, away.team_name AS away_team, m.status
            FROM `Match` m
            JOIN Tournament tr ON m.tournament_id = tr.tourney_id
            JOIN Team home     ON m.home_team_id = home.team_id
            JOIN Team away     ON m.away_team_id = away.team_id
            WHERE 1=1
        """
        params = []

        if team_id:
            query += " AND (m.home_team_id = %s OR m.away_team_id = %s)"
            params.extend([team_id, team_id])
        if tournament_id:
            query += " AND m.tournament_id = %s"
            params.append(tournament_id)

        query += " ORDER BY m.match_date DESC"
        cursor.execute(query, params)
        matches = cursor.fetchall()
        return jsonify(matches), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /matches/<id> — one match [Andrew-3]
@matches.route("/matches/<int:match_id>", methods=["GET"])
def get_match(match_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT m.match_id, tr.year, m.stage, m.match_date,
                   home.team_name AS home_team, m.home_score,
                   m.away_score, away.team_name AS away_team, m.status
            FROM `Match` m
            JOIN Tournament tr ON m.tournament_id = tr.tourney_id
            JOIN Team home     ON m.home_team_id = home.team_id
            JOIN Team away     ON m.away_team_id = away.team_id
            WHERE m.match_id = %s
        """
        cursor.execute(query, (match_id,))
        match = cursor.fetchone()
        if not match:
            return jsonify({"error": "Match not found"}), 404
        return jsonify(match), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# POST /matches — add a new match [Jake-1]
@matches.route("/matches", methods=["POST"])
def create_match():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        required_fields = ["tournament_id", "stage", "match_date", "home_team_id", "away_team_id"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        query = """
            INSERT INTO `Match` (tournament_id, stage, match_date,
                                 home_team_id, away_team_id, home_score, away_score, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data["tournament_id"], data["stage"], data["match_date"],
            data["home_team_id"], data["away_team_id"],
            data.get("home_score", 0), data.get("away_score", 0),
            data.get("status", "scheduled")
        ))
        get_db().commit()
        return jsonify({"message": "Match created", "match_id": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# PUT /matches/<id> — update a match [Jake-2]
@matches.route("/matches/<int:match_id>", methods=["PUT"])
def update_match(match_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        query = "SELECT match_id FROM `Match` WHERE match_id = %s"
        cursor.execute(query, (match_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Match not found"}), 404

        allowed_fields = ["stage", "match_date", "home_score", "away_score", "status"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(match_id)
        query = f"UPDATE `Match` SET {', '.join(update_fields)} WHERE match_id = %s"
        cursor.execute(query, params)
        get_db().commit()
        return jsonify({"message": "Match updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /match-events — goals, cards, penalties with filters [Maria-2], [Andrew-1], [Andrew-6]
@matches.route("/match-events", methods=["GET"])
def get_match_events():
    cursor = get_db().cursor(dictionary=True)
    try:
        team_id = request.args.get("team_id")
        event_type = request.args.get("event_type")

        query = """
            SELECT me.event_id, me.match_id,
                   CONCAT(p.first_name, ' ', p.last_name) AS player_name,
                   t.team_name, me.minute, me.event_type,
                   me.card_type, me.is_penalty_goal, tr.year
            FROM MatchEvent me
            JOIN Player p      ON me.player_id = p.player_id
            JOIN Team t        ON me.team_id = t.team_id
            JOIN `Match` m     ON me.match_id = m.match_id
            JOIN Tournament tr ON m.tournament_id = tr.tourney_id
            WHERE 1=1
        """
        params = []

        if team_id:
            query += " AND me.team_id = %s"
            params.append(team_id)
        if event_type:
            query += " AND me.event_type = %s"
            params.append(event_type)

        query += " ORDER BY tr.year DESC, me.minute"
        cursor.execute(query, params)
        events = cursor.fetchall()
        return jsonify(events), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# POST /match-events — add a new event [Jake-1]
@matches.route("/match-events", methods=["POST"])
def create_match_event():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        required_fields = ["match_id", "team_id", "player_id", "event_type"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        query = """
            INSERT INTO MatchEvent (match_id, team_id, player_id, minute,
                                    event_type, card_type, is_penalty_goal)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data["match_id"], data["team_id"], data["player_id"],
            data.get("minute"), data["event_type"],
            data.get("card_type"), data.get("is_penalty_goal", 0)
        ))
        get_db().commit()
        return jsonify({"message": "Event created", "event_id": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# PUT /match-events/<id> — update an event [Jake-2]
@matches.route("/match-events/<int:event_id>", methods=["PUT"])
def update_match_event(event_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        query = "SELECT event_id FROM MatchEvent WHERE event_id = %s"
        cursor.execute(query, (event_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Event not found"}), 404

        allowed_fields = ["player_id", "minute", "event_type", "card_type", "is_penalty_goal"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(event_id)
        query = f"UPDATE MatchEvent SET {', '.join(update_fields)} WHERE event_id = %s"
        cursor.execute(query, params)
        get_db().commit()
        return jsonify({"message": "Event updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()