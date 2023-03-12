import inspect
import logging
import boto3
from logging.handlers import RotatingFileHandler

class S3Handler(logging.Handler):
    def __init__(self, bucket_name, folder_path):
        super().__init__()
        self.bucket_name = bucket_name
        self.folder_path = folder_path
        self.s3 = boto3.client('s3')

    def emit(self, record):
        try:
            key_name = self.folder_path + '/' + self.format(record) + '.log'
            self.s3.put_object(Body=self.format(record), Bucket=self.bucket_name, Key=key_name)
        except Exception as e:
            print('log file save failed')

class custLogger:

    def __init__(self,logLevel=logging.INFO):
        self.logLevel = logLevel
        self.s3_handler=S3Handler(bucket_name='saifineuronproject',folder_path='log_files')

    def custlogger(self,logger_name=False):
        
        #logger_name = inspect.stack()[1][3]
        #logger = logging.getLogger(logger_name)
        #inspect.stack()[1][1].split("/")[-1].split(".")[0]
        
        if logger_name:
            pass
        else:
            logger_name = f'{inspect.stack()[1][1].split(f"{chr(92)}")[-1]} | {inspect.stack()[1][3]} | lineno-{inspect.stack()[1][2]}'
        
        logger = logging.getLogger(str(logger_name))

        logger.setLevel(self.logLevel)
        #fh=RotatingFileHandler("C:\\Users\\saifa\\OneDrive\\Desktop\\ineuron projects\\my_own_ineuron_proj\\custom_logging\\ineuron_scrapper.log",maxBytes=10000,backupCount=5)
        #fh=logging.FileHandler("C:\\Users\\saifa\\OneDrive\\Desktop\\ineuron projects\\my_own_ineuron_proj\\custom_logging\\ineuron_scrapper.log")
        formatter= logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.s3_handler.setFormatter(formatter)
        logger.addHandler(self.s3_handler)
        return logger