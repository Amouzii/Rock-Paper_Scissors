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
def frequency_predictor(history, window=5):
    if not history:
        return None

    recent = history[-window:]
    return max(set(recent), key=recent.count)

def update_markov(markov, history):
    if len(history) < 2:
        return
    prev = history[-2]
    curr = history[-1]
    markov[prev][curr] += 1


def markov_predictor(markov, last_move, min_samples=3):
    if last_move is None:
        return None

    next_moves = markov[last_move]
    total = sum(next_moves.values())

    if total < min_samples:
        return None

    return max(next_moves, key=next_moves.get)

def win_stay_lose_shift(history, last_result):
    if not history or last_result is None:
        return None

    last_move = history[-1]

    if last_result == "win":
        return last_move

    if last_result == "lose":
        options = [m for m in choices if m != last_move]
        return random.choice(options)

    return None

def anti_cycle(history):
    if len(history) < 2:
        return None

    a, b = history[-2], history[-1]

    cycle = {
        ("Rock", "Paper"): "Scissors",
        ("Paper", "Scissors"): "Rock",
        ("Scissors", "Rock"): "Paper"
    }

    return cycle.get((a, b))

def anti_cycle(history):
    if len(history) < 2:
        return None

    a, b = history[-2], history[-1]

    cycle = {
        ("Rock", "Paper"): "Scissors",
        ("Paper", "Scissors"): "Rock",
        ("Scissors", "Rock"): "Paper"
    }

    return cycle.get((a, b))

def choose_predictor(predictions, predictors):
    best = None
    best_score = -999

    for name, move in predictions.items():
        if move is None:
            continue
        if predictors[name]["score"] > best_score:
            best = move
            best_score = predictors[name]["score"]

    return best

def update_scores(predictions, user_move, predictors):
    for name, predicted in predictions.items():
        if predicted == user_move:
            predictors[name]["score"] += 1
        else:
            predictors[name]["score"] -= 1



# AI decision
def ai_move(history, markov, last_result, predictors, epsilon=0.1):
    if random.random() < epsilon:
        return random.choice(choices)

    predictions = {
        "markov": markov_predictor(markov, history[-1] if history else None),
        "frequency": frequency_predictor(history),
        "win_stay": win_stay_lose_shift(history, last_result),
        "anti_cycle": anti_cycle(history)
    }

    predicted_user_move = choose_predictor(predictions, predictors)

    if predicted_user_move is None:
        return random.choice(choices)

    return counter[predicted_user_move]


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

    if user_win == 5:
        print("\n🎉 You win the game")
        break
    elif ai_win == 5:
        print("\n🤖 AI wins the game")
        break
