"""A small multiple-choice Python quiz game."""
import random

QUESTIONS = [
    {"question": "Which keyword defines a function?",
     "options": ["A. loop", "B. def", "C. func", "D. make"],
     "answer": "B", "explanation": "The def keyword starts a function."},
    {"question": "Which type stores True or False?",
     "options": ["A. int", "B. str", "C. bool", "D. list"],
     "answer": "C", "explanation": "bool represents Boolean values."},
    {"question": "Which symbol starts a comment?",
     "options": ["A. #", "B. //", "C. <!--", "D. **"],
     "answer": "A", "explanation": "Python comments start with #."},
    {"question": "Which collection uses key-value pairs?",
     "options": ["A. tuple", "B. set", "C. list", "D. dict"],
     "answer": "D", "explanation": "A dictionary stores key-value pairs."},
    {"question": "What does len([4, 5, 6]) return?",
     "options": ["A. 2", "B. 3", "C. 4", "D. 6"],
     "answer": "B", "explanation": "The list contains three elements."},
    {"question": "Which loop repeats while a condition is true?",
     "options": ["A. if", "B. for", "C. while", "D. try"],
     "answer": "C", "explanation": "A while loop checks its condition."},
    {"question": "Which method adds an item to a list?",
     "options": ["A. append", "B. addkey", "C. insertall", "D. pushback"],
     "answer": "A", "explanation": "append adds an item at the end."},
    {"question": "Which value represents no value?",
     "options": ["A. 0", "B. False", "C. empty", "D. None"],
     "answer": "D", "explanation": "None represents the absence of a value."},
    {"question": "Which operator checks equality?",
     "options": ["A. =", "B. ==", "C. !=", "D. >="],
     "answer": "B", "explanation": "Double equals compares two values."},
    {"question": "Which statement handles an exception?",
     "options": ["A. catch", "B. error", "C. try", "D. test"],
     "answer": "C", "explanation": "try and except handle exceptions."},
]


def ask_question(question, number, total):
    """Show one question and return whether it was answered correctly."""
    print(f"\nQuestion {number}/{total}")
    print(question["question"])
    for option in question["options"]:
        print("  " + option)
    answer = input("Your answer (A/B/C/D): ").strip().upper()
    if answer == question["answer"]:
        print("Correct!")
        return True
    print("Not quite. Correct answer:", question["answer"])
    return False


def play_round():
    """Play one shuffled round and return the score."""
    questions = QUESTIONS.copy()
    random.shuffle(questions)
    score = 0
    for number, question in enumerate(questions, start=1):
        if ask_question(question, number, len(questions)):
            score += 1
        print("Explanation:", question["explanation"])
    return score, len(questions)


def show_result(score, total):
    """Display the final score and percentage."""
    percentage = (score / total) * 100
    print("\n=== QUIZ RESULT ===")
    print(f"Correct answers: {score}/{total}")
    print(f"Percentage: {percentage:.1f}%")
    if percentage >= 80:
        print("Excellent work!")
    elif percentage >= 50:
        print("Good effort. Keep practising!")
    else:
        print("Review the basics and try again.")


def main():
    """Run the quiz and allow replay."""
    print("Welcome to the Python Knowledge Quiz!")
    while True:
        score, total = play_round()
        show_result(score, total)
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
# Practice idea: modify this program and run it again.
# Practice idea: modify this program and run it again.
# Practice idea: modify this program and run it again.
# Practice idea: modify this program and run it again.
# Practice idea: modify this program and run it again.
# Practice idea: modify this program and run it again.
# Practice idea: modify this program and run it again.
# Practice idea: modify this program and run it again.
# Practice idea: modify this program and run it again.
