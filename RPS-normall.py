import random

user_win = 0
system_win = 0

choices = {
    1: "Rock",
    2: "Paper",
    3: "Scissors"
}

while True:
    user_input = int(input("Enter your choice:\n1- Rock\n2- Paper\n3- Scissors\n"))
    user_choice = choices[user_input]

    system_choice = random.choice(list(choices.values()))
    print(f"Computer chose: {system_choice}")

    if user_choice == system_choice:
        print("Draw")
    elif (
        (user_choice == "Rock" and system_choice == "Scissors") or
        (user_choice == "Paper" and system_choice == "Rock") or
        (user_choice == "Scissors" and system_choice == "Paper")
    ):
        user_win += 1
        print("You win this round")
    else:
        system_win += 1
        print("Computer wins this round")

    print(f"User: {user_win} | Computer: {system_win}")

    if user_win == 3:
        print("You win the game ")
        break
    elif system_win == 3:
        print("You lose the game ")
        break
