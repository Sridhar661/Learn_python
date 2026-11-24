email = input("enter your email : ")

index = email.index("@")
username = email[:index]
domain = email[index:]

print(f"your email is {username } and your domain is {domain}")