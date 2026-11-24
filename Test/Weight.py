    





weight = float(input("Enter your weight: "))
units = input("Enter the unit kilogram (K) or pounds (L): ")

if units.lower() == 'k':
    weight = weight * 2.20462
    units = "LBS"
    print(f"Your weight in pounds is {weight:.2f} {units}")

elif units.lower() == 'l':
    weight = weight / 2.20462
    units = "KG"
    print(f"Your weight in kilograms is {weight:.2f} {units}")

else:
    print("Enter correct values")
