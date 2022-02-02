import pyRofex
import errors
from operations import update_prices, map_of_instruments
from orders import process_transaction

from typing import List

# First we define the handlers that will process the messages and exceptions.
def market_data_handler(message):
    print("Market Data Message Received: {0}".format(message))
    try:
        order_instructions = update_prices(message, map_of_instruments)
        print("-Order Instruction:", order_instructions)
        if order_instructions != None:
            order_details = process_transaction(**order_instructions)
            print(f"----------Orden de compra: {0}----------\n----------Order de venta: {1}----------",
            order_details["buyOrder"], order_details["sellOrder"])
        print("---------------------------------------------------------------------------------------")
    except errors.ProcessOrderError as e:
        print("Error processing order:", e)
def order_report_handler(message):
    print("Order Report Message Received: {0}".format(message))
def error_handler(message):
    print("Error Message Received: {0}".format(message))
def exception_handler(e):
    print("Exception Occurred: {0}".format(e.message))

def init_websocket_connection():
    # Initiate Websocket Connection
    pyRofex.init_websocket_connection(market_data_handler=market_data_handler,
                                  order_report_handler=order_report_handler,
                                  error_handler=error_handler,
                                  exception_handler=exception_handler)


def subscribe_market_and_order(instruments: List[str]):
    # Uses the MarketDataEntry enum to define the entries we want to subscribe to
    entries = [pyRofex.MarketDataEntry.BIDS,
           pyRofex.MarketDataEntry.OFFERS]
           #pyRofex.MarketDataEntry.LAST] I don't think this is neccesary 
    # Subscribes to receive market data messages **
    pyRofex.market_data_subscription(instruments, # Picks up the instruments list from a .env file or environment variables
                                    entries=entries)

    # Subscribes to receive order report messages (default account will be used) **
    pyRofex.order_report_subscription()