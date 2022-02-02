from cmath import log
import config, errors

# This module has it's own test suit, 
# use the command pytest tests\test_operations.py to test it.

# Initializes an empty dict to save the latest entry of each instrument
map_of_instruments = dict()

def compare_points(buy:float, sell:float, cost:float=config.costs.cost):
    if sell > buy + cost:
        return sell - (buy + cost)
    return 0

def contracts_mini_to_obtain(mini:int, standard:int):
    # this helper function is used to determine how many contracts we can acquire while keeping a neutral position
    # meaning we need to check both contract's availability and pick the min.
    # We can only opperate in multiples of 10 for mini contracts.
    if mini//10 > standard:
        return standard * 10
    return (mini//10)*10

def contracts_standard_to_obtain(standard:int, mini:int):
    # this helper function is used to determine how many contracts we can acquire while keeping a neutral position
    # meaning we need to check both contract's availability and pick the min.
    if mini//10 > standard:
        return standard
    return mini//10

def find_opposite_contract(instrument:str):
    # helper function to find the matching mini and standard contracts for a pair of instruments
    if "ROS" in instrument:
        return instrument.replace("ROS", "MIN")
    elif "MIN" in instrument:
        return instrument.replace("MIN", "ROS")
    else:
        raise errors.FindInstrumentError(instrument)

def stardarize_maps(message:dict):
    # standarizes any received message
    if message["marketData"]["OF"] == [] or message["marketData"]["OF"] == None:
        message["marketData"]["OF"] = [{"price": 0, "size": 0}]
    if message["marketData"]["BI"] == [] or message["marketData"]["BI"] == None:
        message["marketData"]["BI"] = [{"price": 0, "size": 0}]
    return message

def compare_messages(new_map, map_to_update):
    instrument_name = new_map["instrumentId"]["symbol"]
    counter_instrument = find_opposite_contract(instrument_name)
    # Checks if the update is on the OF or the BI side of the instrument and sets variables accordingly
    if new_map["marketData"]["OF"] != map_to_update[instrument_name]["marketData"]["OF"]:
        update_side = "OF"
        counter_side = "BI"
        buy_instrument = new_map
        sell_instrument = map_to_update[counter_instrument]
    elif new_map["marketData"]["BI"] != map_to_update[instrument_name]["marketData"]["BI"]:
        update_side = "BI"
        counter_side = "OF"
        buy_instrument = map_to_update[counter_instrument]
        sell_instrument = new_map
    else:
        # No changes in the instrument
        return None
    price_difference = compare_points(
        buy_instrument["marketData"]["OF"][0]["price"],
        sell_instrument["marketData"]["BI"][0]["price"]
    )
    if "ROS" in buy_instrument["instrumentId"]["symbol"]:
        contracts_to_buy = contracts_standard_to_obtain(
            buy_instrument["marketData"]["OF"][0]["size"], 
            sell_instrument["marketData"]["BI"][0]["size"]
        )
        contracts_to_sell = contracts_to_buy * 10
        tons = contracts_to_sell * 10
    elif "MIN" in buy_instrument["instrumentId"]["symbol"]:
        contracts_to_buy = contracts_mini_to_obtain(
            buy_instrument["marketData"]["OF"][0]["size"], 
            sell_instrument["marketData"]["BI"][0]["size"]
        )
        contracts_to_sell = contracts_to_buy //10
        tons = contracts_to_sell * 100

    return {
        "buy_instrument": buy_instrument["instrumentId"]["symbol"],
        "buy_size": contracts_to_buy,
        "buy_price": buy_instrument["marketData"]["OF"][0]["price"],
        "sell_instrument": sell_instrument["instrumentId"]["symbol"],
        "sell_size": contracts_to_sell,
        "sell_price": sell_instrument["marketData"]["BI"][0]["price"],
        "update_side": update_side,
        "price_difference": price_difference,
        "instrument_name": instrument_name,
        "counter_instrument": counter_instrument,
        "tons": tons
    }



def update_prices(new_map, map_to_update):
    # Standarize the new map to remove any instances of empty lists or None in them
    new_map = stardarize_maps(new_map)
    if new_map["instrumentId"]["symbol"] not in map_to_update.keys():
        # If the instrument is not already registered, it adds it to our register
        map_to_update[new_map["instrumentId"]["symbol"]] = new_map
        print("-new entry registered")

        # If the instrument is already registered, this will compare the new price if needed,
        # and print the difference between the instrument price, the counter element,
        # and how much there's available while maintaining a neutral position
    if find_opposite_contract(new_map["instrumentId"]["symbol"]) not in map_to_update.keys():
        # checks if the counter instrument is in the map of instruments
        print("-Unmatched instrument")
        return None
    else:
        # This helper function will compare the new message to the previous one of the same instrument
        values = compare_messages(new_map, map_to_update)
        if values != None:
            # Print the updated price, the difference with the counter instrument, and the volume available to operate while keeping a neutral position
            print('Update for{}({})\nOld price: {} => New price: {}\nPrice difference with {}: {}\nOld Size: {} => New Size: {}\nQuantity of contracts available to operate:\nBuy {} | Sell {} | Tons {}'.format(
            new_map["instrumentId"]["symbol"], # instrument name
            values["update_side"], # OF or BI
            map_to_update[new_map["instrumentId"]["symbol"]]["marketData"][values["update_side"]][0]["price"], # previous price
            new_map["marketData"][values["update_side"]][0]["price"], # new price
            values["counter_instrument"], # counter instrument ROS=>MIN/MIN=>ROS
            values["price_difference"], # price difference
            map_to_update[new_map["instrumentId"]["symbol"]]["marketData"][values["update_side"]][0]["size"], # previous size
            new_map["marketData"][values["update_side"]][0]["size"], # new size
            values["buy_size"], # Quantity to buy
            values["sell_size"], # Quantity to sell
            values["tons"]
            ))
        else:
            print("-No updated values")
            return None # if the update is only of size, don't do anythin

        # Finally we replace the old map with the new one
        map_to_update[values["instrument_name"]] = new_map
        # if there's an opportunity to obtain a profit while maintaining a neutral position, we return the values to be
        # used to place the orders
        if values["price_difference"] > 0 and values["buy_size"] > 0:
            print("-found profit opportunity")
            return {
                "buy_instrument": values["buy_instrument"],
                "buy_size": values["buy_size"],
                "buy_price": values["buy_price"],
                "sell_instrument": values["sell_instrument"],
                "sell_size": values["sell_size"],
                "sell_price": values["sell_price"]
            }
        else:
            # If there's no profit opportunity, return None
            return None