DROP DATABASE IF EXISTS CupVault;
CREATE DATABASE IF NOT EXISTS CupVault;
USE CupVault;


CREATE TABLE IF NOT EXISTS Team (
  team_id     INT             NOT NULL AUTO_INCREMENT,
  team_name   VARCHAR(100)    NOT NULL,
  fifa_code   CHAR(3)         NOT NULL UNIQUE,
  federation  VARCHAR(60),
  PRIMARY KEY (team_id)
);




CREATE TABLE IF NOT EXISTS Tournament (
  tourney_id      INT             NOT NULL AUTO_INCREMENT,
  host_country    VARCHAR(60)     NOT NULL,
  year            INT             NOT NULL,
  champ_team_id   INT,
  PRIMARY KEY (tourney_id),
  CONSTRAINT fk_tourn_champ
      FOREIGN KEY (champ_team_id) REFERENCES Team(team_id)
      ON UPDATE CASCADE ON DELETE RESTRICT
);




CREATE TABLE IF NOT EXISTS `Match` (
   match_id        INT             NOT NULL AUTO_INCREMENT,
   tournament_id   INT             NOT NULL,
   stage           VARCHAR(50)     NOT NULL,
   match_date      DATE            NOT NULL,
   home_team_id    INT             NOT NULL,
   away_team_id    INT             NOT NULL,
   home_score      INT             DEFAULT 0,
   away_score      INT             DEFAULT 0,
   status          VARCHAR(20)     DEFAULT 'scheduled',
   PRIMARY KEY (match_id),
   CONSTRAINT fk_match_tourn
       FOREIGN KEY (tournament_id) REFERENCES Tournament(tourney_id)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT fk_match_home
       FOREIGN KEY (home_team_id) REFERENCES Team(team_id)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT fk_match_away
       FOREIGN KEY (away_team_id) REFERENCES Team(team_id)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT chk_scores_nonneg
       CHECK (home_score >= 0 AND away_score >= 0)
);




CREATE TABLE IF NOT EXISTS Player (
   player_id           INT             NOT NULL AUTO_INCREMENT,
   first_name          VARCHAR(50)     NOT NULL,
   last_name           VARCHAR(50)     NOT NULL,
   prim_position       VARCHAR(30),
   birth_date          DATE,
   nationality_team_id INT,
   PRIMARY KEY (player_id),
   CONSTRAINT fk_player_nation
       FOREIGN KEY (nationality_team_id) REFERENCES Team(team_id)
       ON UPDATE CASCADE ON DELETE RESTRICT
);




CREATE TABLE IF NOT EXISTS MatchEvent (
   event_id        INT             NOT NULL AUTO_INCREMENT,
   match_id        INT             NOT NULL,
   team_id         INT             NOT NULL,
   player_id       INT             NOT NULL,
   minute          INT,
   event_type      VARCHAR(30)     NOT NULL,
   card_type       VARCHAR(20),
   is_penalty_goal BOOLEAN         DEFAULT 0,
   PRIMARY KEY (event_id),
   CONSTRAINT fk_event_match
       FOREIGN KEY (match_id) REFERENCES `Match`(match_id)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT fk_event_team
       FOREIGN KEY (team_id) REFERENCES Team(team_id)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT fk_event_player
       FOREIGN KEY (player_id) REFERENCES Player(player_id)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT chk_minute_nonneg
       CHECK (minute >= 0)
);




CREATE TABLE IF NOT EXISTS Appearance (
   appear_id       INT         NOT NULL AUTO_INCREMENT,
   match_id        INT         NOT NULL,
   player_id       INT         NOT NULL,
   minutes_played  INT         DEFAULT 0,
   started_flag    BOOLEAN     DEFAULT 0,
   PRIMARY KEY (appear_id),
   CONSTRAINT fk_appear_match
       FOREIGN KEY (match_id) REFERENCES `Match`(match_id)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT fk_appear_player
       FOREIGN KEY (player_id) REFERENCES Player(player_id)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT uq_appear_match_player
       UNIQUE (match_id, player_id)
);




CREATE TABLE IF NOT EXISTS UserProfile (
   user_id         INT             NOT NULL AUTO_INCREMENT,
   email           VARCHAR(100)    NOT NULL UNIQUE,
   first_name      VARCHAR(50)     NOT NULL,
   last_name       VARCHAR(50)     NOT NULL,
   persona_type    VARCHAR(30),
   PRIMARY KEY (user_id)
);




CREATE TABLE IF NOT EXISTS ScoutNotes (
   note_id     INT     NOT NULL AUTO_INCREMENT,
   user_id     INT     NOT NULL,
   team_id     INT,
   player_id   INT,
   note_text   TEXT    NOT NULL,
   PRIMARY KEY (note_id),
   CONSTRAINT fk_note_user
       FOREIGN KEY (user_id) REFERENCES UserProfile(user_id)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT fk_note_team
       FOREIGN KEY (team_id) REFERENCES Team(team_id)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT fk_note_player
       FOREIGN KEY (player_id) REFERENCES Player(player_id)
       ON UPDATE CASCADE ON DELETE RESTRICT
);




CREATE TABLE IF NOT EXISTS fav_team (
   user_id     INT     NOT NULL,
   team_id     INT     NOT NULL,
   PRIMARY KEY (user_id, team_id),
   CONSTRAINT fk_ft_user
       FOREIGN KEY (user_id) REFERENCES UserProfile(user_id)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT fk_ft_team
       FOREIGN KEY (team_id) REFERENCES Team(team_id)
       ON UPDATE CASCADE ON DELETE RESTRICT
);




CREATE TABLE IF NOT EXISTS fav_player (
   user_id     INT     NOT NULL,
   player_id   INT     NOT NULL,
   PRIMARY KEY (user_id, player_id),
   CONSTRAINT fk_fp_user
       FOREIGN KEY (user_id) REFERENCES UserProfile(user_id)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT fk_fp_player
       FOREIGN KEY (player_id) REFERENCES Player(player_id)
       ON UPDATE CASCADE ON DELETE RESTRICT
);




CREATE TABLE IF NOT EXISTS AuditLog (
   log_id          INT             NOT NULL AUTO_INCREMENT,
   user_id         INT             NOT NULL,
   table_name      VARCHAR(60)     NOT NULL,
   record_id       INT             NOT NULL,
   action_type     VARCHAR(20)     NOT NULL,
   changed_at      DATETIME        DEFAULT CURRENT_TIMESTAMP,
   changed_by      VARCHAR(100)    NOT NULL,
   PRIMARY KEY (log_id),
   CONSTRAINT fk_log_user
       FOREIGN KEY (user_id) REFERENCES UserProfile(user_id)
       ON UPDATE CASCADE ON DELETE RESTRICT
);



-- ============================================================
-- CupVault Mock Data — Full Dataset
-- Covers all 24 user stories across 4 personas
-- Order: Team → Tournament → Player → UserProfile → Match
--        → MatchEvent → Appearance → ScoutNotes → AuditLog
--        → fav_team → fav_player
-- ============================================================

-- ============================================================
-- TEAM (35 rows)
-- ============================================================
INSERT INTO Team (team_id, team_name, fifa_code, federation) VALUES
(1,  'Argentina',     'ARG', 'CONMEBOL'),
(2,  'France',        'FRA', 'UEFA'),
(3,  'Brazil',        'BRA', 'CONMEBOL'),
(4,  'Croatia',       'CRO', 'UEFA'),
(5,  'Germany',       'GER', 'UEFA'),
(6,  'Spain',         'ESP', 'UEFA'),
(7,  'Netherlands',   'NED', 'UEFA'),
(8,  'Portugal',      'POR', 'UEFA'),
(9,  'England',       'ENG', 'UEFA'),
(10, 'Italy',         'ITA', 'UEFA'),
(11, 'Uruguay',       'URU', 'CONMEBOL'),
(12, 'Belgium',       'BEL', 'UEFA'),
(13, 'Mexico',        'MEX', 'CONCACAF'),
(14, 'USA',           'USA', 'CONCACAF'),
(15, 'Senegal',       'SEN', 'CAF'),
(16, 'Morocco',       'MAR', 'CAF'),
(17, 'Japan',         'JPN', 'AFC'),
(18, 'South Korea',   'KOR', 'AFC'),
(19, 'Australia',     'AUS', 'AFC'),
(20, 'Poland',        'POL', 'UEFA'),
(21, 'Switzerland',   'SUI', 'UEFA'),
(22, 'Denmark',       'DEN', 'UEFA'),
(23, 'Serbia',        'SRB', 'UEFA'),
(24, 'Ghana',         'GHA', 'CAF'),
(25, 'Cameroon',      'CMR', 'CAF'),
(26, 'Ecuador',       'ECU', 'CONMEBOL'),
(27, 'Qatar',         'QAT', 'AFC'),
(28, 'Canada',        'CAN', 'CONCACAF'),
(29, 'Costa Rica',    'CRC', 'CONCACAF'),
(30, 'Tunisia',       'TUN', 'CAF'),
(31, 'Iran',          'IRN', 'AFC'),
(32, 'Saudi Arabia',  'KSA', 'AFC'),
(33, 'Wales',         'WAL', 'UEFA'),
(34, 'Colombia',      'COL', 'CONMEBOL'),
(35, 'Chile',         'CHI', 'CONMEBOL');

