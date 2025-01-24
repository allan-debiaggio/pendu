import pygame
import random
import os

pygame.init()

window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Hangman Game")

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHT_GRAY = (211, 211, 211)  

font = pygame.font.Font(None, 40)

def load_words():
    if os.path.exists("words.txt"):
        with open("words.txt", "r") as f:
            return f.read().splitlines()
    else:
        return []

def display_text(text, color, x, y):
    displayed_text = font.render(text, True, color)
    window.blit(displayed_text, (x, y))

def load_hangman_image(attempts):
    try:
        # Images are named image1.png, image2.png, etc.
        image = pygame.image.load(f"images/image{attempts + 1}.png")
        return image
    except pygame.error:
        return None

def play():
    words = load_words()
    if not words:
        print("No words available in the file.")
        return

    word = random.choice(words).lower()
    guessed_letters = ['_'] * len(word)
    used_letters = set()
    attempts = 0
    max_attempts = 6

    while attempts < max_attempts and '_' in guessed_letters:
        window.fill(LIGHT_GRAY)
        
        display_text(' '.join(guessed_letters), BLACK, 350, 200)

        display_text(f"Attempts remaining: {max_attempts - attempts}", BLACK, 300, 250)

        hangman_image = load_hangman_image(attempts)
        if hangman_image:
            window.blit(hangman_image, (50, 100))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                letter = chr(event.key).lower()
                if letter.isalpha() and letter not in used_letters:
                    used_letters.add(letter)
                    if letter in word:
                        for i in range(len(word)):
                            if word[i] == letter:
                                guessed_letters[i] = letter
                    else:
                        attempts += 1

        pygame.time.wait(500)

    window.fill(LIGHT_GRAY)
    if '_' not in guessed_letters:
        display_text("You Win!", GREEN, 350, 350)
    else:
        display_text(f"You Lose! The word was: {word}", RED, 200, 350)

    pygame.display.update()
    pygame.time.wait(2000)
    main_menu()

def show_menu():
    window.fill(LIGHT_GRAY)
    pygame.draw.rect(window, BLUE, (5, 5, window_width - 10, window_height - 10), 5)
    display_text("Main Menu", BLACK, 300, 100)
    display_text("1. Play", BLACK, 350, 200)
    display_text("2. Add a word", BLACK, 300, 300)
    display_text("3. Quit", BLACK, 350, 400)

def main_menu():
    while True:
        show_menu()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  
                    play()
                elif event.key == pygame.K_2:  
                    add_word()
                elif event.key == pygame.K_3:  
                    pygame.quit()
                    return

def add_word():
    word = input("Enter a new word to add to the file: ").strip()
    with open("words.txt", "a") as f:
        f.write(word + "\n")

if __name__ == "__main__":
    main_menu()
    pygame.quit()

