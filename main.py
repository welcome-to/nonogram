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
        return all(map(lambda i: i != UNKNOWN, self.row(row) if row is not None else self.column(column)))

    def is_complete(self):
        return all(map(lambda r: self.is_filled(row=r),  range(self.size)))

    def is_correct(self):
        pass

    def __eq__(self, other):
        # fixme
        return self.data == other.data

    def __str__(self):
        return '\n'.join([' '.join([str(i)+ (2-len(str(i))) * ' ' for i in row]) for row in self.data])

    def set_row(self, row, line):
        self.data[row] = copy(line)

    def set_column(self, column, line):
        for y in range(self.size):
            self.data[y][column] = line[y]


def update_line(line, pattern):
    if sum(pattern) + len(pattern) - 1 == 15:
        line = [1 for _ in range(15)]
        j = 0
        for i in range(len(pattern)):
            j += pattern[i]
            if j + 1 < 15:
                line[j+1]==-1

    return line


def main():
    rows = [[4],[8],[10],[11],[11],[11],[2,2,4],[1,3,2,3],[1,5,2,3],[1,5,2,3],[1,3,3,3],[2,4,2],[11],[9],[7]]
    columns = [[5],[1,3],[1,2,3],[5,3],[3,4,3],[4,4,3],[5,2,3],[5,4],[7,5],[14],[6,6],[7],[11],[11],[9]]
    board = Board(15, rows, columns)

    while not board.is_complete():
        new_board = Board(board.size, board.row_patterns, board.column_patterns)
        for i in range(board.size):
            row = board.row(i)
            new_row = update_line(row, board.row_patterns[i])
            new_board.set_row(i, new_row)

        for j in range(board.size):
            column = board.column(j)
            new_column = update_line(column, new_board.row_patterns[j])
            new_board.set_column(j, new_column)

        if (new_board == board):
            print(new_board)
            raise RuntimeError("Эвристик не хватило")

        board = new_board
    print(board)

if __name__ == "__main__":
    main()