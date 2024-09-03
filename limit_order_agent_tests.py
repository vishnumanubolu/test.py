import unittest
from unittest.mock import MagicMock
from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient
class TestLimitOrderAgent(unittest.TestCase):

    def setUp(self):
        # Create a mock ExecutionClient with the correct spec
        self.execution_client = MagicMock(spec=ExecutionClient)
        self.agent = LimitOrderAgent(self.execution_client)

    def test_buy_order_execution(self):
        # Add a buy order for IBM
        self.agent.add_order('buy', 'IBM', 1000, 100)

        # Trigger a price tick below the limit
        self.agent.on_price_tick('IBM', 99)

        # Verify that the order was executed
        self.execution_client.execute_order.assert_called_once_with(
            side='buy',
            product_id='IBM',
            amount=1000,
            price=99
        )

    def test_sell_order_execution(self):
        # Add a sell order for IBM
        self.agent.add_order('sell', 'IBM', 1000, 100)

        # Trigger a price tick above the limit
        self.agent.on_price_tick('IBM', 101)

        # Verify that the order was executed
        self.execution_client.execute_order.assert_called_once_with(
            side='sell',
            product_id='IBM',
            amount=1000,
            price=101
        )

if __name__ == '__main__':
    unittest.main()
