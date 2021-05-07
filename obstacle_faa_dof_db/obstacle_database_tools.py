import psycopg2


class ObstacleDatabaseTools:

    def __init__(self, uri):
        self.uri = uri

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
