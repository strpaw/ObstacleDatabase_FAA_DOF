CREATE OR REPLACE PROCEDURE insert_obstacle(
    state_id int,
    obst_ident varchar(9),
    obst_type_id int,
    lat_src char(12),
    lon_src char(13),
    agl float,
    amsl float,
    vert_acc_code char(1),
    hor_acc_code int,
    marking_code char(1),
    lighting_code char(1),
    verif_status_code char(1),
    city_name varchar(20),
    lon_dd float,
    lat_dd float
)
LANGUAGE plpgsql
AS $$

#variable_conflict use_variable

DECLARE
    obst_loc geometry;
    is_within bool;
    state_name varchar;
BEGIN

    SELECT ST_SetSRID(ST_MakePoint(lon_dd, lat_dd), 4326)
    INTO obst_loc;

    SELECT
        ST_Within(obst_loc, boundary)
    INTO is_within
    FROM
        us_state
    WHERE
        us_state.state_id = state_id;

    IF is_within THEN
        INSERT INTO obstacle (state_id,
                              obst_ident,
                              obst_type_id,
                              lat_src,
                              lon_src,
                              agl,
                              amsl,
                              vert_acc_code,
                              hor_acc_code,
                              marking_code,
                              lighting_code,
                              verif_status_code,
                              city_name,
                              geo_location)
        VALUES (state_id,
                obst_ident,
                obst_type_id,
                lat_src,
                lon_src,
                agl,
                amsl,
                vert_acc_code,
                hor_acc_code,
                marking_code,
                lighting_code,
                verif_status_code,
                city_name,
                obst_loc :: geography);
    ELSE
        SELECT us_state.state_name
        INTO state_name
        FROM us_state
        WHERE us_state.state_id = state_id;
        RAISE NOTICE 'Obstacle outside % state!', state_name;
    END IF;
END; $$
