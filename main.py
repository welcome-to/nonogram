from data import *
from heuristics import *

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


def is_line_correct(line,pattern,no_err=False):
    real_patern = []
    current_segment = 0
    for i in line:
        if i == UNKNOWN and not no_err:
            raise RuntimeError("Невозможно устоновить коректность, строка не полна")
        elif i == TRUE:
            current_segment += 1
        else:
            if current_segment !=0:
                real_patern.append(current_segment)
            current_segment = 0

    return real_patern == pattern

"""
Если суммарная длина отрезков вместе с пробелами равна стороне, то положение клеточек определено однозначно.
"""
def fill_exact_matches(line, pattern):
    if sum(pattern) + len(pattern) - 1 == 15:
        line = [TRUE for _ in range(15)]
        j = 0
        for i in range(len(pattern)):
            j += pattern[i] + 1
            if j < 15:
                line[j-1] = FALSE
    return line

"""
Отметим те (центральные) части достаточно длинных кусков, про которые уже всё ясно
"""
def mark_existing_centers(line, pattern):
    size = len(line)

    pattern_size = sum(pattern) + len(pattern) - 1
    if 2 * pattern_size > len(line):
        #print(pattern)
        for i in range(size - pattern_size, size - pattern_size + max(0,pattern[0]- (size - pattern_size))):
            line[i] = TRUE
        for i in range(pattern_size,pattern_size - max(0, pattern[-1]- (size - pattern_size)),-1):
            line[i-1] = TRUE
    return line

#def mark_from_exact_starts(line, pattern):
#    return line

def mark_from_inexact_start(line, pattern):
    #print("Line: {0}, pattern: {1}".format(line, pattern))
    for i in range(len(line)):
        if line[i] != FALSE:
            break
    start = i

    first = pattern[0]
    if not all(map(lambda x: x != FALSE, line[i:i + first])):
        return line

    for i in range(i, len(line)):
        if line[i] == UNKNOWN:
            continue
        if line[i] == FALSE:
            return line
        else:
            break
        i += 1

    #print(start, i, first)
    for j in range(i, i + first - (i - start)):
        line[j] = TRUE

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
    grouped = groupby(line, key=lambda x: {TRUE: TRUE, FALSE: FALSE, UNKNOWN: FALSE}[x])
    true_pattern = [len(list(group)) for key, group in filter(lambda item: item[0] == TRUE, grouped)]
    if true_pattern == pattern:
        line = [FALSE if item == UNKNOWN else item for item in line]
    return line

# Returns tuple (new_line, new_pattern)
# FIXME: we also need `how many items did we get rid of`
def extract_unknown_tail(line, pattern):
    new_line = line
    new_pattern = pattern
    try:
        while pattern:
            start = new_line.index(TRUE)
            end = start + new_pattern[0]
            if not all(map(lambda item: item == TRUE, line[start:end])):
                return new_line, new_pattern
            new_line = new_line[end:]
            new_pattern = new_pattern[1:]
    except ValueError:
        return new_line, new_pattern
    # this is excess
    return new_line, new_pattern

def extract_unknown_part(line, pattern):
    #fixme
    return extract_unknown_tail(line, pattern)

def update_line(line, pattern):
    #print("Called update_line with pattern", pattern)
    line = fill_exact_matches(line, pattern)
    line = mark_existing_centers(line, pattern)
    line = mark_too_short_missing(line, pattern)
    line = mark_missing_borders(line, pattern)
    line = mark_from_inexact_start(line, pattern)
    # fixme
    line = fill_full_lines(line, pattern)
    return line


def pos_lines(row):
    ans = []
    for i in range(len(row)):
        if row[i] == UNKNOWN:
            t = copy(row)
            t[i] = TRUE
            ans.append(t)
    return ans

"""
def main(rows, columns, board=None):
    if board is None:
        board = Board(5, rows, columns)

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
            for i in range(len(board.data)):
                if not is_line_correct(board.data[i],board.row_patterns[i],no_err=True):
                    for line in pos_lines(board.data[i]): 
                        old_board = deepcopy(board)
                        board.data[i]=line
                        t = main(board.row_patterns,board.column_patterns,board=board)
                        if t[0]:
                            return t[1]
                        else:
                            board = deepcopy(old_board)
                            del old_board

            print(new_board)
            #raise RuntimeError("Эвристик не хватило")

        board = new_board
    return (board.is_complete() and board.is_correct(),board)
"""

def main(rows, columns, board=None):
    if board is None:
        board = Board(len(rows), rows, columns)
    
    while not board.is_complete():
        new_board = update_lines(board)

        if (new_board == board):
            """
            for i in range(len(board.data)):
                if not is_line_correct(board.data[i],board.row_patterns[i],no_err=True):
                    for line in pos_lines(board.data[i]): 
                        old_board = deepcopy(board)
                        board.data[i]=line
                        t = main(board.row_patterns,board.column_patterns,board=board)
                        if t[0]:
                            return t[1]
                        else:
                            board = deepcopy(old_board)
                            del old_board

            print(new_board)
            """
            print('Эвристик не хватило')
            #print(new_board)
            break

        board = new_board

    return board


def update_lines(board):
    new_board = Board(board.size, board.row_patterns, board.column_patterns)
    for i in range(board.size):
        row = board.row(i)
        new_row = update_line(row, board.row_patterns[i])
        new_board.set_row(i, new_row)

    for j in range(board.size):
        column = new_board.column(j)
        new_column = update_line(column, new_board.column_patterns[j])
        new_board.set_column(j, new_column)

    return new_board


if __name__ == "__main__":
    #print(main(*pets_data()))
    print(main(*small_data()))
