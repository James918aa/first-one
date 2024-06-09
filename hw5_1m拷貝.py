import random
import json
import time

class Minesweeper:
    def __init__(self):
        # 初始化遊戲屬性
        self.board_size = 9  # 棋盤大小
        self.num_mines = 10  # 地雷數量
        # 使用 dictionary 來儲存棋盤狀態，鍵為 (row, col) tuple，值為該格子的內容
        self.board = {(row, col): ' ' for row in range(self.board_size) for col in range(self.board_size)}
        self.mines = set()  # 地雷位置集合
        self.flags = set()  # 旗幟位置集合
        self.safe_first_cell = True  # 第一個打開的格子是否安全

    def print_board(self, show_mines=False):
        # 打印棋盤
        print("    a   b   c   d   e   f   g   h   i")
        print("  +---+---+---+---+---+---+---+---+---+")
        for i in range(self.board_size):
            row = [self.board[(i, j)] for j in range(self.board_size)]
            print(f"{i + 1} | {' | '.join(row)} |")
            print("  +---+---+---+---+---+---+---+---+---+")
        if show_mines:
            print("\nMines:")
            for m in self.mines:
                print(f"{chr(m[1] + ord('a'))}{m[0] + 1}", end=", ")
            print("\b\b ")

    def display_instructions(self):
        # 顯示遊戲說明
        print("\nInstructions:")
        print("- Enter 'u' to unfold a cell.")
        print("- Enter 'f' to flag/unflag a cell.")
        print("- Enter 'q' to quit the game.")
        print("- Enter 'help' to display instructions again.")

    def display_remaining_mines(self):
        # 顯示剩餘的地雷數量
        remaining_mines = self.num_mines - len(self.flags)
        print(f"\nRemaining Mines: {remaining_mines}")

    def place_mines(self, first_move):
        # 隨機放置地雷，確保第一步不會踩到地雷
        valid_cells = [(i, j) for i in range(self.board_size) for j in range(self.board_size)]
        valid_cells.remove(first_move)
        self.mines = set(random.sample(valid_cells, self.num_mines))

    def count_adjacent_mines(self, row, col):
        # 計算指定格子周圍的地雷數量
        count = 0
        for i in range(max(0, row - 1), min(row + 2, self.board_size)):
            for j in range(max(0, col - 1), min(col + 2, self.board_size)):
                if (i, j) != (row, col) and (i, j) in self.mines:
                    count += 1
        return count

    def initialize_board(self, first_move):
        # 初始化棋盤，確保第一步安全
        self.place_mines(first_move)
        for i in range(self.board_size):
            for j in range(self.board_size):
                if (i, j) not in self.mines:
                    count = self.count_adjacent_mines(i, j)
                    self.board[(i, j)] = str(count) if count > 0 else ' '

    def unfold_cell(self, cell):
        # 打開指定的格子
        row = int(cell[1]) - 1
        col = ord(cell[0]) - ord('a')
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            print("Invalid cell. Please enter again.")
            return
        if (row, col) in self.flags:
            print("Cannot unfold a flagged cell.")
            return
        if self.safe_first_cell:
            while (row, col) in self.mines or self.board[(row, col)] != ' ':
                self.__init__()
                self.initialize_board((row, col))
        self.safe_first_cell = False

        if (row, col) in self.mines:
            self.board[(row, col)] = 'X'
            self.print_board(show_mines=True)
            print("Game Over! You hit a mine!")
            return False

        if self.board[(row, col)] == ' ':
            self.board[(row, col)] = str(self.count_adjacent_mines(row, col))
            if self.board[(row, col)] == '0':
                for i in range(max(0, row - 1), min(row + 2, self.board_size)):
                    for j in range(max(0, col - 1), min(col + 2, self.board_size)):
                        if (i, j) != (row, col):
                            self.unfold_cell(chr(j + ord('a')) + str(i + 1))
        return True

    def toggle_flag(self, cell):
        # 標記或取消標記指定的格子
        row = int(cell[1]) - 1
        col = ord(cell[0]) - ord('a')
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            print("Invalid cell. Please enter again.")
            return
        if self.board[(row, col)] != ' ' and self.board[(row, col)] != 'F':
            print("Cannot put a flag there.")
            return
        if (row, col) not in self.flags:
            self.flags.add((row, col))
            self.board[(row, col)] = 'F'
        else:
            self.flags.remove((row, col))
            self.board[(row, col)] = ' '

    def check_win(self):
        # 檢查是否獲勝
        for row in range(self.board_size):
            for col in range(self.board_size):
                if (row, col) not in self.mines and self.board[(row, col)] == ' ':
                    return False
        return True

    # 新增的函數
    def save_game(self, filename):
        # 儲存遊戲狀態到文件
        game_data = {
            'board_size': self.board_size,
            'num_mines': self.num_mines,
            'board': {(str(k)): v for k, v in self.board.items()},
            'mines': list(self.mines),
            'flags': list(self.flags),
            'safe_first_cell': self.safe_first_cell
        }
        with open(filename, 'w') as f:
            json.dump(game_data, f)
        print(f"Game saved to {filename}")

    def load_game(self, filename):
        # 從文件讀取遊戲狀態
        try:
            with open(filename, 'r') as f:
                game_data = json.load(f)
            self.board_size = game_data['board_size']
            self.num_mines = game_data['num_mines']
            self.board = {tuple(map(int, k.strip('()').split(','))): v for k, v in game_data['board'].items()}
            self.mines = set(tuple(m) for m in game_data['mines'])
            self.flags = set(tuple(f) for f in game_data['flags'])
            self.safe_first_cell = game_data['safe_first_cell']
            print(f"Game loaded from {filename}")
        except FileNotFoundError:
            print(f"No saved game found with the name {filename}")

    def reset_game(self):
        # 重置遊戲到初始狀態
        self.__init__()
        print("Game has been reset.")

def main():
    import json

    while True:
        game = Minesweeper()
        game.display_instructions()
        game.print_board()
        game.display_remaining_mines()
        first_move = input("\nEnter the cell to unfold (e.g., 'a1'): ")
        game.initialize_board((int(first_move[1]) - 1, ord(first_move[0]) - ord('a')))
        game.print_board()
        game.display_remaining_mines()
        start_time = time.time()
        while True:
            command = input("\nEnter 'u' to unfold, 'f' to flag/unflag, 'q' to quit, 's' to save, 'l' to load, or 'r' to reset: ")
            if command == 'q':
                print("Quitting the game.")
                return
            elif command == 'help':
                game.display_instructions()
                continue
            elif command == 's':
                filename = input("Enter filename to save: ")
                game.save_game(filename)
                continue
            elif command == 'l':
                filename = input("Enter filename to load: ")
                game.load_game(filename)
                game.print_board()
                game.display_remaining_mines()
                continue
            elif command == 'r':
                game.reset_game()
                game.print_board()
                game.display_remaining_mines()
                continue
            cell = input("Enter the cell (e.g., 'a1'): ")
            if not cell[0].isalpha() or not cell[1:].isdigit() or len(cell) != 2:
                print("Invalid cell. Please enter again.")
                continue
            if command == 'u':
                if not game.unfold_cell(cell):
                    print("Game Over! You hit a mine!")
                    break
                game.print_board()
                if game.check_win():
                    end_time = time.time()
                    print("Congratulations! You win!")
                    print(f"Time taken: {end_time - start_time:.2f} seconds")
                    break
                game.display_remaining_mines()
            elif command == 'f':
                game.toggle_flag(cell)
                game.print_board()

if __name__ == "__main__":
    main()
