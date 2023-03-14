import os
from selenium import webdriver
import datetime
from ineuron_scrapping.pagescrapping import scrappingOperations
from mongoDb.mongodb import mongodbOperations
#from mySql.mysql import mysqlOpeartions
from createpdf import createPdfoperations
from custom_logging.customLogger import custLogger


class autoScrapper:

    '''
    This class shall be used for auto scrapping, It will trigger all the methods of this application in a chronological order
    Written By: Saif Ali
    Version: 1
    Revision: None
    '''

    def __init__(self):
    
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--no-sandbox")
        #self.driver_path=os.environ.get("CHROMEDRIVER_PATH")
        # self.driver_path = './chromedriver'
        self.dbName = 'i_nearon_scrapping'
        self.collectionName = self.mongo_collect_name()
        self.dbOps = mongodbOperations(username='saif_1', password='saif_1')
        #self.dbsql= mysqlOpeartions(username="root",password="Shakil@321",host="localhost")
        self.pdfobj = createPdfoperations(username="saif_1",password="saif_1",dbName=self.dbName,collectionName=self.collectionName,singlefile=True)
        self.logger=custLogger("INFO")


    def mongo_collect_name(self):
        try:
            collectionName = datetime.datetime.now().strftime("collect_%d_%h_%Y_%I_%M_%S_%p")
            return collectionName

        except Exception as e:
            self.logger.custlogger().info(f"db intiatisation dailed with error :: {e}")
            return False
    def mongo_db_name_add(self, collname):
        """
        This method will create or check coll_data collection in mongo db, coll_data collection will store the primary collections details
        """
        try:
            collection_name="coll_data"
            if self.dbOps.isCollectionPresent(dbName=self.dbName, collectionName=collection_name):
                coll_name_data={'collection_name_iNeauron' : collname}
                self.dbOps.insertOneData(dbName=self.dbName,collectionName=collection_name,data=coll_name_data)
                self.dbOps.updatePrimaryColl(dbName=self.dbName,primary_coll_name=self.collectionName,status_data="in_progress")
            else:
                self.dbOps.createCollection(dbName=self.dbName, collectionName=collection_name)
                coll_name_data={'collection_name_iNeauron' : collname}
                self.dbOps.insertOneData(dbName=self.dbName,collectionName=collection_name,data=coll_name_data)
                self.dbOps.updatePrimaryColl(dbName=self.dbName,primary_coll_name=self.collectionName,status_data="in_progress")
        except Exception as e:
            self.logger.custlogger().error(f"failed to save the name of the primary collection with error :: {e}")

    def mongo_connection_check(self):
        if self.collectionName is not False:
            if self.dbOps.isCollectionPresent(dbName=self.dbName, collectionName=self.collectionName):
                return True
            else:
                try:
                    self.dbOps.createCollection(dbName=self.dbName, collectionName=self.collectionName)
                    self.logger.custlogger().info("collection created in mongo db")
                    self.mongo_db_name_add(self.collectionName)
                    
                    return True
                except Exception as e:
                    self.logger.custlogger().error(f"failed with an error :: {e} :: at creating collection on mongo db")
                    return False
        else:
            return False
            
    def mysql_connection_check(self):
        if self.dbsql.createCursor():
            return True
        else:
            self.logger.custlogger().info("failed creating cursor for the mysql db")
            return False
    
    def appstart(self,course_count):
        self.logger.custlogger().info("Application start##############################################")
        print(f"{course_count} courses will be scrapped") #debug
        collection_count=self.dbOps.getDocCount(self.dbName,"coll_data")
        if isinstance(collection_count,int):
            if collection_count > 5:
                try:
                    oldest_coll=self.dbOps.getCollectionName_oldest(self.dbName)
                    self.dbOps.deleteCollection(self.dbName,oldest_coll)
                    self.logger.custlogger().error(f"collection {oldest_coll} deleted successfully")
                except Exception as e:
                    self.logger.custlogger().error(f"collection {oldest_coll} deletion failed, current count of primary collection are : {collection_count}")
            else:
                self.logger.custlogger().info(f"primary collection less than 5")
        else:
            self.logger.custlogger().info(f"no data in coll_data collection")

        if self.mongo_connection_check():# and self.mysql_connection_check():
            try:
                #self.dbsql.createTables(schema_name="ineuron_course")
                self.autoscrapping(course_count)
            except Exception as e:
                self.logger.custlogger().error(f"failed with error :: {e}")

            
        else:
            print("check connections please")

    def autoscrapping(self,course_count):
        
        scrapper = scrappingOperations(chrome_options=self.chrome_options) # initialization of scrapping
        source_link="https://ineuron.ai/courses"
        all_course_link_list=scrapper.getAllCourseLink(source_link,load_time=10)

        counter=0
        #for course_link in all_course_link_list:
        print(course_count,len(all_course_link_list))
        self.logger.custlogger().info(f"count from user {course_count} and total links {len(all_course_link_list)}")
        if course_count <= len(all_course_link_list):
            logger_instance=self.logger.custlogger()
            for i in range(0,course_count):  #for testing a batch

                course_link = all_course_link_list[i]  # for testing 
                logger_instance.info(f" course link -----------------------> {course_link}")
                course_code_bs=scrapper.get_course_code(course_link)
                course_data_dict=scrapper.basic_course_data(course_code_bs)
                curr_project_code=scrapper.curr_and_proj(course_code_bs)
                curr_data_dict=scrapper.curr_data(curr_project_code)
                project_data_dict=scrapper.project_data(curr_project_code)

                course_data_dict["course_link"] = course_link
                #course_data_dict["curriculum_details"] = curr_data_dict

                if curr_data_dict:
                    course_data_dict["curriculum_details"] = curr_data_dict
                    curr_track=True
                else:
                    curr_track=False
                    logger_instance.info(f"curr is not present in this course :: {course_link}")

                if project_data_dict:
                    course_data_dict["project_details"] = project_data_dict
                    project_track=True
                else:
                    project_track=False
                    logger_instance.info(f"project not present in {course_link}")
                
                try:
                    self.dbOps.insertOneData(dbName=self.dbName,collectionName=self.collectionName,data=course_data_dict)
                except Exception as e:
                    logger_instance.info(f"error at mongo db insert with :: {e}")

                try:
                    pass
                    #self.dbsql.masterInsertSql(course_link=course_link,course_data_dict=course_data_dict,project_track=project_track,curr_track=curr_track)
                except Exception as e:
                    logger_instance.info(f"error at mysql db insert with :: {e}")

                counter+=1

                
            try:
                self.pdfobj.createPdf()
            except Exception as e:
                self.logger.custlogger().info(f"error at create pdf with :: {e}")
            print("all completed")
            #dbName,primary_coll_name,status_data,
            self.dbOps.updatePrimaryColl(dbName=self.dbName,primary_coll_name=self.collectionName,status_data="completed")
            print(counter)
            return True
        else:
            self.logger.custlogger().info("count too high")
            return False

                       
    def autoscrapping_one(self):
        self.logger.custlogger().info("Application start##############################################")
        
        print("program is inside autoscrapping one")
        if self.mongo_connection_check() and self.mysql_connection_check():
            scrapper = scrappingOperations(chrome_options=self.chrome_options) # initialization of scrapping
            
            source_link="https://ineuron.ai/courses"
            #all_course_link_list=scrapper.getAllCourseLink(source_link,load_time=30)

            try:
                self.dbsql.createTables(schema_name="ineuron_course")
            except Exception as e:
                raise e

            #INDEX_TEST=all_course_link_list.index('https://ineuron.ai/course/Data-Science-Masters')

            #course_link=all_course_link_list[INDEX_TEST] # manually entering which course to scrap
            course_link="https://ineuron.ai/course/Data-Science-Masters"           

            course_code_bs=scrapper.get_course_code(course_link)
            course_data_dict=scrapper.basic_course_data(course_code_bs)
            curr_project_code=scrapper.curr_and_proj(course_code_bs)
            curr_data_dict=scrapper.curr_data(curr_project_code)
            project_data_dict=scrapper.project_data(curr_project_code)

            course_data_dict["course_link"] = course_link
            course_data_dict["curriculum_details"] = curr_data_dict

            if curr_data_dict:
                course_data_dict["curriculum_details"] = curr_data_dict
                curr_track=True
            else:
                curr_track=False
                self.logger.custlogger().info(f"curr is not present in this course :: {course_link}")

            if project_data_dict:
                course_data_dict["project_details"] = project_data_dict
                project_track=True
            else:
                project_track=False
                self.logger.custlogger().info(f"project is not present in this course :: {course_link}")

            
            try:
                self.dbOps.insertOneData(dbName="i_nearon_scrapping",collectionName="course_data",data=course_data_dict)
            except Exception as e:
                self.logger.custlogger().info(f"error at mongo db insert with :: {e}")
            
            try:
                self.dbsql.masterInsertSql(course_link=course_link,course_data_dict=course_data_dict,project_track=project_track,curr_track=curr_track)
            except Exception as e:
                self.logger.custlogger().info(f"error at mysql db insert with :: {e}")
            try:
                self.pdfobj.createPdf()
            except Exception as e:
                self.logger.custlogger().info(f"error at create pdf with :: {e}")
            print("all completed")
        else:
            print("connections could not established")


if __name__ == "__main__":

    scrap_test= autoScrapper()
    scrap_test.autoscrapping_one()
    
    #appstart(400)
    #autoscrapping_one
    #autoscrapping
    


