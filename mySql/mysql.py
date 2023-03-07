import mysql.connector 
import sys
sys.path.append("C:\\Users\\saifa\\OneDrive\\Desktop\\ineuron projects\\my_own_ineuron_proj")

from custom_logging.customLogger import custLogger

class mysqlOpeartions:

    '''
    desc : This class shall be used to create Mysql objects and insert data into the Mysql database
    Written By: Saif Ali
    Version: 1
    Revision: None
    '''

    def __init__(self, username, password, host):
        self.username =username
        self.password =password
        self.host =host
        self.mydb=self.myDb()
        self.mycursor = self.createCursor()
        self.logger = custLogger("INFO")

    def myDb(self):

        '''
        desc : This method shall be used to initiate the mySql database (connect to database)
        return : mySql object
        Written By: Saif Ali
        Version: 1
        Revision: None
        '''

        mydb = mysql.connector.connect(
        host=self.host,
        user=self.username,
        password=self.password)

        return mydb


    def createCursor(self):
        
        '''
        desc : This method shall be used to create cursor it will automaticaly call the myDb method
        return : cursor object
        Written By: Saif Ali
        Version: 1
        Revision: None
        '''

        try:
            mycursor = self.mydb.cursor()
        except Exception as e:
            self.logger.custlogger().info(f"error at cursor creation with :: {e} ")
            mycursor=False
        return mycursor
    
    def sqlObjectCheck(self):
        '''
        desc : This method shall be used to check if the object are already presnt in the database or not
        Written By: Saif Ali
        Version: 1
        Revision: None
        '''
        pass

    def createTables(self,schema_name):

        '''
        desc : This method shall be used to create all the database object in the mySql database
        return : boolean (True or False)
        Written By: Saif Ali
        Version: 1
        Revision: None
        '''
        try:
            self.mycursor.execute(f"""
            create table {schema_name}.all_course (
            course_link varchar(1000),
            topic_name varchar(1000),
            sub_topic_name varchar(1000),
            course_name varchar(1000),
            course_desc varchar(1000)
            );
            """)
        except Exception as e:
            self.logger.custlogger().info(f"error at table all_course creation with :: {e} ")
            print('table already exists')
            
        try:
            self.mycursor.execute(f"""
            create table {schema_name}.all_features (
            course_link varchar(1000),
            course_feature varchar(1000)
            );
            """)
        except Exception as e:
            self.logger.custlogger().info(f"error at table all_features creation with :: {e} ")
            print('table already exists')
        
        try:
            self.mycursor.execute(f"""
            create table {schema_name}.all_what_you_will_learn(
            course_link varchar(1000),
            learning_topics varchar(1000)
            );
            """)
        except Exception as e:
            self.logger.custlogger().info(f"error at table all_what_you_will_learn creation with :: {e} ")
            print('table already exists')
        
        try:
            self.mycursor.execute(f"""
            create table {schema_name}.all_requirenments(
            course_link varchar(1000),
            course_require varchar(1000)
            );
            """)
        except Exception as e:
            self.logger.custlogger().info(f"error at table all_requirenments creation with :: {e} ")
            print('table already exists')
        
        try:
            self.mycursor.execute(f"""
            create table {schema_name}.all_curriculum(
            course_link varchar(1000),
            course_curriculum varchar(1000),
            course_details varchar(1000)
            );
            """)
        except Exception as e:
            self.logger.custlogger().info(f"error at table all_curriculum creation with :: {e} ")
            print('table already exists')
        
        try:
            self.mycursor.execute(f"""
            create table {schema_name}.all_projects(
            course_link varchar(1000),
            project_name varchar(1000),
            project_details varchar(1000)
            );
            """)
        except Exception as e:
            self.logger.custlogger().info(f"error at table all_projects creation with :: {e} ")
            print('table already exists')
        
        try:
            self.mycursor.execute(f"""
            create table {schema_name}.all_instructors(
            course_link varchar(1000),
            instructor_name varchar(1000),
            instructor_details varchar(1000)
            );
            """)
            
        except Exception as e:
            self.logger.custlogger().info(f"error at table all_instructors creation with :: {e} ")
            print('table already exists')
        
        return True
    
    def insertBasicData(self,course_link,basic_data):

        '''
        desc : This method shall be used to insert the basic data realted to course in the tables all_course, all_features, all_what_you_will_learn & all_requirenments
        return : boolean (True or False)
        Written By: Saif Ali
        Version: 1
        Revision: None
        '''
        try:
            sql_1="insert into ineuron_course.all_course values (%s,%s,%s,%s,%s)"
            all_course_value=(course_link,basic_data["topic"],basic_data["sub_topic"],basic_data["course_name"],basic_data["course_description"])

            sql_2="insert into ineuron_course.all_features values (%s,%s)"
            all_features_value=[(course_link,i) for i in basic_data["course_feature"]]

            sql_3="insert into ineuron_course.all_what_you_will_learn values (%s,%s)"
            what_u_will_learn_value=[(course_link,i) for i in basic_data["what_u_will_learn"]]

            sql_4="insert into ineuron_course.all_requirenments values (%s,%s)"
            all_requirenments_value=[(course_link,i) for i in basic_data["requirements"]]
        except Exception as e:
            self.logger.custlogger().critical(f"error at qury build with :: {e} ")

        try:
            self.mycursor.execute(sql_1,all_course_value)
            
        except Exception as e:
            self.logger.custlogger().critical(f"error at insert on table all_course with :: {e} ")
            return False
            
        try:
            self.mycursor.executemany(sql_2,all_features_value)

        except Exception as e:
            self.logger.custlogger().critical(f"error at insert on table all_features with :: {e} ")
            return False
        
        try:
            self.mycursor.executemany(sql_3,what_u_will_learn_value)
        except Exception as e:
            self.logger.custlogger().critical(f"error at insert on table all_what_you_will_learn with :: {e} ")
            return False
            
        try:
            self.mycursor.executemany(sql_4,all_requirenments_value)
        except Exception as e:
            self.logger.custlogger().critical(f"error at insert on table all_requirenments with :: {e} ")
            return False
        
        return True
    
    def insertMentorData(self,course_link,mentor_dict):
        '''
        desc : This method shall be used to insert the instroctor data into the table all_instructors
        return : boolean (True or False)
        Written By: Saif Ali
        Version: 1
        Revision: None
        '''
        try:
            sql_1="insert into ineuron_course.all_instructors values (%s,%s,%s)"
            for key, values in mentor_dict.items():
                key=key.strip()
                if not len(values):
                    mentor_value=(course_link,key,'NULL')
                    
                else:
                    values=values.strip()
                    mentor_value=(course_link,key,values)
                    
                self.mycursor.execute(sql_1,mentor_value)
        except Exception as e:
            self.logger.custlogger().critical(f"error at insert with :: {e} ")
            return False
            
        
        return True
    
    
    def insertCurrData(self,course_link,dictionary):
        '''
        desc : This method shall be used to insert the curriculum data into the table all_curriculum
        return : boolean (True or False)
        Written By: Saif Ali
        Version: 1
        Revision: None
        '''
        try:
            sql_1="insert into ineuron_course.all_curriculum values (%s,%s,%s)"
            
            course_link_lst=[course_link]
            for key, values in dictionary.items():
                key=key.strip()
                if not len(values):
                    curr_value=(course_link_lst[0],key,'NULL')
                else:
                    curr_value=[(course_link_lst[0],key,i.strip()) for i in values]
                    
                self.mycursor.executemany(sql_1,curr_value)
        except Exception as e:
            try:
                for key, values in dictionary.items():
                    key=key.strip()
                    if not len(values):
                        self.mycursor.execute(f"""insert into ineuron_course.all_curriculum values ("{course_link}","{key}","null")""")
                        
                    else:
                        key_temp=key
                        for i in values:
                            i=i.strip()
                            
                            i_temp=i
                            self.mycursor.execute(f"""insert into ineuron_course.all_curriculum values ("{course_link}","{key}","{i}")""")
                            del i_temp
                        del key_temp
                        

            except Exception as e1:
                self.logger.custlogger().critical(f' insert failed for curriculum with error :: {e1}')
                self.logger.custlogger().critical(f"""insert into ineuron_course.all_curriculum values ("{course_link}","{key_temp}","{i_temp}")""")
                
                return False
        return True
    

    def insertProjectData(self,course_link,dictionary):

        '''
        desc : This method shall be used to insert the project data into the table all_projects
        return : boolean (True or False)
        Written By: Saif Ali
        Version: 1
        Revision: None
        '''
        
        if dictionary==False:
            return True
        else:
            try:
                course_link=[course_link]
                sql_1="insert into ineuron_course.all_projects values (%s,%s,%s)"
                for key, values in dictionary.items():
                    key=key.strip()
                    if not len(values):
                        project_values=(course_link[0],key,'NULL')    
                    else:
                        project_values=[(course_link[0],key,i.strip()) for i in values]

                    self.mycursor.executemany(sql_1,project_values)
            except Exception as e:
                self.logger.custlogger().info(f"error at insert with :: {e} ")
                return False
            
            return True
    def masterInsertSql(self,course_link,course_data_dict,project_track,curr_track):
        
        '''
        desc : This method will call all the other methods of the class to insert the required data, this method will pass the correct data to them 
                and will commit once all insert completed successfully
        Written By: Saif Ali
        Version: 1
        Revision: None
        '''
        

        try:
            
            commit_1=self.insertBasicData(course_link,course_data_dict)

            commit_2=self.insertMentorData(course_link,course_data_dict["instructor_details"])

            if curr_track:
                commit_3=self.insertCurrData(course_link,course_data_dict["curriculum_details"])
            else:
                commit_3=True  # becuase if there is no project inn the source still we want to insert the shole data in mysql

            if project_track:
                commit_4=self.insertProjectData(course_link,course_data_dict["project_details"])
            else:
                commit_4=True # becuase if there is no project inn the source still we want to insert the shole data in mysql
            
            if commit_1==commit_2==commit_3==commit_4==True:
                self.mydb.commit()
            else:
                self.mydb.commit()
                #self.mydb.rollback()
                self.logger.custlogger().critical(f"rollback is triggered, please check logs for the mysql errors")
            
        except Exception as e:
            self.logger.custlogger().critical(f"error in master sql method with :: {e} ")




    
            
    
    
    
        
