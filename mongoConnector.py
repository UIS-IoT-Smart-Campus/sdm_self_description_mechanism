import re
from pymongo import MongoClient

#Mongodb connection parameters
CONNECTION_STRING = "mongodb://localhost:27017"

class MongoConnector():

    def __init__(self,dbname='iot'):
        self.client = MongoClient(CONNECTION_STRING)
        self.db = self.client[dbname]
        self.collection = None
    
    def get_database(self):
        return self.db
    
    def get_all(self):
        devices_list = self.collection.all()
        return devices_list
    
    def create_or_set_collection(self,c_name):
        self.collection = self.db[c_name]
    
    def insert_document(self,document):
        document = self.collection.insert_one(document)
        return document

    def update_document(self,document):
        filter = {'global_id':document["global_id"]}
        old_document = self.get_one_document(filter)        
        data = self.get_update_data(old_document,document)
        document = self.collection.update_one(filter,data)
        return document
    
    def delete_document(self,document):
        filter = {'global_id':document["global_id"]}
        self.collection.delete_one(filter)
    
    def get_one_document(self,filter):
        document = self.collection.find_one(filter)
        if document:
            return document
        else:
            return None
    
    def get_update_data(self,old_document,new_document):
        update_data = {}
        delete_data = {}
        for key in new_document.keys():
            if key in old_document.keys():
                if new_document[key] != old_document[key]:
                    update_data[key] = new_document[key]
            else:
                update_data[key] = new_document[key]
        
        for key in old_document.keys():
            if key not in new_document.keys():
                delete_data["key"] = ""
        
        return {"$set":update_data,"$unset":delete_data}




