from main import *



def test_inexact():
    pattern = [1]
    line = [
        FALSE,
        FALSE,
        UNKNOWN,
        TRUE,
        UNKNOWN,
        UNKNOWN,
        UNKNOWN,
        UNKNOWN,
        UNKNOWN,
        UNKNOWN,
        UNKNOWN]
    print("BEFORE:", line)
    print("AFTER:", mark_from_inexact_start(line, pattern))


def test_exact():
    pattern = [13, 1]
    line = [UNKNOWN for _ in range(15)]
    print("BEFORE:", line)
    print("AFTER:", fill_exact_matches(line, pattern))

test_exact()
