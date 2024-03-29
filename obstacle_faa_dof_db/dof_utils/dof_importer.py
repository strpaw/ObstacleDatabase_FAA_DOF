""" Convert original Digital Obstacle File (dat format) into CSV, KML, SHP formats. """
from obstacle_faa_dof_db.dof_utils.dof_parser import DOFParser
from obstacle_faa_dof_db.dof_utils.dof_raw_data_validator import DOFRawDataValidator
from ..obstacle_database_tools import *
from obstacle_faa_dof_db.dof_utils.dof_logger import custom_logger


class DOFImporter:

    def __init__(self, path_dof_format):
        self.parser = DOFParser(path_dof_format)

    def import_dof(self, dof_path, db_uri, import_path):
        """ Import DOF (dat file) into database.
        param: dof_path: str
        param: db_uri: uri to database
        param: output_path: str
        """
        import_logger = custom_logger('dof_importer', import_path)

        obstacle_validator = DOFRawDataValidator()
        db_tools = ObstacleDatabaseTools(db_uri)
        conn = db_tools.get_database_connection()

        with open(dof_path, 'r') as input_dof:
            line_nr = 0
            for line in input_dof:
                line_nr += 1
                if line_nr >= 5:
                    obstacle_data = self.parser.parse_dof_line(line)
                    converted_data = obstacle_validator.validate_raw_data(obstacle_data)

                    if obstacle_validator._err_msg:
                        import_logger.error("DOF file line number: {} | {} ".format(line_nr, obstacle_validator._err_msg))
                    else:
                        proc_params = ObstacleDatabaseTools.get_procedure_parameters(converted_data)
                        query = "CALL insert_obstacle({})".format(proc_params)

                        db_tools.execute_sql_query(conn, query)
                        if db_tools.error:
                            import_logger.error("DOF file line number: {} | {} ".format(line_nr, db_tools.error))
