import random
import time
import Color
import StatsDB

class CashGame():
    def __init__(self):
        self.Stats = [0, 0, 0, 0] # correct, incorrect, average, rate, first
        self.times = 0
        self.name = "Cash Game"
        self.initializeStatsFromDB()
    
    def initializeStatsFromDB(self):
        name, self.Stats[0], self.Stats[1], self.Stats[2], self.Stats[3], self.times = StatsDB.statsDB.getData("Cash Game")

    def play(self):
        print(f"{Color.ORANGE}Enter -1 to stop this game, 'p' to pause it.{Color.RESET}")
        flag = False # permite evitar que se lance una nueva operacion si el input es invalido (si se da el except)
        firstOperation = True # asegura que inputs incorrectos o invalidos no reseteen el timer
        while True:
            if flag == False:
                total, pays = self.setOperands()
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
                        number = input(f"Total: {total}, pays: {pays}: ")
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
                        result = self.operation(number, pays - total)
                        if result:
                            endTime = time.time()
                            timer = (endTime - startTime) - (pauseEnd - pauseStart)
                            print(round(timer, 3))
                            self.times += timer # añade el tiempo solamente si el resultado fue correcto
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

    def operation(self, input, difference):
        flag = True if input == difference else False
        if flag:
            print(f"{Color.GREEN}YES!{Color.RESET}")
            self.Stats[0] += 1
        else:
            print(f"{Color.RED}NO!{Color.RESET}")
            self.Stats[1] += 1
        return flag
        
    def setOperands(self):
        total = random.randint(200, 80000) # el total de la compra
        operationStep = random.choice([10, 100, 1000, 10000])
        pays = 0
        operation = 0
        while True:
            if total < operation + 100:
                pays = random.choice([100, 200, 500, 1000, 2000, 10000]) + operation
            elif total < operation + 200:
                pays = random.choice([200, 500, 1000, 2000, 10000]) + operation
            elif total < operation + 500:
                pays = random.choice([500, 1000, 2000, 10000]) + operation
            elif total < operation + 1000:
                pays = random.choice([1000, 2000, 10000]) + operation
            elif total < operation + 2000:
                pays = random.choice([2000, 10000]) + operation
            elif total < operation + 10000:
                pays = random.choice([10000]) + operation
            if pays >= total:
                break
            operation += operationStep
        return total, pays
    
    def calculateStats(self): # se le pasa la dificultad para evitar copiar y pegar 3 veces con variacion
        try:
            newAverage = round(self.times / self.Stats[0], 3)
            newRate = round(self.Stats[0] * 100 / (self.Stats[0] + self.Stats[1]), 3) # porcentaje de correcto
            # informar si se superaron los stats anteriores
            if newAverage < self.Stats[2]:
                print(f"{Color.GREEN}Better Average Time Than Last Record! -> {newAverage}s ({(self.Stats[2] - newAverage):.3f}s less!){Color.RESET}")
            if newRate > self.Stats[3] and self.Stats[3] != 0:
                print(f"{Color.GREEN}Better Rate Than Last Record! -> {newRate}% (Up {newRate - self.Stats[3]:.3f}%!){Color.RESET}")
            self.Stats[2] = newAverage
            self.Stats[3] = newRate
            # mostrar stats
            print(f"{Color.YELLOW}Game Mode: {self.name}\n{Color.GREEN}Correct: {self.Stats[0]}\n{Color.RED}Incorrect: {self.Stats[1]}{Color.RESET}\nAverage Time: {self.Stats[2]}s\nRate: {self.Stats[3]}%")
            StatsDB.statsDB.updateDB(self.name, self.Stats[0], self.Stats[1], self.Stats[2], self.Stats[3], self.times)
        except ZeroDivisionError:
            print("No records yet!")

    def startGame(self): # maneja el flujo
        print(f"{Color.MAGENTA}Welcome to: {self.name}{Color.RESET}")
        self.play()
        self.calculateStats()

cashGame = CashGame()