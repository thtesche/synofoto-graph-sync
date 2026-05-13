CREATE TABLE user_info (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE folder (
    id SERIAL PRIMARY KEY,
    id_user INTEGER NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE unit (
    id SERIAL PRIMARY KEY,
    id_user INTEGER NOT NULL,
    type SMALLINT NOT NULL DEFAULT 0,
    filename TEXT NOT NULL,
    id_folder INTEGER NOT NULL
);

CREATE TABLE person (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE many_unit_has_many_person (
    unit_id INTEGER NOT NULL,
    person_id INTEGER NOT NULL
);

-- Insert dummy data
INSERT INTO user_info (id, name) VALUES (1, 'thtesche'), (2, 'otheruser');

INSERT INTO folder (id, id_user, name) VALUES 
(1, 1, '/2026/02'), 
(2, 1, '/2026/03'),
(3, 2, '/2026/02');

INSERT INTO unit (id, id_user, type, filename, id_folder) VALUES 
(100, 1, 0, 'pic1.jpg', 1),
(101, 1, 0, 'pic2.jpg', 1),
(102, 1, 0, 'pic3.jpg', 2),
(103, 1, 1, 'video.mp4', 1), -- not type 0, should be ignored
(104, 2, 0, 'other.jpg', 3);

INSERT INTO person (id, name) VALUES 
(10, 'Alice'), 
(11, 'Bob'), 
(12, 'Charlie');

INSERT INTO many_unit_has_many_person (unit_id, person_id) VALUES 
(100, 10),
(100, 11),
(101, 12);
