def title() :
    print("WELCOME TO THE HANGMAN !")
    player_name = input("Give me your name, please : ")
    print(f"Okay {player_name}, let's go !")

def menu() :
    print("***MENU***")
    print("1.New Game")
    print("2.Choose difficulty")
    print("3.Add word")
    print("4.Leaderboards")
    choice=input("Choose your option : ")
    if choice == "1" :
        enter_word()
    elif choice == "2" :
        enter_word()
    elif choice == "3" :
        enter_word()
    elif choice == "4" :
        enter_word()
    else : 
        print("I didn't understand your request.")

def enter_word() :
    word=input("What word do you want to add to the game ? ")
    with open ("mots.txt", "a") as file :
        file.write(f"{word}")

while True :
    try :
        title()
        menu()
    except KeyboardInterrupt :
        print("\nQuitting the game...")
        break