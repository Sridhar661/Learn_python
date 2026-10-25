"""A small number guessing game."""

secret_number = 7

while True:
    guess_text = input("Guess the number (1-10), or q to quit: ").strip()
    if guess_text.lower() == "q":
        print("Goodbye!")
        break

    try:
        guess = int(guess_text)
    except ValueError:
        print("Please enter a whole number or q.")
        continue

    if guess == secret_number:
        print("Correct! You guessed it.")
        break
    elif guess < secret_number:
        print("Too low. Try again.")
    else:
        print("Too high. Try again.")
