print("Welcome to QueensLand")
age = int(input("what is your age: "))
if age >= 18:
    print("your need to pay RS:1500")
elif age >= 5:
    print("you need to pay RS:700") 
else:
    print("not allowded") 

amount = int(input("pay amount: "))
if amount == 1500 :
    print("you booked adult ticket")
elif amount == 700:
    print("you booked child ticket")    
else:
    print("pay correct amount")    
