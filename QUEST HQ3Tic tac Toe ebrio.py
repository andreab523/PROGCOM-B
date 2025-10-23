import tkinter as tk
from tkinter import messagebox
import random

# Función para rotar el tablero 90 grados en sentido horario (solo para Modo Ebrio)
def rotar_tablero(tablero):
    return [list(reversed(col)) for col in zip(*tablero)]

# Función para verificar si hay un ganador
def verificar_ganador(tablero):
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] != ' ':
            return tablero[i][0]
        if tablero[0][i] == tablero[1][i] == tablero[2][i] != ' ':
            return tablero[0][i]
    if tablero[0][0] == tablero[1][1] == tablero[2][2] != ' ':
        return tablero[0][0]
    if tablero[0][2] == tablero[1][1] == tablero[2][0] != ' ':
        return tablero[0][2]
    return None

# Función para verificar si el tablero está lleno
def tablero_lleno(tablero):
    return all(c != ' ' for fila in tablero for c in fila)

# Algoritmo Minimax para la IA
def minimax(tablero, profundidad, es_maximizador, simbolo_ia):
    simbolo_jugador = 'X' if simbolo_ia == 'O' else 'O'
    ganador = verificar_ganador(tablero)
    if ganador == simbolo_ia:
        return 1
    elif ganador == simbolo_jugador:
        return -1
    elif tablero_lleno(tablero):
        return 0
    
    if es_maximizador:
        max_eval = -float('inf')
        for i in range(3):
            for j in range(3):
                if tablero[i][j] == ' ':
                    tablero[i][j] = simbolo_ia
                    eval = minimax(tablero, profundidad + 1, False, simbolo_ia)
                    tablero[i][j] = ' '
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if tablero[i][j] == ' ':
                    tablero[i][j] = simbolo_jugador
                    eval = minimax(tablero, profundidad + 1, True, simbolo_ia)
                    tablero[i][j] = ' '
                    min_eval = min(min_eval, eval)
        return min_eval

# Función para el mejor movimiento de la IA
def mejor_movimiento(tablero, simbolo_ia):
    mejor_valor = -float('inf')
    mejor_mov = None
    for i in range(3):
        for j in range(3):
            if tablero[i][j] == ' ':
                tablero[i][j] = simbolo_ia
                valor_mov = minimax(tablero, 0, False, simbolo_ia)
                tablero[i][j] = ' '
                if valor_mov > mejor_valor:
                    mejor_valor = valor_mov
                    mejor_mov = (i, j)
    return mejor_mov

# Función para intercambiar dos casillas aleatorias (solo para Modo Ebrio)
def intercambiar_casillas_aleatorias(tablero):
    casillas_vacias = [(i, j) for i in range(3) for j in range(3) if tablero[i][j] == ' ']
    if len(casillas_vacias) >= 2:
        a, b = random.sample(casillas_vacias, 2)
        tablero[a[0]][a[1]], tablero[b[0]][b[1]] = tablero[b[0]][b[1]], tablero[a[0]][a[1]]

