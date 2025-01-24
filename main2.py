import random
import pygame
import requests
import json
import os

pygame.mixer.init()

JSON_FILE_PATH = 'words.json'

API_URLS = [
    "https://trouve-mot.fr/api/categorie/6",
    "https://trouve-mot.fr/api/categorie/19",
    "https://trouve-mot.fr/api/categorie/16",
    "https://trouve-mot.fr/api/categorie/17",
    "https://trouve-mot.fr/api/categorie/5",
]

def title():
    try:
        print("WELCOME TO HANGMAN!")
        player_name = input("Give me your name, please: ")
        print(f"Okay {player_name}, let's go!")
        return player_name
    except KeyboardInterrupt:
        print("\nQuitting the game...")
        quit()

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

def load_words():
    words = []
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r') as file:
            words = json.load(file)

    for url in API_URLS:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for entry in data:
                    word = entry.get('name', '').strip().lower()
                    if word and word not in words:
                        words.append(word)
        except requests.exceptions.RequestException:
            print(f"Error connecting to API: {url}")
            continue

    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(words, file, ensure_ascii=False, indent=4)

    return words

def get_random_word(words):
    if words:
        return random.choice(words)
    print("No words available.")
    return None

def choose_difficulty():
    while True:
        try:
            print("1. Kindergarten")
            print("2. Average Joe")
            print("3. Hardcore Henry")
            print("4. Ultraviolence")
            choice = input("Choose a difficulty: ")
            attempts = 0 # Guesses
            if choice == "1":
                attempts = 10
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
            return attempts, difficulty
        except (TypeError, UnboundLocalError): 
            print("Erhm, you can't do that, Billy.")

def enter_word():
    word = input("What word do you want to add to the game? ").strip().lower()
    with open(JSON_FILE_PATH, "r") as file:
        words = json.load(file)

    if word not in words:
        words.append(word)
        with open(JSON_FILE_PATH, "w") as file:
            json.dump(words, file, ensure_ascii=False, indent=4)
        print("Word added successfully!")
    else:
        print("Word already exists in the list.")

def new_game():
    words = load_words()
    rand_word = get_random_word(words)
    if not rand_word:
        print("No words available! Please add some words first.")
        return

    underscore_rand_word = ["_"] * len(rand_word)
    print("Randomly chosen word:", " ".join(underscore_rand_word))

    attempts, difficulty = choose_difficulty()
    guessed_letters = set()

    while attempts > 0 and "_" in underscore_rand_word:
        print(f"\nAttempts left: {attempts}")
        letter = input("Enter a letter to guess: ").strip().lower()
        if letter == rand_word:
            print("WHAT A GUESS !!! CORRECT !!!")
            play_sound("denis_ah.mp3")
            scores_saves(player_name, attempts, difficulty)
            return

        elif len(letter) != 1:
            print("This is not one letter!")
        elif letter in guessed_letters:
            print("You've already guessed this letter!")
        else:
            guessed_letters.add(letter)
            if letter in rand_word or letter == rand_word:
                print("Correct guess!")
                for i, char in enumerate(rand_word):
                    if char == letter:
                        underscore_rand_word[i] = letter
            else:
                print("Wrong guess!")
                attempts -= 1

            print("Current word:", " ".join(underscore_rand_word))

    if "_" not in underscore_rand_word:
        play_sound("denis_ah.mp3")
        print("Congratulations! You guessed the word!")
        scores_saves(player_name, attempts, difficulty)
    else:
        play_sound("motus_boule_noire.mp3")
        hangman()
        print(f"Out of attempts! The word was: {rand_word}")
        print(f"The word you were looking for was: {rand_word}")

def play_sound(file_name):
    try:
        sound = pygame.mixer.Sound(file_name)
        sound.play()
    except pygame.error:
        print("Sound could not be played:", file_name)

def scores_saves(player_name, points, difficulty):
    with open("scores.txt", "a") as file:
        file.write(f"{player_name} {points} {difficulty}\n")
    print("Score saved !")

def leaderboards_menu():
    print("1.Print Leaderboards")
    print("2.Erase Leaderboards")
    choice = input("Choose your option : ")
    if choice == "1":
        leaderboards()
    elif choice == "2":
        erase_leaderboards()
    else:
        print("I didn't understand your request.")

def leaderboards():
    try:
        with open("scores.txt", "r") as file:
            content = file.read()
            print(content if content else "No scores yet!")
    except FileNotFoundError:
        print("No leaderboard available yet.")

def erase_leaderboards():
    with open("scores.txt", "w") as file: 
        pass

def hangman():
    print("  _______")
    print("  |     |")
    print("  |     O")
    print("  |    /|\\")
    print("  |    / \\")
    print("__|__")

player_name = title()

while True:
    try:
        menu()
    except KeyboardInterrupt:
        print("\nQuitting the game... ")
        break
