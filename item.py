class Item:
	def __init__(self, name, price, taxable, involved_people):
		self.name = name
		self.price = price
		self.taxable = taxable
		self.involved_people = involved_people

	def __str__(self):
		return f"{self.name:<15}{float(self.price):>4.2f}{self.taxable:^3}{self.involved_people}"

		
