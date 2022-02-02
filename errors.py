class ProcessOrderError(Exception):
    # raised when there's a problem processing an order
    def __init__(self, order, message="Error processing order"):
        self.status = order["order"]["status"]
        self.text = order["order"]["text"]
        self.message = message
        super().__init__(self.message)
        
    def __str__(self):
        return f"{self.message}:\n Status: {self.status}\nText: {self.text}"

class FindInstrumentError(Exception):
    # raised when an instrument can't be found
    def __init__(self, instrument, message="Error finding instrument"):
        self.instrument = instrument
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.instrument}"

class WrongOrderTypeInstruction(Exception):
    # raised when the order isn't "sell" or "buy", this shouldn't be a problem
    # since the values are hard coded but who knows
    def __init__(self, instruction_type, message="Unrecognized instruction type"):
        self.instruction_type = instruction_type
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.instruction_type}"

class CancelOrderError(Exception):
    # raised when there's a problem cancelling an order
    def __init__(self, order_id, message="Error cancelling an order"):
        self.order_id = order_id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} with ID: {self.order_id}"