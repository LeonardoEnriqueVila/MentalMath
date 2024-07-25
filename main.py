import SimpleGame
import CashGame
import Color

class Menu():
    def __init__(self):
        self.state = False
        self.mainMenuMessage = f"{Color.YELLOW}Main Menu{Color.RESET}\n1. Play Game\n2. Show Stats\n3. Quit\n{Color.LIGHT_BLUE}Select an Option:{Color.RESET} "
        self.gameMenuMessage = f"{Color.YELLOW}Game Menu{Color.RESET}\n1. Multiply!\n2. Add!\n3. Substract!\n4. Cash Game!\n5. Go Back.\n{Color.LIGHT_BLUE}Select an Option:{Color.RESET} "
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
                while gameOption != 5:
                    gameOption = self.getOption([1, 2, 3, 4, 5], self.gameMenuMessage) # menu de juegos
                    if gameOption == 1:
                        SimpleGame.multiplyGame.startGame() 
                    elif gameOption == 2:
                        SimpleGame.addGame.startGame()
                    elif gameOption == 3:
                        SimpleGame.substractGame.startGame()
                    elif gameOption == 4:
                        CashGame.cashGame.startGame()
            case 2:
                print("Show Stats Placeholder") # quizas no se quede aca esto
            case 3:
                quit()
        return True # permite que se siga ejecutando el bucle principal

menu = Menu()