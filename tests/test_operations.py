import pytest
import operations


class TestOperations:

    @pytest.mark.parametrize("buy, sell, cost, expected",
    [
        (100, 150, 10, 40),
        (200, 100, 100, 0),
        (120, 200, 30, 50),
        (150, 200, 50, 0),
        (10, 200, 0, 190)
    ])
    def test_compare_points(self, buy, sell, cost, expected):
        assert operations.compare_points(buy, sell, cost) == expected

    @pytest.mark.parametrize("mini, standard, expected",
    [
        (23, 1, 10),
        (15, 4, 10),
        (25, 3, 20),
        (8, 0, 0),
        (5, 1, 0),
        (58, 6, 50)
    ])
    def test_mini_to_obtains(self, mini, standard, expected):
        assert operations.contracts_mini_to_obtain(mini, standard) == expected

    @pytest.mark.parametrize("mini, standard, expected",
    [
        (23, 1, 1),
        (15, 4, 1),
        (25, 3, 2),
        (8, 0, 0),
        (5, 1, 0),
        (58, 6, 5)
    ])
    def test_standard_to_obtain(self, mini, standard, expected):
        assert operations.contracts_standard_to_obtain(standard, mini) == expected

    @pytest.mark.parametrize("instrument, expected",
    [
        ('SOJ.ROS/MAY22', 'SOJ.MIN/MAY22'),
        ('MAI.ROS/ABR22', 'MAI.MIN/ABR22'),
        ('TRI.ROS/JUL22', 'TRI.MIN/JUL22'),
        ('SOJ.MIN/MAY22', 'SOJ.ROS/MAY22'),
        ('TRI.MIN/JUL22', 'TRI.ROS/JUL22'),
        ('MAI.MIN/ABR22', 'MAI.ROS/ABR22')
    ])
    def test_find_opposite_contract(self, instrument, expected):
        assert operations.find_opposite_contract(instrument) == expected


    def test_update_prices(self, message, instruments, decoded_json, values):
        result = operations.update_prices(message, instruments)
        # assert instruments[decoded_json["instrumentId"]['symbol']] == decoded_json
        assert result == values