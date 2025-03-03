import tkinter as tk
from tkinter import font, messagebox
from game import TicTacToe
from player import SmartComputerPlayer, HumanPlayer
import time

class DarkTicTacToe:
    def __init__(self):
        self.game = TicTacToe()
        self.x_player = SmartComputerPlayer('X')
        self.o_player = HumanPlayer('O')
        self.current_player = self.x_player
        self.animation_running = False
        self.animation_step = 0
        
        # Main window setup
        self.root = tk.Tk()
        self.root.title("CyberTac")
        self.root.configure(bg='#1a1a1a')
        self.root.resizable(False, False)
        
        # Custom fonts
        self.bold_font = font.Font(family='Segoe UI', size=14, weight='bold')
        self.symbol_font = font.Font(family='Segoe UI', size=32, weight='bold')
        
        # Create UI elements
        self.create_header()
        self.create_board()
        self.create_status_bar()
        
        # Start first move
        self.root.after(500, self.handle_computer_move)
        self.root.mainloop()

    def create_header(self):
        header_frame = tk.Frame(self.root, bg='#1a1a1a', pady=10)
        header_frame.pack(fill='x')
        
        self.title_label = tk.Label(
            header_frame,
            text="CYBERTAC",
            font=('Segoe UI', 24, 'bold'),
            fg='#00ff9d',
            bg='#1a1a1a'
        )
        self.title_label.pack()

    def create_board(self):
        board_frame = tk.Frame(self.root, bg='#2d2d2d', padx=10, pady=10)
        board_frame.pack()
        
        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                board_frame,
                text=' ', 
                font=self.symbol_font,
                width=2,
                height=1,
                relief='flat',
                bg='#2d2d2d',
                fg='white',
                activebackground='#3d3d3d',
                borderwidth=4,
                command=lambda idx=i: self.on_human_move(idx)
            )
            btn.grid(
                row=i//3,
                column=i%3,
                padx=5,
                pady=5,
                sticky='nsew'
            )
            self.buttons.append(btn)
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: self.on_hover(e, b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_leave(e, b))

    def create_status_bar(self):
        status_frame = tk.Frame(self.root, bg='#1a1a1a', pady=10)
        status_frame.pack(fill='x')
        
        self.status_label = tk.Label(
            status_frame,
            text="AI is thinking...",
            font=self.bold_font,
            fg='#00ff9d',
            bg='#1a1a1a'
        )
        self.status_label.pack()
        
        self.thinking_dots = tk.Label(
            status_frame,
            text="",
            font=self.bold_font,
            fg='#00ff9d',
            bg='#1a1a1a'
        )
        self.thinking_dots.pack()

    def on_hover(self, event, button):
        if button['state'] == 'normal':
            button['bg'] = '#3d3d3d'
            button['fg'] = '#00ff9d'

    def on_leave(self, event, button):
        if button['state'] == 'normal':
            button['bg'] = '#2d2d2d'
            button['fg'] = 'white'

    def animate_thinking(self, count=0):
        dots = '.' * (count % 4)
        self.thinking_dots.config(text=dots)
        if not self.game.current_winner and self.current_player == self.x_player:
            self.root.after(500, lambda: self.animate_thinking(count + 1))

    def update_board(self):
        for idx, cell in enumerate(self.game.board):
            color = '#00ff9d' if cell == 'X' else '#ff006e'
            self.buttons[idx].config(
                text=cell,
                fg=color,
                state=tk.DISABLED if cell != ' ' else tk.NORMAL
            )
            if cell == ' ':
                self.buttons[idx].config(bg='#2d2d2d')

    def toggle_buttons(self, enable):
        state = tk.NORMAL if enable else tk.DISABLED
        for idx in self.game.available_moves():
            self.buttons[idx].config(state=state)


    def on_human_move(self, square):
        if self.current_player != self.o_player or self.game.board[square] != ' ':
            return
        
        if self.game.make_move(square, self.o_player.letter):
            self.update_board()
            self.check_game_end()
            
            if not self.game.current_winner and self.game.empty_squares():
                self.current_player = self.x_player
                self.status_label.config(text="AI is thinking")
                self.toggle_buttons(False)
                self.root.after(800, self.handle_computer_move)

    def check_game_end(self):
        if self.game.current_winner:
            self.highlight_winning_line()
            self.end_game(f"{self.game.current_winner} Wins!")
        elif not self.game.empty_squares():
            self.end_game("Cosmic Stalemate!")

    def highlight_winning_line(self):
        if not hasattr(self.game, 'winning_combination') or not self.game.winning_combination:
            return
        
        self.animation_running = True
        self.animation_step = 0
        self.start_winning_animation()

    def start_winning_animation(self):
        if not self.animation_running:
            return
        
        colors = ['#00ff9d', '#1a1a1a'] if self.game.current_winner == 'X' else ['#ff006e', '#1a1a1a']
        current_color = colors[self.animation_step % 2]
        
        for idx in self.game.winning_combination:
            self.buttons[idx].config(bg=current_color)
        
        self.animation_step += 1
        self.root.after(500, self.start_winning_animation)

    def end_game(self, message):
        self.animation_running = False
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        
        self.status_label.config(text=message)
        self.thinking_dots.config(text="")
        
        # Reset winning combination colors
        if hasattr(self.game, 'winning_combination'):
            for idx in self.game.winning_combination:
                self.buttons[idx].config(bg='#2d2d2d')
        
        self.root.after(1000, self.show_game_over, message)

    def show_game_over(self, message):
        messagebox.showinfo("Game Over", message)
        self.root.destroy()
    
    def handle_computer_move(self):
        if self.game.current_winner or not self.game.empty_squares():
            return

        self.status_label.config(text="AI is thinking")
        self.animate_thinking()
        self.toggle_buttons(False)
        self.root.after(500, self.process_computer_move)

    def process_computer_move(self):
        square = self.current_player.get_move(self.game)
        if self.game.make_move(square, self.current_player.letter):
            self.update_board()
            self.check_game_end()
            if not self.game.current_winner and self.game.empty_squares():
                self.current_player = self.o_player
                self.status_label.config(text="Your Turn")
                self.toggle_buttons(True)
                self.thinking_dots.config(text="")

if __name__ == "__main__":
    DarkTicTacToe()