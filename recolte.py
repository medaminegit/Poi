from kafka import KafkaProducer
import pandas as pd
import requests
import re
import ijson
from Sql_DataAccess import Sql_DataAccess as sda
from NoSqlDataAccess import NoSqlDataAccess as no_sda

def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        f.close()
    return local_filename


#récuperation et traitement flux de données
def recolte_flux():
  url = "https://diffuseur.datatourisme.fr/webservice/71f73ef88ca23d12922211ebf458da06/b573255b-a872-4bad-89f4-2bd223849347"
  #filename=download_file(url)
  filename="/home/ubuntu/copievm/projet_poi/Poi/flux_04122022.json"
  graphs = ijson.items(open(filename), '@graph.item')
  return graphs

def alimenter_region():
    regions=pd.read_csv("/home/ubuntu/copievm/projet_poi/Poi/region.csv",sep=",",header=0)
    access_mysql=sda()
    access_mysql.insert_regions(regions)
def alimenter_departement():
    departements=pd.read_csv("/home/ubuntu/copievm/projet_poi/Poi/departement.csv",sep=",",header=0)
    access_mysql=sda()
    access_mysql.insert_departements(departements)

def traitement_data_frame_Nosql(data):
  data_graph_result=pd.DataFrame()
  data_graph = pd.DataFrame(data)
  data_graph_result['id']=data_graph['isLocatedAt'].str['schema:geo'].str["@id"]
  data_graph_result['type'] = data_graph["@type"]
  data_graph_result["latitude"] = data_graph['isLocatedAt'].str["schema:geo"].str["schema:latitude"].str["@value"]
  data_graph_result["longitude"] = data_graph['isLocatedAt'].str["schema:geo"].str["schema:longitude"].str["@value"]
  data_graph_result["adresse"] = data_graph['isLocatedAt'].str["schema:address"].str["schema:streetAddress"]
  data_graph_result["code_insee"] = data_graph["isLocatedAt"].str["schema:address"].str['hasAddressCity'].str['insee']
  return data_graph_result
def traitement_data_frame_sql(data):
  data_graph_result=pd.DataFrame()
  data_graph = pd.DataFrame(data)
  data_graph_result['id']=data_graph['@id']
  data_graph_result['lieu'] = data_graph["rdfs:label"].str["@value"]
  data_graph_result['contact']=data_graph["hasContact"].str["schema:telephone"].fillna('0')
  data_graph_result['date_modif_Datatourisme']=data_graph['lastUpdate'].str["@value"]
  data_graph_result['localisation_id']=data_graph['isLocatedAt'].str['schema:geo'].str["@id"]
  # data_graph_result["description"] = data_graph["owl:topObjectProperty"].str["owl:topDataProperty"].str["@value"].fillna('')
  #.replace('[\\r\\nœ\\]','',regex=True).astype(str)
  #data_graph_result["description"] = data_graph["description"].replace('[\\r\\nœ\\]','',regex=True).astype(str)
  
  '''
  data_graph = data_graph.dropna(subset=['lieu'])
  data_graph['type'] = data_graph["@type"]
  data_graph['type'] = data_graph['type'].replace('\[','',regex=True).astype(str)
  data_graph['type'] = data_graph['type'].replace("\'"," ",regex=True).astype(str)
  data_graph['type'] = data_graph['type'].replace("schema:","",regex=True).astype(str)
  data_graph["latitude"] = data_graph['isLocatedAt'].str["schema:geo"].str["schema:latitude"].str["@value"]
  data_graph["latitude"].isnull().values.any()
  data_graph = data_graph.dropna(subset=['latitude'])
  data_graph["longitude"] = data_graph['isLocatedAt'].str["schema:geo"].str["schema:longitude"].str["@value"]
  data_graph['latlong'] = data_graph['isLocatedAt'].str["schema:geo"].str['latlon'].str['@value']
  data_graph["ville"] = data_graph['isLocatedAt'].str["schema:address"].str["schema:addressLocality"]   
  data_graph["ville"] = data_graph["ville"].str.upper()
  data_graph["ville"]= data_graph["ville"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
  data_graph["ville"] = data_graph["ville"].replace('\-',' ',regex=True).astype(str)
  data_graph = data_graph.dropna(subset=['ville'])
  data_graph["adresse"] = data_graph['isLocatedAt'].str["schema:address"].str["schema:streetAddress"]
  data_graph["adresse"] = data_graph["adresse"].replace('\[','',regex=True).astype(str)
  data_graph["adresse"] = data_graph["adresse"].replace('\]','',regex=True).astype(str)
  data_graph["adresse"] = data_graph["adresse"].replace("\'",'',regex=True).astype(str)
  data_graph["adresse"] = data_graph["adresse"].replace('\"','',regex=True).astype(str)
  data_graph['region'] = data_graph.isLocatedAt.str['schema:address'].str['hasAddressCity'].str['isPartOfDepartment'].str['isPartOfRegion'].str['rdfs:label'].str['@value']
  data_graph["code_insee"] = data_graph["isLocatedAt"].str["schema:address"].str['hasAddressCity'].str['insee']
  data_graph["date_de_fin"] = data_graph['schema:endDate'].str['@value']
  data_graph = data_graph[['lieu','type','description', 'latitude', 'longitude', 'latlong', 'ville', 'adresse', 'code_insee','date_de_fin']]
  '''
  return data_graph_result

def push_flux_topic(df):
  kafka_producer = KafkaProducer(bootstrap_servers="localhost:9093")
  sep=","
  for index, row in df.iterrows(): 
    line=row["lieu"]+sep+str(row["lieu"])+sep+row["description"]+sep+row["latitude"]+sep+row["longitude"]+sep
    kafka_producer.send(topic="topic_poi", value=f"{line}".encode("utf-8"))
  kafka_producer.flush()


def main():
  print("function recolt")
  data=recolte_flux()
  print("function traitement_data_frame_Nosql")
  df=traitement_data_frame_Nosql(data)
  
  # sql=sda()
  #sql.insert_poi(df)
  neo4j_dataAccess=no_sda()
  neo4j_dataAccess.add_localisations(df)
  neo4j_dataAccess.close()

main()
