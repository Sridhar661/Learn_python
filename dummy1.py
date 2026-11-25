menu = {
    "pizza" : 150.00,
    "popcorn" : 120.00,
    "fish chips" : 450.50,
    "fries" : 100.00,
    "hamburger" : 200.75,
    "chicken nuggets" : 350.50,
    "soda" : 55.00,
    "brewed coffe" : 99.00
}
cart = []
total_price = 0
print('-------------menu----------------')
for key, values in menu.items():
    print(f'{key} : {values:.2f}')
print("---------------------------------")    


while True:
    food = input("enter the food you want to eat(q to quit):  ").lower()
    if (food == 'q' or food == 'Q'):
        break
    elif menu.get(food) is not None:
        cart.append(food)

for item in cart:
    print(cart)


for item in cart:
    total_price = total_price + menu.get(item)
print(f"Your Total Bill is:  {total_price:.2f}")            