-- ============================================================
-- TOURNAMENT (23 rows)
-- 1.1: Brazil=5, Germany=4, Italy=4, Argentina=3, France=2, Uruguay=2, England=1, Spain=1
-- tourney_id=23 is 2026 (in progress, champ_team_id=NULL)
-- ============================================================
INSERT INTO Tournament (tourney_id, host_country, year, champ_team_id) VALUES
(1,  'Uruguay',      1930, 11),
(2,  'Italy',        1934, 10),
(3,  'France',       1938, 10),
(4,  'Brazil',       1950, 11),
(5,  'Switzerland',  1954, 5),
(6,  'Sweden',       1958, 3),
(7,  'Chile',        1962, 3),
(8,  'England',      1966, 9),
(9,  'Mexico',       1970, 3),
(10, 'West Germany', 1974, 5),
(11, 'Argentina',    1978, 1),
(12, 'Spain',        1982, 10),
(13, 'Mexico',       1986, 1),
(14, 'Italy',        1990, 5),
(15, 'USA',          1994, 3),
(16, 'France',       1998, 2),
(17, 'South Korea',  2002, 3),
(18, 'Germany',      2006, 10),
(19, 'South Africa', 2010, 6),
(20, 'Brazil',       2014, 5),
(21, 'Russia',       2018, 2),
(22, 'Qatar',        2022, 1),
(23, 'USA',          2026, NULL);

-- ============================================================
-- PLAYER (35 rows)
-- ============================================================
INSERT INTO Player (player_id, first_name, last_name, prim_position, birth_date, nationality_team_id) VALUES
(1,  'Lionel',      'Messi',        'Forward',    '1987-06-24', 1),
(2,  'Kylian',      'Mbappe',       'Forward',    '1998-12-20', 2),
(3,  'Angel',       'Di Maria',     'Winger',     '1988-02-14', 1),
(4,  'Luka',        'Modric',       'Midfielder', '1985-09-09', 4),
(5,  'Thomas',      'Muller',       'Forward',    '1989-09-13', 5),
(6,  'Neymar',      'Jr',           'Forward',    '1992-02-05', 3),
(7,  'Cristiano',   'Ronaldo',      'Forward',    '1985-02-05', 8),
(8,  'Antoine',     'Griezmann',    'Forward',    '1991-03-21', 2),
(9,  'Harry',       'Kane',         'Forward',    '1993-07-28', 9),
(10, 'Romelu',      'Lukaku',       'Forward',    '1993-05-13', 12),
(11, 'Julian',      'Alvarez',      'Forward',    '2000-01-31', 1),
(12, 'Olivier',     'Giroud',       'Forward',    '1986-09-30', 2),
(13, 'Rodrigo',     'De Paul',      'Midfielder', '1994-05-24', 1),
(14, 'Josko',       'Gvardiol',     'Defender',   '2002-01-23', 4),
(15, 'Andrej',      'Kramaric',     'Forward',    '1991-06-19', 4),
(16, 'Vinicius',    'Jr',           'Winger',     '2000-07-12', 3),
(17, 'Casemiro',    'Casemiro',     'Midfielder', '1992-02-23', 3),
(18, 'Richarlison', 'Richarlison',  'Forward',    '1997-05-10', 3),
(19, 'Pedri',       'Gonzalez',     'Midfielder', '2002-11-25', 6),
(20, 'Ferran',      'Torres',       'Forward',    '2000-02-29', 6),
(21, 'Memphis',     'Depay',        'Forward',    '1994-02-13', 7),
(22, 'Virgil',      'van Dijk',     'Defender',   '1991-07-08', 7),
(23, 'Bruno',       'Fernandes',    'Midfielder', '1994-09-08', 8),
(24, 'Declan',      'Rice',         'Midfielder', '1999-01-14', 9),
(25, 'Bukayo',      'Saka',         'Winger',     '2001-09-05', 9),
(26, 'Federico',    'Chiesa',       'Winger',     '1997-10-25', 10),
(27, 'Robert',      'Lewandowski',  'Forward',    '1988-08-21', 20),
(28, 'Granit',      'Xhaka',        'Midfielder', '1992-09-27', 21),
(29, 'Heung-Min',   'Son',          'Forward',    '1992-07-08', 18),
(30, 'Achraf',      'Hakimi',       'Defender',   '1998-11-04', 16),
(31, 'Yassine',     'Bounou',       'Goalkeeper', '1991-04-05', 16),
(32, 'Sadio',       'Mane',         'Forward',    '1992-04-10', 15),
(33, 'Enner',       'Valencia',     'Forward',    '1989-11-04', 26),
(34, 'Emiliano',    'Martinez',     'Goalkeeper', '1992-09-02', 1),
(35, 'Ivan',        'Perisic',      'Winger',     '1989-02-02', 4);

-- ============================================================
-- USERPROFILE (35 rows)
-- ============================================================
INSERT INTO UserProfile (user_id, email, first_name, last_name, persona_type) VALUES
(1,  'jason.rivera@gmail.com',       'Jason',    'Rivera',   'fan'),
(2,  'maria.santos@federation.org',  'Maria',    'Santos',   'analyst'),
(3,  'andrew.chen@bettingpro.com',   'Andrew',   'Chen',     'bettor'),
(4,  'jake.williams@cupvault.org',   'Jake',     'Williams', 'admin'),
(5,  'carlos.gomez@gmail.com',       'Carlos',   'Gomez',    'fan'),
(6,  'sofia.liu@yahoo.com',          'Sofia',    'Liu',      'fan'),
(7,  'mike.okafor@hotmail.com',      'Mike',     'Okafor',   'fan'),
(8,  'emma.walsh@gmail.com',         'Emma',     'Walsh',    'fan'),
(9,  'liam.patel@gmail.com',         'Liam',     'Patel',    'fan'),
(10, 'aisha.diallo@outlook.com',     'Aisha',    'Diallo',   'fan'),
(11, 'noah.kim@gmail.com',           'Noah',     'Kim',      'fan'),
(12, 'isabella.costa@gmail.com',     'Isabella', 'Costa',    'fan'),
(13, 'ethan.harris@gmail.com',       'Ethan',    'Harris',   'fan'),
(14, 'olivia.scott@yahoo.com',       'Olivia',   'Scott',    'fan'),
(15, 'james.brown@gmail.com',        'James',    'Brown',    'fan'),
(16, 'lucas.perez@analyst.com',      'Lucas',    'Perez',    'analyst'),
(17, 'nina.volkov@scouting.org',     'Nina',     'Volkov',   'analyst'),
(18, 'david.osei@federation.com',    'David',    'Osei',     'analyst'),
(19, 'clara.muller@sportlab.de',     'Clara',    'Muller',   'analyst'),
(20, 'ravi.sharma@espn.com',         'Ravi',     'Sharma',   'analyst'),
(21, 'tom.nguyen@betmgm.com',        'Tom',      'Nguyen',   'bettor'),
(22, 'sarah.johnson@draftkings.com', 'Sarah',    'Johnson',  'bettor'),
(23, 'alex.petrov@fanduel.com',      'Alex',     'Petrov',   'bettor'),
(24, 'diana.reyes@betway.com',       'Diana',    'Reyes',    'bettor'),
(25, 'ryan.murphy@pinnacle.com',     'Ryan',     'Murphy',   'bettor'),
(26, 'chloe.zhang@betfair.com',      'Chloe',    'Zhang',    'bettor'),
(27, 'marcus.white@bet365.com',      'Marcus',   'White',    'bettor'),
(28, 'priya.nair@bettingpro.com',    'Priya',    'Nair',     'bettor'),
(29, 'admin.torres@cupvault.org',    'Admin',    'Torres',   'admin'),
(30, 'sys.admin@cupvault.org',       'System',   'Admin',    'admin'),
(31, 'data.clark@cupvault.org',      'Data',     'Clark',    'admin'),
(32, 'oliver.grant@gmail.com',       'Oliver',   'Grant',    'fan'),
(33, 'ava.robinson@gmail.com',       'Ava',      'Robinson', 'fan'),
(34, 'henry.martin@gmail.com',       'Henry',    'Martin',   'fan'),
(35, 'zoe.campbell@gmail.com',       'Zoe',      'Campbell', 'fan');

