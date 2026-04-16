from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for user routes
users = Blueprint("users", __name__)


# GET /favorites/<user_id> — saved favorites [Jason-4]
@users.route("/favorites/<int:user_id>", methods=["GET"])
def get_favorites(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT t.team_id, t.team_name, t.fifa_code
            FROM fav_team ft
            JOIN Team t ON ft.team_id = t.team_id
            WHERE ft.user_id = %s
        """
        cursor.execute(query, (user_id,))
        fav_teams = cursor.fetchall()

        query = """
            SELECT p.player_id, p.first_name, p.last_name, t.team_name
            FROM fav_player fp
            JOIN Player p ON fp.player_id = p.player_id
            LEFT JOIN Team t ON p.nationality_team_id = t.team_id
            WHERE fp.user_id = %s
        """
        cursor.execute(query, (user_id,))
        fav_players = cursor.fetchall()

        return jsonify({"favorite_teams": fav_teams, "favorite_players": fav_players}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# POST /favorites/<user_id> — add a favorite [Jason-4]
# Body: {"type": "team", "id": 1} or {"type": "player", "id": 2}
@users.route("/favorites/<int:user_id>", methods=["POST"])
def add_favorite(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        fav_type = data.get("type")
        fav_id = data.get("id")

        if not fav_type or not fav_id:
            return jsonify({"error": "Missing type and id"}), 400

        if fav_type == "team":
            query = "INSERT INTO fav_team (user_id, team_id) VALUES (%s, %s)"
            cursor.execute(query, (user_id, fav_id))
        elif fav_type == "player":
            query = "INSERT INTO fav_player (user_id, player_id) VALUES (%s, %s)"
            cursor.execute(query, (user_id, fav_id))
        else:
            return jsonify({"error": "type must be 'team' or 'player'"}), 400

        get_db().commit()
        return jsonify({"message": f"Favorite {fav_type} added"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# DELETE /favorites/<user_id> — remove a favorite [Jason-4]
# Body: {"type": "team", "id": 1} or {"type": "player", "id": 2}
@users.route("/favorites/<int:user_id>", methods=["DELETE"])
def remove_favorite(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        fav_type = data.get("type")
        fav_id = data.get("id")

        if not fav_type or not fav_id:
            return jsonify({"error": "Missing type and id"}), 400

        if fav_type == "team":
            query = "DELETE FROM fav_team WHERE user_id = %s AND team_id = %s"
            cursor.execute(query, (user_id, fav_id))
        elif fav_type == "player":
            query = "DELETE FROM fav_player WHERE user_id = %s AND player_id = %s"
            cursor.execute(query, (user_id, fav_id))
        else:
            return jsonify({"error": "type must be 'team' or 'player'"}), 400

        get_db().commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Favorite not found"}), 404
        return jsonify({"message": f"Favorite {fav_type} removed"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /notes/<user_id> — all scouting notes [Maria-6]
@users.route("/notes/<int:user_id>", methods=["GET"])
def get_notes(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT sn.note_id, sn.note_text, t.team_name,
                   CONCAT(p.first_name, ' ', p.last_name) AS player_name
            FROM ScoutNotes sn
            LEFT JOIN Team t   ON sn.team_id = t.team_id
            LEFT JOIN Player p ON sn.player_id = p.player_id
            WHERE sn.user_id = %s
            ORDER BY sn.note_id DESC
        """
        cursor.execute(query, (user_id,))
        notes = cursor.fetchall()
        return jsonify(notes), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# POST /notes/<user_id> — add a scouting note [Maria-6]
@users.route("/notes/<int:user_id>", methods=["POST"])
def create_note(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        if "note_text" not in data:
            return jsonify({"error": "Missing required field: note_text"}), 400

        query = """
            INSERT INTO ScoutNotes (user_id, team_id, player_id, note_text)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, data.get("team_id"), data.get("player_id"), data["note_text"]))
        get_db().commit()
        return jsonify({"message": "Note created", "note_id": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /notes/detail/<note_id> — one note [Maria-6]
@users.route("/notes/detail/<int:note_id>", methods=["GET"])
def get_note(note_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = "SELECT * FROM ScoutNotes WHERE note_id = %s"
        cursor.execute(query, (note_id,))
        note = cursor.fetchone()
        if not note:
            return jsonify({"error": "Note not found"}), 404
        return jsonify(note), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# PUT /notes/detail/<note_id> — update a note [Maria-6]
@users.route("/notes/detail/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        query = "SELECT note_id FROM ScoutNotes WHERE note_id = %s"
        cursor.execute(query, (note_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Note not found"}), 404

        allowed_fields = ["note_text", "team_id", "player_id"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(note_id)
        query = f"UPDATE ScoutNotes SET {', '.join(update_fields)} WHERE note_id = %s"
        cursor.execute(query, params)
        get_db().commit()
        return jsonify({"message": "Note updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# DELETE /notes/detail/<note_id> — delete a note [Maria-6]
@users.route("/notes/detail/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = "SELECT note_id FROM ScoutNotes WHERE note_id = %s"
        cursor.execute(query, (note_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Note not found"}), 404

        query = "DELETE FROM ScoutNotes WHERE note_id = %s"
        cursor.execute(query, (note_id,))
        get_db().commit()
        return jsonify({"message": "Note deleted"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()