from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """
        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.orders = []

    def add_order(self, side: str, product_id: str, amount: int, limit_price: float):
        """
        Adds an order to the agent's order book.

        :param side: 'buy' or 'sell'
        :param product_id: ID of the product to trade
        :param amount: Number of shares to buy or sell
        :param limit_price: The price at which to buy or sell
        """
        self.orders.append({
            'side': side,
            'product_id': product_id,
            'amount': amount,
            'limit_price': limit_price
        })

    def on_price_tick(self, product_id: str, price: float):
        """
        Called whenever there is a price update.

        :param product_id: The product ID for the price tick
        :param price: The latest price of the product
        """
        # Iterate through the list of orders to check if any can be executed
        for order in self.orders[:]:
            if order['product_id'] == product_id:
                if (order['side'] == 'buy' and price <= order['limit_price']) or \
                        (order['side'] == 'sell' and price >= order['limit_price']):
                    # Execute the order
                    self.execution_client.execute_order(
                        side=order['side'],
                        product_id=product_id,
                        amount=order['amount'],
                        price=price
                    )
                    # Remove the executed order from the list
                    self.orders.remove(order)
