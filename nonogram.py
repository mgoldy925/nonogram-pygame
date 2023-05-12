import random

class Nonogram:

    def __init__(self, size):
      self.size = size
      rows = self.size + 1
      cols = self.size + 1
      self.board = [[0 for _ in range(cols)] for __ in range(rows)]
      self.answer = [[random.randint(0, 9) < 6 for _ in range(cols)] for __ in range(rows)]
      self._init_board()

    def _init_board(self):

        count = 0
        for i in range(0, self.size):
            newRow = []
            for j in range(0, self.size):
                if self.answer[i][j]:
                    count = count + 1
                elif not (self.answer[i][j] or j == self.size - 1) and count != 0:
                    newRow.append(count)
                    count = 0
            self.board[i+1][0] = newRow
            count = 0

        for i in range (0, self.size):
            newCol = []
            for j in range(0, self.size):
                if self.answer[j][i]:
                    count = count + 1
                elif not (self.answer[j][i] or j == self.size - 1) and count != 0:
                    newCol.append(count)
                    count = 0
            self.board[0][i+1] = newCol
            count = 0

    def check_board(self):

        for i in range (0, self.size):
            for j in range (0, self.size):
                if self.board[i+1][j+1] ^ self.answer[i][j]:
                    return False

        return True
