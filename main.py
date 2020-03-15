from copy import copy, deepcopy

TRUE = 1
FALSE = -1
UNKNOWN = 0

class Board:
    def __init__(self, size, rows,columns, data=None):
        self.size = size
        self.row_patterns = rows
        self.column_patterns = columns
        if data is None:
            self.data = [[UNKNOWN for _ in range(size)] for _ in range(self.size)]
        else:
            self.data = deepcopy(data)

    def row(self, index):
        return copy(self.data[index])

    def column(self, index):
        return [self.data[i][index] for i in range(self.size)]

    def is_filled(self, row=None, column=None):
        if row is None == column is None:
            raise RuntimeError("Invalid data")
        return all(lambda i: i != UNKNOWN, self.row(row) if row is not None else self.column(column))

    def is_complete(self):
        return all(lambda r: self.is_filled(row=r),  range(self.size))

    def is_correct(self):
        pass

    def __eq__(self, other):
        # fixme
        return True

    def set_row(self, row, line):
        self.data[row] = copy(line)

    def set_column(self, column, line):
        for y in range(self.size):
            self.data[y][column] = line[i]


def update_line(line, pattern):
    # здесь могли бы быть ваши эвристики
    return line


def main():
    rows = [...]
    columns = [...]
    board = Board(15, rows, columns)

    while not board.is_complete():
        new_board = Board(board.size, board.rows, board.columns)
        for i in range(board.size):
            row = board.row(i)
            new_row = update_line(row, board.row_patterns[i])
            new_board.set_row(i, new_row)

        for j in range(board.size):
            column = board.column(j)
            new_column = update_line(column, new_board.row_patterns[j])
            new_board.set_column(j, new_column)

        if (new_board == board):
            raise RuntimeError("Эвристик не хватило")

        board = new_board
