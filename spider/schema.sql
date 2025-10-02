-- execute this file only during installation

CREATE DATABASE cuny_research_record;

CREATE TABLE author (
    author_id PRIMARY KEY,
    first_name VARCHAR(30),
    middle_initial CHAR(1) DEFAULT '',
    last_name VARCHAR(30) NOT NULL,
);

CREATE TABLE paper (
    paper_id PRIMARY KEY,
    title,
    url,
    year
);

CREATE TABLE research (
    paper_id,
    author_id
    paper_id REFERENCES paper.paper_id
    author_id REFERENCES author.author_id
);

CREATE TABLE college (
    college_id PRIMARY KEY,
    college_name VARCHAR(50) NOT NULL,
    city VARCHAR(30),
    state VARCHAR(25),
    country VARCHAR(25)
);

CREATE TABLE affliation (
    college_id,
    author_id
);

CREATE TABLE cited_by (
    paper_id
);



