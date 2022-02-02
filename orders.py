import errors
import pyRofex

def process_order(instrument:str, side:str, size:int, price:float):
    if side=="buy":
        pyRofex_side = pyRofex.Side.BUY
    elif side == "sell":
        pyRofex_side = pyRofex.Side.SELL
    else:
        raise errors.WrongOrderTypeInstruction(side)
    order = pyRofex.send_order(ticker=instrument,
                                side=pyRofex_side,
                                size=size,
                                price=price,
                                order_type=pyRofex.OrderType.LIMIT)
    # todo: check which camp we need to use to check the order was procesed properly
    return pyRofex.get_order_status(order["order"]["clientId"])

def cancel_order(order:str):
    # this will be called to cancel a potential purchase order if
    # the selling order produces an error, keeping the neutral position
    cancellation = pyRofex.cancel_order(order)
    if cancellation["order"]["status"] != "CANCELLED":
        raise errors.CancelOrderError(order)
    else:
        print(f"Order {order} successfully cancelled")

def process_transaction(buy_instrument:str, buy_size:int, buy_price:float, 
                        sell_instrument:str, sell_size:int, sell_price:float):
    buy_order = process_order(buy_instrument, "buy", buy_size, buy_price)
    if buy_order["order"]["status"] not in ["PENDING_NEW", "FILLED"]:
        raise errors.ProcessOrderError(buy_order)
    sell_order = process_order(sell_instrument, "sell", sell_size, sell_price)
    if sell_order["order"]["status"] not in ["PENDING_NEW", "FILLED"]:
        try:
            print("Trying to cancel order: " + buy_order)
            cancel_order(buy_order)
        except errors.CancelOrderError as e:
            print(e)
        raise errors.ProcessOrderError(sell_order)
    return {"buyOrder": buy_order, "sellOrder": sell_order}