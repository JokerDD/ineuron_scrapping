import mysql.connector 

class mysqlOpeartions:

    def __init__(self, username, password, host):
        self.username =username
        self.password =password
        self.host =host
        self.mydb=self.myDb()
        self.mycursor = self.createCursor()

    def myDb(self):
        mydb = mysql.connector.connect(
        host=self.host,
        user=self.username,
        password=self.password)

        return mydb


    def createCursor(self):
        
        try:
            mycursor = self.mydb.cursor()
        except Exception as e:
            mycursor=False
        return mycursor
    
    def createTables(self,schema_name):
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
            raise e
            
        try:
            self.mycursor.execute(f"""
            create table {schema_name}.all_features (
            course_link varchar(1000),
            course_feature varchar(1000)
            );
            """)
        except Exception as e:
            raise e
        
        try:
            self.mycursor.execute(f"""
            create table {schema_name}.all_what_you_will_learn(
            course_link varchar(1000),
            learning_topics varchar(1000)
            );
            """)
        except Exception as e:
            raise e
        
        try:
            self.mycursor.execute(f"""
            create table {schema_name}.all_requirenments(
            course_link varchar(1000),
            course_require varchar(1000)
            );
            """)
        except Exception as e:
            raise e
        
        try:
            self.mycursor.execute(f"""
            create table {schema_name}.all_curriculum(
            course_link varchar(1000),
            course_curriculum varchar(1000),
            course_details varchar(1000)
            );
            """)
        except Exception as e:
            raise e
        
        try:
            self.mycursor.execute(f"""
            create table {schema_name}.all_projects(
            course_link varchar(1000),
            project_name varchar(1000),
            project_details varchar(1000)
            );
            """)
        except Exception as e:
            raise e
        
        try:
            self.mycursor.execute(f"""
            create table {schema_name}.all_instructors(
            course_link varchar(1000),
            instructor_name varchar(1000),
            instructor_details varchar(1000)
            );
            """)
            
        except Exception as e:
            raise e
        
        return True
    
    def insertBasicData(self,course_link,basic_data):

        try:
            self.mycursor.execute(f""" 
            insert into ineuron_course.all_course values ("{course_link}","{basic_data[0]}","{basic_data[1]}","{basic_data[2]}","{basic_data[3]}")
            """)
            
        except Exception as e:
            return False
            
        
        try:
            for i in basic_data[4]:
                self.mycursor.execute(f""" 
                insert into ineuron_course.all_features values ("{course_link}","{i}");
                """)

        except Exception as e:
            return False
            
        
        try:
            for i in basic_data[5]:
                self.mycursor.execute(f""" 
                insert into ineuron_course.all_what_you_will_learn values ("{course_link}","{i}");
                """)
        except Exception as e:
            return False
            
        
        try:
            for i in basic_data[6]:
                self.mycursor.execute(f""" 
                insert into ineuron_course.all_requirenments values ("{course_link}","{i}");
                """)
        except Exception as e:
            return False
        
        return True
    
    def insertMentorData(self,course_link,mentor_dict):
    
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
    def masterInsertSql(self,course_link,basic_data,all_curriculum_dict,all_project_dict):
    
        try:
            
                       
            commit_1=self.insertBasicData(course_link,basic_data)

            commit_2=self.insertMentorData(course_link,basic_data[7])

            commit_3=self.insertCurrData(course_link,all_curriculum_dict)

            commit_4=self.insertProjectData(course_link,all_project_dict)
            
            if commit_1==commit_2==commit_3==commit_4==True:
                self.mydb.commit()
            else:
                self.mydb.rollback()
            
        except Exception as e:
            
            raise e




    
            
    
    
    
        
