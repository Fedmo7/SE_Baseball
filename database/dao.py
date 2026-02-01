from database.DB_connect import DBConnect
from model.TEAM import Team

class DAO:

    @staticmethod
    def query_year():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct t.`year` 
                    from team t 
                    where t.`year` >=1980 """

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def query_team(year):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ select t.id,t.team_code,t.name , sum(s.salary) as salary 
                    from team t, salary s 
                    where t.`year`=%s and t.id=s.team_id 
                    group by t.id,t.team_code,t.name
                """

        cursor.execute(query,(year,))

        for row in cursor:
            result[row['id']] = Team(row['id'], row['team_code'], row['name'], row['salary'])

        cursor.close()
        conn.close()
        return result