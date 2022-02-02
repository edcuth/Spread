import pytest

@pytest.fixture
def instruments():
    instruments = {
        'TRI.ROS/JUL22': {
            'type': 'Md', 
            'timestamp': 1643656468309, 
            'instrumentId': {
                'marketId': 'ROFX', 
                'symbol': 'TRI.ROS/JUL22'
            }, 
            'marketData': {
                'BI': [
                    {'price': 250.0, 
                    'size': 2}
                ], 
                'OF': [
                    {'price': 250.1, 
                    'size': 6}
                ]
            }
        },
        'TRI.MIN/JUL22': {
            'type': 'Md', 
            'timestamp': 1643656586728, 
            'instrumentId': {
                'marketId': 'ROFX', 
                'symbol': 'TRI.MIN/JUL22'
            }, 
            'marketData': {
                'BI': [
                    {'price': 250.5, 
                    'size': 10}
                    ], 
                'OF': [
                    {'price': 251.0, 
                    'size': 10}
                ]
            }
        }
    }
    yield instruments

@pytest.fixture
def message():
    yield {
        'type': 'Md', 
        'timestamp': 1643656677011, 
        'instrumentId': {
            'marketId': 'ROFX', 
            'symbol': 'TRI.ROS/JUL22'
        }, 
        'marketData': {
            'BI': [
                {'price': 250.0, 
                'size': 2
                }
            ], 
            'OF': [
                {'price': 250.3, 
                'size': 6
                }
            ]
        }
    }
    
@pytest.fixture
def decoded_json():
    yield {
        'type': 'Md', 
        'timestamp': 1643656677011, 
        'instrumentId': {
            'marketId': 'ROFX', 
            'symbol': 'TRI.ROS/JUL22'
        }, 
        'marketData': {
            'BI': [
                {'price': 250.0, 
                'size': 3
                }
            ], 
            'OF': [
                {'price': 250.1, 
                'size': 4}
            ]
        }
    }


@pytest.fixture
def empty_message():
    yield {'type': 'Md', 'timestamp': 1643656677011, 'instrumentId': {'marketId': 'ROFX', 'symbol': 'TRI.ROS/JUL22'}, 'marketData': {'BI': [], 'OF': None}}

@pytest.fixture
def empty_decoded_json():
    yield {
        'type': 'Md', 
        'timestamp': 1643656677011, 
        'instrumentId': {
            'marketId': 'ROFX', 
            'symbol': 'TRI.ROS/JUL22'
        }, 
        'marketData': {
            'BI': [
                {'price': 0, 
                'size': 0
                }
            ], 
            'OF': [
                {'price': 0, 
                'size': 0}
            ]
        }
    }

@pytest.fixture
def values():
    yield {
        "buy_instrument": "TRI.ROS/JUL22",
        "buy_size": 1,
        "buy_price": 250.3,
        "sell_instrument": "TRI.MIN/JUL22",
        "sell_size": 10,
        "sell_price": 250.5
    }