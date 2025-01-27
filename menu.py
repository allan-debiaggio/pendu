import subprocess
import sys

def menu() :
    while True :
        try :
            print("1. Launch Terminal version")
            print("2. Launch Pygame version")
            choice = input("Enter your choice (1 or 2) : ")
            if choice == "1" :
                subprocess.run([sys.executable, "Logiciel/Pendu/pendu.py"])
            elif choice == "2" : 
                subprocess.run([sys.executable, "Logiciel/Pendu/pendu_pygame.py"])
            else :
                print("I didn't understand your request ! Ask again !")
        except KeyboardInterrupt :
            print("\nQuitting...")
            break

menu()