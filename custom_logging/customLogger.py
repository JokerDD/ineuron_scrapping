import inspect
import logging


class custLogger:

    def __init__(self,logLevel=logging.INFO):
        self.logLevel = logLevel

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
        fh=logging.FileHandler("C:\\Users\\saifa\\OneDrive\\Desktop\\ineuron projects\\my_own_ineuron_proj\\custom_logging\\ineuron_scrapper.log")
        formatter= logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger