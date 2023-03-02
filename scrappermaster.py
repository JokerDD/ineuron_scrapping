import os
from selenium import webdriver
from ineuron_scrapping.pagescrapping import scrappingOperations
from mongoDb.mongodb import mongodbOperations
from mySql.mysql import mysqlOpeartions
from createpdf import createPdfoperations


class autoScrapper:

    '''
    This class shall be used for auto scrapping, It will trigger all the methods of this application in a chronological order
    Written By: Saif Ali
    Version: 1
    Revision: None
    '''

    def __init__(self):
        try:
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
            #self.lg = app_log(username='ineuron_scrapper', password='iNeuron')
        except Exception as e:
            raise e

    def connection_check(self):
        if self.dbOps.isCollectionPresent(dbName=self.dbName, collectionName=self.collectionName) and self.dbsql.createCursor():
            return True
        else:
            return False

    def autoscrapping(self):
        try:
            if self.connection_check():
                scrapper = scrappingOperations(chrome_options=self.chrome_options) # initialization of scrapping
                source_link="https://ineuron.ai/courses"
                all_course_link_list=scrapper.getAllCourseLink(source_link,load_time=120)

                try:
                    self.dbsql.createTables(schema_name="ineuron_course")
                except Exception as e:
                    raise e
            
                for course_link in all_course_link_list:

                    course_code_bs=scrapper.get_course_code(course_link)
                    course_data_dict=scrapper.basic_course_data(course_code_bs)
                    curr_project_code=scrapper.curr_and_proj(course_code_bs)
                    curr_data_dict=scrapper.curr_data(curr_project_code)
                    project_data_dict=scrapper.project_data(curr_project_code)

                    course_data_dict["course_link"] = course_link
                    course_data_dict["curriculum_details"] = curr_data_dict

                    if project_data_dict:
                        course_data_dict["project_details"] = project_data_dict
                        project_track=True
                    else:
                        project_track=True

                    self.dbOps.insertOneData(dbName="i_nearon_scrapping",collectionName="course_data",data=project_data_dict)

                    self.dbsql.masterInsertSql(course_link=course_link,course_data_dict=project_data_dict,project_track=project_track)

                self.pdfobj.createPdf()

            else:
                pass #check connections please
                
        except Exception as e:
            raise e
        
    def autoscrapping_one(self):
        try:
            if self.connection_check():
                scrapper = scrappingOperations(chrome_options=self.chrome_options) # initialization of scrapping
                source_link="https://ineuron.ai/courses"
                all_course_link_list=scrapper.getAllCourseLink(source_link,load_time=120)

                try:
                    self.dbsql.createTables(schema_name="ineuron_course")
                except Exception as e:
                    raise e

                course_link=all_course_link_list[143] # manually entering which course to scrap

                course_code_bs=scrapper.get_course_code()
                course_data_dict=scrapper.basic_course_data(course_code_bs)
                curr_project_code=scrapper.curr_and_proj(course_code_bs)
                curr_data_dict=scrapper.curr_data(curr_project_code)
                project_data_dict=scrapper.project_data(curr_project_code)

                course_data_dict["course_link"] = course_link
                course_data_dict["curriculum_details"] = curr_data_dict

                if project_data_dict:
                    course_data_dict["project_details"] = project_data_dict
                    project_track=True
                else:
                    project_track=True

                self.dbOps.insertOneData(dbName="i_nearon_scrapping",collectionName="course_data",data=project_data_dict)
                self.dbsql.masterInsertSql(course_link=course_link,course_data_dict=project_data_dict,project_track=project_track)
                self.pdfobj.createPdf()
                print("all completed")
            else:
                print("connections could not established")
                     
        except Exception as e:
            raise e

if __name__ == "__main__":
    
    scrap_test= autoScrapper()
    scrap_test.autoscrapping_one()
    


