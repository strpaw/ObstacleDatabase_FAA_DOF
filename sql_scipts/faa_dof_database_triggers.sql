DROP TRIGGER IF EXISTS obstacle_modified ON obstacle;

CREATE OR REPLACE FUNCTION update_modification_data() RETURNS TRIGGER AS
/* Updates modification_user, modification_tmsp columns when record is modified */
$BODY$
begin
    new.modification_user = (select current_user);
    new.modification_tmsp = now();
    return new;
end;
$BODY$
language PLPGSQL;

CREATE TRIGGER obstacle_modified
    BEFORE UPDATE
    ON obstacle
    FOR EACH ROW
    EXECUTE PROCEDURE update_modification_data();
