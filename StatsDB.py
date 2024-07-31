import sqlite3
import datetime

class StatsDB:
    def __init__(self): 
        self.conn = sqlite3.connect('mentalMathDB.sqlite')
        self.cursor = self.conn.cursor()
        self.initializeDB() # inicializar db

    def initializeDB(self):
        names = ["Multiply Easy", "Multiply Medium", "Multiply Hard", "Add Easy", "Add Medium", "Add Hard", "Substract Easy", "Substract Medium", "Substract Hard", "Cash Game", "Divide Easy", "Divide Medium", "Divide Hard"]
        # stats contiene los ultimos datos actualizados, StatsHistory contiene un registro de las actualizaciones
        self.cursor.executescript('''                                         
            CREATE TABLE IF NOT EXISTS Stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            correct INTEGER,
            incorrect INTEGER,
            times INTEGER,
            averageTime REAL,
            rate REAL);
                            
            CREATE TABLE IF NOT EXISTS StatsHistory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_id INTEGER,
            correct INTEGER,
            incorrect INTEGER,
            averageTime REAL,
            rate REAL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (name_id) REFERENCES Stats(id));''')                     

        for name in names:
            self.cursor.execute('''               
                INSERT OR IGNORE INTO Stats (name, correct, incorrect, averageTime, rate, times) VALUES (?, ?, ?, ?, ?, ?)''',              
                (name, 0, 0, 0, 0, 0))

        self.conn.commit()
    
    def updateDB(self, name, correct, incorrect, averageTime, rate, times): # actualizar al hacer click en el checkbox
        # Obtener el id del juego
        self.cursor.execute('SELECT id FROM Stats WHERE name = ? ', (name, ))
        name_id = self.cursor.fetchone()

        # actualizar stats actuales
        self.cursor.execute('''
            UPDATE Stats
            SET correct = ?, incorrect = ?, averageTime = ?, rate = ?, times = ?
            WHERE name = ?''', 
        (correct, incorrect, averageTime, rate, times, name))

        # agregar fila a historial de updates de stats
        self.cursor.execute('''
            INSERT INTO StatsHistory (name_id, correct, incorrect, averageTime, rate, date)
            VALUES (?, ?, ?, ?, ?, ?)''',
            (name_id[0], correct, incorrect, averageTime, rate, datetime.datetime.now()))
        self.conn.commit()

    def getData(self, name): # obtiene los datos de los stats
        self.cursor.execute('''SELECT name, correct, incorrect, averageTime, rate, times FROM Stats
                               WHERE name = ?''', (name, )) 
        return self.cursor.fetchall()[0]

# recordar que la DB tiene que ser cerrada, probablemente eso se haga en main al elegir quit   
statsDB = StatsDB()
