CREATE TABLE user_info (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE folder (
    id SERIAL PRIMARY KEY,
    id_user INTEGER NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE address (
    id SERIAL PRIMARY KEY,
    id_unit INTEGER NOT NULL,
    lang SMALLINT NOT NULL,
    level INTEGER NOT NULL,
    admin SMALLINT NOT NULL,
    value TEXT NOT NULL,
    id_user INTEGER NOT NULL
);

CREATE TABLE unit (
    id SERIAL PRIMARY KEY,
    id_user INTEGER NOT NULL,
    type SMALLINT NOT NULL DEFAULT 0,
    filename TEXT NOT NULL,
    id_folder INTEGER NOT NULL,
    takentime BIGINT NOT NULL DEFAULT 0,
    cache_key TEXT
);

CREATE TABLE metadata (
    id_unit INTEGER PRIMARY KEY,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);

CREATE TABLE person (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE face (
    id SERIAL PRIMARY KEY,
    id_unit INTEGER NOT NULL,
    id_person INTEGER NOT NULL,
    id_user INTEGER NOT NULL
);

CREATE TABLE general_tag (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE many_unit_has_many_general_tag (
    id_unit INTEGER NOT NULL,
    id_general_tag INTEGER NOT NULL
);

-- Insert dummy data
INSERT INTO user_info (id, name) VALUES (1, 'thtesche'), (2, 'otheruser');

INSERT INTO folder (id, id_user, name) VALUES 
(1, 1, '/2026/02'), 
(2, 1, '/2026/03'),
(3, 2, '/2026/02');

INSERT INTO unit (id, id_user, type, filename, id_folder, takentime, cache_key) VALUES 
(100, 1, 0, 'pic1.jpg', 1, 1715684400, 'key100'),
(101, 1, 0, 'pic2.jpg', 1, 1715688000, 'key101'),
(102, 1, 0, 'pic3.jpg', 2, 1715691600, 'key102'),
(103, 1, 1, 'video.mp4', 1, 1715695200, 'key103'),
(104, 2, 0, 'other.jpg', 3, 1715698800, 'key104');

INSERT INTO address (id_unit, lang, level, admin, value, id_user) VALUES 
(100, 0, 1, 1, 'Germany', 1),
(100, 0, 2, 2, 'Berlin', 1),
(100, 0, 3, 3, 'Mitte', 1),
(101, 0, 1, 1, 'Germany', 1),
(101, 0, 2, 2, 'Hamburg', 1);

INSERT INTO metadata (id_unit, latitude, longitude) VALUES 
(100, 52.52, 13.405),
(101, 53.55, 9.99);

INSERT INTO person (id, name) VALUES 
(10, 'Alice'), 
(11, 'Bob'), 
(12, 'Charlie');

INSERT INTO face (id_unit, id_person, id_user) VALUES 
(100, 10, 1),
(100, 11, 1),
(101, 12, 1);

INSERT INTO general_tag (id, name) VALUES 
(20, 'Landscape'), 
(21, 'Architecture');

INSERT INTO many_unit_has_many_general_tag (id_unit, id_general_tag) VALUES 
(100, 20),
(101, 20),
(101, 21);
