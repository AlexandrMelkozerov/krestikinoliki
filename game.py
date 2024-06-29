import tkinter as tk
from tkinter import messagebox, colorchooser
import json
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.score = {'X': 0, 'O': 0}
        self.single_player = False
        self.difficulty = "Easy"
        self.history = []
        self.theme = {"bg": "white", "fg": "black"}
        self.load_settings()
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Выберите режим игры", font='normal 20 bold', bg=self.theme["bg"], fg=self.theme["fg"])
        self.label.grid(row=0, column=0, columnspan=3)

        self.single_player_button = tk.Button(self.root, text="Один игрок", font='normal 15 bold', command=lambda: self.start_game(single_player=True), bg=self.theme["bg"], fg=self.theme["fg"])
        self.single_player_button.grid(row=1, column=0, columnspan=3)

        self.two_player_button = tk.Button(self.root, text="Два игрока", font='normal 15 bold', command=lambda: self.start_game(single_player=False), bg=self.theme["bg"], fg=self.theme["fg"])
        self.two_player_button.grid(row=2, column=0, columnspan=3)

        self.settings_button = tk.Button(self.root, text="Настройки", font='normal 15 bold', command=self.open_settings, bg=self.theme["bg"], fg=self.theme["fg"])
        self.settings_button.grid(row=5, column=0, columnspan=3)

        self.about_button = tk.Button(self.root, text="О программе", font='normal 15 bold', command=self.show_about, bg=self.theme["bg"], fg=self.theme["fg"])
        self.about_button.grid(row=6, column=0, columnspan=3)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        messagebox.showinfo("Выбор сложности", f"Вы выбрали уровень сложности: {difficulty}")

    def start_game(self, single_player):
        self.single_player = single_player
        self.label.config(text=f"Игрок {self.current_player} начинает")
        self.single_player_button.grid_forget()
        self.two_player_button.grid_forget()
        self.create_board()
        self.create_score_and_reset()

    def create_board(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.root, text=' ', font='normal 20 bold', height=2, width=5, command=lambda row=row, col=col: self.on_button_click(row, col), bg=self.theme["bg"], fg=self.theme["fg"])
                button.grid(row=row + 1, column=col)
                self.buttons[row][col] = button

    def create_score_and_reset(self):
        self.score_label = tk.Label(self.root, text=self.get_score_text(), font='normal 15 bold', bg=self.theme["bg"], fg=self.theme["fg"])
        self.score_label.grid(row=5, column=0, columnspan=3)

        self.save_button = tk.Button(self.root, text="Сохранить игру", font='normal 15 bold', command=self.save_game, bg=self.theme["bg"], fg=self.theme["fg"])
        self.save_button.grid(row=6, column=0)

        self.load_button = tk.Button(self.root, text="Загрузить игру", font='normal 15 bold', command=self.load_game, bg=self.theme["bg"], fg=self.theme["fg"])
        self.load_button.grid(row=6, column=1)

        self.reset_button = tk.Button(self.root, text="Сбросить игру", font='normal 15 bold', command=self.reset_board, bg=self.theme["bg"], fg=self.theme["fg"])
        self.reset_button.grid(row=6, column=2)

        self.history_button = tk.Button(self.root, text="История ходов", font='normal 15 bold', command=self.show_history, bg=self.theme["bg"], fg=self.theme["fg"])
        self.history_button.grid(row=7, column=0, columnspan=3)

    def get_score_text(self):
        return f"Счёт: Игрок X - {self.score['X']} | Игрок O - {self.score['O']}"

    def on_button_click(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            self.history.append((self.current_player, row, col))
            if self.check_winner(self.current_player):
                messagebox.showinfo("Победа!", f"Игрок {self.current_player} победил!")
                self.score[self.current_player] += 1
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Ничья", "Игра окончилась вничью!")
                self.reset_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.label.config(text=f"Ход игрока {self.current_player}")
                if self.single_player and self.current_player == 'O':
                    self.computer_move()

    def computer_move(self):
        if self.difficulty == "Easy":
            empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ' ']
            if empty_cells:
                row, col = random.choice(empty_cells)
                self.on_button_click(row, col)
        elif self.difficulty == "Hard":
            best_score = -float('inf')
            best_move = None
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] == ' ':
                        self.board[r][c] = 'O'
                        score = self.minimax(self.board, 0, False)
                        self.board[r][c] = ' '
                        if score > best_score:
                            best_score = score
                            best_move = (r, c)
            if best_move:
                self.on_button_click(best_move[0], best_move[1])

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner('O'):
            return 1
        elif self.check_winner('X'):
            return -1
        elif self.check_draw():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == ' ':
                        board[r][c] = 'O'
                        score = self.minimax(board, depth + 1, False)
                        board[r][c] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == ' ':
                        board[r][c] = 'X'
                        score = self.minimax(board, depth + 1, True)
                        board[r][c] = ' '
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        for row in self.board:
            if all(s == player for s in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2-i] == player for i in range(3)):
            return True
        return False

    def check_draw(self):
        return all(all(cell != ' ' for cell in row) for row in self.board)

    def reset_board(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.history = []
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text=' ')
        self.label.config(text=f"Ход игрока {self.current_player}")
        self.score_label.config(text=self.get_score_text())

    def save_game(self):
        with open("tic_tac_toe_save.json", "w") as file:
            json.dump({
                'board': self.board,
                'current_player': self.current_player,
                'score': self.score,
                'single_player': self.single_player,
                'difficulty': self.difficulty,
                'history': self.history,
                'theme': self.theme
            }, file)
        messagebox.showinfo("Сохранение игры", "Игра успешно сохранена!")

    def load_game(self):
        try:
            with open("tic_tac_toe_save.json", "r") as file:
                data = json.load(file)
                self.board = data['board']
                self.current_player = data['current_player']
                self.score = data['score']
                self.single_player = data['single_player']
                self.difficulty = data['difficulty']
                self.history = data['history']
                self.theme = data.get('theme', {"bg": "white", "fg": "black"})
                for row in range(3):
                    for col in range(3):
                        self.buttons[row][col].config(text=self.board[row][col], bg=self.theme["bg"], fg=self.theme["fg"])
                self.label.config(text=f"Ход игрока {self.current_player}", bg=self.theme["bg"], fg=self.theme["fg"])
                self.score_label.config(text=self.get_score_text(), bg=self.theme["bg"], fg=self.theme["fg"])
            messagebox.showinfo("Загрузка игры", "Игра успешно загружена!")
        except FileNotFoundError:
            messagebox.showwarning("Загрузка игры", "Сохранённая игра не найдена!")

    def show_history(self):
        history_text = "\n".join([f"{i+1}. Игрок {move[0]}: ({move[1]}, {move[2]})" for i, move in enumerate(self.history)])
        messagebox.showinfo("История ходов", history_text if history_text else "Нет истории ходов")

    def open_settings(self):
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Настройки")
        self.settings_window.geometry("300x200")

        self.theme_button = tk.Button(self.settings_window, text="Выбрать тему", font='normal 15 bold', command=self.choose_theme)
        self.theme_button.pack(pady=20)

        self.difficulty_label = tk.Label(self.settings_window, text="Выберите уровень сложности", font='normal 15 bold')
        self.difficulty_label.pack()

        self.easy_button = tk.Button(self.settings_window, text="Легкий", font='normal 15 bold', command=lambda: self.set_difficulty("Easy"))
        self.easy_button.pack(pady=5)

        self.hard_button = tk.Button(self.settings_window, text="Сложный", font='normal 15 bold', command=lambda: self.set_difficulty("Hard"))
        self.hard_button.pack(pady=5)

        # Load current difficulty setting
        current_difficulty_label = tk.Label(self.settings_window, text=f"Текущий уровень сложности: {self.difficulty}", font='normal 12')
        current_difficulty_label.pack(pady=10)

    def choose_theme(self):
        bg_color = colorchooser.askcolor(title="Выберите цвет фона")[1]
        fg_color = colorchooser.askcolor(title="Выберите цвет текста")[1]
        if bg_color and fg_color:
            self.theme = {"bg": bg_color, "fg": fg_color}
            self.apply_theme()

    def apply_theme(self):
        self.root.config(bg=self.theme["bg"])
        self.label.config(bg=self.theme["bg"], fg=self.theme["fg"])
        self.single_player_button.config(bg=self.theme["bg"], fg=self.theme["fg"])
        self.two_player_button.config(bg=self.theme["bg"], fg=self.theme["fg"])
        self.settings_button.config(bg=self.theme["bg"], fg=self.theme["fg"])
        self.about_button.config(bg=self.theme["bg"], fg=self.theme["fg"])
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(bg=self.theme["bg"], fg=self.theme["fg"])
        self.score_label.config(bg=self.theme["bg"], fg=self.theme["fg"])
        self.save_button.config(bg=self.theme["bg"], fg=self.theme["fg"])
        self.load_button.config(bg=self.theme["bg"], fg=self.theme["fg"])
        self.reset_button.config(bg=self.theme["bg"], fg=self.theme["fg"])
        self.history_button.config(bg=self.theme["bg"], fg=self.theme["fg"])

    def load_settings(self):
        try:
            with open("tic_tac_toe_settings.json", "r") as file:
                settings = json.load(file)
                self.difficulty = settings.get('difficulty', 'Easy')
                self.theme = settings.get('theme', {"bg": "white", "fg": "black"})
        except FileNotFoundError:
            pass

    def save_settings(self):
        with open("tic_tac_toe_settings.json", "w") as file:
            json.dump({'difficulty': self.difficulty, 'theme': self.theme}, file)

    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("О программе")
        about_window.geometry("600x400")

        about_label = tk.Label(about_window, text="Курсовой проект по крестикам-ноликам\nАвторы:\n Мелкозеров А.Ю.\nДубовицкий Д.А.\nРИВ-220906у", font='normal 15 bold')
        about_label.pack(pady=20)

    def on_closing(self):
        self.save_settings()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.protocol("WM_DELETE_WINDOW", game.on_closing)
    root.mainloop()