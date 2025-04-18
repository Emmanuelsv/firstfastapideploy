
# coneccion a la base de datos "C:\Users\PC\OneDrive\Workspace\Mongodb\bin\mongod.exe" --dbpath="C:\Users\PC\OneDrive\Workspace\Mongodb\data\db"

from pymongo import MongoClient


#db_client = MongoClient().local # si no se le pasa nada, se conecta a la base  de datos levantada en local    

#Base de datos remota

db_client = MongoClient(
    "mongodb+srv://emmanuelvas0521:6mg3CdWQWkcCtQdv@cluster0.acvleef.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test

     
