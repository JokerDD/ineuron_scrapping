import pandas as pd
from fpdf import FPDF
import math
import datetime
from mongoDb.mongodb import mongodbOperations
from custom_logging.customLogger import custLogger


now = datetime.datetime.now()

formatted_date_time = now.strftime("%d_%b_%y")

class createPdfoperations:
    '''
    desc : This class shall be used to create pdf files from mongo database
    return : list of all the courses
    Written By: Saif Ali
    Version: 1
    Revision: None
    '''

    def __init__(self,username,password,dbName,collectionName, singlefile=True):
        self.username=username
        self.password=password
        self.dbName=dbName
        self.collectionName=collectionName
        self.singlefile=singlefile
        self.mongoobj=mongodbOperations(self.username,self.password)
        self.logger=custLogger()

    def createDataframe(self):
    
        '''
        desc : This method shall be used to create dataframe from the mongo database
        return : dataframe object
        Written By: Saif Ali
        Version: 1
        Revision: None
        '''
        try:
            cursor = self.mongoobj.getData(self.dbName,self.collectionName)
            df_pdf = pd.DataFrame(list(cursor))
            if len(df_pdf) >0:
                return df_pdf
            else:
                return False
        except Exception as e:
            self.logger.custlogger().error(f"error at creating dataframe with :: {e}")
            return False
    
    def elementCheckDeclare(self,column_name,loop_number,df_name,log_instance):

        '''
        desc : This method shall be used to check if the column is present or not in the df, and return the value
        return : str
        Written By: Saif Ali
        Version: 1
        Revision: None
        '''
        try:
            value=df_name[column_name][loop_number]

            if isinstance(value,dict) and len(value)>0:
                return value
            elif isinstance(value,list) and len(value)>0:
                return value
            elif isinstance(value,str) and len(value)>0:
                return value
            elif isinstance(value,int) and len(value)>0:
                return value
            elif isinstance(value,set) and len(value)>0:
                return value
            elif isinstance(value,bool):
                if math.isnan(value):
                    return False
            else:
                return False
        except Exception as e:
            if column_name=='project_details':
                log_instance.debug(f"possibly column {column_name} not present in df with error :: {e}")
            else:
                log_instance.error(f"possibly column {column_name} not present in df with error :: {e}")
            return False

        
        
    def createPdf(self):
        '''
        desc : This method shall be used to create pdf file from the df data
        return : NaN
        Written By: Saif Ali
        Version: 1
        Revision: None
        '''
        df_pdf=self.createDataframe()
        
        if isinstance(df_pdf, pd.DataFrame):
            
            if not df_pdf.empty:
                pdf = FPDF()
                    # Add a new page to the PDF
                logger_instance=self.logger.custlogger()
                for df_i in range(len(df_pdf)):
                    

                    course_link=self.elementCheckDeclare(column_name='course_link',loop_number=df_i,df_name=df_pdf,log_instance=logger_instance)
                    topic_name=self.elementCheckDeclare(column_name='topic',loop_number=df_i,df_name=df_pdf,log_instance=logger_instance)
                    sub_topic_name=self.elementCheckDeclare(column_name='sub_topic',loop_number=df_i,df_name=df_pdf,log_instance=logger_instance)
                    course_name=self.elementCheckDeclare(column_name='course_name',loop_number=df_i,df_name=df_pdf,log_instance=logger_instance)
                    course_descript=self.elementCheckDeclare(column_name='course_description',loop_number=df_i,df_name=df_pdf,log_instance=logger_instance)
                    course_feature=self.elementCheckDeclare(column_name='course_feature',loop_number=df_i,df_name=df_pdf,log_instance=logger_instance)
                    what_u_will_learn=self.elementCheckDeclare(column_name='what_u_will_learn',loop_number=df_i,df_name=df_pdf,log_instance=logger_instance)
                    requirements=self.elementCheckDeclare(column_name='requirements',loop_number=df_i,df_name=df_pdf,log_instance=logger_instance)
                    instructor_details=self.elementCheckDeclare(column_name='instructor_details',loop_number=df_i,df_name=df_pdf,log_instance=logger_instance)
                    curriculum_details=self.elementCheckDeclare(column_name='curriculum_details',loop_number=df_i,df_name=df_pdf,log_instance=logger_instance)
                    project_details=self.elementCheckDeclare(column_name='project_details',loop_number=df_i,df_name=df_pdf,log_instance=logger_instance)
                    """
                    course_link=self.elementCheckDeclare(df_pdf['course_link'][df_i])
                    topic_name=self.elementCheckDeclare(df_pdf['topic'][df_i])
                    sub_topic_name=self.elementCheckDeclare(df_pdf['sub_topic'][df_i])
                    course_name=self.elementCheckDeclare(df_pdf['course_name'][df_i])
                    course_descript=self.elementCheckDeclare(df_pdf['course_description'][df_i])
                    course_feature=self.elementCheckDeclare(df_pdf['course_feature'][df_i])
                    what_u_will_learn=self.elementCheckDeclare(df_pdf['what_u_will_learn'][df_i])
                    requirements=self.elementCheckDeclare(df_pdf['requirements'][df_i])
                    instructor_details=self.elementCheckDeclare(df_pdf['instructor_details'][df_i])
                    curriculum_details=self.elementCheckDeclare(df_pdf['curriculum_details'][df_i])
                    project_details=self.elementCheckDeclare(df_pdf['project_details'][df_i])
                    """
                    # Create a PDF object

                    pdf.add_page()

                    if course_name:
                        pdf.set_font('Arial', 'B', 15)
                        pdf.multi_cell(0, 10, course_name ,'B',15,"C")
                    else:
                        pdf.set_font('Arial', 'B', 15)
                        pdf.cell(0, 10, 'Course name not present' ,'B',15,"C")

                    pdf.cell(2, 6, '' ,'',8,"L")

                    if topic_name:
                        pdf.set_font('Arial', '', 10)
                        pdf.cell(2, 6, 'Topic Name : ' + topic_name ,'',8,"L")

                    if sub_topic_name:
                        pdf.set_font('Arial', '', 10)
                        pdf.cell(2, 6, 'Sub-topic Name : ' + sub_topic_name ,'',8,"L")

                    if course_link:
                        pdf.set_font('Arial', '', 10)
                        pdf.cell(2, 6, 'Course link : ' + course_link ,'',8,"L")

                    if course_descript:
                        pdf.set_font('Arial', 'U', 10)
                        pdf.cell(2, 6, 'Course Description :-','',8,"L")
                        #pdf.cell(2, 4, '' ,'',8,"L")


                        pdf.set_font('Arial', '', 8)
                        pdf.multi_cell(170, 5, course_descript,align='L')

                    if course_feature:

                        pdf.set_font('Arial', 'U', 10)
                        pdf.cell(2, 6, 'Course Features :-','',8,"L")
                        pdf.set_font('Arial', '', 8)
                        for i in course_feature:
                            pdf.multi_cell(170, 5, '=> ' + i,align='L')

                    if what_u_will_learn:
                        pdf.set_font('Arial', 'U', 10)
                        pdf.cell(2, 6, 'What you will learn :-','',8,"L")
                        pdf.set_font('Arial', '', 8)
                        for i in what_u_will_learn:
                            pdf.multi_cell(170, 5, '=> ' + i,align='L')

                    if requirements:
                        pdf.set_font('Arial', 'U', 10)
                        pdf.cell(2, 6, 'Requirements :-','',8,"L")
                        pdf.set_font('Arial', '', 8)
                        for i in requirements:
                            pdf.multi_cell(170, 5, '=> ' + i,align='L')

                    if instructor_details:
                        pdf.set_font('Arial', 'U', 10)
                        pdf.cell(2, 6, 'Instructors :-','',8,"L")
                        #instructor_details

                        for key, value in instructor_details.items():
                            pdf.set_font('Arial', '', 8)
                            pdf.multi_cell(170, 5, '=> ' + key + ' :',align='L')
                            pdf.set_font('Arial', 'I', 7)
                            pdf.multi_cell(170, 3, ' ~ ' + value,align='L')


                    if curriculum_details:
                        pdf.set_font('Arial', 'U', 10)
                        pdf.cell(2, 6, 'Curriculum details :-','',8,"L")


                        for key, value in curriculum_details.items():
                            if isinstance(value, list) and len(value)>0:
                                pdf.set_font('Arial', '', 8)
                                pdf.multi_cell(170, 5, '=> ' + key + ' :',align='L')

                                pdf.set_font('Arial', 'I', 7)
                                for item in value:
                                    pdf.multi_cell(170, 3, ' ~ ' + item,align='L')
                            else:
                                pdf.set_font('Arial', '', 8)
                                pdf.multi_cell(170, 5, '=> ' + key ,align='L')

                    #project_details

                    if project_details:
                        pdf.set_font('Arial', 'U', 10)
                        pdf.cell(2, 6, 'Project details :-','',8,"L")

                        for key, value in project_details.items():
                            if isinstance(value, list) and len(value)>0:
                                pdf.set_font('Arial', '', 8)
                                pdf.multi_cell(170, 5, '=> ' + key + ' :',align='L')

                                pdf.set_font('Arial', 'I', 7)
                                for item in value:
                                    pdf.multi_cell(170, 3, ' ~ ' + item,align='L')
                            else:
                                pdf.set_font('Arial', '', 8)
                                pdf.multi_cell(170, 5, '=> ' + key ,align='L')
                    
                    if self.singlefile == False:
                        try:
                            pdf.output(f'pdfs_many/{course_name}_{formatted_date_time}.pdf', 'F')
                        except Exception as e:
                            logger_instance.error(f"error at creating many pdf file with :: {e}")

                if self.singlefile == True:
                    try:
                        pdf.output(f'pdfs_single/all_courses_{formatted_date_time}.pdf', 'F')
                    except Exception as e:
                        self.logger.custlogger().error(f"error at creating single pdf file with :: {e}")
            else:
                self.logger.custlogger().info(f"dataframe is empty possibly becuase there is no data in mongo DB, check mongo class")
        else:
            self.logger.custlogger().info(f"dataframe not created possibly becuase there is no data in mongo DB, check mongo class")
        


if __name__ == "__main__":
    manual_pdf_object=createPdfoperations(username="saif_1",password="saif_1",dbName="i_nearon_scrapping",collectionName="course_data",singlefile=True)
    manual_pdf_object.createPdf()


