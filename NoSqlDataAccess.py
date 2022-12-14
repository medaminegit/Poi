from neo4j import GraphDatabase, basic_auth
import pandas as pd
class NoSqlDataAccess:

    def __init__(self):
        self.driver = GraphDatabase.driver('bolt://54.195.243.32:7687',auth=basic_auth('neo4j', 'neo4j'))
    
    def close(self):
        self.driver.close()
   
    def create_localisation_line(tx,type, latitude, longitude, lieu,code_insee,id_datatourisme):
            query = "CREATE (n:Localisation {type: $type ,latitude: $latitude,longitude: $longitude, lieu: $lieu,code_insee: $code_insee,id_datatourisme: $id_datatourisme}) RETURN id(n) AS node_id"
            
            tx.run(query,type = type,latitude = latitude, longitude = longitude, lieu = lieu,code_insee=code_insee,id_datatourisme=id_datatourisme)
            

    def add_localisations(self,datagraph):
       with self.driver.session() as session:
            for i, row in datagraph.iterrows():
                if i==100:
                    break
                else:
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