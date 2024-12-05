DROP DATABASE IF EXISTS football_db;

CREATE DATABASE IF NOT EXISTS football_db;

USE football_db;

CREATE TABLE IF NOT EXISTS team (
	id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT,
    team_name VARCHAR(255),
    logo VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS fixture (
    fixture_id INT PRIMARY KEY,
    home_team_id INT,
    home_team_name VARCHAR(255),
    away_team_id INT,
    away_team_name VARCHAR(255),
    match_date DATETIME
);

CREATE TABLE IF NOT EXISTS team_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT,
    fixture_id INT,
    match_date DATETIME,
    team_name VARCHAR(255),
    away_team_id INT,
    away_team_name VARCHAR(255),
    goals_home INT,
    goals_away INT,
    yellow_cards_home INT DEFAULT 0,
    yellow_cards_away INT DEFAULT 0,
    red_cards_home INT DEFAULT 0,
    red_cards_away INT DEFAULT 0,
    corner_home INT DEFAULT 0,
    corner_away INT DEFAULT 0,
    team_strength_home DOUBLE DEFAULT 100,
    team_strength_away DOUBLE DEFAULT 100,
    match_result ENUM('WIN', 'LOSE', 'DRAW')
);
