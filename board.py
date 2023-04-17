import random

class Board:

    def __init__(self, size):
      self.size = size
      rows = self.size + 1
      cols = self.size + 1
      self.board = [[false]*cols]*rows
      self.answer = [[bool(random.randint(0, 1)) for i in range(cols)] for j in range(rows)]

    def _init_board(self):

        count = 0;
        for i in range(1, self.size + 1):
            newRow = []
            for j in range(0, self.size):
                if answer[i][j]:
                    count = count + 1
                else:
                    newRow.append(count)
                    count = 0
            board[i][0] = newRow

        for i in range (1, self.size + 1):
            newCol = []
            for j in range(0, self.size):
                if answer[j][i]:
                    count = count + 1
                else:
                    newCol.append(count)
                    count = 0
            board[0][i] = newCol
