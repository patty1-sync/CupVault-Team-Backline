# ⚽ CupVault

CupVault is a centralized platform for exploring historical FIFA World Cup data. It brings together team records, player statistics, match results, and tournament history into one searchable, user-friendly application — built for fans, analysts, bettors, and database administrators.

## Team Backline

| Name | Email |
|------|-------|
| Patrick Schick (Point Person) | schick.p@northeastern.edu |
| Esteban Gómez Perdomo | gomezperdomo.e@northeastern.edu |
| Mark Abousleiman | abousleiman.m@northeastern.edu |
| Jose Armando Guerrero | guerrerotoro.j@northeastern.edu |

## Demo Video

[Watch our pitch and demo video here](PASTE_YOUR_VIDEO_LINK_HERE)

## Getting Started

### Prerequisites
- Docker and Docker Compose installed
- Git

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/patty1-sync/CupVault-Team-Backline.git
   cd CupVault-Team-Backline
   ```

2. Create the `.env` file in the `api/` folder. Copy the template and fill in your password:
   ```bash
   cp api/.env.template api/.env
   ```
   Then open `api/.env` and set the following values:
   ```
   SECRET_KEY=<any-random-string>
   DB_USER=root
   DB_HOST=db
   DB_PORT=3306
   DB_NAME=ngo_db
   MYSQL_ROOT_PASSWORD=<your-password>
   ```

3. Start all services:
   ```bash
   docker compose up -d
   ```

4. The app will be available at:
   - **Streamlit UI**: http://localhost:8501
   - **Flask API**: http://localhost:4000

### Rebuilding the Database

If you make changes to the SQL files in `database-files/`, you need to recreate the database container:
```bash
docker compose down db -v && docker compose up db -d
```

## Project Overview

### User Roles

- **Fan (Jason)** — Browse team World Cup history, look up player goal records, view match brackets, and manage a favorites list.
- **Sports Analyst (Maria)** — Filter player stats across tournaments, view top scorers, and create/edit scouting notes.
- **Sports Bettor (Andrew)** — Explore yellow card and penalty data, compare head-to-head team records, and analyze goals-per-game trends.
- **Database Admin (Jake)** — Add, edit, and delete records across all tables, view the audit log, and run data integrity checks.

### Tech Stack

- **Frontend**: Streamlit (Python)
- **Backend**: Flask REST API (Python)
- **Database**: MySQL 8
- **Containerization**: Docker & Docker Compose
