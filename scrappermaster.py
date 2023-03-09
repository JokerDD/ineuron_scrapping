import os
from selenium import webdriver
from ineuron_scrapping.pagescrapping import scrappingOperations
from mongoDb.mongodb import mongodbOperations
from mySql.mysql import mysqlOpeartions
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
        self.collectionName = 'course_data'
        self.dbOps = mongodbOperations(username='saif_1', password='saif_1')
        self.dbsql= mysqlOpeartions(username="root",password="Shakil@321",host="localhost")
        self.pdfobj = createPdfoperations(username="saif_1",password="saif_1",dbName="i_nearon_scrapping",collectionName="course_data",singlefile=True)
        self.logger=custLogger("INFO")
        

    def mongo_connection_check(self):
        if self.dbOps.isCollectionPresent(dbName=self.dbName, collectionName=self.collectionName):
            return True
        else:
            try:
                self.dbOps.createCollection(dbName=self.dbName, collectionName=self.collectionName)
                self.logger.custlogger().info("collection created in mongo db")
                
                return True
            except Exception as e:
                self.logger.custlogger().error(f"failed with an error :: {e} :: at creating collection on mongo db")
                return False
            
    def mysql_connection_check(self):
        if self.dbsql.createCursor():
            return True
        else:
            self.logger.custlogger().info("failed creating cursor for the mysql db")
            return False
            

    def autoscrapping(self):
        self.logger.custlogger().info("Application start##############################################")
        print("program is inside autoscrapping for loop") #debug
        if self.mongo_connection_check() and self.mysql_connection_check():
            scrapper = scrappingOperations(chrome_options=self.chrome_options) # initialization of scrapping
            source_link="https://ineuron.ai/courses"
            all_course_link_list=scrapper.getAllCourseLink(source_link,load_time=30)

            try:
                self.dbsql.createTables(schema_name="ineuron_course")
            except Exception as e:
                self.logger.custlogger().error("failed creating tables in mySQL")
            counter=0
            #for course_link in all_course_link_list:
            logger_instance=self.logger.custlogger()
            for i in range(0,10):  #for testing a batch

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
                    self.dbOps.insertOneData(dbName="i_nearon_scrapping",collectionName="course_data",data=course_data_dict)
                except Exception as e:
                    logger_instance.info(f"error at mongo db insert with :: {e}")

                try:
                    self.dbsql.masterInsertSql(course_link=course_link,course_data_dict=course_data_dict,project_track=project_track,curr_track=curr_track)
                except Exception as e:
                    logger_instance.info(f"error at mysql db insert with :: {e}")

                counter+=1

                
            try:
                self.pdfobj.createPdf()
            except Exception as e:
                self.logger.custlogger().info(f"error at create pdf with :: {e}")
            print("all completed")
            print(counter)

        else:
            print("check connections please")
                       
        
        
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
            course_link="https://ineuron.ai/course/Deep-Learning-With-Computer-Vision-and-Advanced-NLP"           

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
    scrap_test.autoscrapping()
    
    #autoscrapping_one
    #autoscrapping
    


