from database.DB_connect import DBConnect
from model.arco import Arco
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getS():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct shape
                    from sighting s 
                    where s.shape is not null
                    order by shape DESC
                """
        cursor.execute(query)
        res = []
        for row in cursor:
            res.append(row["shape"])

        cursor.close()
        cnx.close()
        return res


    @staticmethod
    def getLa():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()
        query = """select distinct s.Lat 
                    from state s
                """
        cursor.execute(query, ())
        res = []
        for row in cursor:
            res.append(row[0])  # qua non serve il dictionary

        cursor.close()
        cnx.close()
        return res


    @staticmethod
    def getLo():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()
        query = """
                select distinct s.Lng
                from state s
                """
        cursor.execute(query, ())
        res = []
        for row in cursor:
            res.append(row[0])  # qua non serve il dictionary

        cursor.close()
        cnx.close()
        return res


    @staticmethod
    def getN(s, lat, lon):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select s.*
                    from state s, sighting s2 
                    where s.id  = s2.state and s.Lat > %s and s.Lng > %s and shape = %s"""
        cursor.execute(query, (lat, lon, s))
        res = []
        for row in cursor:
            res.append(State(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getA(s, lat, lon, mappa):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select n.state1 as st1, n.state2 as st2, (stato1.sommaavv1 + stato2.sommaavv2) as peso
from neighbor n, (select sta1.id as id1, SUM(sa1.duration) as sommaavv1
				from state sta1, sighting sa1
				where sta1.id  = sa1.state and sta1.Lat > %s and sta1.Lng > %s and sa1.shape = %s
				group by sa1.state ) as stato1,
	(select sta2.id as id2, SUM(sa2.duration) as sommaavv2
	from state sta2, sighting sa2
	where sta2.id  = sa2.state and sta2.Lat > %s and sta2.Lng > %s and sa2.shape = %s
	group by sa2.state) as stato2 
where n.state1 = stato1.id1 and n.state2 = stato2.id2
"""
        cursor.execute(query, (lat, lon, s, lat, lon, s))
        res = []
        for row in cursor:
            res.append((Arco(mappa[row["st1"]], mappa[row["st2"]], row["peso"])))
        cursor.close()
        cnx.close()
        return res




