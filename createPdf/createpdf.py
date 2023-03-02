import pandas as pd
from fpdf import FPDF
import math
import datetime
from mongoDb import mongodb


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
        self.mongoobj=mongodb(self.username,self.password)

    def createDataframe(self):
    
        '''
        desc : This method shall be used to create dataframe from the mongo database
        return : dataframe object
        Written By: Saif Ali
        Version: 1
        Revision: None
        '''
        cursor = self.mongoobj.getData(self.dbName,self.collectionName)
        df_pdf = pd.DataFrame(list(cursor))
        return df_pdf
    
    def elementCheckDeclare(self,value):

        '''
        desc : This method shall be used to check if the column is present or not in the df, and return the value
        return : str
        Written By: Saif Ali
        Version: 1
        Revision: None
        '''

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
        
    def createPdf(self):
        '''
        desc : This method shall be used to create pdf file from the df data
        return : NaN
        Written By: Saif Ali
        Version: 1
        Revision: None
        '''
        df_pdf=self.createDataframe()
        pdf = FPDF()
            # Add a new page to the PDF
        for df_i in range(len(df_pdf)):

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
                    pdf.output(f'pdfs/{course_name}_{formatted_date_time}.pdf', 'F')
                except Exception as e:
                    raise e

        if self.singlefile == True:
            try:
                pdf.output(f'pdfs/all_courses_{formatted_date_time}.pdf', 'F')
            except Exception as e:
                raise e


