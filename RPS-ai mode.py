import random

choices = ["Rock", "Paper", "Scissors"]

counter = {
    "Rock": "Paper",
    "Paper": "Scissors",
    "Scissors": "Rock"
}

#memory
history = []

markov = {
    "Rock": {"Rock": 0, "Paper": 0, "Scissors": 0},
    "Paper": {"Rock": 0, "Paper": 0, "Scissors": 0},
    "Scissors": {"Rock": 0, "Paper": 0, "Scissors": 0}
}

user_win = 0
ai_win = 0


# Predict
def frequency_predictor(history):
    if not history:
        return None
    return max(set(history), key=history.count)

def update_markov(markov, history):
    if len(history) < 2:
        return
    prev = history[-2]
    curr = history[-1]
    markov[prev][curr] += 1


def markov_predictor(markov, last_move):
    if last_move is None:
        return None

    next_moves = markov[last_move]
    if sum(next_moves.values()) == 0:
        return None

    return max(next_moves, key=next_moves.get)


# AI decision
def ai_move(history, markov):
    prediction = None

    if history:
        prediction = markov_predictor(markov, history[-1])

    if prediction is None:
        prediction = frequency_predictor(history)

    if prediction is None:
        return random.choice(choices)

    return counter[prediction]


# Main game
while True:
    user_input = int(input("\n1- Rock\n2- Paper\n3- Scissors\nChoose: "))
    user_choice = choices[user_input - 1]

    ai_choice = ai_move(history, markov)

    print(f"User: {user_choice}")
    print(f"AI:   {ai_choice}")

    if user_choice == ai_choice:
        print("Draw")
    elif counter[user_choice] == ai_choice:
        ai_win += 1
        print("AI wins this round")
    else:
        user_win += 1
        print("User wins this round")


    history.append(user_choice)
    update_markov(markov, history)

    print(f"\nScore → User: {user_win} | AI: {ai_win}")

    if user_win == 3:
        print("\n🎉 You win the game")
        break
    elif ai_win == 3:
        print("\n🤖 AI wins the game")
        break
