import sys
sys.path.append("C:\\Users\\saifa\\OneDrive\\Desktop\\ineuron projects\\my_own_ineuron_proj")

#C:\Users\saifa\OneDrive\Desktop\ineuron projects\my_own_ineuron_proj

from custom_logging.customLogger import custLogger

class testing:

    def __init__(self):
        self.logger = custLogger("DEBUG")
    def raise_exception(self):

        self.logger.custlogger().info(f"new testing of logger")
            


if __name__ == "__main__":
    testobj=testing()
    testobj.raise_exception()

