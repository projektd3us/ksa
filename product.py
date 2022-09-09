class Product:
    def __init__(self):
        self.name = ''
        self.priceToday = 0
        self.priceFull = 0
        self.stock = ''
        self.categories = []

    def __str__(self):
        return f"\n" \
               f"Name: {self.name} \n" \
               f"Price: {self.priceToday} \n" \
               f"OldPrice: {self.priceFull} \n" \
               f"Stock: {self.stock}"
