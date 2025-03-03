import tkinter as tk
from tkinter import messagebox
from game import TicTacToe
from player import SmartComputerPlayer, HumanPlayer

class TicTacToeGUI:
    def __init__(self):
        self.game = TicTacToe()
        self.x_player = SmartComputerPlayer('X')
        self.o_player = HumanPlayer('O')
        self.current_player = self.x_player  # X starts first

        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        
        # Configure grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create game board buttons
        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                self.root, text=' ', font=('Helvetica', 24), 
                width=4, height=2, relief='flat', bg='#F0F0F0',
                command=lambda idx=i: self.on_human_move(idx)
            )
            row, col = divmod(i, 3)
            btn.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')
            self.buttons.append(btn)
        
        # Status label
        self.status_label = tk.Label(
            self.root, text="X's turn", font=('Helvetica', 12), pady=10
        )
        self.status_label.grid(row=3, column=0, columnspan=3)
        
        # Start first move
        self.root.after(100, self.handle_computer_move)
        self.root.mainloop()

    def handle_computer_move(self):
        if self.game.current_winner or not self.game.empty_squares():
            return
        
        square = self.current_player.get_move(self.game)
        if self.game.make_move(square, self.current_player.letter):
            self.update_board()
            if self.game.current_winner:
                self.end_game(f"{self.current_player.letter} Wins!")
            elif not self.game.empty_squares():
                self.end_game("It's a Tie!")
            else:
                self.current_player = self.o_player
                self.status_label.config(text="O's Turn")
                self.toggle_buttons(True)

    def on_human_move(self, square):
        if self.current_player != self.o_player or self.game.board[square] != ' ':
            return
        
        if self.game.make_move(square, self.o_player.letter):
            self.update_board()
            if self.game.current_winner:
                self.end_game(f"{self.o_player.letter} Wins!")
            elif not self.game.empty_squares():
                self.end_game("It's a Tie!")
            else:
                self.current_player = self.x_player
                self.status_label.config(text="X's Turn")
                self.toggle_buttons(False)
                self.root.after(800, self.handle_computer_move)

    def update_board(self):
        for idx, cell in enumerate(self.game.board):
            color = '#333' if cell == 'X' else '#E74C3C'
            self.buttons[idx].config(
                text=cell, 
                fg=color,
                state=tk.DISABLED if cell != ' ' else tk.NORMAL
            )

    def toggle_buttons(self, enable):
        state = tk.NORMAL if enable else tk.DISABLED
        for idx in self.game.available_moves():
            self.buttons[idx].config(state=state)

    def end_game(self, message):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        self.status_label.config(text=message)
        messagebox.showinfo("Game Over", message)
        self.root.after(2000, self.root.destroy)

if __name__ == "__main__":
    TicTacToeGUI()