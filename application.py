from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS, cross_origin
from mongoDb.mongodb import mongodbOperations
from custom_logging.customLogger import custLogger
import scrappermaster as sm


dbOps = mongodbOperations(username='saif_1', password='saif_1')
sm_obj= sm.autoScrapper()
logging=custLogger("INFO")


application = Flask(__name__)
app = application

@app.route("/", methods = ['GET'])
def homepage():
    logging.custlogger().info("web app start###############################################")
    logging.custlogger().info("home_page hit by machine:{}".format(request.remote_addr))
    return render_template("index.html")

@app.route("/course_list", methods = ['GET'])
#@cross_origin()
def datafetch():
    try:
        if dbOps.getDocCount(dbName="i_nearon_scrapping",collectionName="coll_data") > 0:
            primary_collection_name=dbOps.getCollectionName_latest(dbName="i_nearon_scrapping")
            if dbOps.isCollectionPresent(dbName='i_nearon_scrapping',collectionName=primary_collection_name):
                print('collection is present')
                all_course_data=dbOps.getData(dbName='i_nearon_scrapping',collectionName=primary_collection_name)
                print('collection is present and data fetched')
                return render_template("result.html", results=all_course_data)
            else:
                print('no data present')
                return "no data present in MongoDb, please run the scrapping application first, contact dev for more info"
    
    except Exception as e:
        logging.custlogger().error(f"somthing went wrong with error :: {e}")
        return "something went wrong, you know whom to contact :P"

@app.route("/appstart",methods = ['GET','POST'])

def app_start():
    if request.method== 'POST':
        try:
            serachstring= request.form['course_count'].replace(" ","")
            sm_obj.appstart(course_count=int(serachstring))
            return redirect(url_for('datafetch'))
        except ValueError:
            return "Please enter numric values only"
        except Exception as e:
            logging.custlogger().error(f"error at app start with :: {e}")
            return "soemthing went wrong here, check with developer"
    else:
        return "not a POST method"

if __name__=="__main__":
    app.run()