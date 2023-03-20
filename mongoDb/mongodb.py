import pymongo
import sys
sys.path.append("C:\\Users\\saifa\\OneDrive\\Desktop\\ineuron projects\\my_own_ineuron_proj")
from custom_logging.customLogger import custLogger

class mongodbOperations:

    def __init__(self, username, password):
        
        self.username = username
        self.password = password
        self.url=f"mongodb+srv://{self.username}:{self.password}@cluster0.s896o.mongodb.net/?retryWrites=true&w=majority"
        self.logger = custLogger("INFO")
        
        
    def getMongoClient(self):
        '''
        Method Name: getMongoClient
        Description: It creates connection with the database
        Output: MongoClient
        On Failure: Exception

        Written By: Saif Ali
        Version: 1.0
        Revision: None
        '''
        try:
            client = pymongo.MongoClient(self.url)
            return client
        except Exception as e:
            self.logger.custlogger().info(f"error at cursor creation with :: {e} ")
            

    def getDatabase(self, dbName):
        '''
        Method Name: getDatabase
        Description: Gives database
        Output: database
        On Failure: Exception

        Written By: Saif Ali
        Version: 1.0
        Revision: None
        '''

        try:
            client = self.getMongoClient()
            database = client[dbName]
            return database
        except Exception as e:
            self.logger.custlogger().info(f"error at getting database with :: {e} ")
        
    def getCollection(self, dbName, collectionName):
        '''
        Method Name: getCollection
        Description: Gives collection of a database
        Output: collection
        On Failure: Exception

        Written By: Saif Ali
        Version: 1.0
        Revision: None
        '''
        try:
            database = self.getDatabase(dbName)
            collection = database[collectionName]
            return collection
        except Exception as e:
            self.logger.custlogger().info(f"error at collection creation with :: {e} ")
        
    def isDatabasePresent(self, dbName):
        '''
        Method Name: isDatabasePresent
        Description: Checks whether database present or not
        Output: True if present else False
        On Failure: Exception

        Written By: Saif Ali
        Version: 1.0
        Revision: None
        '''

        try:
            client = self.getMongoClient()
            if dbName in client.list_database_names():
                return True
            else:
                return False
        except Exception as e:
            self.logger.custlogger().info(f"error at database check with :: {e} ")
        
    
    def isCollectionPresent(self, dbName, collectionName):
        '''
        Method Name: isCollectionPresent
        Description: Checks whether collection under a given database present or not
        Output: True if present else False
        On Failure: Exception

        Written By: Saif Ali
        Version: 1.0
        Revision: None
        '''
        try:
            if self.isDatabasePresent(dbName):
                database = self.getDatabase(dbName)
                if collectionName in database.list_collection_names():
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            self.logger.custlogger().info(f"error at collection check with :: {e} ")
        

    
    def createDatabase(self, dbName):
        '''
        Method Name: createDatabase
        Description: creates a database
        Output: None
        On Failure: Exception

        Written By: Saif Ali
        Version: 1.0
        Revision: None
        '''

        try:
            client = self.getMongoClient()
            database = client[dbName]
        except Exception as e:
            self.logger.custlogger().info(f"error at database create with :: {e} ")

    def createCollection(self, dbName, collectionName):
        '''
        Method Name: createCollection
        Description: Creates collection under a given database
        Output: None
        On Failure: Exception

        Written By: Saif Ali
        Version: 1.0
        Revision: None
        '''
        try:
            database = self.getDatabase(dbName)
            collection = database[collectionName]
        except Exception as e:
            self.logger.custlogger().info(f"error at collection create with :: {e} ")
        
    def insertOneData(self,dbName,collectionName,data):
        '''
        Method Name: insertOneData
        Description: insert one data only
        Output: None
        On Failure: Exception

        Written By: Saif Ali
        Version: 1.0
        Revision: None
        '''

        try:
            collection = self.getCollection(dbName, collectionName)
            collection.insert_one(data)
        except Exception as e:
            self.logger.custlogger().info(f"error at insertion with :: {e} ")
        
    def getData(self,dbName, collectionName):
        '''
        Method Name: getData
        Description: Returns all data from a collection of the given database
        Output: Returns a cursor
        On Failure: Exception

        Written By: Saif Ali
        Version: 1.0
        Revision: None
        ''' 

        try:
            if self.isCollectionPresent(dbName, collectionName):
                collection=self.getCollection(dbName,collectionName)
                data= collection.find()
                return data
        except Exception as e:
            
            self.logger.custlogger().info(f"error at importing all data at once with :: {e} ")

    def deleteCollection(self,dbName,collectionName):

        try:
            if self.isCollectionPresent(dbName, collectionName):
                collection=self.getCollection(dbName,collectionName)
                collection.drop()
        except Exception as e:
            self.logger.custlogger().error(f"error at deleting collection in mongo db :: {e} ")

    def getCollectionName_latest(self,dbName,collectionName="coll_data",key_name="collection_name_iNeauron"):

        try:
            if self.isCollectionPresent(dbName, collectionName):
                collection=self.getCollection(dbName,collectionName)
                data= collection.find_one(sort=[('$natural', pymongo.DESCENDING)])
                last_primary_coll_name=data[key_name]
                return last_primary_coll_name
        except Exception as e:
            
            self.logger.custlogger().info(f"error at importing the primary collection name with :: {e} ")
    
    def getCollectionName_oldest(self,dbName,collectionName="coll_data"):

        try:
            if self.isCollectionPresent(dbName, collectionName):
                collection=self.getCollection(dbName,collectionName)
                oldest_doc = collection.find().sort([("_id", pymongo.ASCENDING)]).limit(1)[0]
                last_primary_coll_name=oldest_doc['collection_name_iNeauron']
                return last_primary_coll_name
        except Exception as e:
            
            self.logger.custlogger().info(f"error at importing the oldest collection name with :: {e} ")
    
    def updatePrimaryColl(self,dbName,primary_coll_name,status_data,collectionName="coll_data"):
        try:
            filter = {"collection_name_iNeauron":primary_coll_name}
            update= {"$set": {"status": status_data}}
            collection = self.getCollection(dbName, collectionName)
            collection.update_one(filter, update)
            
        except Exception as e:
            self.logger.custlogger().info(f"error at insertion with :: {e} ")

    def getDocCount(self,dbName,collectionName="coll_data"):

        try:
            if self.isCollectionPresent(dbName, collectionName):
                collection=self.getCollection(dbName,collectionName)
                count_doc= collection.count_documents({})
                return count_doc
        except Exception as e:
            self.logger.custlogger().info(f"error at doc count with :: {e} ")


    
        





    