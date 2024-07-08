#!/usr/bin/python3

from contextlib import redirect_stdout
from item import Item
from member import Member

def show_menu():
	print('\nPlease select one of the following options')
	print('1. Add items')
	print('2. Modify an item')
	print('3. Delete an item')
	print('4. Show receipt')
	print('5. Save receipt to file')
	print('6. Add person')
	print('7. Modify person')
	print('8. Delete person')
	print('9. Exit')

def enter_item():
	name = input('\nItem (x to exit): ')
	if(name == 'x'):
		return Item(name, '', '', [])
	price = input('Price: ')
	taxable = input('Taxable (y/n): ')
	people = input('Involved people: ')
	person_list = [person.casefold().strip() for person in people.split(',')]
	return Item(name, price, taxable, person_list)
	
def list_all(list):
	for index, entry in enumerate(list):
		print(f"{index+1:<3}: {entry}")

def is_valid_index(index, list):
	if index == 'x':
		print('Returning to menu...')
		return False

	if index.isnumeric() is False:
		print('Returning...')
		return False

	index = int(index)
	if(index < 0 or index > len(list)):
		print('Enter a valid index')
		return False
	else:
		return True

def modify_item():
	if len(items) == 0:
		print('Please add an item first')
		return
	list_all(items)
	index = input('Enter the index of the item to modify (x to exit): ')
	if(is_valid_index(index, 'items')):	
		item = items[int(index)-1]
		print(f"Modifying {item.name}...")
		items[int(index)-1] = enter_item()
		print(f"Updated {item.name}")

def delete_item():
	if len(items) == 0:
		print('Please add an item first')
		return
	list_all(items)
	index = input('Enter the index of the item to delete (x to exit): ')
	if(is_valid_index(index, 'items')):
		items.pop(int(index)-1)
	
def get_people():
	unique_people = set()
	for item in items:
		if 'all' not in item.involved_people:
			for person in item.involved_people:
				unique_people.add(person.casefold())
			#unique_people.update(item.involved_people)
	
	for member in members:
		unique_people.add(member.name.casefold())
	
	return unique_people

def get_item_count(person = 'all'):
	count = 0
	if person.casefold() != 'all':
		for item in items:
			if person in item.involved_people:
				count += 1
			if 'all' in item.involved_people:
				count += 1
	else:
		count = len(items)
	return count
		
def get_tax_total(person = 'all'):
	total_tax = 0
	if person.casefold() != 'all':
		for item in items:
			if item.taxable.casefold() == 'y' and (person in item.involved_people or 'all' in item.involved_people):
				total_tax += (hst * float(item.price)) / len(item.involved_people)
	else:
		for item in items:
			if item.taxable.casefold() == 'y':
				total_tax += hst * float(item.price)
	return f"{total_tax:.2f}"

def get_subtotal(person = 'all'):
	subtotal = 0
	if person.casefold() != 'all':
		for item in items:
			if person in item.involved_people:
				subtotal += float(item.price) / len(item.involved_people)
			if 'all' in item.involved_people:
				subtotal += float(item.price) / len(get_people())
	else:
		for item in items:
			subtotal += float(item.price)

	return f"{subtotal:.2f}"

def get_total(person = 'all'):
	total = float(get_tax_total(person)) + float(get_subtotal(person))
	return f"{total:.2f}"

def get_group_totals():
	print(f"Total items: {get_item_count():d}")
	print(f"Subtotal: {get_subtotal()}")
	print(f"HST ({hst*100}%): {get_tax_total()}")
	print(f"Total: {get_total()}")

def get_person_totals(person = 'all'):
	print(f"{person.title()}'s total items: {get_item_count(person)}")
	print(f"{person.title()}'s subtotal: {get_subtotal(person)}")
	print(f"HST ({hst*100}%): {get_tax_total(person)}")
	print(f"{person.title()}'s total: {get_total(person)}")

def build_receipt():
	print(f"{store_name:^24s}")
	print(f"{date:^24s}")
	print()
	print('{item:^15s}{price:^6s}{tax:^3s}{who}'.format(item="Item", price="Price", tax="Tax", who='Who'))
	for item in items:
		print(item)
	print()
	print(get_group_totals())
	print()

	print('Member totals')
	for person in get_people():
		print(get_person_totals(person))
		print()

def save_receipt():
	with open(f"receipts/{date}_{store_name}.txt", "w") as f:
		with redirect_stdout(f):
			build_receipt()

def enter_member():
	name = input('\nName (x to exit): ')
	if(name == 'x'):
		return
	else:
		new_member = Member(name.casefold())
		members.append(new_member)

def modify_member():
	if len(members) == 0:
		print('Please add a member first')
		return
	list_all(members)
	index = input('Enter the index of the person to modify (x to exit): ')
	if(is_valid_index(index, 'members')):	
		member = members[int(index)-1]
		print(f"Modifying {member.name}...")
		items[int(index)-1] = enter_member()
		print(f"Updated {member.name}")

def delete_member():
	if len(members) == 0:
		print('Please add a member first')
		return
	list_all(members)
	index = input('Enter the index of the member to delete (x to exit): ')
	if(is_valid_index(index, 'members')):
		members.pop(int(index)-1)

	
members = []
items = []
hst = 0.13
menu_choice = 1

print('Welcome to BillSplitter!')

store_name = input('Please enter the business name: ')
date = input('Date of bill (YYYY-MM-DD): ')

while (menu_choice != '9'):
	show_menu()
	menu_choice = input('Selection: ')
	
	if(menu_choice == '1'):
		while(1):
			new_item  = enter_item()
			if(new_item.name == 'x'):
				break
			else:
				items.append(new_item)

	if(menu_choice == '2'):	
		modify_item()
		
	if(menu_choice == '3'):
		delete_item()

	if(menu_choice == '4'):
		build_receipt()

	if(menu_choice == '5'):
		save_receipt()

	if(menu_choice == '6'):
		enter_member()
	
	if(menu_choice == '7'):
		modify_member()
	
	if(menu_choice == '8'):
		delete_member()

	if(menu_choice=='9'):
		print('Goodbye!')
