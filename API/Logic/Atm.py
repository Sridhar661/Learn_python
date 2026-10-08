Atm_card = input(str("insert card:  "))

if Atm_card == "card":
    print ("Card Verified")

    Atm_Pin = int(input(("Enter your PIN:  ")))
    pin = 1234 
    if Atm_Pin == pin:
        print("domestic")
        print("international")


        cash = int(input("enter cash amount: "))
        if cash >0 :
            print('collect your cash: ', cash)
        else:
            print("Retry")    
    else:
        print("Invaldi PIN")
        

else:
    print("invalid card")        

        

        


