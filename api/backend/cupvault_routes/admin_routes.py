from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for admin routes
admin = Blueprint("admin", __name__)


# GET /tournaments — all tournaments [Maria-2]
@admin.route("/tournaments", methods=["GET"])
def get_tournaments():
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT tr.tourney_id, tr.year, tr.host_country,
                   t.team_name AS champion
            FROM Tournament tr
            LEFT JOIN Team t ON tr.champ_team_id = t.team_id
            ORDER BY tr.year DESC
        """
        cursor.execute(query)
        tournaments = cursor.fetchall()
        return jsonify(tournaments), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /tournaments/<id> — one tournament [Jake-4]
@admin.route("/tournaments/<int:tourney_id>", methods=["GET"])
def get_tournament(tourney_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT tr.tourney_id, tr.year, tr.host_country,
                   t.team_name AS champion
            FROM Tournament tr
            LEFT JOIN Team t ON tr.champ_team_id = t.team_id
            WHERE tr.tourney_id = %s
        """
        cursor.execute(query, (tourney_id,))
        tournament = cursor.fetchone()
        if not tournament:
            return jsonify({"error": "Tournament not found"}), 404
        return jsonify(tournament), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# POST /tournaments — add a tournament [Jake-1]
@admin.route("/tournaments", methods=["POST"])
def create_tournament():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        required_fields = ["host_country", "year"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        query = """
            INSERT INTO Tournament (host_country, year, champ_team_id)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (data["host_country"], data["year"], data.get("champ_team_id")))
        get_db().commit()
        return jsonify({"message": "Tournament created", "tourney_id": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# PUT /tournaments/<id> — update a tournament [Jake-2]
@admin.route("/tournaments/<int:tourney_id>", methods=["PUT"])
def update_tournament(tourney_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        query = "SELECT tourney_id FROM Tournament WHERE tourney_id = %s"
        cursor.execute(query, (tourney_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Tournament not found"}), 404

        allowed_fields = ["host_country", "year", "champ_team_id"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(tourney_id)
        query = f"UPDATE Tournament SET {', '.join(update_fields)} WHERE tourney_id = %s"
        cursor.execute(query, params)
        get_db().commit()
        return jsonify({"message": "Tournament updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# GET /audit-log — recent changes [Jake-4]
@admin.route("/audit-log", methods=["GET"])
def get_audit_log():
    cursor = get_db().cursor(dictionary=True)
    try:
        table_name = request.args.get("table_name")
        action_type = request.args.get("action_type")

        query = """
            SELECT al.log_id, al.changed_at, al.action_type,
                   al.table_name, al.record_id, al.changed_by
            FROM AuditLog al
            WHERE 1=1
        """
        params = []

        if table_name:
            query += " AND al.table_name = %s"
            params.append(table_name)
        if action_type:
            query += " AND al.action_type = %s"
            params.append(action_type)

        query += " ORDER BY al.changed_at DESC LIMIT 50"
        cursor.execute(query, params)
        logs = cursor.fetchall()
        return jsonify(logs), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()