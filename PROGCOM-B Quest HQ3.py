import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe - Tres en Raya")
        self.root.geometry("300x350")
        
        # Tablero: 3x3, None = vacío, 'X' = jugador, 'O' = máquina
        self.board = [[None for _ in range(3)] for _ in range(3)]
        
        # Turno actual: True = jugador, False = máquina
        self.player_turn = True
        
        # Crear botones
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(self.root, text="", font=("Arial", 20), width=5, height=2,
                                command=lambda row=i, col=j: self.player_move(row, col))
                btn.grid(row=i, column=j, padx=1, pady=1)
                row.append(btn)
            self.buttons.append(row)
        
        # Botón para reiniciar
        restart_btn = tk.Button(self.root, text="Reiniciar Juego", command=self.restart_game,
                                font=("Arial", 12), bg="lightblue")
        restart_btn.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Etiqueta de turno
        self.turn_label = tk.Label(self.root, text="Tu turno (X)", font=("Arial", 14))
        self.turn_label.grid(row=4, column=0, columnspan=3)
        
        # Iniciar el juego
        self.root.mainloop()
    
    def player_move(self, row, col):
        if self.board[row][col] is not None or not self.player_turn:
            return  # Posición ocupada o no es turno del jugador
        
        # Colocar X
        self.board[row][col] = 'X'
        self.buttons[row][col].config(text='X', state='disabled')
        
        # Verificar victoria o empate
        if self.check_winner('X'):
            messagebox.showinfo("¡Ganaste!", "¡Felicidades! Ganaste con X.")
            self.end_game()
            return
        if self.is_board_full():
            messagebox.showinfo("Empate", "¡Es un empate!")
            self.end_game()
            return
        
        # Cambiar turno
        self.player_turn = False
        self.turn_label.config(text="Turno de la máquina (O)")
        
        # Hacer movimiento de la máquina
        self.root.after(500, self.machine_move)  # Pequeño delay para simular pensamiento
    
    def machine_move(self):
        best_score = -float('inf')
        best_row, best_col = -1, -1
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is None:
                    self.board[i][j] = 'O'
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = None
                    if score > best_score:
                        best_score = score
                        best_row, best_col = i, j
        
        if best_row != -1 and best_col != -1:
            self.board[best_row][best_col] = 'O'
            self.buttons[best_row][best_col].config(text='O', state='disabled')
            
            if self.check_winner('O'):
                messagebox.showinfo("¡Perdiste!", "La máquina ganó con O. ¡Inténtalo de nuevo!")
                self.end_game()
                return
            if self.is_board_full():
                messagebox.showinfo("Empate", "¡Es un empate!")
                self.end_game()
                return
        
        # Cambiar turno de vuelta
        self.player_turn = True
        self.turn_label.config(text="Tu turno (X)")
    
    def minimax(self, board, depth, is_maximizing):
        # Terminal: alguien ganó
        if self.check_winner('X'):
            return -1  # Máquina pierde
        if self.check_winner('O'):
            return 1   # Máquina gana
        
        if self.is_board_full():
            return 0    # Empate
        
        if is_maximizing:  # Turno de máquina (maximizar)
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = 'O'
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = None
                        best_score = max(score, best_score)
            return best_score
        else:  # Turno del jugador (minimizar)
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = 'X'
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = None
                        best_score = min(score, best_score)
            return best_score
    
    def check_winner(self, player):
        # Filas, columnas y diagonales
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2-i] == player for i in range(3)):
            return True
        return False
    
    def is_board_full(self):
        return all(all(cell is not None for cell in row) for row in self.board)
    
    def end_game(self):
        self.player_turn = False  # Bloquear más movimientos
        for row in self.buttons:
            for btn in row:
                btn.config(state='disabled')
    
    def restart_game(self):
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.player_turn = True
        self.turn_label.config(text="Tu turno (X)")
        for row in self.buttons:
            for btn in row:
                btn.config(text="", state='normal')

# Ejecutar el juego
if __name__ == "__main__":
    game = TicTacToe()
