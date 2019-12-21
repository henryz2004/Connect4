from typing import List


class Board:

    CONTINUE = -1
    STALEMATE = 0
    P_ONE_WIN = 1
    P_TWO_WIN = 2

    def __init__(self):

        self.board = self.col_count = None          # Stop the inspections from complaining
        self.reset()

    @property
    def available_columns(self):

        return [i for i in range(7) if self.col_count[i] < 6]

    @property
    def game_state(self):
        """Returns state representing current game state"""

        # For now, brute force check all the rows, columns, and diagonals
        # Further optimization is needed

        # Check all rows
        for r in range(6):
            for c in range(4):
                section = self.board[r][c:c+4]
                four_in_a_row = self._four_in_a_row(section)
                if four_in_a_row:
                    return four_in_a_row

        # Check all columns
        for c in range(7):
            for r in range(3):
                section = [self.board[i][c] for i in range(r, r+4)]
                four_in_a_row = self._four_in_a_row(section)
                if four_in_a_row:
                    return four_in_a_row

        # Check all diagonals (\) direction
        for r in range(3):
            for c in range(4):
                section = [self.board[r+i][c+i] for i in range(4)]
                four_in_a_row = self._four_in_a_row(section)
                if four_in_a_row:
                    return four_in_a_row

        # Check all diagonals (/) direction
        for r in range(3):
            for c in range(3, 7):
                section = [self.board[r+i][c-i] for i in range(4)]
                four_in_a_row = self._four_in_a_row(section)
                if four_in_a_row:
                    return four_in_a_row

        # If board is full then stalemate
        if len(self.available_columns) == 0:
            return Board.STALEMATE

        return Board.CONTINUE

    def p_one_play(self, column) -> int:

        return self._play(column, 1)

    def p_two_play(self, column) -> int:

        return self._play(column, 2)

    def reset(self):

        self.board = [[0 for j in range(7)] for i in range(6)]
        self.col_count = [0 for i in range(7)]  # Stores the number of pieces in each column

    def _play(self, column, piece) -> int:

        piece_count = self.col_count[column]

        # If column is filled, raise exception
        if piece_count >= 6:
            raise ValueError("Column " + str(column) + " is already full")

        row = 5 - piece_count  # Find row to place piece
        self.board[row][column] = piece
        self.col_count[column] += 1  # Update number of pieces in column

        return row

    def _four_in_a_row(self, piece_sequence: List[int]) -> int:
        """Returns if and which player has a 4-in-a-row given the piece sequence"""

        piece_set = set(piece_sequence)     # Convert sequence to set to filter out duplicates
        if len(piece_set) == 1:             # If all pieces are of one type
            return piece_set.pop()         # Return singular piece

        return 0                            # No 4-in-a-row

    def __repr__(self):

        return '\n'.join([' '.join([str(piece) for piece in row]) for row in self.board])
