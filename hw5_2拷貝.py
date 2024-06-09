import random


class BoardGame:
    def __init__(self):
        # 初始化遊戲參數
        self.board_length = 30  # 遊戲板長度為 30
        self.board = self.generate_board()  # 生成遊戲板
        self.player_positions = {'A': 0, 'B': 0}  # 玩家初始位置
        self.skip_turn = {'A': False, 'B': False}  # 玩家是否需要跳過回合的標記

    def generate_board(self):
        # 生成遊戲板，懲罰格概率為 30%
        return ['_' if random.random() > 0.3 else 'P' for _ in range(self.board_length)]

    def roll_dice(self):
        # 擲骰子，返回隨機數字 1 到 6
        return random.randint(1, 6)

    def move_player(self, player):
        # 移動玩家的方法
        if self.skip_turn[player]:
            # 如果玩家需要跳過回合
            self.skip_turn[player] = False
            return 0  # 返回移動距離 0

        # 擲骰子，計算新位置
        dice_roll = self.roll_dice()
        new_position = self.player_positions[player] + dice_roll

        if new_position >= self.board_length - 1:
            # 如果新位置超過或等於終點
            move_distance = self.board_length - 1 - self.player_positions[player]
            self.player_positions[player] = self.board_length - 1  # 將玩家位置設置為終點
            return move_distance  # 返回移動距離
        else:
            move_distance = dice_roll  # 移動距離為擲骰子的結果
            self.player_positions[player] = new_position  # 更新玩家位置
            if self.board[new_position] == 'P':
                # 如果新位置是懲罰格
                self.skip_turn[player] = True  # 設置下回合需要跳過
            return move_distance  # 返回移動距離

    def print_board(self, a_move, b_move):
        # 打印遊戲板及玩家移動距離
        display_board = ['_' for _ in range(self.board_length)]

        pos_a = self.player_positions['A']
        pos_b = self.player_positions['B']

        if pos_a == pos_b:
            if self.board[pos_a] == 'P':
                display_board[pos_a] = 'x'  # 兩玩家同一位置且為懲罰格，顯示為 'x'
            else:
                display_board[pos_a] = 'X'  # 兩玩家同一位置且為安全格，顯示為 'X'
        else:
            if self.board[pos_a] == 'P':
                display_board[pos_a] = 'a'  # 玩家 A 的位置為懲罰格，顯示為 'a'
            else:
                display_board[pos_a] = 'A'  # 玩家 A 的位置為安全格，顯示為 'A'

            if self.board[pos_b] == 'P':
                display_board[pos_b] = 'b'  # 玩家 B 的位置為懲罰格，顯示為 'b'
            else:
                display_board[pos_b] = 'B'  # 玩家 B 的位置為安全格，顯示為 'B'

        print(''.join(display_board), f"(A: {a_move}, B: {b_move})")  # 打印遊戲板及移動距離

    def print_hidden_board(self):
        # 打印隱藏的懲罰格
        hidden_board = ['P' if cell == 'P' else '_' for cell in self.board]
        print(''.join(hidden_board))

    def play_game(self):
        # 遊戲主循環
        while True:
            a_move = self.move_player('A')  # 玩家 A 移動
            b_move = self.move_player('B')  # 玩家 B 移動
            self.print_board(a_move, b_move)  # 打印遊戲板及移動距離

            # 如果任一玩家到達終點，結束遊戲
            if self.player_positions['A'] == self.board_length - 1 or self.player_positions[
                'B'] == self.board_length - 1:
                break

        self.print_hidden_board

