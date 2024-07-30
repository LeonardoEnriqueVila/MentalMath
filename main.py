import SimpleGame
import CashGame
import Color
import StatsDB

class Menu():
    def __init__(self):
        self.state = False
        self.mainMenuMessage = f"{Color.YELLOW}Main Menu{Color.RESET}\n1. Play Game\n2. Show Stats\n3. Quit\n{Color.LIGHT_BLUE}Select an Option:{Color.RESET} "
        self.gameMenuMessage = f"{Color.YELLOW}Game Menu{Color.RESET}\n1. Multiply!\n2. Add!\n3. Substract!\n4. Divide!\n5. Cash Game!\n6. Go Back.\n{Color.LIGHT_BLUE}Select an Option:{Color.RESET} "
        self.mainMenuLoop()
    
    def mainMenuLoop(self): # bucle del menu principal
        while self.callOption(self.getOption([1, 2, 3], self.mainMenuMessage)):
            pass
            
    def getOption(self, options, message): # obtener una opcion del menu con input de usuario y retornarla
        self.mainMessage = False
        while True:
            try:
                option = int(input(message))
                if option in options:
                    return option
            except ValueError:
                option = -1
                pass
            if option not in options:
                print(f"{Color.RED}Enter a valid option.{Color.RESET}")
                message = f"{Color.LIGHT_BLUE}Select an Option: {Color.RESET}"

    def callOption(self, option): # llamar a la opcion que se eligió en el menu
        match option:
            case 1:
                gameOption = -1
                while gameOption != 6:
                    gameOption = self.getOption([1, 2, 3, 4, 5, 6], self.gameMenuMessage) # menu de juegos
                    if gameOption == 1:
                        SimpleGame.multiplyGame.startGame() 
                    elif gameOption == 2:
                        SimpleGame.addGame.startGame()
                    elif gameOption == 3:
                        SimpleGame.substractGame.startGame()
                    elif gameOption == 4:
                        SimpleGame.divideGame.startGame()
                    elif gameOption == 5:
                        CashGame.cashGame.startGame()
            case 2: # muestra los ultimos stats del juego deseado 
                flag = True
                while flag:
                    name = input("Enter Game Name: ").split()
                    for i in range(len(name)):
                        name[i] = name[i].capitalize()
                    name = " ".join(name)
                    if name in ["Multiply Easy", "Multiply Medium", "Multiply Hard", "Add Easy", "Add Medium", "Add Hard", "Substract Easy", "Substract Medium", "Substract Hard", "Cash Game", "Divide Easy", "Divide Medium", "Divide Hard"]:
                        name, correct, incorrect, averageTime, rate = StatsDB.statsDB.getData(name) # raw data, proximamente a procesar y presentar de forma adecuada
                        print(f"{Color.YELLOW}{name} Stats\n{Color.GREEN}Correct: {correct}\n{Color.RED}Incorrect: {incorrect}{Color.RESET}\nAverage Time: {averageTime}s\nRate: {rate}%")
                        flag = False
                    else: 
                        print(f"Game names include: 'Multiply' (Easy, Medium, Hard), 'Add' (Easy, Medium, Hard), 'Substract' (Easy, Medium, Hard), , 'Divide' (Easy, Medium, Hard) and 'Cash Game'")
            case 3:
                quit()
        return True # permite que se siga ejecutando el bucle principal

menu = Menu()