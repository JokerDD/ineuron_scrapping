from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs
import sys
sys.path.append("C:\\Users\\saifa\\OneDrive\\Desktop\\ineuron projects\\my_own_ineuron_proj")
from custom_logging.customLogger import custLogger


class scrappingOperations:
    '''
    desc : This class shall be used to scrap the ineuron courses page
    return : list of all the courses
    Written By: Saif Ali
    Version: 1
    Revision: None
    '''

    def __init__(self, chrome_options):
    
        self.chrome_options=chrome_options
        self.logger=custLogger()
        

    def getAllCourseLink(self, source_link, load_time):
        '''
        desc : This method shall get all the course link in the ineuron
        return : list of all the courses
        Written By: Saif Ali
        Version: 1
        Revision: None
        '''

        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
            driver.get(source_link)

            # scroll down to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # wait for the page to load
            time.sleep(load_time)

            html_source = driver.page_source
            course_source=bs(html_source, "html.parser")
            master_box=course_source.findAll("div", {"class": "Course_course-card__f7WLr Course_card__rBLhD card"})
            master_box[0].div.findAll("div", {"class":"Course_right-area__JqFFV"})[0].a["href"]
            course_link="https://ineuron.ai"
            course_link + master_box[0].div.findAll("div", {"class":"Course_right-area__JqFFV"})[0].a["href"]
            distinct_course_links=set()
            distinct_course_links.clear()

            for master_box_loop in master_box:
                distinct_course_links.add(course_link+master_box_loop.div.findAll("div", {"class":"Course_right-area__JqFFV"})[0].a["href"])

            distinct_course_links_list=list(distinct_course_links)

            return distinct_course_links_list
        except Exception as e:
            self.logger.custlogger().error(f"error at getting course link with :: {e} ")
        
    def get_course_code(self,course_links):
    
        '''
        desc : This method shall get the source code of any courses in ineuron, this will be running inside the loop of course link
        return : bs object containing source code
        Written By: Saif Ali
        Version: 1
        Revision: None
        '''
        
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        driver.get(course_links)

        #CurriculumAndProjects_view-more-btn__iZ72A
        #CurriculumAndProjects_view-more-btn__iZ72A
        #fas fa-times

        time.sleep(2)
        
        try:
            view_more_1 = driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > section:nth-child(7) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > span:nth-child(3)")
            view_more_1.click()
        except Exception as e:
            self.logger.custlogger().debug(f"error at expanding curr with :: {e} ")
            
        time.sleep(1)
        
        try:
            
            view_more_2 = driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > section:nth-child(7) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > span:nth-child(3)")
            view_more_2.click()
        except Exception as e: 
            self.logger.custlogger().debug(f"error at expanding project with :: {e} ")
        #actions = ActionChains(driver)
        #time.sleep(5)
        #actions.move_to_element(view_more).click().perform()
        topics_source = driver.page_source        
        bs_topic_wise_source = bs(topics_source, "html.parser")
                
        return bs_topic_wise_source
    
    def encode_decode(self,text_data):
        '''
        desc : This method shall convert all the literals into it's ascii and ignore those which doesn't match it then encode it (this may loose some data)
        return : str
        Written By: Saif Ali
        Version: 1
        Revision: None
        '''         
        text_data=text_data.encode('ascii','ignore')
        text_data=text_data.decode()
        return text_data

    
    def basic_course_data(self,course_source_code_bs):
        
        '''
        desc : This method shall get all the basic data of the ccourse
        return : dict
        Written By: Saif Ali
        Version: 1
        Revision: None
        ''' 

        try:
            Topic=course_source_code_bs.findAll("div", {"class": "Hero_course-category-breadcrumb__9wzAH"})[0].findAll("a")[0].text
            Topic=self.encode_decode(Topic)
        except Exception as e:
            #logging.info(f'error at topic {e}')
            self.logger.custlogger().info(f"error at fetching Topic name code with :: {e} ")
            Topic='Null'
        
        try:
            Subtopic=course_source_code_bs.findAll("div", {"class": "Hero_course-category-breadcrumb__9wzAH"})[0].findAll("a")[1].text
            Subtopic=self.encode_decode(Subtopic)
        except Exception as e:
            #logging.info(f'error at subtop : {e}')
            self.logger.custlogger().info(f"error at fetching subtopic name code with :: {e} ")
            Subtopic='Null'
        
        try:
            Course_Name=course_source_code_bs.findAll("h3", {"class": "Hero_course-title__4JX81"})[0].text
            Course_Name=self.encode_decode(Course_Name)
        except Exception as e:
            #logging.info(f'error at subtop : {e}')
            self.logger.custlogger().info(f"error at fetching Course_Name name code with :: {e} ")
            Course_Name='Null'

        try:
            Course_Description=course_source_code_bs.findAll("div", {"class": "Hero_course-desc__lcACM"})[0].text
            Course_Description=self.encode_decode(Course_Description)
        except Exception as e:
            #logging.info(f'error at Course_Description : {e}')
            self.logger.custlogger().info(f"error at fetching Course_Description name code with :: {e} ")
            Course_Description='Null'
        
        try:
            course_feeaturs=course_source_code_bs.findAll("div", {"class": "CoursePrice_course-features__IBpSY"})[0].findAll("li")
            course_feeaturs=[self.encode_decode(feature.text) for feature in course_feeaturs]
        except Exception as e:
            #logging.info(f'error at course_feeaturs : {e}')
            self.logger.custlogger().info(f"error at fetching course_feeaturs name code with :: {e} ")
            course_feeaturs='Null'
        
        try:
            what_u_will_learn=course_source_code_bs.findAll("div", {"class": "CourseLearning_card__0SWov card"})[0].findAll("li")
            what_u_will_learn=[self.encode_decode(topics.text) for topics in what_u_will_learn]
        except Exception as e:
            #logging.info(f'error at what_u_will_learn : {e}')
            self.logger.custlogger().info(f"error at fetching what_u_will_learn data code with :: {e} ")
            what_u_will_learn='Null'

        try:
            requirements=course_source_code_bs.findAll("div", {"class": "CourseRequirement_card__lKmHf requirements card"})[0].findAll("li")
            requirements=[self.encode_decode(require.text) for require in requirements]
        except Exception as e:
            self.logger.custlogger().info(f"error at fetching requirements data code with :: {e} ")
            requirements='Null'
            #raise e

        try:
            instruct_source=course_source_code_bs.findAll("div",{"class":"InstructorDetails_left__nVSdv"})
            instructor_dict={}
            for instruct_loop in instruct_source:
                key=self.encode_decode(instruct_loop.h5.text)
                value=instruct_loop.p.text
                value=self.encode_decode(value)
                instructor_dict[key]=value
        except Exception as e:
            self.logger.custlogger().info(f"error at fetching instructor_dict data code with :: {e} ")
            instructor_dict='Null'
            #raise e
        
        basic_data_dict={
        "topic" : Topic,
        "sub_topic" : Subtopic,
        "course_name" : Course_Name,
        "course_description" : Course_Description,
        "course_feature" : course_feeaturs,
        "what_u_will_learn" : what_u_will_learn,
        "requirements" : requirements,
        "instructor_details" : instructor_dict
        }

        #basic_data_list=[Topic,Subtopic,Course_Name,Course_Description,course_feeaturs,what_u_will_learn,requirements,instructor_dict]
        #make above dictionary
        
        return basic_data_dict
    
    def curr_and_proj(self,course_source_code_bs):
        '''
        desc : This method shall filter all the code to project and curricullum
        return : bs object source code of curr and project
        Written By: Saif Ali
        Version: 1
        Revision: None
        ''' 
        curr_and_proj_code=course_source_code_bs.findAll("div", {"class":"CurriculumAndProjects_course-curriculum__C9K5U CurriculumAndProjects_card__rF6YN card"})

        return curr_and_proj_code
    
    def curr_data(self,curr_and_proj_code):

        '''
        desc : This method shall save all the curriculam details in a dict called all_curriculum_dict
        return : dict
        Written By: Saif Ali
        Version: 1
        Revision: None
        ''' 
        try:
            curr_all=curr_and_proj_code[0].div.findAll("div", {"class":"CurriculumAndProjects_curriculum-accordion__fI8wj CurriculumAndProjects_card__rF6YN card"})
            all_curriculum_dict={}
            count_1=0

            for i in curr_all:
                course_desc_loop=i.findAll("div",{"class":"CurriculumAndProjects_course-curriculum-list__OBOTg"})
                key=i.div.text
                key=self.encode_decode(key)
                value=[]
                for j in course_desc_loop:
                    text_data=j.text
                    
                    text_data=self.encode_decode(text_data)
                    value.append(text_data)
                    count_1+=1
                all_curriculum_dict[key]=list(value)
        except Exception as e:
            self.logger.custlogger().info(f"error at fetching curr data code with :: {e} ")
            all_curriculum_dict=False
        return all_curriculum_dict

    def project_data(self,curr_and_proj_code):

        '''
        desc : This method shall save all the project details in a dict called all_curriculum_dict (if not present it will return Flase)
        return : dict or boolean
        Written By: Saif Ali
        Version: 1
        Revision: None
        '''

        try:
            project_all=curr_and_proj_code[1].div.findAll("div", {"class":"CurriculumAndProjects_curriculum-accordion__fI8wj CurriculumAndProjects_card__rF6YN card"})
            all_project_dict={}
            count_2=0
            for i in project_all:
                project_desc_loop=i.findAll("div",{"class":"CurriculumAndProjects_course-curriculum-list__OBOTg"})
                key=i.div.text
                key=self.encode_decode(key)
                value=[]
                for j in project_desc_loop:
                    text_data=j.text
                    text_data=self.encode_decode(text_data)
                    value.append(text_data)
                    count_2+=1
                all_project_dict[key]=list(value)
        except Exception as e:
            #logging.error(f"error at project --> {e}")
            self.logger.custlogger().debug(f"error at fetching project data code with :: {e} ")
            all_project_dict = False
        
        return all_project_dict


