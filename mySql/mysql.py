import mysql.connector 

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
            print('table already exists')
            
        try:
            self.mycursor.execute(f"""
            create table {schema_name}.all_features (
            course_link varchar(1000),
            course_feature varchar(1000)
            );
            """)
        except Exception as e:
            print('table already exists')
        
        try:
            self.mycursor.execute(f"""
            create table {schema_name}.all_what_you_will_learn(
            course_link varchar(1000),
            learning_topics varchar(1000)
            );
            """)
        except Exception as e:
            print('table already exists')
        
        try:
            self.mycursor.execute(f"""
            create table {schema_name}.all_requirenments(
            course_link varchar(1000),
            course_require varchar(1000)
            );
            """)
        except Exception as e:
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
            self.mycursor.execute(f""" 
            insert into ineuron_course.all_course values ("{course_link}","{basic_data["topic"]}","{basic_data["subtopic"]}","{basic_data["Course_Name"]}","{basic_data["Course_Description"]}")
            """)
            
        except Exception as e:
            return False
            
        try:
            for i in basic_data["course_feeaturs"]:
                self.mycursor.execute(f""" 
                insert into ineuron_course.all_features values ("{course_link}","{i}");
                """)

        except Exception as e:
            return False
        
        try:
            for i in basic_data["what_u_will_learn"]:
                self.mycursor.execute(f""" 
                insert into ineuron_course.all_what_you_will_learn values ("{course_link}","{i}");
                """)
        except Exception as e:
            return False
            
        try:
            for i in basic_data["requirements"]:
                self.mycursor.execute(f""" 
                insert into ineuron_course.all_requirenments values ("{course_link}","{i}");
                """)
        except Exception as e:
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
            for key, values in mentor_dict.items():
                key=key.strip()
                if not len(values):
                    self.mycursor.execute(f"""insert into ineuron_course.all_instructors values ("{course_link}","{key}",'null')""")
                else:
                    values=values.strip()
                    self.mycursor.execute(f"""insert into ineuron_course.all_instructors values ("{course_link}","{key}","{values}")""")
        except Exception as e:
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
            for key, values in dictionary.items():
                key=key.strip()
                if not len(values):
                    self.mycursor.execute(f"""insert into ineuron_course.all_curriculum values ("{course_link}","{key}","null")""")
                    
                else:
                    for i in values:
                        i=i.strip()
                        self.mycursor.execute(f"""insert into ineuron_course.all_curriculum values ("{course_link}","{key}","{i}")""")
        except Exception as e:
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
                for key, values in dictionary.items():
                    key=key.strip()
                    if not len(values):
                        self.mycursor.execute(f"""insert into ineuron_course.all_projects values ("{course_link}","{key}",'null')""")
                    else:
                        for i in values:
                            i=i.strip()
                            self.mycursor.execute(f"""insert into ineuron_course.all_projects values ("{course_link}","{key}","{i}")""")
            except Exception as e:
                return False
            
            return True
    def masterInsertSql(self,course_link,course_data_dict,project_track):
        
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

            commit_3=self.insertCurrData(course_link,course_data_dict["curriculum_details"])

            if project_track:
                commit_4=self.insertProjectData(course_link,course_data_dict["project_details"])
            else:
                commit_4=True
            
            if commit_1==commit_2==commit_3==commit_4==True:
                self.mydb.commit()
            else:
                self.mydb.rollback()
            
        except Exception as e:
            
            raise e




    
            
    
    
    
        
