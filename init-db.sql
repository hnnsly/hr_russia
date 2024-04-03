CREATE DATABASE hr_russia;

CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    is_adult BOOLEAN,
    city VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS messages (
    name VARCHAR(255) PRIMARY KEY,
    content TEXT NOT NULL,
    link TEXT
);

CREATE TABLE IF NOT EXISTS articles (
    name TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    link TEXT
);

CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    interaction VARCHAR(255) NOT NULL,
    content TEXT,
    time TIMESTAMP
);

CREATE USER andrey115527 WITH PASSWORD 'pasik';
GRANT ALL PRIVILEGES ON DATABASE hr_russia TO andrey11527;
