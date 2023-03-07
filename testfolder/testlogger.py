import sys
sys.path.append("C:\\Users\\saifa\\OneDrive\\Desktop\\ineuron projects\\my_own_ineuron_proj")

#C:\Users\saifa\OneDrive\Desktop\ineuron projects\my_own_ineuron_proj

from custom_logging.customLogger import custLogger

class testing:

    def __init__(self):
        self.logger = custLogger("DEBUG")
        self.test_list=['saif','sharique','shadan','shakil','shama']
    def raise_exception(self):
        logger_instance = self.logger.custlogger()
        logger_instance.info(f"###################################")
        for i in self.test_list:
            
            logger_instance.info(f"testing multiple value {i}")
            print(i)
        for i in self.test_list:
            
            logger_instance.info(f"testing multiple second value {i}")
            print(i)
            


if __name__ == "__main__":
    testobj=testing()
    testobj.raise_exception()