# Clase principal del juego con Tkinter
class TriquiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Triqui: Modo Clásico o Ebrio")
        self.tablero = [[' ' for _ in range(3)] for _ in range(3)]
        self.botones = [[None for _ in range(3)] for _ in range(3)]
        self.simbolo_jugador = None
        self.simbolo_ia = None
        self.modo_ebrio = False  # False = Clásico, True = Ebrio
        self.turno_jugador = False  # IA juega primero
        self.temporizador_activo = False
        self.tiempo_restante = 10
        self.crear_pantalla_inicio()

    def crear_pantalla_inicio(self):
        self.frame_inicio = tk.Frame(self.root)
        self.frame_inicio.pack()
        
        tk.Label(self.frame_inicio, text="Selecciona tu logo (símbolo):", font=("Arial", 14)).pack(pady=10)
        
        frame_simbolos = tk.Frame(self.frame_inicio)
        frame_simbolos.pack()
        tk.Button(frame_simbolos, text="X", font=("Arial", 20), command=lambda: self.seleccionar_simbolo('X')).pack(side=tk.LEFT, padx=20)
        tk.Button(frame_simbolos, text="O", font=("Arial", 20), command=lambda: self.seleccionar_simbolo('O')).pack(side=tk.RIGHT, padx=20)
        
        tk.Label(self.frame_inicio, text="Selecciona el modo:", font=("Arial", 14)).pack(pady=10)
        frame_modos = tk.Frame(self.frame_inicio)
        frame_modos.pack()
        tk.Button(frame_modos, text="Clásico (sin rotación ni caos)", font=("Arial", 12), command=lambda: self.seleccionar_modo(False)).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_modos, text="Ebrio (con rotación y caos)", font=("Arial", 12), command=lambda: self.seleccionar_modo(True)).pack(side=tk.RIGHT, padx=10)

    def seleccionar_simbolo(self, simbolo):
        self.simbolo_jugador = simbolo
        self.simbolo_ia = 'O' if simbolo == 'X' else 'X'

    def seleccionar_modo(self, ebrio):
        if self.simbolo_jugador is None:
            messagebox.showerror("Error", "Primero selecciona tu símbolo.")
            return
        self.modo_ebrio = ebrio
        self.frame_inicio.destroy()
        self.iniciar_juego()

    def iniciar_juego(self):
        self.frame_juego = tk.Frame(self.root)
        self.frame_juego.pack()
        
        self.label_turno = tk.Label(self.frame_juego, text=f"Turno de la IA ({self.simbolo_ia})", font=("Arial", 12))
        self.label_turno.pack(pady=10)
        
        self.label_temporizador = tk.Label(self.frame_juego, text="", font=("Arial", 12))
        self.label_temporizador.pack()
        
        self.frame_tablero = tk.Frame(self.frame_juego)
        self.frame_tablero.pack()
        
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.frame_tablero, text=' ', font=("Arial", 24), width=5, height=2,
                                command=lambda r=i, c=j: self.hacer_movimiento(r, c))
                btn.grid(row=i, column=j)
                self.botones[i][j] = btn
        
        tk.Button(self.frame_juego, text="Reiniciar", command=self.reiniciar_juego).pack(pady=10)
        
        # IA juega primero
        self.jugar_ia()

    def hacer_movimiento(self, fila, col):
        if self.tablero[fila][col] == ' ' and self.turno_jugador and self.temporizador_activo:
            self.detener_temporizador()
            self.tablero[fila][col] = self.simbolo_jugador
            self.actualizar_tablero()
            self.verificar_y_siguiente()

    def jugar_ia(self):
        if not self.turno_jugador:
            mov = mejor_movimiento(self.tablero, self.simbolo_ia)
            if mov:
                self.tablero[mov[0]][mov[1]] = self.simbolo_ia
                self.actualizar_tablero()
                self.verificar_y_siguiente()

    def verificar_y_siguiente(self):
        if self.modo_ebrio:
            self.tablero = rotar_tablero(self.tablero)
            intercambiar_casillas_aleatorias(self.tablero)
            messagebox.showinfo("Modo Ebrio", "Tablero rotado y casillas intercambiadas aleatoriamente!")
        else:
            messagebox.showinfo("Modo Clásico", "Movimiento completado.")
        
        self.actualizar_tablero()
        
        ganador = verificar_ganador(self.tablero)
        if ganador:
            if ganador == self.simbolo_jugador:
                messagebox.showinfo("Resultado", "¡Ganaste!")
            else:
                messagebox.showinfo("Resultado", "La IA ganó. ¡Inténtalo de nuevo!")
            self.deshabilitar_tablero()
        elif tablero_lleno(self.tablero):
            messagebox.showinfo("Resultado", "¡Empate!")
            self.deshabilitar_tablero()
        else:
            self.turno_jugador = not self.turno_jugador
            self.label_turno.config(text=f"Turno de {'ti' if self.turno_jugador else 'la IA'} ({self.simbolo_jugador if self.turno_jugador else self.simbolo_ia})")
            if self.turno_jugador:
                self.iniciar_temporizador()
            else:
                self.root.after(1000, self.jugar_ia)

    def iniciar_temporizador(self):
        self.tiempo_restante = 10
        self.temporizador_activo = True
        self.actualizar_temporizador()

    def actualizar_temporizador(self):
        if self.tiempo_restante > 0 and self.temporizador_activo:
            self.label_temporizador.config(text=f"Tiempo restante: {self.tiempo_restante} segundos")
            self.tiempo_restante -= 1
            self.root.after(1000, self.actualizar_temporizador)
        elif self.temporizador_activo:
            self.detener_temporizador()
            messagebox.showinfo("Tiempo agotado", "¡Perdiste el turno! La IA juega.")
            self.jugar_ia()

    def detener_temporizador(self):
        self.temporizador_activo = False
        self.label_temporizador.config(text="")

    def actualizar_tablero(self):
        for i in range(3):
            for j in range(3):
                self.botones[i][j].config(text=self.tablero[i][j])

    def deshabilitar_tablero(self):
        for fila in self.botones:
            for btn in fila:
                btn.config(state=tk.DISABLED)

    def reiniciar_juego(self):
        self.frame_juego.destroy()
        self.tablero = [[' ' for _ in range(3)] for _ in range(3)]
        self.turno_jugador = False
        self.temporizador_activo = False
        self.simbolo_jugador = None
        self.modo_ebrio = False
        self.crear_pantalla_inicio()

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = TriquiApp(root)
    root.mainloop()
