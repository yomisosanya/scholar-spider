-- execute this file only during installation

CREATE DATABASE cuny_research_record;

USE DATABASE cuny_research_record;


-- referenced by the following table(s):
--                           1. affliation
--                           2. research
CREATE TABLE author (
    author_id INT PRIMARY KEY,
    first_name VARCHAR(30),
    middle_initial CHAR(1) DEFAULT '',
    last_name VARCHAR(30) NOT NULL,
);

CREATE TABLE paper (
    paper_id INT PRIMARY KEY,
    title TEXT,
    url VARCHAR(100),
    year YEAR
);

CREATE TABLE research (
    paper_id INT,
    author_id INT,
    PRIMARY KEY (paper_id, author_id),
    paper_id REFERENCES paper.paper_id
    author_id REFERENCES author.author_id
);

-- referenced by the following table(s):
--                            1. affliation
CREATE TABLE college (
    college_id INT PRIMARY KEY,
    college_name VARCHAR(50) NOT NULL,
    city VARCHAR(30),
    state VARCHAR(25),
    country VARCHAR(25)
);

CREATE TABLE affliation (
    college_id INT,
    author_id INT,
    PRIMARY KEY (college_id, author_id)
    college_id REFERENCES college.college_id
    author_id REFERENCES author.author_id
);

CREATE TABLE cited_by (
    paper_id INT
);



