import random

options = ['rock' , 'paper' , 'scissor']

player = input("enter your choice (rock , paper , scissor):")

computer = random.choice(options)
print(player)

print(computer)
if player == computer :
    print("It's a tie" )

elif player == 'rock' and computer == 'scissor':
    print("you win!")
elif player == 'scissor' and computer == 'paper':
    print('you win!')

elif player == 'paper' and computer == 'rock':
    print('you win!')
else:
    print('you lose!')    
