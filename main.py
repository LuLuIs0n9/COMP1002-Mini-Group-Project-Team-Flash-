import pickle

class HouseGame:
    def __init__(self, size=5):
        self.size = size
        self.house_map = [[' ' for _ in range(size)] for _ in range(size)]
        self.thief_position = (0, 0)
        self.police_positions = [(size-1, size-1), (size-1, size-2), (size-1, size-3)]
        self.exit_position = (size-1, 0)
        self.load_game_stats()
        self.selected_police = None

    def print_map(self):
        for row in self.house_map:
            print(' '.join(row))
        print()

    def move_police(self, index, direction):
        movements = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
        x, y = self.police_positions[index]
        move = movements.get(direction)
        if move:
            new_x, new_y = x + move[0], y + move[1]
            if 0 <= new_x < self.size and 0 <= new_y < self.size and self.house_map[new_x][new_y] == ' ':
                self.police_positions[index] = (new_x, new_y)

    def move_thief(self, direction):
        movements = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
        x, y = self.thief_position
        move = movements.get(direction)
        if move:
            new_x, new_y = x + move[0], y + move[1]
            if 0 <= new_x < self.size and 0 <= new_y < self.size and self.house_map[new_x][new_y] == ' ':
                self.thief_position = (new_x, new_y)

    def check_valid_move(self, position):
        x, y = position
        return 0 <= x < self.size and 0 <= y < self.size and self.house_map[x][y] == ' '

    def check_game_over(self):
        if self.thief_position == self.exit_position:
            print("Thief wins! Police lose!")
            self.wins += 1
            self.save_game_stats()
            return True
        elif all(not self.check_valid_move(pos) for pos in self.police_positions):
            print("Police win! Thief caught!")
            self.losses += 1
            self.save_game_stats()
            return True
        return False

    def play(self):
        while True:
            self.house_map = [[' ' for _ in range(self.size)] for _ in range(self.size)]
            self.house_map[self.thief_position[0]][self.thief_position[1]] = 'T'
            for i, pos in enumerate(self.police_positions):
                self.house_map[pos[0]][pos[1]] = chr(ord('A') + i)

            self.print_map()

            self.selected_police = input("Choose a police officer to move (A, B, C): ")
            index = ord(self.selected_police.upper()) - ord('A')
            if 0 <= index < len(self.police_positions):
                self.move_police(index, input(f"Move police {self.selected_police} (up, down, left, right): "))
                if self.check_game_over():
                    return

                self.move_thief(input("Move thief (up, down, left, right): "))
                if self.check_game_over():
                    return
            else:
                print("Please enter a valid police officer!!")

    def load_game_stats(self):
        try:
            with open('game_stats.pkl', 'rb') as file:
                stats = pickle.load(file)
                self.wins = stats.get('wins', 0)
                self.losses = stats.get('losses', 0)
        except FileNotFoundError:
            self.wins = 0
            self.losses = 0

    def save_game_stats(self):
        with open('game_stats.pkl', 'wb') as file:
            stats = {'wins': self.wins, 'losses': self.losses}
            pickle.dump(stats, file)

if __name__ == "__main__":
    game = HouseGame()
    game.play()