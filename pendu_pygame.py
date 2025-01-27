import pygame
import random

pygame.init()

# Window dimensions
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")
icon = pygame.image.load("Logiciel/Pendu/images/icon.png")
pygame.display.set_icon(icon)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
MENU_FONT = pygame.font.SysFont('comicsans', 40)
TITLE_FONT = pygame.font.SysFont('comicsans', 60)
INPUT_FONT = pygame.font.SysFont('comicsans', 30)
LETTER_FONT = pygame.font.SysFont('comicsans', 30)
WORD_FONT = pygame.font.SysFont('comicsans', 50)

# Difficulty settings
DIFFICULTIES = {
    "Kindergarten": 10,
    "Average Joe": 7,
    "Hardcore Henry": 5,
    "Ultraviolence": 3
}

# Game variables
hangman_status = 0
guessed = []
incorrect = []
word = ""


def load_words():
    """Load words from a text file."""
    try:
        with open("mots.txt", "r") as file:
            words = file.read().splitlines()
            if not words:
                return None
            return words
    except FileNotFoundError:
        return None


def save_word(word):
    """Save a word to the mots.txt file."""
    with open("mots.txt", "a") as file:
        file.write(f"{word}\n")


def draw_menu():
    """Draw the main menu screen."""
    win.fill(WHITE)

    # Title
    title_text = TITLE_FONT.render("Hangman Game", 1, BLACK)
    win.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, 100))

    # Menu options
    options = ["1. New Game", "2. Add Word", "3. View Scores", "4. Quit"]
    for i, option in enumerate(options):
        text = MENU_FONT.render(option, 1, BLACK)
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, 200 + i * 60))

    pygame.display.update()

def draw_wrapped_text(text, font, max_width, y_pos):
    """Draw wrapped text on the screen."""
    words = text.split(' ')
    current_line = ""
    line_height = font.get_height() + 5
    for word in words:
        test_line = current_line + " " + word if current_line else word
        test_width = font.size(test_line)[0]
        
        if test_width <= max_width:
            current_line = test_line
        else:
            text_surface = font.render(current_line, True, BLACK)
            win.blit(text_surface, (WIDTH / 2 - text_surface.get_width() / 2, y_pos))
            y_pos += line_height
            current_line = word

    # Draw the last line
    if current_line:
        text_surface = font.render(current_line, True, BLACK)
        win.blit(text_surface, (WIDTH / 2 - text_surface.get_width() / 2, y_pos))
        y_pos += line_height

    return y_pos

def view_scores():
    """Display the scores from the scores.txt file."""
    win.fill(WHITE)

    try:
        with open("scores.txt", "r") as file:
            scores = file.read()
    except FileNotFoundError:
        scores = "No scores found."

    y_pos = 150  # Start Y position to display the scores
    y_pos = draw_wrapped_text(scores, INPUT_FONT, WIDTH - 40, y_pos)  # Wrap the text to fit the screen

    # Instruction to return to the menu
    instruction_text = MENU_FONT.render("Press any key to return to menu", True, BLACK)
    win.blit(instruction_text, (WIDTH / 2 - instruction_text.get_width() / 2, y_pos))

    pygame.display.update()

    # Wait for the user to press a key to go back to the menu
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
                return  # Go back to the menu

def draw_input_box(prompt, user_text):
    """Draw an input box on the screen."""
    win.fill(WHITE)

    # Prompt
    prompt_text = INPUT_FONT.render(prompt, 1, BLACK)
    win.blit(prompt_text, (WIDTH / 2 - prompt_text.get_width() / 2, 200))

    # Input box
    input_box = pygame.Rect(WIDTH / 2 - 150, 300, 300, 50)
    pygame.draw.rect(win, BLACK, input_box, 2)

    # User input
    text_surface = INPUT_FONT.render(user_text, 1, BLACK)
    win.blit(text_surface, (input_box.x + 10, input_box.y + 10))

    pygame.display.update()


def add_word_screen():
    """Display the screen for adding a new word."""
    user_text = ""
    prompt = "Enter a word to add:"
    run = True

    while run:
        draw_input_box(prompt, user_text)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_text:
                        save_word(f"\n{user_text.lower()}")
                        return
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode


def draw_hangman(status):
    """Draw the hangman figure based on the current status."""
    # Gallows structure
    pygame.draw.line(win, BLACK, (100, 400), (250, 400), 5)  # Base
    pygame.draw.line(win, BLACK, (175, 150), (175, 400), 5)  # Vertical pole
    pygame.draw.line(win, BLACK, (175, 150), (250, 150), 5)  # Horizontal beam
    pygame.draw.line(win, BLACK, (250, 150), (250, 180), 5)  # Rope

    if status >= 1:  # Head
        pygame.draw.circle(win, BLACK, (250, 200), 20, 3)
    if status >= 2:  # Body
        pygame.draw.line(win, BLACK, (250, 220), (250, 300), 3)
    if status >= 3:  # Left arm
        pygame.draw.line(win, BLACK, (250, 240), (220, 260), 3)
    if status >= 4:  # Right arm
        pygame.draw.line(win, BLACK, (250, 240), (280, 260), 3)
    if status >= 5:  # Left leg
        pygame.draw.line(win, BLACK, (250, 300), (220, 340), 3)
    if status >= 6:  # Right leg
        pygame.draw.line(win, BLACK, (250, 300), (280, 340), 3)


