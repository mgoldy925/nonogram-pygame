import random

class Nonogram:

    def __init__(self, size):
      self.size = size
      rows = self.size + 1
      cols = self.size + 1
      self.board = [[0 for _ in range(cols)] for __ in range(rows)]
      self.answer = [[random.randint(0, 1) for _ in range(cols)] for __ in range(rows)]
      self._init_board()

    def _init_board(self):

        count = 0;
        for i in range(1, self.size + 1):
            newRow = []
            for j in range(0, self.size):
                if self.answer[i][j]:
                    count = count + 1
                else:
                    newRow.append(count)
                    count = 0
            self.board[i][0] = newRow

        for i in range (1, self.size + 1):
            newCol = []
            for j in range(0, self.size):
                if self.answer[j][i]:
                    count = count + 1
                else:
                    newCol.append(count)
                    count = 0
            self.board[0][i] = newCol