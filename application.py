from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from mongoDb.mongodb import mongodbOperations
from custom_logging.customLogger import custLogger


dbOps = mongodbOperations(username='saif_1', password='saif_1')
logging=custLogger("INFO")


application = Flask(__name__)
app = application

@app.route("/", methods = ['GET'])
def homepage():
    logging.custlogger().info("home_page hit by machine:{}".format(request.remote_addr))
    return render_template("index.html")

@app.route("/course_list", methods = ['GET'])
#@cross_origin()
def datafetch():
    try:
        if dbOps.isCollectionPresent(dbName='i_nearon_scrapping',collectionName='course_data'):
            print('collection is present')
            all_course_data=dbOps.getData(dbName='i_nearon_scrapping',collectionName='course_data')
            print('collection is present and data fetched')
            return render_template("result.html", results=all_course_data)
        else:
            print('no data present')
            return "no data present in MongoDb, please run the scrapping application first, contact dev for more info"
    
    except Exception as e:
        logging.custlogger().error(f"somthing went wrong with error :: {e}")
        return "something went wrong, you know whom to contact :P"
if __name__=="__main__":
    app.run()