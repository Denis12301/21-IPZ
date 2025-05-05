... class Trader:
...     def __init__(self, name, trading_system, repayment_module):
...         self.name = name
...         self.trading_system = trading_system
...         self.repayment_module = repayment_module
... 
...     def request_loan(self, amount, terms):
...         print(f"1. {self.name} → TradingSystem: ЗапитПозики(suma={amount}, umovy='{terms}')")
...         order = self.trading_system.create_debt(amount, terms, self)
...         return order
... 
...     def receive_funds(self, amount):
...         print(f"4. StockExchange → {self.name}: НадатиПозиченіКошти(suma={amount})")
... 
...     def return_loan(self, order):
...         print(f"5. {self.name} → Module: ПовернутиБорг(suma={order.amount}, vidsotky={order.interest})")
...         self.repayment_module.return_loan(order)
... 
... 
... class TradingSystem:
...     def __init__(self, exchange):
...         self.exchange = exchange
... 
...     def create_debt(self, amount, interest, trader):
...         print(f"2. TradingSystem → Order: СтворитиБорг(suma={amount}, vidsotky={interest})")
...         order = Order(amount, interest, trader, self.exchange)
...         return order
... 
... 
... class Order:
    def __init__(self, amount, interest, trader, exchange):
        self.amount = amount
        self.interest = interest
        self.trader = trader
        self.exchange = exchange

    def reserve_funds(self):
        print("3. Order → StockExchange: РезервуватиКошти()")
        self.exchange.reserve_funds(self)

    def update_status(self):
        print("7. StockExchange → Order: ОновитиСтатусБоргу()")


class StockExchange:
    def reserve_funds(self, order):
        # крок 4
        order.trader.receive_funds(order.amount)

    def close_debt(self, order):
        # крок 6
        print("6. Module → StockExchange: ЗакритиБорг()")
        # а тепер крок 7
        order.update_status()


class RepaymentModule:
    def __init__(self, exchange):
        self.exchange = exchange

    def return_loan(self, order):
        # це викликає сам крок 6 (чеки і print)
        self.exchange.close_debt(order)


def main():
    # Створюємо об'єкти
    exchange = StockExchange()
    trading_system = TradingSystem(exchange)
    module = RepaymentModule(exchange)
    trader = Trader("Trader", trading_system, module)

    # Запускаємо сценарій
    order = trader.request_loan(amount=1000, terms="1 year @5%")
    order.reserve_funds()
    trader.return_loan(order)


if __name__ == "__main__":
    main()
