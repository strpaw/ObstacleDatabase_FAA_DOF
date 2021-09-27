CREATE OR REPLACE FUNCTION update_modification_data() RETURNS TRIGGER AS
$BODY$
declare
    current_upd timestamptz;
    last_upd timestamptz;
    mod_user varchar(10);
begin
    SELECT now() INTO current_upd;
    SELECT coalesce (OLD.modification_tmsp, OLD.insert_tmsp) INTO last_upd;
    SELECT coalesce (OLD.modification_user, OLD.insert_user) INTO mod_user;

    new.modification_user = (select current_user);
    new.modification_tmsp = current_upd;

    INSERT INTO history_obstacle (rec_id,
                                  state_id,
                                  obst_ident,
                                  obst_type_id,
                                  lat_src,
                                  lon_src,
                                  agl,
                                  amsl,
                                  vert_acc_code,
                                  hor_acc_code,
                                  quantity,
                                  marking_code,
                                  lighting_code,
                                  verif_status_code,
                                  city_name,
                                  faa_study_number,
                                  julian_date,
                                  eff_from,
                                  eff_till,
                                  modification_user,
                                  geo_location)
    VALUES (OLD.rec_id,
            OLD.state_id,
	        OLD.obst_ident,
	        OLD.obst_type_id,
	        OLD.lat_src,
	        OLD.lon_src,
	        OLD.agl,
	        OLD.amsl,
	        OLD.vert_acc_code,
	        OLD.hor_acc_code,
	        OLD.quantity,
	        OLD.marking_code,
	        OLD.lighting_code,
	        OLD.verif_status_code,
	        OLD.city_name,
	        OLD.faa_study_number,
	        OLD.julian_date,
	        last_upd,
	        current_upd,
	        mod_user,
	        OLD.geo_location);
    return new;
end;
$BODY$
language PLPGSQL;

DROP TRIGGER IF EXISTS obstacle_modified ON obstacle;

CREATE TRIGGER obstacle_modified
    BEFORE UPDATE
    ON obstacle
    FOR EACH ROW
    EXECUTE PROCEDURE update_modification_data();
