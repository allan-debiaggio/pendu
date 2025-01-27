import pygame
import random
import os
import json
import requests

# Initialisation de Pygame
pygame.init()

# Définition des constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FONT = pygame.font.Font(None, 36)

JSON_FILE_PATH = 'words.json' # PATH WORDS JSON
SCORES_FILE_PATH = 'scores.txt' # scores for leaderboard
ASSETS_PATH = 'assets/win.png' 

API_URLS = [ #API for words
    "https://trouve-mot.fr/api/categorie/6",
    "https://trouve-mot.fr/api/categorie/19",
    "https://trouve-mot.fr/api/categorie/16",
    "https://trouve-mot.fr/api/categorie/17",
    "https://trouve-mot.fr/api/categorie/5",
]

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

def save_score(player_name, attempts_left, difficulty): # Save score in file
    with open(SCORES_FILE_PATH, 'a') as file:
        file.write(f"{player_name} {attempts_left} {difficulty}\n")

def load_leaderboard():
    if not os.path.exists(SCORES_FILE_PATH):
        return []
    with open(SCORES_FILE_PATH, 'r') as file:
        scores = [line.strip() for line in file.readlines()]
    return scores

def draw_text(screen, text, x, y, color=BLACK):
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_hangman(screen, attempts): # Draw hangman
    base_x = 150
    base_y = 400
    if attempts <= 5:
        pygame.draw.line(screen, BLACK, (base_x, base_y), (base_x, base_y - 150), 4)
    if attempts <= 4:
        pygame.draw.line(screen, BLACK, (base_x, base_y - 150), (base_x + 100, base_y - 150), 4)
    if attempts <= 3:
        pygame.draw.line(screen, BLACK, (base_x + 100, base_y - 150), (base_x + 100, base_y - 120), 4)
    if attempts <= 2:
        pygame.draw.circle(screen, BLACK, (base_x + 100, base_y - 100), 20, 4)
    if attempts <= 1:
        pygame.draw.line(screen, BLACK, (base_x + 100, base_y - 80), (base_x + 100, base_y - 30), 4)
    if attempts == 0:
        pygame.draw.line(screen, BLACK, (base_x + 100, base_y - 30), (base_x + 80, base_y), 4)
        pygame.draw.line(screen, BLACK, (base_x + 100, base_y - 30), (base_x + 120, base_y), 4)

def get_player_name(screen): 
    name = ""
    running = True
    while running:
        screen.fill(WHITE)
        draw_text(screen, "Enter your name:", 50, 50, RED)
        draw_text(screen, name, 50, 100, BLACK)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode.isalpha() or event.unicode == " ":
                    name += event.unicode

    return name.strip()

def choose_difficulty(screen):
    difficulties = {
        "1": (10, "Kindergarten"),
        "2": (7, "Average Joe"),
        "3": (5, "Hardcore Henry"),
        "4": (3, "Ultraviolence")
    }
    running = True
    while running: # Choose difficulty
        screen.fill(WHITE)
        draw_text(screen, "Choose a difficulty:", 50, 50, RED)
        draw_text(screen, "1. Kindergarten (10 attempts)", 50, 100)
        draw_text(screen, "2. Average Joe (7 attempts)", 50, 150)
        draw_text(screen, "3. Hardcore Henry (5 attempts)", 50, 200)
        draw_text(screen, "4. Ultraviolence (3 attempts)", 50, 250)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.unicode in difficulties:
                    return difficulties[event.unicode]

def leaderboard_screen(screen):
    leaderboard = load_leaderboard()
    running = True
    while running:
        screen.fill(WHITE)
        draw_text(screen, "Leaderboard:", 50, 50, RED)

        for i, entry in enumerate(leaderboard):
            draw_text(screen, entry, 50, 100 + i * 30)

        draw_text(screen, "Press ESC to return to the menu.", 50, 500, BLACK)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

def victory_screen(screen):
    if not os.path.exists(ASSETS_PATH):
        print("Victory image not found! Please ensure win.png is in the assets folder.")
        return

    win_image = pygame.image.load(ASSETS_PATH)
    win_image = pygame.transform.scale(win_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    screen.blit(win_image, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)

def game_loop():
    words = load_words()
    if not words:
        print("No words available! Please add some words first.")
        return

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Hangman Game")

    clock = pygame.time.Clock()

    player_name = get_player_name(screen)
    attempts, difficulty = choose_difficulty(screen)
    rand_word = random.choice(words)
    underscore_word = ["_"] * len(rand_word)
    guessed_letters = set()

    running = True
    while running:
        screen.fill(WHITE)
        draw_text(screen, f"Player: {player_name}", 50, 20, GREEN)
        draw_text(screen, f"Difficulty: {difficulty}", 50, 60)
        draw_text(screen, f"Attempts left: {attempts}", 50, 100)
        draw_text(screen, "Word: " + " ".join(underscore_word), 50, 140)
        draw_text(screen, "Guessed letters: " + ", ".join(sorted(guessed_letters)), 50, 180)
        draw_hangman(screen, attempts)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    letter = event.unicode.lower()
                    if letter in guessed_letters:
                        continue

                    guessed_letters.add(letter)
                    if letter in rand_word:
                        for i, char in enumerate(rand_word):
                            if char == letter:
                                underscore_word[i] = letter
                    else:
                        attempts -= 1

        if "_" not in underscore_word:
            victory_screen(screen)
            save_score(player_name, attempts, difficulty)
            running = False

        if attempts == 0:
            draw_text(screen, f"You lost! The word was: {rand_word}", 50, 220, RED)
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False

        pygame.display.flip()
        clock.tick(30)

    leaderboard_screen(screen)

def main_menu():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Hangman Main Menu")

    clock = pygame.time.Clock()
    running = True

    while running: # Main menu
        screen.fill(WHITE)
        draw_text(screen, "Main Menu", 50, 50, RED)
        draw_text(screen, "1. Start Game", 50, 100)
        draw_text(screen, "2. View Leaderboard", 50, 150)
        draw_text(screen, "3. Quit", 50, 200)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.unicode == "1":
                    game_loop()
                if event.unicode == "2":
                    leaderboard_screen(screen)
                if event.unicode == "3":
                    running = False

        clock.tick(30)

main_menu()
pygame.quit()
