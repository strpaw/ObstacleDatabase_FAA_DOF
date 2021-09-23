import psycopg2


class ObstacleDatabaseTools:

    def __init__(self, uri):
        self.uri = uri
        self.error = None

    def get_database_connection(self):
        return psycopg2.connect(host=self.uri.host(),
                                database=self.uri.database(),
                                user=self.uri.username(),
                                password=self.uri.password())

    def select_data_from_obstacle_db(self, query):
        connection = self.get_database_connection()
        cur = connection.cursor()
        cur.execute(query)
        fetched_data = cur.fetchall()
        cur.close()
        connection.commit()
        return fetched_data

    @staticmethod
    def get_procedure_parameters(data):
        """
        data: dict
        return: str
        """
        proc_params = ""
        for key, value in data.items():
            if type(value) in (int, float):
                proc_params += "{} := {}".format(key, value) + ','
            else:
                proc_params += "{} := '{}'".format(key, value) + ','

        return  proc_params.rstrip(',')

    def execute_stored_procedure(self, query):
        connection = self.get_database_connection()
        cur = connection.cursor()
        try:
            cur.execute(query)
            cur.close()
            connection.commit()
        except psycopg2.Error as e:
            self.error = e
        finally:
            cur.close()

    def execute_sql_query(self, connection, query):
        self.error = None
        cur = connection.cursor()
        try:
            cur.execute(query)
        except psycopg2.Error as e:
            self.error = e
        finally:
            cur.close()
            connection.commit()
