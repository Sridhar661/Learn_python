questions = [
    ["What is the capital of France ?", "Berlin", "Paris", "Rome", "Chennai", 2],
    ["Which planet is known as the Red Planet?", "Earth", "Mars", "Jupiter", "Venus", 2],
    ["Who wrote 'Romeo and Juliet'?", "William Shakespeare", "Charles Dickens", "Mark Twain", "Jane Austen", 1],
    ["What is the largest ocean on Earth?", "Atlantic Ocean", "Indian Ocean", "Pacific Ocean", "Arctic Ocean", 3],
    ["Which gas do plants absorb from the atmosphere?", "Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen", 3],
    ["Who painted the Mona Lisa?", "Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo", 3],
    ["What is the hardest natural substance on Earth?", "Iron", "Diamond", "Gold", "Quartz", 2],
    ["Which country hosted the 2016 Summer Olympics?", "China", "Brazil", "UK", "Japan", 2],
    ["What is the smallest prime number?", "0", "1", "2", "3", 3]
]

# Total points track panna oru variable
points = 0

for question in questions:
    print("\n" + question[0])
    print(f"A.{question[1]}")
    print(f"B.{question[2]}")
    print(f"C.{question[3]}")    
    print(f"D.{question[4]}")  

    answer = int(input("Type the option here , 1 for A, 2 for B, 3 for C, 4 for D: "))

    if question[5] == answer:
        print('Correct answer! (+10 points)')
        points += 10  # Correct answer-ku 10 points add aagum
    else:
        print(f"Wrong Answer, The correct answer is {question[5]}")
        print('Better luck next time')

# Ella questions-um mudinjathum final points print aagum
print("\n---------------------------")
print(f"Quiz Over! Your Total Points: {points} / {len(questions) * 10}")