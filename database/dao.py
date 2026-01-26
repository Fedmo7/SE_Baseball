from database.DB_connect import DBConnect
from model.TEAM import Team

class DAO:
    @staticmethod
    def query_year():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct t.`year` 
                    from team t     
                    where t.`year` >1980"""

        cursor.execute(query)

        for row in cursor:
            result.append(row['year'])

        cursor.close()
        conn.close()
        return result




    @staticmethod
    def get_all_team(anno):

        conn = DBConnect.get_connection()
        result = {}

        cursor = conn.cursor(dictionary=True)

        query ='''  select t.id,t.`year` ,t.team_code ,t.name ,sum(s.salary) as salary
                    from team t ,salary s 
                    where t.`year`=%s and s.team_id=t.id 
                    group by t.id,t.`year` ,t.team_code ,t.name 
                '''


        cursor.execute(query,(anno,))

        for row in cursor:
            squadra=Team(row['id'], row['year'], row['team_code'], row['name'],row['salary'])
            result[row['id']] = squadra

        cursor.close()
        conn.close()
        return result