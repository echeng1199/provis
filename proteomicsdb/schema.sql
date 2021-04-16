/* we will use SQLite to store user info and file info into tables
user table will store username and password
post table will store posts
 */ 


DROP TABLE IF EXISTS user; -- don't create tables if they already exist 
DROP TABLE IF EXISTS post;

CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,   -- id of user in program
	first_name TEXT NOT NULL,               -- first name
	last_name TEXT NOT NULL,                -- last name
    email TEXT NOT NULL,                    -- email address
	username TEXT UNIQUE NOT NULL,		    -- username
	password TEXT NOT NULL,                 -- password
    affiliation TEXT NOT NULL               -- affiliation
);

CREATE TABLE post (
	id INTEGER PRIMARY KEY AUTOINCREMENT,                   -- id of post
	author_id INTEGER NOT NULL,                             -- author id
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,   -- time of post
	title TEXT NOT NULL,                                    -- title of post
	description TEXT NOT NULL,                              -- description of post
	file_name TEXT,                                         -- name of file uploaded to post
	species TEXT,                                           -- species
	condition TEXT,                                         -- experimental conditions (i.e. infection type)
	timept TEXT,                                            -- time points
	FOREIGN KEY (author_id) REFERENCES user (id)            -- author id is the same as user id
);
