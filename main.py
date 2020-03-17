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
        for i in range(self.size):
            if not is_line_correct(self.row(i),self.row_patterns[i]):
                return False
            if not is_line_correct(self.row(i),self.row_patterns[i]):
                return False

    def __eq__(self, other):
        return self.data == other.data

    def __str__(self):
        return '\n'.join([' '.join([str(i)+ (2-len(str(i))) * ' ' for i in row]) for row in self.data])

    def set_row(self, row, line):
        self.data[row] = copy(line)

    def set_column(self, column, line):
        for y in range(self.size):
            self.data[y][column] = line[y]


def is_line_correct(line,pattern):
    real_patern = []
    current_segment = 0
    for i in line:
        if i == UNKNOWN:
            raise RuntimeError("Невозможно устоновить коректность, строка не полна")
        elif i == TRUE:
            current_segment += 1
        else:
            if current_segment !=0:
                real_patern.append(current_segment)
            current_segment = 0

    return real_patern == pattern


def fill_exact_matches(line, pattern):
    if sum(pattern) + len(pattern) - 1 == 15:
        line = [TRUE for _ in range(15)]
        j = 0
        for i in range(len(pattern)):
            j += pattern[i]
            if j + 1 < 15:
                line[j+1] == FALSE
    return line

def mark_existing_centers(line, pattern):
    size = len(line)

    pattern_size = sum(pattern) + len(pattern) - 1
    if 2 * pattern_size > len(line):
        print(pattern)
        for i in range(size - pattern_size, size - pattern_size + max(0,pattern[0]- (size - pattern_size))):
            line[i] = TRUE
        for i in range(pattern_size,pattern_size - max(0, pattern[-1]- (size - pattern_size)),-1):
            line[i-1] = TRUE
    return line

def mark_from_exact_starts(line, border):
    return line

def mark_missing_borders(line, pattern):
    def rindex(line, item):
        return len(line) - list(reversed(line)).index(item) - 1

    if len(pattern) > 1 or TRUE not in line:
        return line

    s, e = line.index(TRUE), rindex(line, TRUE)
    part = e - s + 1
    remaining = pattern[0] - (e - s + 1)

    for i in set(range(s - remaining)) | set(range(e + 1 + remaining, len(line))):
        line[i] = FALSE

    return line

def fill(line, start, end, value):
    for j in range(start, end):
        line[j] = value

def mark_too_short_missing(line, pattern):
    shortest = min(pattern)

    first = 0
    for i in range(1, len(line)):
        if line[i-1] == FALSE and line[i] == UNKNOWN:
            first = i
        if line[i-1] == UNKNOWN and line[i] == FALSE:
            if i - first < shortest:
                fill(line, first, i, FALSE)
    if line[-1] == UNKNOWN and len(line) - first < shortest:
        fill(line, first, len(line), FALSE)
    return line

def fill_full_lines(line, pattern):
    return line

def update_line(line, pattern):
    print("Called update_line with pattern", pattern)
    line = fill_exact_matches(line, pattern)
    line = mark_existing_centers(line, pattern)
    line = mark_too_short_missing(line, pattern)
    line = mark_missing_borders(line, pattern)
    line = mark_from_exact_starts(line, pattern)
    # fixme
    line = fill_full_lines(line, pattern)
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
            column = new_board.column(j)
            new_column = update_line(column, new_board.column_patterns[j])
            new_board.set_column(j, new_column)

        if (new_board == board):
            print(new_board)
            raise RuntimeError("Эвристик не хватило")

        board = new_board
    print(board)

if __name__ == "__main__":
    #main()
    """
    line = [UNKNOWN for _ in range(4)] + [TRUE for _ in range(10)] + [UNKNOWN]
    print(line)
    pattern = [10]
    result = mark_missing_borders(line, pattern)
    print(result)
    """
    pattern = [4]
    line = [
        UNKNOWN,
        UNKNOWN,
        FALSE,
        UNKNOWN,
        FALSE,
        UNKNOWN,
        UNKNOWN,
        UNKNOWN]
    print(line)
    print(mark_too_short_missing(line, pattern))
