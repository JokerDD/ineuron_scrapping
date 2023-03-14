import inspect
import logging
import boto3
#from logging.handlers import RotatingFileHandler

class S3Handler(logging.Handler):

    def __init__(self, bucket_name, folder_path, file_name):
        super().__init__()
        self.bucket_name = bucket_name
        self.folder_path = folder_path
        self.log_file_name = file_name
        self.s3 = boto3.client(service_name='s3')
                    #region_name='eu-north-1',
                    #aws_access_key_id='AKIAS7QUN5WYHQHFP7OR',
                    #aws_secret_access_key='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')

    def emit(self, record):
        existing_data = ''
        key_name = self.folder_path + '/' + self.log_file_name + '.log'
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=key_name)
            existing_data = response['Body'].read().decode('utf-8')
        except self.s3.exceptions.NoSuchKey:
            pass
        except Exception as e:
            print(f'error in file read with :: {e}')
        try:
            new_data = self.format(record)
            data = existing_data + "\n" + new_data
        except Exception as e:
            print(f'error while appending in text variable with :: {e}')
        
        try:
            
            self.s3.put_object(Body=data, Bucket=self.bucket_name, Key=key_name)
            #self.s3.Object(self.bucket_name, key_name).put(Body=self.format(record))
        except Exception as e:
            print(f'log file save failed with error :: {e}')



class custLogger:

    def __init__(self,logLevel=logging.INFO):
        self.logLevel = logLevel
        self.s3_handler=S3Handler(bucket_name='saifineuronproject',folder_path='log_files',file_name="ineuron_scrapper")

    def custlogger(self,logger_name=False):
        logger_name = f'{inspect.stack()[1][1].split(f"{chr(92)}")[-1]} | {inspect.stack()[1][3]} | lineno-{inspect.stack()[1][2]}'
        
        logger = logging.getLogger(str(logger_name))

        logger.setLevel(self.logLevel)
        
        formatter= logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.s3_handler.setFormatter(formatter)
        logger.addHandler(self.s3_handler)
        
        return logger