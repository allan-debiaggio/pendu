import random

def title() :
    print("WELCOME TO THE HANGMAN !")
    player_name = input("Give me your name, please : ")
    print(f"Okay {player_name}, let's go !")
    return player_name

def menu() :
    print("***MENU***")
    print("1.New Game")
    print("2.Choose difficulty")
    print("3.Add word")
    print("4.Leaderboards")
    choice=input("Choose your option : ")
    if choice == "1" :
        new_game()
    elif choice == "2" :
        choose_difficulty()
    elif choice == "3" :
        enter_word()
    elif choice == "4" :
        leaderboards()
    else : 
        print("I didn't understand your request.")

def choose_difficulty() :
    print("1. Kindergarten")
    print("2. Average Joe")
    print("3. Hardcore Henry")
    print("4. Ultraviolence")
    choice = input("Choose a difficulty : ")
    if choice == "1" :
        difficulty = 1
    elif choice == "2" :
        difficulty = 2
    elif choice == "3" :
        difficulty = 3
    elif choice == "4" :
        difficulty = 4
    else :
        print("I did not understand your request.")
    return difficulty

def enter_word() :
    word=input("What word do you want to add to the game ? ")
    with open ("mots.txt", "a") as file :
        file.write(f"{word}")

def new_game() :
    with open("mots.txt", "r") as file :
        lines = file.readlines()
        rand_number = random.randint(0, len(lines) - 1)
        rand_word = lines [rand_number].strip()
        print(f"Randomly chosen word : {"_ " * len(rand_word)}")

def scores_saves() :
    with open ("scores.txt", "a") as file :
        file.write(f"{title(), " ", "points"}")

def leaderboards() :
    with open ("scores.txt", "r") as file :
        content = file.read()
        print(content)

while True :
    try :
        title()
        menu()
    except KeyboardInterrupt :
        print("\nQuitting the game...")
        break