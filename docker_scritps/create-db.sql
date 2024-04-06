CREATE DATABASE hr_russia;

CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        is_adult BOOLEAN,
                        city VARCHAR(255)
                    );

CREATE TABLE IF NOT EXISTS messages (
                        name TEXT PRIMARY KEY UNIQUE ,
                        content TEXT
                    );

CREATE TABLE IF NOT EXISTS articles (
                        name TEXT PRIMARY KEY,
                        is_job BOOLEAN NOT NULL,
                        for_adult BOOLEAN NOT NULL,
                        content TEXT,
                        link TEXT
                    );

CREATE TABLE IF NOT EXISTS logs (
                        id SERIAL PRIMARY KEY,
                        username TEXT NOT NULL,
                        interaction TEXT,
                        content TEXT,
                        time TIMESTAMP
                    );

INSERT INTO messages VALUES ('start','срарт');
INSERT INTO messages VALUES ('help','хелр');
INSERT INTO messages VALUES ('вакансии от 18','для дедов');
INSERT INTO messages VALUES ('вакансии до 18','для детсадовцев');
INSERT INTO messages VALUES ('нет ответа','пасхалко 1488');

INSERT INTO users VALUES ('hnnssssssly',true,'пасхалко 1488 хохохо');

INSERT INTO articles VALUES ('смерть',true,true,'для трупов','google.com');
INSERT INTO articles VALUES ('рождение',true,false,'для младенцев','pornhub.com');

CREATE USER root WITH PASSWORD 'root';
CREATE USER andrey115527 WITH PASSWORD 'pasik';
GRANT ALL PRIVILEGES ON DATABASE hr_russia TO andrey11527,root;