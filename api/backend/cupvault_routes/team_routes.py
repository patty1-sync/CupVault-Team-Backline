from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error



# Create a Blueprint for team routes
teams = Blueprint("teams", __name__)

# GET /teams — all teams with titles won [Jason-1], [Andrew-1]
@teams.route("/teams", methods=["GET"])
def get_teams():
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT t.team_id, t.team_name, t.fifa_code, t.federation,
                   COUNT(tr.tourney_id) AS titles_won
            FROM Team t
            LEFT JOIN Tournament tr ON tr.champ_team_id = t.team_id
            GROUP BY t.team_id, t.team_name, t.fifa_code, t.federation
            ORDER BY titles_won DESC
        """
        cursor.execute(query)
        teams = cursor.fetchall()
        return jsonify(teams), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 
 
# GET /teams/<id> — one team's info [Jason-1], [Andrew-3]
@teams.route("/teams/<int:team_id>", methods=["GET"])
def get_team(team_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = "SELECT * FROM Team WHERE team_id = %s"
        cursor.execute(query, (team_id,))
        team = cursor.fetchone()
        if not team:
            return jsonify({"error": "Team not found"}), 404
        return jsonify(team), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 
 
# POST /teams — add a new team [Jake-1]
@teams.route("/teams", methods=["POST"])
def create_team():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
 
        required_fields = ["team_name", "fifa_code"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
 
        query = """
            INSERT INTO Team (team_name, fifa_code, federation)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (data["team_name"], data["fifa_code"], data.get("federation")))
        get_db().commit()
        return jsonify({"message": "Team created", "team_id": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 
 
# PUT /teams/<id> — update a team [Jake-2]
@teams.route("/teams/<int:team_id>", methods=["PUT"])
def update_team(team_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
 
        query = "SELECT team_id FROM Team WHERE team_id = %s"
        cursor.execute(query, (team_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Team not found"}), 404
 
        allowed_fields = ["team_name", "fifa_code", "federation"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]
 
        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400
 
        params.append(team_id)
        query = f"UPDATE Team SET {', '.join(update_fields)} WHERE team_id = %s"
        cursor.execute(query, params)
        get_db().commit()
        return jsonify({"message": "Team updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 
 
# GET /players — all players, optional filter by team_id [Jason-2], [Maria-2], [Maria-3]
@teams.route("/players", methods=["GET"])
def get_players():
    cursor = get_db().cursor(dictionary=True)
    try:
        team_id = request.args.get("team_id")
 
        if team_id:
            query = """
                SELECT p.player_id, p.first_name, p.last_name,
                       p.prim_position, p.birth_date, t.team_name
                FROM Player p
                LEFT JOIN Team t ON p.nationality_team_id = t.team_id
                WHERE p.nationality_team_id = %s
                ORDER BY p.last_name
            """
            cursor.execute(query, (team_id,))
        else:
            query = """
                SELECT p.player_id, p.first_name, p.last_name,
                       p.prim_position, p.birth_date, t.team_name
                FROM Player p
                LEFT JOIN Team t ON p.nationality_team_id = t.team_id
                ORDER BY p.last_name
            """
            cursor.execute(query)
 
        players = cursor.fetchall()
        return jsonify(players), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 
 
# POST /players — add a new player [Jake-1]
@teams.route("/players", methods=["POST"])
def create_player():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
 
        required_fields = ["first_name", "last_name"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
 
        query = """
            INSERT INTO Player (first_name, last_name, prim_position, birth_date, nationality_team_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data["first_name"], data["last_name"],
            data.get("prim_position"), data.get("birth_date"), data.get("nationality_team_id")
        ))
        get_db().commit()
        return jsonify({"message": "Player created", "player_id": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 
 
# GET /players/<id> — one player's profile [Jason-2]
@teams.route("/players/<int:player_id>", methods=["GET"])
def get_player(player_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT p.player_id, p.first_name, p.last_name,
                   p.prim_position, p.birth_date, t.team_name
            FROM Player p
            LEFT JOIN Team t ON p.nationality_team_id = t.team_id
            WHERE p.player_id = %s
        """
        cursor.execute(query, (player_id,))
        player = cursor.fetchone()
        if not player:
            return jsonify({"error": "Player not found"}), 404
        return jsonify(player), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()