import random

choices = ["Rock", "Paper", "Scissors"]

counter = {
    "Rock": "Paper",
    "Paper": "Scissors",
    "Scissors": "Rock"
}

# ---------------- Memory ----------------
history = []

markov = {
    "Rock": {"Rock": 0, "Paper": 0, "Scissors": 0},
    "Paper": {"Rock": 0, "Paper": 0, "Scissors": 0},
    "Scissors": {"Rock": 0, "Paper": 0, "Scissors": 0}
}

predictors = {
    "markov": {"score": 0},
    "frequency": {"score": 0},
    "win_stay": {"score": 0},
    "anti_cycle": {"score": 0}
}

user_win = 0
ai_win = 0
last_result = None   # win / lose / draw

# ---------------- Predictors ----------------
def frequency_predictor(history, window=5):
    if not history:
        return None
    recent = history[-window:]
    return max(set(recent), key=recent.count)


def update_markov(markov, history):
    if len(history) < 2:
        return
    prev, curr = history[-2], history[-1]
    markov[prev][curr] += 1


def markov_predictor(markov, last_move, min_samples=3):
    if last_move is None:
        return None
    next_moves = markov[last_move]
    if sum(next_moves.values()) < min_samples:
        return None
    return max(next_moves, key=next_moves.get)


def win_stay_lose_shift(history, last_result):
    if not history or last_result is None:
        return None
    last_move = history[-1]
    if last_result == "win":
        return last_move
    if last_result == "lose":
        return random.choice([m for m in choices if m != last_move])
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


def choose_predictor(predictions, predictors):
    best_move = None
    best_score = -999
    for name, move in predictions.items():
        if move is None:
            continue
        if predictors[name]["score"] > best_score:
            best_score = predictors[name]["score"]
            best_move = move
    return best_move


def update_scores(predictions, user_move, predictors):
    for name, predicted in predictions.items():
        if predicted == user_move:
            predictors[name]["score"] += 1
        else:
            predictors[name]["score"] -= 1


# ---------------- AI Decision ----------------
def ai_move(history, markov, last_result, predictors, epsilon=0.1):
    if random.random() < epsilon:
        return random.choice(choices)

    predictions = {
        "markov": markov_predictor(markov, history[-1] if history else None),
        "frequency": frequency_predictor(history),
        "win_stay": win_stay_lose_shift(history, last_result),
        "anti_cycle": anti_cycle(history)
    }

    predicted_user = choose_predictor(predictions, predictors)

    if predicted_user is None:
        return random.choice(choices)

    return counter[predicted_user]


# ---------------- Main Game ----------------
while True:
    user_input = int(input("\n1- Rock\n2- Paper\n3- Scissors\nChoose: "))
    user_choice = choices[user_input - 1]

    ai_choice = ai_move(history, markov, last_result, predictors)

    print(f"User: {user_choice}")
    print(f"AI:   {ai_choice}")

    if user_choice == ai_choice:
        print("Draw")
        last_result = "draw"
    elif counter[user_choice] == ai_choice:
        ai_win += 1
        print("AI wins this round")
        last_result = "lose"
    else:
        user_win += 1
        print("User wins this round")
        last_result = "win"

    predictions = {
        "markov": markov_predictor(markov, history[-1] if history else None),
        "frequency": frequency_predictor(history),
        "win_stay": win_stay_lose_shift(history, last_result),
        "anti_cycle": anti_cycle(history)
    }

    update_scores(predictions, user_choice, predictors)

    history.append(user_choice)
    update_markov(markov, history)

    print(f"\nScore → User: {user_win} | AI: {ai_win}")
    #print(f"Predictor scores: { {k:v['score'] for k,v in predictors.items()} }")

    if user_win == 5:
        print("\n🎉 You win the game")
        break
    elif ai_win == 5:
        print("\n🤖 AI wins the game")
        break
