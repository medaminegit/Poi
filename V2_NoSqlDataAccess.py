from neo4j import GraphDatabase, basic_auth
import pandas as pd
import math

#df = pd.read_csv('data_graph_def.csv')
#df = df[['lieu', 'type', 'latitude', 'longitude', 'ville']]
#df = df.head(500)

class Point:
    def __init__(self,longitude,latitude):
        self.longitude=longitude
        self.latitude=latitude

class NoSqlDataAccess:

    def __init__(self):
        self.driver = GraphDatabase.driver('bolt://localhost:11003',auth=basic_auth("neo4j", "projetdatascientest"))
    
    def close(self):
        self.driver.close()
   
    def create_localisation_line(tx,type, latitude, longitude, lieu,code_insee,id_datatourisme):
            query = "CREATE (n:Localisation {type: $type ,latitude: $latitude,longitude: $longitude, lieu: $lieu,code_insee: $code_insee,id_datatourisme: $id_datatourisme}) RETURN id(n) AS node_id"
            
            tx.run(query,type = type,latitude = latitude, longitude = longitude, lieu = lieu,code_insee=code_insee,id_datatourisme=id_datatourisme)
            

    def add_localisations(self,datagraph):
       with self.driver.session() as session:
            for i, row in datagraph.iterrows():
                #if i==100000:
                #    break
                #else:
                type = row['type']
                latitude = row['latitude']
                longitude = row['longitude']
                lieu = row['adresse']
                code_insee=row['code_insee']
                id_datatourisme=row['id']
                query = "CREATE (n:Localisation {type:"+str(row['type'])+",latitude:"+str(latitude)+",longitude: "+str(longitude)+", lieu: "+str(lieu)+",code_insee: "+str(code_insee)+",id_datatourisme:"+str(id_datatourisme)+"})"
                print(query)
                session.run(query)
       self.close()


    def recherche_distance(self):
        with self.driver.session() as session:
            cypher_query = '''
                MATCH (s1:Info)
                WITH point({x : toFloat(s1.latitude), y : toFloat(s1.longitude)}) AS p1, point({x:toFloat(45.4396416), y:toFloat(4.3857321)}) AS p2, s1
                RETURN point.distance(p1,p2) AS Distance, s1.lieu AS Lieu ORDER BY Distance
                '''

            result = session.run(cypher_query)
            return result.fetch(5)
        self.close()

