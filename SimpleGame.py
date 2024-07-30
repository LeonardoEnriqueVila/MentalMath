import random
import time
import Color
import StatsDB

class SimpleGame():
    def __init__(self, operationSign):
        # stats del juego
        self.first = True
        self.easyStats = [0, 0, 0, 0] # correct, incorrect, average, rate
        self.mediumStats = [0, 0, 0, 0]
        self.hardStats = [0, 0, 0, 0]
        self.operationSign = operationSign # determina el operador matematico del juego
        self.difficulty = ""
        # quizas se podria mostrar stats generales y de la partida actual por separado
        self.times = {
            "multiplyEasy": 0,
            "multiplyMedium": 0,
            "multiplyHard": 0,
            "addEasy": 0,
            "addMedium": 0,
            "addHard": 0,
            "substractEasy": 0,
            "substractMedium": 0,
            "substractHard": 0,
            "divideEasy": 0,
            "divideMedium": 0,
            "dividetHard": 0,
        }
        self.gameMode = ""
        self.name = ""

    def operation(self, inputNumber, number1, number2):
        flag = False
        match self.operationSign:
            case "*":
                flag = True if inputNumber == number1 * number2 else False
            case "/":
                flag = True if inputNumber == number1 / number2 else False
            case "+":
                flag = True if inputNumber == number1 + number2 else False
            case "-":
                flag = True if inputNumber == number1 - number2 else False
        self.processOperation(flag)
        return flag

    def processOperation(self, flag):
        if flag:
            print(f"{Color.GREEN}YES!{Color.RESET}")
        else:
            print(f"{Color.RED}NO!{Color.RESET}")
        match self.difficulty:
            case "Easy":
                if flag:
                    self.easyStats[0] += 1
                else:
                    self.easyStats[1] += 1
            case "Medium":
                if flag:
                    self.mediumStats[0] += 1
                else:
                    self.mediumStats[1] += 1
            case "Hard":
                if flag:
                    self.hardStats[0] += 1
                else:
                    self.hardStats[1] += 1

    def setOperands(self):
        match self.difficulty:
            case "Easy":
                return (random.randint(2,20), random.randint(2,20))
            case "Medium":
                return (random.randint(2,100), random.randint(2,100))
            case "Hard":
                return (random.randint(2,1000), random.randint(2,1000))

    def play(self):
        print(f"{Color.ORANGE}Enter -1 to stop this game, 'p' to pause it.{Color.RESET}")
        flag = False # permite evitar que se lance una nueva operacion si el input es invalido (si se da el except)
        repeat = True # asegura que la resta no de negativa 
        firstOperation = True # asegura que inputs incorrectos o invalidos no reseteen el timer
        while True:
            if flag == False:
                repeat = True
                while repeat == True: # se repite cuando en la resta el segundo nro es mayor que el primero
                    numbers = self.setOperands()
                    if self.operationSign == "-":
                        if numbers[1] < numbers[0]:
                            repeat = False
                    elif self.operationSign == "/":
                        if (numbers[1] < numbers[0]) and (numbers[0] % numbers[1] == 0): 
                            repeat = False
                    else:
                        repeat = False
            else:
                flag = False
            try:
                result = False
                while result == False:
                    pauseStart = 0
                    pauseEnd = 0
                    if firstOperation: # reiniciar el timer solamente si es la primera operacion (evitar reiniciar timer en incorrectas)
                        startTime = time.time() # timer que mide el tiempo de respuesta
                    number = -1
                    while number != "p": # bucle que tiene en cuenta una posible pausa
                        number = input(f"{numbers[0]} {self.operationSign} {numbers[1]}: ")
                        if number != "p":
                            number = int(number) # si la entrada es un numero valido, continuar
                            break
                        elif number == "p":
                            print(f"{Color.YELLOW}GAME PAUSED{Color.RESET}")
                            pauseStart = time.time()
                            stopPause = ""
                            while stopPause != "p": # salir de la pausa
                                stopPause = input(f"{Color.LIGHT_BLUE}Press 'p' to continue: {Color.RESET}")
                                if stopPause == "p":
                                    pauseEnd = time.time()
                                    print(f"{Color.YELLOW}GAME CONTINUES{Color.RESET}")
                                    number = -1 # permite que se vuelva a efectuar el input de numero o pausar nuevamente
                                    
                    if number >= 0: # ALERTA: no permite resta negativa
                        result = self.operation(number, numbers[0], numbers[1])
                        if result:
                            endTime = time.time()
                            timer = (endTime - startTime) - (pauseEnd - pauseStart)
                            print(round(timer, 3))
                            self.times[self.gameMode] += timer # añade el tiempo solamente si el resultado fue correcto
                            firstOperation = True # resetear para la nueva operacion
                        else: # si el resultado es incorrecto
                            firstOperation = False
                    else: 
                        firstOperation = True # resetear antes de terminar juego
                        return # termina el juego si se ingresa un numero negativo
            except ValueError:
                firstOperation = False
                print(f"{Color.RED}Enter a valid option.{Color.RESET}")
                flag = True

    def setDificulty(self):
        while True:
            dificulty = input(f"{Color.LIGHT_BLUE}Set Dificulty ('Easy', 'Medium', 'Hard'): {Color.RESET}").capitalize()
            if dificulty in ["Easy", "Medium", "Hard"]:
                self.difficulty = dificulty
                print(f"{Color.YELLOW}Picked {self.difficulty} Mode!{Color.RESET}")
                return
    
    def setGameMode(self):
        gameMode = self.operationSign + self.difficulty # mediante concatenacion se obtiene valor para match
        match gameMode: # settear el valor self.gameMode permite acceder al dict "times" que guarda los tiempos de cada modo
            case "*Easy":
                self.gameMode = "multiplyEasy"
                self.name = "Multiply Easy"
            case "*Medium":
                self.gameMode = "multiplyMedium"
                self.name = "Multiply Medium"
            case "*Hard":
                self.gameMode = "multiplyHard"
                self.name = "Multiply Hard"
            case "+Easy":
                self.gameMode = "addEasy"
                self.name = "Add Easy"
            case "+Medium":
                self.gameMode = "addMedium"
                self.name = "Add Medium"
            case "+Hard":
                self.gameMode = "addHard"
                self.name = "Add Hard"
            case "-Easy":
                self.gameMode = "substractEasy"
                self.name = "Substract Easy"
            case "-Medium":
                self.gameMode = "substractMedium"
                self.name = "Substract Medium"
            case "-Hard":
                self.gameMode = "substractHard"
                self.name = "Substract Hard"
            case "/Easy":
                self.gameMode = "divideEasy"
                self.name = "Divide Easy"
            case "/Medium":
                self.gameMode = "divideMedium"
                self.name = "Divide Medium"
            case "/Hard":
                self.gameMode = "divideHard"
                self.name = "Divide Hard"
                
    def startGame(self): # maneja el flujo
        self.setDificulty()
        self.setGameMode()
        print(f"{Color.MAGENTA}Welcome to: {self.name}{Color.RESET}")
        self.play()
        self.calculateStats()

    def calculateStats(self):
        match self.difficulty:
            case "Easy":
                self.getStats(self.easyStats)
            case "Medium":
                self.getStats(self.mediumStats)
            case "Hard":
                self.getStats(self.hardStats)

    def getStats(self, statsList): # se le pasa la dificultad para evitar copiar y pegar 3 veces con variacion
        try:
            newAverage = round(self.times[self.gameMode] / statsList[0], 3)
            newRate = round(statsList[0] * 100 / (statsList[0] + statsList[1]), 3) # porcentaje de correcto
            # informar si se superaron los stats anteriores
            if newAverage < statsList[2]:
                print(f"{Color.GREEN}New Average Time Record! -> {newAverage}s ({(statsList[2] - newAverage):.3f}s less!){Color.RESET}")
            if newRate > statsList[3] and self.first == False:
                print(f"{Color.GREEN}New Rate Record! -> {newRate}% (Up {newRate - statsList[3]:.3f}%!){Color.RESET}")
            if self.first:
                self.first = False
            statsList[2] = newAverage
            statsList[3] = newRate
            # mostrar stats
            print(f"{Color.YELLOW}Game Mode: {self.name}\n{Color.GREEN}Correct: {statsList[0]}\n{Color.RED}Incorrect: {statsList[1]}{Color.RESET}\nAverage Time: {statsList[2]}s\nRate: {statsList[3]}%")
            # Actualizar base de datos
            StatsDB.statsDB.updateDB(self.name, statsList[0], statsList[1], statsList[2], statsList[3])
                    
        except ZeroDivisionError:
            print("No records yet!")
        
multiplyGame = SimpleGame("*")
addGame = SimpleGame("+")
substractGame = SimpleGame("-")
divideGame = SimpleGame("/")