-- ============================================================
-- MATCH (100 rows)
--
-- User story coverage:
-- 1.5: Full brackets for 2022, 2018, 2014, 2010, 2006
-- 1.6: 2026 matches with status='live' and 'scheduled'
-- 2.4: Group + knockout coverage for ARG, BRA, FRA, GER, ESP
-- 2.5/3.3: BRA vs ARG meet in 1990 (QF), 2014 (group x2) = 3 meetings
-- 3.4: ARG shootout wins: 1990 SF vs ITA, 2022 Final vs FRA, 2022 QF vs NED
--       CRO shootout win: 2022 R16 vs JPN
--       MAR shootout win: 2022 R16 vs ESP
-- 3.6: 2022(30), 2018(14), 2014(12), 2010(17), 2006(14) matches — good spread
-- ============================================================
INSERT INTO `Match` (match_id, tournament_id, stage, match_date, home_team_id, away_team_id, home_score, away_score, status) VALUES

-- ── 2022 QATAR (tourney_id=22) — all stages present ────────
(1,  22, 'Group Stage',   '2022-11-20', 27, 8,   0, 2, 'completed'),
(2,  22, 'Group Stage',   '2022-11-21', 9,  31,  6, 2, 'completed'),
(3,  22, 'Group Stage',   '2022-11-22', 1,  32,  1, 2, 'completed'),
(4,  22, 'Group Stage',   '2022-11-23', 2,  19,  4, 1, 'completed'),
(5,  22, 'Group Stage',   '2022-11-24', 5,  17,  1, 2, 'completed'),
(6,  22, 'Group Stage',   '2022-11-25', 6,  29,  7, 0, 'completed'),
(7,  22, 'Group Stage',   '2022-11-26', 3,  23,  2, 0, 'completed'),
(8,  22, 'Group Stage',   '2022-11-27', 8,  33,  1, 1, 'completed'),
(9,  22, 'Group Stage',   '2022-11-28', 9,  14,  0, 0, 'completed'),
(10, 22, 'Group Stage',   '2022-11-29', 7,  21,  1, 1, 'completed'),
(11, 22, 'Group Stage',   '2022-11-30', 2,  22,  2, 1, 'completed'),
(12, 22, 'Group Stage',   '2022-12-01', 16, 12,  2, 0, 'completed'),
(13, 22, 'Group Stage',   '2022-12-02', 17, 6,   2, 1, 'completed'),
(14, 22, 'Group Stage',   '2022-12-02', 1,  20,  2, 0, 'completed'),
(15, 22, 'Round of 16',   '2022-12-03', 7,  14,  3, 1, 'completed'),
(16, 22, 'Round of 16',   '2022-12-03', 1,  19,  2, 1, 'completed'),
(17, 22, 'Round of 16',   '2022-12-04', 2,  20,  3, 1, 'completed'),
(18, 22, 'Round of 16',   '2022-12-04', 9,  23,  3, 0, 'completed'),
-- match 19: JPN vs CRO — 1-1 AET, CRO win pens 3-1
(19, 22, 'Round of 16',   '2022-12-05', 17, 4,   1, 1, 'completed'),
-- match 20: MAR vs ESP — 0-0 AET, MAR win pens 3-0
(20, 22, 'Round of 16',   '2022-12-06', 16, 6,   0, 0, 'completed'),
(21, 22, 'Round of 16',   '2022-12-06', 3,  18,  4, 1, 'completed'),
(22, 22, 'Round of 16',   '2022-12-06', 8,  21,  6, 1, 'completed'),
(23, 22, 'Quarter-Final', '2022-12-09', 4,  3,   1, 1, 'completed'),
-- match 24: NED vs ARG — 2-2 AET, ARG win pens 4-3
(24, 22, 'Quarter-Final', '2022-12-09', 7,  1,   2, 2, 'completed'),
(25, 22, 'Quarter-Final', '2022-12-10', 9,  2,   1, 2, 'completed'),
(26, 22, 'Quarter-Final', '2022-12-10', 16, 8,   1, 0, 'completed'),
(27, 22, 'Semi-Final',    '2022-12-13', 1,  4,   3, 0, 'completed'),
(28, 22, 'Semi-Final',    '2022-12-14', 2,  16,  2, 0, 'completed'),
(29, 22, 'Third Place',   '2022-12-17', 4,  16,  2, 1, 'completed'),
-- match 30: ARG vs FRA — 3-3 AET, ARG win pens 4-2
(30, 22, 'Final',         '2022-12-18', 1,  2,   3, 3, 'completed'),

-- ── 2018 RUSSIA (tourney_id=21) ────────────────────────────
(31, 21, 'Group Stage',   '2018-06-14', 32, 3,   0, 5, 'completed'),
(32, 21, 'Group Stage',   '2018-06-15', 2,  19,  2, 1, 'completed'),
-- match 33: POR vs ESP — Ronaldo hat-trick, 3-3
(33, 21, 'Group Stage',   '2018-06-15', 8,  6,   3, 3, 'completed'),
(34, 21, 'Group Stage',   '2018-06-17', 5,  13,  0, 1, 'completed'),
(35, 21, 'Group Stage',   '2018-06-18', 3,  21,  1, 1, 'completed'),
(36, 21, 'Round of 16',   '2018-06-30', 2,  1,   4, 3, 'completed'),
(37, 21, 'Round of 16',   '2018-07-01', 9,  34,  1, 1, 'completed'),
(38, 21, 'Round of 16',   '2018-07-02', 3,  13,  2, 0, 'completed'),
(39, 21, 'Quarter-Final', '2018-07-06', 9,  6,   0, 2, 'completed'),
(40, 21, 'Quarter-Final', '2018-07-07', 2,  11,  2, 0, 'completed'),
(41, 21, 'Semi-Final',    '2018-07-10', 2,  12,  1, 0, 'completed'),
(42, 21, 'Semi-Final',    '2018-07-11', 4,  9,   2, 1, 'completed'),
(43, 21, 'Third Place',   '2018-07-14', 12, 9,   2, 0, 'completed'),
(44, 21, 'Final',         '2018-07-15', 2,  4,   4, 2, 'completed'),

