from mysql.connector import (connection)
from mysql.connector import Error
from datetime import datetime
import pandas as pd

class Sql_DataAccess:
    def __init__(self):
        self.cnx = connection.MySQLConnection(user='poi', password='&QwtyCEZ53#XJ&1&D9SG7tq9d',
                                 host='127.0.0.1',
                                 database='poi')
    def insert_poi(self,data_graph):
        try:
            cursor= self.cnx.cursor()
            for index,row in data_graph.iterrows():
                libele=row['lieu'] 
                contact=row['contact'][0]
                localisation_id=row['localisation_id']
                lien=row['id']
                date_modification =datetime.strptime(row['date_modif_Datatourisme'],'%Y-%m-%d')
                #description=row['description'][:495]
                datas=(libele, contact,localisation_id,lien,date_modification)
                requete = ("INSERT INTO poi (libele, contact,localisation_id,lien,date_modification) VALUES (%s,%s,%s,%s,%s)")
                print(datas)
                cursor.execute(requete, datas)
                self.cnx.commit()
        except  Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            cursor.close()
            self.cnx.close()    
        finally:
            if self.cnx.is_connected():
                self.cnx.close()  
                cursor.close()
        
    def insert_regions(self,data_graph):
        try:
            cursor= self.cnx.cursor()
            for index,row in data_graph.iterrows():
                libele=row['NCC'] 
                code_inse=row['REG'] 
                datas=(libele,code_inse)
                requete = ("INSERT INTO region (libele,code_inse) VALUES (%s,%s)")
                cursor.execute(requete, datas)
                self.cnx.commit()
        except  Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            cursor.close()
            self.cnx.close()  
        finally:
            if self.cnx.is_connected():
                self.cnx.close()
                cursor.close()  
    def insert_departements(self,data_graph):
        try:
            cursor= self.cnx.cursor()
            for index,row in data_graph.iterrows():
                libele=row['NCC'] 
                code_inse_reg=row['REG'] 
                code_insee=row['DEP']
                requete="""select id from region WHERE code_inse = %s"""
                cursor.execute(requete,(code_inse_reg,))
                row=cursor.fetchone()
                datas=(libele,code_insee,row[0])
                requete = ("INSERT INTO departement (libele,code_insee,region_id) VALUES (%s,%s,%s)")
                cursor.execute(requete, datas)
                self.cnx.commit()
        except  Error as error:
                print("Failed to insert into MySQL table {}".format(error))
                cursor.close()
                self.cnx.close()    
        finally:
            if self.cnx.is_connected():
                self.cnx.close()  
                cursor.close()
