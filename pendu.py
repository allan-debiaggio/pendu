import random

def title():
    print("WELCOME TO HANGMAN!")
    player_name = input("Give me your name, please: ")
    print(f"Okay {player_name}, let's go!")
    return player_name

def menu():
    print("***MENU***")
    print("1. New Game")
    print("2. Change name")
    print("3. Add word")
    print("4. Leaderboards")
    choice = input("Choose your option: ")
    if choice == "1":
        new_game()
    elif choice == "2":
        title()
    elif choice == "3":
        enter_word()
    elif choice == "4":
        leaderboards_menu()
    else:
        print("I didn't understand your request.")

def choose_difficulty():
    print("1. Kindergarten")
    print("2. Average Joe")
    print("3. Hardcore Henry")
    print("4. Ultraviolence")
    choice = input("Choose a difficulty: ")
    attempts = 0
    if choice == "1":
        attempts = 10 # Maximum guesses
        difficulty = "Kindergarten"
    elif choice == "2":
        attempts = 7
        difficulty = "Average Joe"
    elif choice == "3":
        attempts = 5
        difficulty = "Hardcore Henry"
    elif choice == "4":
        attempts = 3
        difficulty = "Ultraviolence"
    else:
        print("I did not understand your request.")
    return attempts, difficulty

def enter_word():
    word = input("What word do you want to add to the game? ").strip().lower()
    with open("mots.txt", "a") as file:
        file.write(f"\n{word}")
    print("Word added successfully!")

def new_game():
    with open("mots.txt", "r") as file:
        lines = file.readlines()
        if not lines:
            print("No words available! Please add some words first.")
            return
        rand_word = random.choice(lines).strip().lower()
        underscore_rand_word = ["_"] * len(rand_word)
        print("Randomly chosen word:", " ".join(underscore_rand_word))
    
    attempts, difficulty = choose_difficulty()
    guessed_letters = set()

    while attempts > 0 and "_" in underscore_rand_word:
        print(f"\nAttempts left: {attempts}")
        letter = input("Enter a letter to guess: ").strip().lower()
        if len(letter) != 1:
            print("This is not one letter!")
        elif letter in guessed_letters:
            print("You've already guessed this letter!")
        else:
            guessed_letters.add(letter)
            if letter in rand_word:
                print("Correct guess!")
                for i, char in enumerate(rand_word):
                    if char == letter:
                        underscore_rand_word[i] = letter
            else:
                print("Wrong guess!")
                attempts -= 1

            print("Current word:", " ".join(underscore_rand_word))

    if "_" not in underscore_rand_word:
        print("Congratulations! You guessed the word!")
        scores_saves(player_name,attempts, difficulty)
    else:
        hangman()
        print(f"Out of attempts! The word was: {rand_word}")

def scores_saves(player_name, points, difficulty):
    with open("scores.txt", "a") as file:
        file.write(f"{player_name} {points} {difficulty}\n")
    print("Score saved !")

def leaderboards_menu() :
    print("1.Print Leaderboards")
    print("2.Erase Leaderboards")
    choice = input("Choose your option : ")
    if choice == "1" :
        leaderboards()
    elif choice == "2" :
        erase_leaderboards()
    else :
        print("I didn't understand your request.")

def leaderboards():
    try:
        with open("scores.txt", "r") as file:
            content = file.read()
            print(content if content else "No scores yet!")
    except FileNotFoundError:
        print("No leaderboard available yet.")

def erase_leaderboards() :
    with open("scores.txt", "w") as file : 
        pass

def hangman() :
    print("  _______")
    print("  |     |")
    print("  |     O")
    print("  |    /|\\")
    print("  |    / \\")
    print("__|__")

player_name = title()

while True :
    try :
        menu()
    except KeyboardInterrupt :
        print("Quitting the game... ")
        break