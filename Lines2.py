# Python_Projects/
# │
# ├── 01_basics/
# │   ├── hello_world.py
# │   ├── variables.py
# │   └── data_types.py
# │
# ├── 02_conditions/
# │   ├── if_else.py
# │   └── comparison.py
# │
# ├── 03_loops/
# │   ├── for_loop.py
# │   └── while_loop.py
# │
# ├── 04_functions/
# │   ├── functions.py
# │   └── lambda_functions.py
# │
# ├── 05_data_structures/
# │   ├── lists.py
# │   ├── tuples.py
# │   └── dictionaries.py
# │
# ├── 06_oop/
# │   └── classes_objects.py
# │
# └── README.md














def blackjack_hand_greater_than(hand_1, hand_2):
    """
    Return True if hand_1 beats hand_2, and False otherwise.
    """

    def hand_total(hand):
        total = 0
        aces = 0

        for card in hand:
            if card in ['J', 'Q', 'K']:
                total += 10
            elif card == 'A':
                aces += 1
                total += 1
            else:
                total += int(card)

        # Upgrade aces from 1 to 11 when possible
        if aces > 0 and total + 10 <= 21:
            total += 10

        return total

    total_1 = hand_total(hand_1)
    total_2 = hand_total(hand_2)

    return total_1 <= 21 and (
        total_1 > total_2 or total_2 > 21
    )


# Check your answer
q3.check()













# Import Luigi's full dataset
from learntools.python.luigi_analysis import full_dataset

def best_items(racers):
    winner_item_counts = {}

    for i in range(len(racers)):
        # The i'th racer dictionary
        racer = racers[i]

        # Count items picked up by first-place finishers
        if racer['finish'] == 1:
            for item in racer['items']:
                if item not in winner_item_counts:
                    winner_item_counts[item] = 0
                winner_item_counts[item] += 1

        # Warn about racers whose names are missing
        if racer['name'] is None:
            print(
                "WARNING: Encountered racer with unknown name "
                "on iteration {}/{} (racer = {})".format(
                    i + 1, len(racers), racer['name']
                )
            )

    return winner_item_counts

# Analyze the full dataset
best_items(full_dataset)
