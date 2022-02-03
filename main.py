import pyRofex
import handlers
from config import settings

# Instruments to subscribe
instruments = ['SOJ.ROS/MAY22', 
            'SOJ.MIN/MAY22', 
            'MAI.ROS/ABR22', 
            'MAI.MIN/ABR22', 
            'TRI.ROS/JUL22', 
            'TRI.MIN/JUL22']

if __name__=="__main__":
    # Sets the parameters for the REMARKET environment
    # This uses pydantic to config these values from either a .env file or environment variables
    pyRofex.initialize(user=settings.user,
                    password=settings.password,
                    account=settings.account,
                    environment=pyRofex.Environment.REMARKET)

    handlers.init_websocket_connection()
    handlers.subscribe_market_and_order(instruments)