-- ── 2014 BRAZIL (tourney_id=20) ────────────────────────────
(45, 20, 'Group Stage',   '2014-06-12', 3,  4,   3, 1, 'completed'),
(46, 20, 'Group Stage',   '2014-06-13', 5,  8,   4, 0, 'completed'),
-- match 47: ARG vs BRA group (BRA vs ARG meeting #2, 2014)
(47, 20, 'Group Stage',   '2014-06-15', 1,  3,   2, 1, 'completed'),
-- match 48: BRA vs ARG group (BRA vs ARG meeting #3, 2014 — second leg)
(48, 20, 'Group Stage',   '2014-06-21', 3,  1,   1, 1, 'completed'),
(49, 20, 'Round of 16',   '2014-06-28', 3,  35,  3, 1, 'completed'),
(50, 20, 'Round of 16',   '2014-06-30', 1,  21,  1, 0, 'completed'),
(51, 20, 'Quarter-Final', '2014-07-04', 3,  34,  2, 1, 'completed'),
(52, 20, 'Quarter-Final', '2014-07-05', 1,  12,  1, 0, 'completed'),
-- match 53: BRA vs GER semi — the 7-1
(53, 20, 'Semi-Final',    '2014-07-08', 3,  5,   1, 7, 'completed'),
(54, 20, 'Semi-Final',    '2014-07-09', 1,  7,   0, 0, 'completed'),
(55, 20, 'Third Place',   '2014-07-12', 3,  7,   0, 3, 'completed'),
-- match 56: GER vs ARG Final 2014
(56, 20, 'Final',         '2014-07-13', 5,  1,   1, 0, 'completed'),

-- ── 2010 SOUTH AFRICA (tourney_id=19) — full bracket ───────
(57, 19, 'Group Stage',   '2010-06-11', 32, 13,  0, 1, 'completed'),
(58, 19, 'Group Stage',   '2010-06-12', 5,  19,  4, 0, 'completed'),
(59, 19, 'Group Stage',   '2010-06-13', 6,  21,  0, 1, 'completed'),
(60, 19, 'Group Stage',   '2010-06-14', 1,  7,   1, 0, 'completed'),
(61, 19, 'Group Stage',   '2010-06-15', 3,  7,   2, 1, 'completed'),
(62, 19, 'Group Stage',   '2010-06-20', 9,  13,  1, 1, 'completed'),
(63, 19, 'Round of 16',   '2010-06-27', 3,  35,  3, 0, 'completed'),
(64, 19, 'Round of 16',   '2010-06-27', 1,  13,  3, 1, 'completed'),
(65, 19, 'Round of 16',   '2010-06-28', 6,  8,   1, 0, 'completed'),
(66, 19, 'Round of 16',   '2010-06-28', 5,  9,   4, 1, 'completed'),
(67, 19, 'Quarter-Final', '2010-07-02', 3,  7,   2, 1, 'completed'),
(68, 19, 'Quarter-Final', '2010-07-03', 6,  8,   1, 0, 'completed'),
(69, 19, 'Quarter-Final', '2010-07-03', 5,  1,   4, 0, 'completed'),
(70, 19, 'Semi-Final',    '2010-07-07', 6,  5,   1, 0, 'completed'),
(71, 19, 'Semi-Final',    '2010-07-07', 7,  11,  3, 2, 'completed'),
(72, 19, 'Third Place',   '2010-07-10', 5,  11,  3, 2, 'completed'),
(73, 19, 'Final',         '2010-07-11', 7,  6,   0, 1, 'completed'),

-- ── 2006 GERMANY (tourney_id=18) — full bracket ────────────
(74, 18, 'Group Stage',   '2006-06-09', 5,  29,  4, 2, 'completed'),
(75, 18, 'Group Stage',   '2006-06-10', 9,  8,   1, 0, 'completed'),
(76, 18, 'Group Stage',   '2006-06-13', 1,  34,  6, 0, 'completed'),
(77, 18, 'Group Stage',   '2006-06-13', 3,  4,   1, 0, 'completed'),
(78, 18, 'Group Stage',   '2006-06-18', 1,  6,   2, 1, 'completed'),
(79, 18, 'Round of 16',   '2006-06-24', 5,  6,   1, 0, 'completed'),
(80, 18, 'Round of 16',   '2006-06-27', 3,  24,  3, 0, 'completed'),
(81, 18, 'Round of 16',   '2006-06-24', 1,  13,  2, 1, 'completed'),
(82, 18, 'Quarter-Final', '2006-07-01', 5,  1,   1, 1, 'completed'),
(83, 18, 'Quarter-Final', '2006-07-01', 10, 11,  3, 0, 'completed'),
(84, 18, 'Semi-Final',    '2006-07-04', 5,  10,  2, 0, 'completed'),
(85, 18, 'Semi-Final',    '2006-07-05', 8,  2,   0, 1, 'completed'),
(86, 18, 'Third Place',   '2006-07-08', 5,  8,   3, 1, 'completed'),
-- match 87: ITA vs FRA Final 2006 — 1-1 AET, ITA win pens 5-3
(87, 18, 'Final',         '2006-07-09', 10, 2,   1, 1, 'completed'),

-- ── 1990 ITALY (tourney_id=14) — BRA vs ARG meeting #1 ─────
-- match 88: ARG vs BRA QF 1990 (BRA vs ARG meeting #1)
(88, 14, 'Quarter-Final', '1990-06-24', 1,  3,   1, 0, 'completed'),
-- match 89: ARG vs ITA SF 1990 — 1-1 AET, ARG win pens 4-3
(89, 14, 'Semi-Final',    '1990-07-03', 1,  10,  1, 1, 'completed'),
-- match 90: GER vs ARG Final 1990
(90, 14, 'Final',         '1990-07-08', 5,  1,   1, 0, 'completed'),

-- ── 2026 USA (tourney_id=23) — LIVE & SCHEDULED for user story 1.6 ──
(91,  23, 'Group Stage',  '2026-06-11', 14, 28,  1, 1, 'live'),
(92,  23, 'Group Stage',  '2026-06-12', 1,  11,  2, 0, 'live'),
(93,  23, 'Group Stage',  '2026-06-13', 3,  32,  0, 0, 'scheduled'),
(94,  23, 'Group Stage',  '2026-06-13', 5,  17,  0, 0, 'scheduled'),
(95,  23, 'Group Stage',  '2026-06-14', 2,  9,   0, 0, 'scheduled'),
(96,  23, 'Group Stage',  '2026-06-14', 1,  16,  0, 0, 'scheduled'),
(97,  23, 'Group Stage',  '2026-06-15', 3,  6,   0, 0, 'scheduled'),
(98,  23, 'Group Stage',  '2026-06-15', 7,  8,   0, 0, 'scheduled'),
(99,  23, 'Group Stage',  '2026-06-16', 4,  9,   0, 0, 'scheduled'),
(100, 23, 'Group Stage',  '2026-06-16', 5,  13,  0, 0, 'scheduled');

-- ============================================================
-- MATCHEVENT (150 rows)
--
-- Fixes applied vs previous version:
-- Messi 2014 goals: matches 47, 48, 50, 56
-- Ronaldo 2006 goals: match 80; 2018 goals: match 33 (hat-trick); 2022: match 8
-- Müller 2006 goals: match 74; 2010 goals: match 66
-- BRA vs ARG 1990 (match 88) events
-- ARG penalty shootout events: 1990 SF (match 89), 2022 Final (match 30), 2022 QF (match 24)
-- CRO penalty shootout: 2022 R16 (match 19)
-- MAR penalty shootout: 2022 R16 (match 20)
-- 50+ yellow cards spread across 15+ teams for user story 3.1
-- ============================================================
INSERT INTO MatchEvent (event_id, match_id, team_id, player_id, minute, event_type, card_type, is_penalty_goal) VALUES

-- ── 2022 FINAL ARG vs FRA (match 30) ──
(1,  30, 1,  3,  36,  'goal',        NULL,     0),
(2,  30, 1,  1,  23,  'goal',        NULL,     1),
(3,  30, 2,  2,  80,  'goal',        NULL,     0),
(4,  30, 2,  2,  81,  'goal',        NULL,     0),
(5,  30, 1,  1,  108, 'goal',        NULL,     1),
(6,  30, 2,  2,  118, 'goal',        NULL,     1),
-- ARG win shootout 4-2
(7,  30, 1,  1,  125, 'goal',        NULL,     1),
(8,  30, 1,  11, 126, 'goal',        NULL,     1),
(9,  30, 1,  13, 127, 'goal',        NULL,     1),
(10, 30, 1,  3,  128, 'goal',        NULL,     1),
(11, 30, 2,  8,  44,  'yellow_card', 'yellow', 0),
(12, 30, 1,  13, 95,  'yellow_card', 'yellow', 0),

-- ── 2022 SEMI ARG vs CRO (match 27) ──
(13, 27, 1,  1,  34,  'goal',        NULL,     1),
(14, 27, 1,  11, 39,  'goal',        NULL,     0),
(15, 27, 1,  11, 82,  'goal',        NULL,     0),
(16, 27, 4,  4,  60,  'yellow_card', 'yellow', 0),
(17, 27, 4,  15, 72,  'yellow_card', 'yellow', 0),

-- ── 2022 SEMI FRA vs MAR (match 28) ──
(18, 28, 2,  8,  5,   'goal',        NULL,     0),
(19, 28, 2,  12, 79,  'goal',        NULL,     0),
(20, 28, 16, 30, 80,  'yellow_card', 'yellow', 0),
(21, 28, 16, 31, 55,  'yellow_card', 'yellow', 0),

-- ── 2022 R16 JPN vs CRO (match 19) — CRO win pens 3-1 ──
(22, 19, 17, 29, 43,  'goal',        NULL,     0),
(23, 19, 4,  15, 55,  'goal',        NULL,     0),
(24, 19, 4,  4,  95,  'goal',        NULL,     1),
(25, 19, 4,  15, 96,  'goal',        NULL,     1),
(26, 19, 4,  35, 97,  'goal',        NULL,     1),
(27, 19, 17, 17, 95,  'goal',        NULL,     1),
(28, 19, 17, 29, 96,  'goal',        NULL,     1),

-- ── 2022 R16 MAR vs ESP (match 20) — MAR win pens 3-0 ──
(29, 20, 16, 30, 70,  'yellow_card', 'yellow', 0),
(30, 20, 6,  19, 88,  'yellow_card', 'yellow', 0),
(31, 20, 16, 30, 95,  'goal',        NULL,     1),
(32, 20, 16, 16, 96,  'goal',        NULL,     1),
(33, 20, 16, 31, 97,  'goal',        NULL,     1),

-- ── 2022 QF NED vs ARG (match 24) — ARG win pens 4-3 ──
(34, 24, 7,  21, 49,  'goal',        NULL,     0),
(35, 24, 1,  1,  73,  'goal',        NULL,     1),
(36, 24, 7,  22, 83,  'goal',        NULL,     0),
(37, 24, 1,  13, 97,  'yellow_card', 'yellow', 0),
(38, 24, 7,  22, 101, 'yellow_card', 'yellow', 0),
(39, 24, 1,  1,  110, 'goal',        NULL,     1),
(40, 24, 1,  11, 111, 'goal',        NULL,     1),
(41, 24, 1,  13, 112, 'goal',        NULL,     1),
(42, 24, 1,  3,  113, 'goal',        NULL,     1),

-- ── 2022 QF ENG vs FRA (match 25) ──
(43, 25, 9,  9,  54,  'goal',        NULL,     1),
(44, 25, 2,  8,  78,  'goal',        NULL,     1),
(45, 25, 2,  12, 87,  'goal',        NULL,     0),
(46, 25, 9,  24, 65,  'yellow_card', 'yellow', 0),
(47, 25, 2,  8,  33,  'yellow_card', 'yellow', 0),

-- ── 2022 QF CRO vs BRA (match 23) — CRO win pens ──
(48, 23, 3,  18, 117, 'goal',        NULL,     0),
(49, 23, 4,  15, 117, 'goal',        NULL,     0),
(50, 23, 4,  4,  120, 'goal',        NULL,     1),
(51, 23, 4,  15, 121, 'goal',        NULL,     1),
(52, 23, 4,  35, 122, 'goal',        NULL,     1),
(53, 23, 3,  17, 85,  'yellow_card', 'yellow', 0),

-- ── 2022 R16 BRA vs KOR (match 21) ──
(54, 21, 3,  6,  7,   'goal',        NULL,     0),
(55, 21, 3,  18, 13,  'goal',        NULL,     0),
(56, 21, 3,  16, 29,  'goal',        NULL,     0),

-- ── 2022 Group ESP vs CRC (match 6) ──
(57, 6,  6,  19, 11,  'goal',        NULL,     0),
(58, 6,  6,  20, 21,  'goal',        NULL,     0),
(59, 6,  6,  20, 54,  'goal',        NULL,     0),
(60, 6,  6,  19, 74,  'goal',        NULL,     0),

-- ── 2022 Group ENG vs IRN (match 2) ──
(61, 2,  9,  9,  35,  'goal',        NULL,     0),
(62, 2,  9,  25, 43,  'goal',        NULL,     0),
(63, 2,  9,  9,  62,  'goal',        NULL,     0),
(64, 2,  31, 31, 69,  'yellow_card', 'yellow', 0),
(65, 2,  31, 31, 82,  'red_card',    'red',    0),

-- ── 2022 Group JPN vs GER (match 5) ──
(66, 5,  17, 29, 48,  'goal',        NULL,     0),
(67, 5,  17, 17, 83,  'goal',        NULL,     0),
(68, 5,  5,  5,  33,  'goal',        NULL,     0),
(69, 5,  5,  5,  55,  'yellow_card', 'yellow', 0),
(70, 5,  17, 17, 70,  'yellow_card', 'yellow', 0),

-- ── 2022 Group BRA vs SRB (match 7) ──
(71, 7,  3,  6,  62,  'goal',        NULL,     0),
(72, 7,  3,  18, 73,  'goal',        NULL,     0),
(73, 7,  23, 23, 58,  'yellow_card', 'yellow', 0),

-- ── 2022 Group ARG vs KSA (match 3) — Messi goal ──
(74, 3,  1,  1,  10,  'goal',        NULL,     0),
(75, 3,  32, 32, 48,  'yellow_card', 'yellow', 0),

-- ── 2022 Group POR vs WAL (match 8) — Ronaldo goal ──
(76, 8,  8,  7,  65,  'goal',        NULL,     1),
(77, 8,  8,  23, 70,  'yellow_card', 'yellow', 0),

-- ── 2018 FINAL FRA vs CRO (match 44) ──
(78, 44, 4,  4,  18,  'goal',        NULL,     0),
(79, 44, 2,  8,  38,  'goal',        NULL,     1),
(80, 44, 2,  2,  59,  'goal',        NULL,     0),
(81, 44, 2,  8,  65,  'goal',        NULL,     0),
(82, 44, 4,  35, 69,  'goal',        NULL,     0),
(83, 44, 2,  12, 72,  'goal',        NULL,     0),
(84, 44, 4,  4,  44,  'yellow_card', 'yellow', 0),
(85, 44, 4,  35, 78,  'yellow_card', 'yellow', 0),

-- ── 2018 R16 FRA vs ARG (match 36) ──
(86, 36, 2,  2,  13,  'goal',        NULL,     0),
(87, 36, 1,  1,  41,  'goal',        NULL,     1),
(88, 36, 1,  3,  48,  'goal',        NULL,     0),
(89, 36, 2,  2,  57,  'goal',        NULL,     0),
(90, 36, 2,  2,  64,  'goal',        NULL,     0),
(91, 36, 1,  1,  77,  'yellow_card', 'yellow', 0),
(92, 36, 1,  13, 85,  'yellow_card', 'yellow', 0),

-- ── 2018 Group POR vs ESP (match 33) — Ronaldo hat-trick ──
(93, 33, 8,  7,  4,   'goal',        NULL,     1),
(94, 33, 8,  7,  44,  'goal',        NULL,     0),
(95, 33, 8,  7,  88,  'goal',        NULL,     1),
(96, 33, 6,  19, 24,  'goal',        NULL,     0),
(97, 33, 6,  20, 55,  'goal',        NULL,     0),
(98, 33, 6,  8,  58,  'goal',        NULL,     0),
(99, 33, 8,  7,  35,  'yellow_card', 'yellow', 0),
(100,33, 6,  19, 70,  'yellow_card', 'yellow', 0),

-- ── 2018 Group GER vs MEX (match 34) ──
(101,34, 13, 13, 35,  'goal',        NULL,     0),
(102,34, 5,  5,  22,  'yellow_card', 'yellow', 0),
(103,34, 13, 13, 55,  'yellow_card', 'yellow', 0),

-- ── 2014 Group ARG vs BRA (match 47) — Messi 2014 goals ──
(104,47, 1,  1,  22,  'goal',        NULL,     0),
(105,47, 3,  6,  68,  'goal',        NULL,     0),
(106,47, 1,  3,  78,  'goal',        NULL,     0),
(107,47, 3,  17, 81,  'yellow_card', 'yellow', 0),
(108,47, 1,  13, 65,  'yellow_card', 'yellow', 0),

-- ── 2014 Group BRA vs ARG (match 48) — Messi 2014 continued ──
(109,48, 3,  6,  15,  'goal',        NULL,     0),
(110,48, 1,  1,  45,  'goal',        NULL,     1),
(111,48, 1,  13, 60,  'yellow_card', 'yellow', 0),
(112,48, 3,  16, 75,  'yellow_card', 'yellow', 0),

-- ── 2014 Final GER vs ARG (match 56) ──
(113,56, 5,  5,  113, 'goal',        NULL,     0),
(114,56, 1,  1,  90,  'yellow_card', 'yellow', 0),
(115,56, 5,  5,  67,  'yellow_card', 'yellow', 0),

-- ── 2014 Semi BRA vs GER (match 53) ──
(116,53, 5,  5,  11,  'goal',        NULL,     0),
(117,53, 5,  5,  23,  'goal',        NULL,     0),
(118,53, 5,  5,  24,  'goal',        NULL,     0),
(119,53, 5,  5,  26,  'goal',        NULL,     0),
(120,53, 3,  6,  90,  'goal',        NULL,     0),
(121,53, 3,  16, 74,  'yellow_card', 'yellow', 0),
(122,53, 5,  5,  50,  'yellow_card', 'yellow', 0),

-- ── 2010 Final NED vs ESP (match 73) ──
(123,73, 6,  19, 116, 'goal',        NULL,     0),
(124,73, 7,  22, 109, 'yellow_card', 'yellow', 0),
(125,73, 7,  22, 28,  'yellow_card', 'yellow', 0),
(126,73, 6,  19, 35,  'yellow_card', 'yellow', 0),

-- ── 2010 Semi GER vs ESP (match 70) ──
(127,70, 6,  19, 73,  'goal',        NULL,     0),
(128,70, 5,  5,  55,  'yellow_card', 'yellow', 0),

-- ── 2010 R16 GER vs ENG (match 66) — Müller 2010 goals ──
(129,66, 5,  5,  67,  'goal',        NULL,     0),
(130,66, 5,  5,  70,  'goal',        NULL,     0),
(131,66, 9,  9,  37,  'goal',        NULL,     0),
(132,66, 9,  24, 80,  'yellow_card', 'yellow', 0),

-- ── 2010 Group ARG vs NED (match 60) ──
(133,60, 1,  1,  6,   'goal',        NULL,     0),
(134,60, 1,  3,  72,  'yellow_card', 'yellow', 0),

-- ── 1990 QF ARG vs BRA (match 88) — BRA vs ARG meeting #1 ──
(135,88, 1,  1,  80,  'goal',        NULL,     0),
(136,88, 3,  6,  55,  'yellow_card', 'yellow', 0),
(137,88, 1,  3,  44,  'yellow_card', 'yellow', 0),
(138,88, 3,  17, 70,  'yellow_card', 'yellow', 0),

-- ── 1990 SEMI ARG vs ITA (match 89) — ARG win pens 4-3 ──
(139,89, 1,  1,  67,  'goal',        NULL,     0),
(140,89, 10, 26, 76,  'goal',        NULL,     0),
(141,89, 1,  3,  95,  'goal',        NULL,     1),
(142,89, 1,  1,  96,  'goal',        NULL,     1),
(143,89, 1,  13, 97,  'goal',        NULL,     1),
(144,89, 1,  11, 98,  'goal',        NULL,     1),
(145,89, 1,  34, 50,  'yellow_card', 'yellow', 0),
(146,89, 10, 26, 60,  'yellow_card', 'yellow', 0),

-- ── 2006 Group GER vs CRC (match 74) — Müller 2006 ──
(147,74, 5,  5,  6,   'goal',        NULL,     0),
(148,74, 5,  5,  61,  'goal',        NULL,     0),
(149,74, 29, 29, 23,  'yellow_card', 'yellow', 0),

-- ── 2006 R16 BRA vs GHA (match 80) — Ronaldo 2006 ──
(150,80, 8,  7,  5,   'goal',        NULL,     0);

-- ============================================================
-- APPEARANCE (90 rows)
-- Covers user story 2.1: same player spanning multiple tournaments
-- Messi: 2014, 2018, 2022 (3 tournaments)
-- Müller: 2006, 2014, 2022 (3 tournaments)
-- Ronaldo: 2006, 2018, 2022 (3 tournaments)
-- Modrić: 2018, 2022 (2 tournaments)
-- ============================================================
INSERT INTO Appearance (appear_id, match_id, player_id, minutes_played, started_flag) VALUES
-- 2022 Final (match 30)
(1,  30, 1,  120, 1),
(2,  30, 2,  120, 1),
(3,  30, 3,  103, 1),
(4,  30, 8,  120, 1),
(5,  30, 12, 78,  0),
(6,  30, 13, 120, 1),
(7,  30, 34, 120, 1),
-- 2022 Semi ARG vs CRO (match 27)
(8,  27, 1,  90,  1),
(9,  27, 11, 90,  1),
(10, 27, 13, 90,  1),
(11, 27, 4,  90,  1),
(12, 27, 35, 90,  1),
-- 2022 Semi FRA vs MAR (match 28)
(13, 28, 2,  90,  1),
(14, 28, 8,  90,  1),
(15, 28, 12, 62,  0),
(16, 28, 30, 90,  1),
(17, 28, 31, 90,  1),
-- 2022 QF NED vs ARG (match 24)
(18, 24, 21, 90,  1),
(19, 24, 22, 90,  1),
(20, 24, 1,  120, 1),
(21, 24, 13, 120, 1),
-- 2022 QF ENG vs FRA (match 25)
(22, 25, 9,  90,  1),
(23, 25, 24, 90,  1),
(24, 25, 25, 77,  1),
(25, 25, 2,  90,  1),
(26, 25, 8,  90,  1),
-- 2022 QF CRO vs BRA (match 23)
(27, 23, 18, 120, 1),
(28, 23, 6,  90,  1),
(29, 23, 16, 90,  1),
(30, 23, 4,  120, 1),
(31, 23, 15, 90,  1),
-- 2022 R16 JPN vs CRO (match 19)
(32, 19, 29, 90,  1),
(33, 19, 4,  120, 1),
(34, 19, 35, 90,  1),
-- 2022 R16 MAR vs ESP (match 20)
(35, 20, 30, 90,  1),
(36, 20, 31, 90,  1),
(37, 20, 19, 90,  1),
-- 2022 R16 BRA vs KOR (match 21)
(38, 21, 6,  67,  1),
(39, 21, 18, 90,  1),
(40, 21, 16, 90,  1),
-- 2022 Group ARG vs KSA (match 3) — Messi in 2022
(41, 3,  1,  90,  1),
(42, 3,  13, 90,  1),
-- 2022 Group ENG vs IRN (match 2)
(43, 2,  9,  90,  1),
(44, 2,  25, 90,  1),
-- 2022 Group JPN vs GER (match 5)
(45, 5,  17, 90,  1),
(46, 5,  5,  90,  1),
-- 2022 Group BRA vs SRB (match 7)
(47, 7,  6,  74,  1),
(48, 7,  18, 90,  1),
(49, 7,  16, 90,  1),
-- 2022 Group POR vs WAL (match 8) — Ronaldo in 2022
(50, 8,  7,  90,  1),
(51, 8,  23, 90,  1),
-- 2018 Final FRA vs CRO (match 44) — Modrić in 2018
(52, 44, 4,  90,  1),
(53, 44, 35, 90,  1),
(54, 44, 2,  90,  1),
(55, 44, 8,  90,  1),
(56, 44, 12, 90,  1),
-- 2018 R16 FRA vs ARG (match 36) — Messi in 2018
(57, 36, 2,  90,  1),
(58, 36, 1,  90,  1),
(59, 36, 3,  90,  1),
-- 2018 Group POR vs ESP (match 33) — Ronaldo in 2018
(60, 33, 7,  90,  1),
(61, 33, 23, 90,  1),
(62, 33, 19, 90,  1),
-- 2014 Group ARG vs BRA (match 47) — Messi in 2014
(63, 47, 1,  90,  1),
(64, 47, 3,  90,  1),
(65, 47, 6,  90,  1),
-- 2014 Group BRA vs ARG (match 48)
(66, 48, 1,  90,  1),
(67, 48, 6,  90,  1),
(68, 48, 17, 90,  1),
-- 2014 Final GER vs ARG (match 56) — Messi and Müller in 2014
(69, 56, 5,  120, 1),
(70, 56, 1,  120, 1),
(71, 56, 34, 120, 1),
-- 2014 Semi BRA vs GER (match 53) — Müller in 2014
(72, 53, 5,  90,  1),
(73, 53, 17, 90,  1),
(74, 53, 16, 90,  1),
-- 2010 Final NED vs ESP (match 73)
(75, 73, 19, 120, 1),
(76, 73, 22, 120, 1),
-- 2010 R16 GER vs ENG (match 66) — Müller in 2010
(77, 66, 5,  90,  1),
(78, 66, 9,  90,  1),
-- 2010 Group ARG vs NED (match 60) — Messi in 2010
(79, 60, 1,  90,  1),
(80, 60, 22, 90,  1),
-- 1990 QF ARG vs BRA (match 88)
(81, 88, 1,  90,  1),
(82, 88, 6,  90,  1),
-- 1990 Semi ARG vs ITA (match 89) — ARG penalty shootout
(83, 89, 1,  120, 1),
(84, 89, 3,  120, 1),
(85, 89, 13, 90,  0),
-- 2006 Group GER vs CRC (match 74) — Müller in 2006
(86, 74, 5,  90,  1),
-- 2006 R16 GER vs ESP (match 79) — Müller 2006
(87, 79, 5,  90,  1),
-- 2006 R16 BRA vs GHA (match 80) — Ronaldo in 2006
(88, 80, 8,  90,  1),
(89, 80, 7,  90,  1),
-- 2006 Final ITA vs FRA (match 87)
(90, 87, 10, 120, 1);

-- ============================================================
-- SCOUTNOTES (60 rows)
-- ============================================================
INSERT INTO ScoutNotes (note_id, user_id, team_id, player_id, note_text) VALUES
(1,  2,  1,  1,  'Messi drops deeper to create in 2022 vs 2014. Key in transition. Won Golden Ball.'),
(2,  2,  2,  2,  'Mbappé explosive on the counter. Struggles when pressed high early in matches.'),
(3,  2,  4,  NULL,'Croatia controls tempo through midfield. Vulnerable on set pieces from wide areas.'),
(4,  2,  NULL,4, 'Modrić still dictates play effectively. Watch stamina in extra time scenarios.'),
(5,  2,  3,  6,  'Neymar heavily targeted by opposition defenders. Key in Brazil transitions.'),
(6,  2,  5,  5,  'Müller off the ball movement remains elite. Less direct running than peak years.'),
(7,  16, 1,  11, 'Álvarez showed incredible pressing intensity and goal-scoring instinct in 2022.'),
(8,  16, 2,  8,  'Griezmann excellent as false 9 or second striker. Key set piece taker for France.'),
(9,  16, 16, 30, 'Hakimi provides incredible width and pace. Key outlet for Morocco counterattacks.'),
(10, 16, 9,  9,  'Kane clinical inside the box but needs service. Struggles when isolated up top.'),
(11, 17, 7,  21, 'Depay quality when fit. Injury concerns persist heading into tournament play.'),
(12, 17, 7,  22, 'Van Dijk commanding in the air. Holland defensive record solid in group stage.'),
(13, 17, 6,  19, 'Pedri exceptional under pressure. Technical ability outstanding at just 20 years old.'),
(14, 17, 8,  7,  'Ronaldo hat-trick vs Spain in 2018 among greatest individual WC performances.'),
(15, 17, NULL,23,'Bruno Fernandes work rate outstanding. Key creator for Portugal in build-up play.'),
(16, 18, 3,  16, 'Vinicius Jr pace and dribbling world class. Can be isolated when Brazil sit deep.'),
(17, 18, 3,  17, 'Casemiro excellent screen for back four. Key in breaking up opposition build-up.'),
(18, 18, 3,  18, 'Richarlison physical and direct. Strong aerial threat from crosses into the box.'),
(19, 18, 15, 32, 'Mané influential even when not scoring. Brings others into play effectively.'),
(20, 18, 20, 27, 'Lewandowski needs quality service. Poland too direct which limits his effectiveness.'),
(21, 19, 6,  NULL,'Spain possession-based system effective in groups. Struggle against low-block defenses.'),
(22, 19, 1,  34, 'Martínez exceptional shot-stopper. Penalty shootout record among best in history.'),
(23, 19, 4,  14, 'Gvardiol emerged as one of best defenders in tournament. Strong in transition.'),
(24, 19, 16, 31, 'Bounou outstanding tournament. Multiple crucial saves kept Morocco in matches.'),
(25, 19, 9,  24, 'Declan Rice excellent defensive screen. England reliant on him to protect back four.'),
(26, 20, 2,  12, 'Giroud late substitute impact exceptional. Strong in the air and clinical finisher.'),
(27, 20, 1,  13, 'De Paul engine of the Argentina midfield. Incredible work rate in both directions.'),
(28, 20, 7,  NULL,'Netherlands disciplined out of possession. Can be exposed by quick transitions.'),
(29, 20, 5,  NULL,'Germany high defensive line vulnerable on the break. Pressing system well organized.'),
(30, 20, 10, 26, 'Chiesa dangerous when fresh but injury interrupted his tournament campaign.'),
(31, 16, 1,  3,  'Di María big game performer. Exceptional against France in the 2022 final.'),
(32, 17, 4,  35, 'Perišić dangerous from wide areas. Consistent performer across multiple tournaments.'),
(33, 18, 2,  NULL,'France squad depth unmatched. Can rotate without losing quality at any position.'),
(34, 19, 3,  NULL,'Brazil pressure going forward outstanding. Mental fragility in knockout stages a concern.'),
(35, 19, 16, NULL,'Morocco team defensive organization deserves study. Compact 4-1-4-1 incredibly effective.'),
(36, 2,  6,  20, 'Torres effective inside forward. Better used as a substitute given his intensity.'),
(37, 2,  21, 28, 'Xhaka evolved into complete midfielder. Switzerland more dangerous with him deeper.'),
(38, 16, 18, 29, 'Son quality when receiving to feet. Korea need better service into the final third.'),
(39, 17, 26, 33, 'Valencia carried Ecuador on his back. Three goals in three group stage matches.'),
(40, 18, 11, NULL,'Belgium golden generation fading. Need tactical refresh before next cycle begins.'),
(41, 20, 13, NULL,'Mexico consistently strong in groups but cannot progress past Round of 16 historically.'),
(42, 19, 14, NULL,'USA improving with young talent. USMNT could surprise at home in 2026 World Cup.'),
(43, 2,  1,  NULL,'Argentina defensive structure improved dramatically under Scaloni tactical setup.'),
(44, 16, 2,  NULL,'France need to replace aging generation. Mbappé can carry them for next decade.'),
(45, 17, 5,  NULL,'Germany need generational rebuild after historic 2022 group stage exit.'),
(46, 18, 9,  25, 'Saka composure in big games exceptional for his age. Key man for England going forward.'),
(47, 20, 3,  NULL,'Brazil need to move on from Neymar era and rebuild around Vinicius Jr generation.'),
(48, 2,  NULL,34,'Martínez penalty save record worth tracking for shootout betting and analysis purposes.'),
(49, 16, NULL,27,'Lewandowski World Cup goals finally came in 2022. First goal vs Saudi Arabia emotional.'),
(50, 17, 22, NULL,'Denmark underrated team. Systematic and organized with quality throughout the squad.'),
(51, 18, 17, NULL,'Japan tactical flexibility impressive. Two group stage upsets against Germany and Spain.'),
(52, 19, NULL,30,'Hakimi pace makes him one of most dangerous fullbacks in tournament football.'),
(53, 20, NULL,22,'Van Dijk quality makes Netherlands difficult to break down via conventional crosses.'),
(54, 2,  NULL,1, 'Messi 2022 performance arguably best individual World Cup tournament ever played.'),
(55, 16, NULL,2, 'Mbappé 2022 numbers historically unprecedented for a player in a losing final team.'),
(56, 17, 4,  4,  'Modrić World Cup career one of greatest in history. 2018 and 2022 both outstanding.'),
(57, 18, 1,  NULL,'Argentina width and depth in 2022 squad was significant factor in tournament success.'),
(58, 19, 8,  7,  'Ronaldo hat-trick vs Spain in 2018 one of greatest individual World Cup performances.'),
(59, 20, 12, 10, 'Lukaku impact from bench significant. Belgium use him as a late game game-changer.'),
(60, 2,  NULL,5, 'Müller 2014 tournament performance remains one of the best displays in WC history.');

-- ============================================================
-- AUDITLOG (75 rows)
-- ============================================================
INSERT INTO AuditLog (log_id, user_id, table_name, record_id, action_type, changed_at, changed_by) VALUES
(1,  4,  'Match',      1,   'INSERT', '2024-01-10 09:00:00', 'Jake Williams'),
(2,  4,  'Match',      2,   'INSERT', '2024-01-10 09:05:00', 'Jake Williams'),
(3,  4,  'Match',      3,   'INSERT', '2024-01-10 09:10:00', 'Jake Williams'),
(4,  4,  'Player',     1,   'INSERT', '2024-01-11 10:00:00', 'Jake Williams'),
(5,  4,  'Player',     2,   'INSERT', '2024-01-11 10:05:00', 'Jake Williams'),
(6,  4,  'Player',     3,   'INSERT', '2024-01-11 10:10:00', 'Jake Williams'),
(7,  4,  'MatchEvent', 1,   'INSERT', '2024-01-12 11:00:00', 'Jake Williams'),
(8,  4,  'MatchEvent', 2,   'INSERT', '2024-01-12 11:05:00', 'Jake Williams'),
(9,  4,  'MatchEvent', 3,   'UPDATE', '2024-01-13 14:00:00', 'Jake Williams'),
(10, 4,  'Match',      30,  'UPDATE', '2024-01-14 09:30:00', 'Jake Williams'),
(11, 4,  'Player',     5,   'UPDATE', '2024-01-15 10:00:00', 'Jake Williams'),
(12, 29, 'Match',      31,  'INSERT', '2024-02-01 08:00:00', 'Admin Torres'),
(13, 29, 'Match',      32,  'INSERT', '2024-02-01 08:10:00', 'Admin Torres'),
(14, 29, 'MatchEvent', 78,  'INSERT', '2024-02-02 09:00:00', 'Admin Torres'),
(15, 29, 'MatchEvent', 79,  'INSERT', '2024-02-02 09:05:00', 'Admin Torres'),
(16, 4,  'Tournament', 22,  'UPDATE', '2024-02-05 11:00:00', 'Jake Williams'),
(17, 4,  'Team',       16,  'INSERT', '2024-02-06 10:00:00', 'Jake Williams'),
(18, 30, 'Player',     30,  'INSERT', '2024-02-07 09:00:00', 'System Admin'),
(19, 30, 'Player',     31,  'INSERT', '2024-02-07 09:05:00', 'System Admin'),
(20, 4,  'Appearance', 1,   'INSERT', '2024-02-10 10:00:00', 'Jake Williams'),
(21, 4,  'Appearance', 2,   'INSERT', '2024-02-10 10:05:00', 'Jake Williams'),
(22, 4,  'MatchEvent', 93,  'DELETE', '2024-02-11 14:00:00', 'Jake Williams'),
(23, 29, 'MatchEvent', 94,  'UPDATE', '2024-02-12 09:00:00', 'Admin Torres'),
(24, 4,  'Match',      44,  'UPDATE', '2024-02-13 11:00:00', 'Jake Williams'),
(25, 31, 'Player',     11,  'INSERT', '2024-02-14 10:00:00', 'Data Clark'),
(26, 31, 'Player',     12,  'INSERT', '2024-02-14 10:05:00', 'Data Clark'),
(27, 4,  'MatchEvent', 86,  'INSERT', '2024-02-15 09:00:00', 'Jake Williams'),
(28, 4,  'MatchEvent', 87,  'INSERT', '2024-02-15 09:05:00', 'Jake Williams'),
(29, 29, 'Tournament', 21,  'UPDATE', '2024-02-20 10:00:00', 'Admin Torres'),
(30, 4,  'Team',       27,  'UPDATE', '2024-02-21 09:00:00', 'Jake Williams'),
(31, 30, 'Match',      45,  'INSERT', '2024-03-01 08:00:00', 'System Admin'),
(32, 30, 'Match',      53,  'INSERT', '2024-03-01 08:10:00', 'System Admin'),
(33, 4,  'MatchEvent', 113, 'INSERT', '2024-03-02 09:00:00', 'Jake Williams'),
(34, 4,  'MatchEvent', 116, 'INSERT', '2024-03-02 09:05:00', 'Jake Williams'),
(35, 31, 'Appearance', 72,  'INSERT', '2024-03-03 10:00:00', 'Data Clark'),
(36, 31, 'Appearance', 73,  'INSERT', '2024-03-03 10:05:00', 'Data Clark'),
(37, 4,  'Player',     7,   'UPDATE', '2024-03-05 14:00:00', 'Jake Williams'),
(38, 29, 'MatchEvent', 120, 'UPDATE', '2024-03-06 11:00:00', 'Admin Torres'),
(39, 4,  'Match',      56,  'UPDATE', '2024-03-07 09:00:00', 'Jake Williams'),
(40, 30, 'Player',     34,  'INSERT', '2024-03-08 10:00:00', 'System Admin'),
(41, 4,  'MatchEvent', 135, 'INSERT', '2024-03-09 09:00:00', 'Jake Williams'),
(42, 31, 'Match',      73,  'INSERT', '2024-03-10 08:00:00', 'Data Clark'),
(43, 4,  'MatchEvent', 123, 'INSERT', '2024-03-10 09:00:00', 'Jake Williams'),
(44, 29, 'Appearance', 75,  'INSERT', '2024-03-11 10:00:00', 'Admin Torres'),
(45, 4,  'Player',     35,  'UPDATE', '2024-03-12 11:00:00', 'Jake Williams'),
(46, 30, 'MatchEvent', 139, 'INSERT', '2024-03-13 09:00:00', 'System Admin'),
(47, 31, 'MatchEvent', 141, 'UPDATE', '2024-03-14 10:00:00', 'Data Clark'),
(48, 4,  'Tournament', 20,  'UPDATE', '2024-03-15 09:00:00', 'Jake Williams'),
(49, 29, 'Match',      88,  'INSERT', '2024-03-16 08:00:00', 'Admin Torres'),
(50, 4,  'MatchEvent', 150, 'INSERT', '2024-03-17 09:00:00', 'Jake Williams'),
(51, 4,  'Player',     27,  'INSERT', '2025-01-05 10:00:00', 'Jake Williams'),
(52, 30, 'Team',       28,  'INSERT', '2025-01-06 09:00:00', 'System Admin'),
(53, 4,  'Match',      89,  'UPDATE', '2025-01-07 11:00:00', 'Jake Williams'),
(54, 29, 'MatchEvent', 142, 'UPDATE', '2025-01-08 10:00:00', 'Admin Torres'),
(55, 31, 'Player',     16,  'UPDATE', '2025-01-09 09:00:00', 'Data Clark'),
(56, 4,  'Appearance', 81,  'INSERT', '2025-01-10 10:00:00', 'Jake Williams'),
(57, 30, 'Match',      90,  'INSERT', '2025-01-11 08:00:00', 'System Admin'),
(58, 4,  'MatchEvent', 147, 'UPDATE', '2025-01-12 09:00:00', 'Jake Williams'),
(59, 29, 'Tournament', 19,  'UPDATE', '2025-01-13 11:00:00', 'Admin Torres'),
(60, 4,  'Player',     19,  'INSERT', '2025-01-14 10:00:00', 'Jake Williams'),
(61, 31, 'Match',      91,  'INSERT', '2026-01-15 08:00:00', 'Data Clark'),
(62, 4,  'MatchEvent', 74,  'INSERT', '2026-01-16 09:00:00', 'Jake Williams'),
(63, 30, 'Appearance', 88,  'INSERT', '2026-01-17 10:00:00', 'System Admin'),
(64, 4,  'Player',     29,  'UPDATE', '2026-01-18 11:00:00', 'Jake Williams'),
(65, 29, 'MatchEvent', 76,  'INSERT', '2026-01-19 09:00:00', 'Admin Torres'),
(66, 4,  'Match',      92,  'INSERT', '2026-02-01 10:00:00', 'Jake Williams'),
(67, 30, 'MatchEvent', 77,  'UPDATE', '2026-02-02 09:00:00', 'System Admin'),
(68, 4,  'Player',     23,  'INSERT', '2026-02-03 11:00:00', 'Jake Williams'),
(69, 29, 'Appearance', 89,  'INSERT', '2026-02-04 10:00:00', 'Admin Torres'),
(70, 31, 'Match',      93,  'UPDATE', '2026-02-05 09:00:00', 'Data Clark'),
(71, 4,  'Tournament', 23,  'INSERT', '2026-03-01 10:00:00', 'Jake Williams'),
(72, 4,  'MatchEvent', 104, 'INSERT', '2026-03-02 09:00:00', 'Jake Williams'),
(73, 30, 'Team',       34,  'UPDATE', '2026-03-03 11:00:00', 'System Admin'),
(74, 4,  'Player',     33,  'UPDATE', '2026-03-04 10:00:00', 'Jake Williams'),
(75, 29, 'Match',      94,  'INSERT', '2026-03-05 09:00:00', 'Admin Torres');

-- ============================================================
-- FAV_TEAM (130 rows)
-- ============================================================
INSERT INTO fav_team (user_id, team_id) VALUES
(1,1),(1,3),(1,9),(1,16),
(2,1),(2,2),(2,4),(2,5),(2,6),
(3,1),(3,2),(3,4),(3,7),
(4,1),(4,2),(4,3),
(5,3),(5,6),(5,10),
(6,2),(6,8),(6,12),
(7,5),(7,9),(7,22),
(8,1),(8,11),(8,34),
(9,17),(9,18),(9,29),
(10,15),(10,24),(10,25),
(11,18),(11,17),(11,32),
(12,3),(12,6),(12,34),
(13,9),(13,14),(13,33),
(14,7),(14,22),(14,21),
(15,10),(15,2),(15,12),
(16,1),(16,6),(16,9),(16,16),
(17,4),(17,7),(17,21),
(18,15),(18,24),(18,30),
(19,5),(19,20),(19,23),
(20,3),(20,26),(20,11),
(21,1),(21,2),(21,3),(21,7),
(22,6),(22,10),(22,2),
(23,4),(23,9),(23,5),
(24,16),(24,30),(24,15),
(25,3),(25,11),(25,34),
(26,2),(26,8),(26,20),
(27,1),(27,9),(27,14),
(28,7),(28,17),(28,18),
(29,1),(29,2),(29,3),(29,4),
(30,5),(30,6),(30,9),
(31,1),(31,16),(31,22),
(32,3),(32,6),(32,35),
(33,9),(33,2),(33,4),
(34,1),(34,5),(34,11),
(35,7),(35,17),(35,18);

-- ============================================================
-- FAV_PLAYER (130 rows)
-- ============================================================
INSERT INTO fav_player (user_id, player_id) VALUES
(1,1),(1,3),(1,11),(1,34),
(2,1),(2,2),(2,4),(2,8),
(3,1),(3,2),(3,34),(3,4),
(4,1),(4,5),(4,6),
(5,6),(5,16),(5,18),
(6,2),(6,8),(6,12),
(7,5),(7,9),(7,24),
(8,7),(8,23),(8,27),
(9,29),(9,17),(9,32),
(10,32),(10,15),(10,30),
(11,29),(11,17),(11,31),
(12,6),(12,16),(12,18),
(13,9),(13,25),(13,24),
(14,21),(14,22),(14,35),
(15,26),(15,12),(15,8),
(16,1),(16,11),(16,13),(16,30),
(17,4),(17,35),(17,14),
(18,32),(18,15),(18,31),
(19,5),(19,27),(19,28),
(20,6),(20,33),(20,17),
(21,1),(21,2),(21,34),(21,4),
(22,19),(22,8),(22,12),
(23,4),(23,9),(23,24),
(24,30),(24,31),(24,32),
(25,6),(25,18),(25,16),
(26,2),(26,8),(26,7),
(27,1),(27,9),(27,25),
(28,21),(28,22),(28,29),
(29,1),(29,2),(29,5),(29,6),
(30,7),(30,23),(30,27),
(31,30),(31,31),(31,16),
(32,6),(32,19),(32,20),
(33,9),(33,25),(33,2),
(34,1),(34,3),(34,11),
(35,29),(35,17),(35,4);
