/*  FAA DOF obstacle database data definition */

DROP TABLE IF EXISTS us_state CASCADE;
DROP TABLE IF EXISTS verif_status CASCADE;
DROP TABLE IF EXISTS vert_acc CASCADE;
DROP TABLE IF EXISTS hor_acc CASCADE;
DROP TABLE IF EXISTS obstacle_type CASCADE;
DROP TABLE IF EXISTS marking CASCADE;
DROP TABLE IF EXISTS lighting CASCADE;
DROP TABLE IF EXISTS obstacle;

CREATE TABLE us_state(
	state_id serial PRIMARY KEY,
	state_name varchar(75) NOT NULL,
	boundary geography(POLYGON, 4326)
);

CREATE TABLE obstacle_type(
	obst_type_id serial PRIMARY KEY,
	obst_type varchar(50) NOT NULL
);

CREATE TABLE hor_acc (
	hor_acc_code int PRIMARY KEY,
	tolerance_value float NOT NULL,
	tolerance_uom varchar(3),
	CONSTRAINT chk_hor_acc_uom CHECK (tolerance_uom IN ('ft', 'NM', 'unk'))
);

CREATE TABLE vert_acc (
	vert_acc_code char(1) PRIMARY KEY,
	tolerance_value float NOT NULL,
	tolerance_uom varchar(3) NOT NULL,
	CONSTRAINT chk_vert_acc_uom CHECK (tolerance_uom IN ('ft', 'unk'))
);

CREATE TABLE marking (
	marking_code char(1) PRIMARY KEY,
	maring_desc varchar(50) NOT NULL
);

CREATE TABLE lighting (
	lighting_code char(1) PRIMARY KEY,
	lighting_desc varchar(50) NOT NULL
);

CREATE TABLE verif_status (
	verif_status_code char(1) PRIMARY KEY,
	status_desc varchar(20) NOT NULL
);

CREATE TABLE obstacle (
	rec_id serial PRIMARY KEY,
	state_id serial NOT NULL,
	obst_ident char(9) NOT NULL UNIQUE,
	obst_type_id serial NOT NULL,
	lat_src char(12) NOT NULL,
	lon_src char(13) NOT NULL,
	agl float NOT NULL,
	amsl float,
	vert_acc_code char(1) NOT NULL,
	hor_acc_code int NOT NULL,
	quantity int NULL,
	marking_code char(1) NOT NULL,
	lighting_code char(1) NOT NULL,
	verif_status_code char(1) NOT NULL,
	city_name varchar(20) NULL,
	faa_study_number char(14) NULL,
	julian_date char(7) NULL,
	insert_tmsp TIMESTAMPTZ DEFAULT now(),
	insert_user VARCHAR(10) DEFAULT current_user,
	modification_tmsp TIMESTAMPTZ NULL,
	modification_user VARCHAR(10) NULL,
	loaction geography(POINT, 4326) NOT NULL,
    CONSTRAINT fk_obstacle_us_state
        FOREIGN KEY (state_id)
        REFERENCES us_state(state_id),
    CONSTRAINT fk_obstacle_obst_type
        FOREIGN KEY (obst_type_id)
        REFERENCES obstacle_type(obst_type_id),
    CONSTRAINT fk_obstacle_vert_acc
        FOREIGN KEY (vert_acc_code)
        REFERENCES vert_acc(vert_acc_code),
    CONSTRAINT fk_obstacle_hor_acc
        FOREIGN KEY (hor_acc_code)
        REFERENCES hor_acc(hor_acc_code),
    CONSTRAINT fk_obstacle_marking
        FOREIGN KEY (marking_code)
        REFERENCES marking(marking_code),
    CONSTRAINT fk_obstacle_lighting
        FOREIGN KEY (lighting_code)
        REFERENCES lighting(lighting_code),
    CONSTRAINT fk_obstacle_verif_status
        FOREIGN KEY (verif_status_code)
    REFERENCES verif_status(verif_status_code)
);

CREATE INDEX idx_obst_ident 
ON obstacle USING btree (obst_ident);
CREATE INDEX idx_obst_lon_src
ON obstacle USING btree (lon_src);
CREATE INDEX idx_obst_lat_src
ON obstacle USING btree (lat_src);