def draw_game():
    """Draw the game screen."""
    win.fill(WHITE)

    # Display word
    display_word = " ".join(guessed)
    word_text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(word_text, (WIDTH / 2 - word_text.get_width() / 2, 400))

    # Display incorrect guesses
    incorrect_text = LETTER_FONT.render("Incorrect: " + " ".join(incorrect), 1, RED)
    win.blit(incorrect_text, (20, 500))

    # Draw hangman
    draw_hangman(hangman_status)

    pygame.display.update()

def draw_difficulty_screen(player_name):
    """Display the difficulty selection screen."""
    win.fill(WHITE)

    # Title
    title_text = TITLE_FONT.render(f"Welcome, {player_name}!", True, BLACK)
    win.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, 100))

    # Difficulty options
    prompt_text = MENU_FONT.render("Select Difficulty:", True, BLACK)
    win.blit(prompt_text, (WIDTH / 2 - prompt_text.get_width() / 2, 200))

    difficulties = list(DIFFICULTIES.keys())
    for i, difficulty in enumerate(difficulties):
        diff_text = MENU_FONT.render(f"{i + 1}. {difficulty}", True, BLACK)
        win.blit(diff_text, (WIDTH / 2 - diff_text.get_width() / 2, 300 + i * 50))

    pygame.display.update()

def get_player_name():
    """Prompt the player to enter their name."""
    user_text = ""
    prompt = "Enter your name:"
    run = True

    while run:
        draw_input_box(prompt, user_text)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and user_text:
                    return user_text.capitalize()
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

def choose_difficulty(player_name):
    """Allow the player to choose a difficulty level."""
    draw_difficulty_screen(player_name)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    difficulty_index = event.key - pygame.K_1
                    return list(DIFFICULTIES.values())[difficulty_index]


def new_game():
    """Start a new game with player name and difficulty selection."""
    global hangman_status, guessed, incorrect, word

    player_name = get_player_name()
    max_attempts = choose_difficulty(player_name)

    words = load_words()
    if not words:
        end_screen("No words found! Please add words first.")
        return

    word = random.choice(words).upper()
    guessed = ["_"] * len(word)
    incorrect = []
    hangman_status = 0

    run = True
    while run:
        draw_game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key >= pygame.K_a and event.key <= pygame.K_z:
                    letter = chr(event.key).upper()
                    if letter in word and letter not in guessed:
                        for i in range(len(word)):
                            if word[i] == letter:
                                guessed[i] = letter
                    elif letter not in word and letter not in incorrect:
                        incorrect.append(letter)
                        hangman_status += 1

        if "_" not in guessed:
            sound = pygame.mixer.Sound("Logiciel/Pendu/denis_ah.mp3")
            sound.play()
            end_screen(f"YOU WON, {player_name}!")
            break

        if hangman_status >= max_attempts:
            sound = pygame.mixer.Sound("Logiciel/Pendu/motus_boule_noire.mp3")
            sound.play()
            end_screen(f"YOU LOST, {player_name}!", correct_word=word)
            break


def end_screen(message, correct_word=None):
    """Display the game end screen with a result message and correct word if applicable."""
    win.fill(WHITE)

    # Main message (YOU WON! or YOU LOST!)
    main_text = TITLE_FONT.render(message, True, RED if "YOU LOST" in message else GREEN)
    win.blit(main_text, (WIDTH / 2 - main_text.get_width() / 2, HEIGHT / 2 - 100))

    # Correct word (if provided)
    if correct_word:
        word_text = INPUT_FONT.render(f"The word was: {correct_word}", True, BLACK)
        win.blit(word_text, (WIDTH / 2 - word_text.get_width() / 2, HEIGHT / 2))

    # Instruction to return to the menu
    instruction_text = MENU_FONT.render("Press any key to return to menu", True, BLACK)
    win.blit(instruction_text, (WIDTH / 2 - instruction_text.get_width() / 2, HEIGHT / 2 + 100))

    pygame.display.update()

    # Wait for user to press any key
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


def main_menu():
    """Display the main menu within the game window."""
    run = True
    while run:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    new_game()
                elif event.key == pygame.K_2:
                    add_word_screen()
                elif event.key == pygame.K_3:
                    view_scores()  # Show the scores screen when selected
                elif event.key == pygame.K_4:
                    run = False

    pygame.quit()


if __name__ == "__main__":
    main_menu()
