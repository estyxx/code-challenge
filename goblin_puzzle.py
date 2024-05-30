# The Enchanted Forest Maze:

# In the Enchanted Forest, there are magical trees that glow with different colors.
# Each tree is represented by a number, and your task is to find the path with
# the maximum sum.
# The catch? You can only move right or down through this mystical grid.

# Write a function that takes a 2D list (matrix) representing the Enchanted
# Forest and returns the maximum sum of the path from the top-left corner to
# the bottom-right corner.

# Here’s the forest grid for your challenge:

# fmt: off
forest = [
    [5, 3, 2, 1],
    [1, 2, 1, 3],
    [4, 2, 1, 2],
    [2, 1, 1, 5]]
# fmt: on

# The function should return: 19
# Path: 5 -> 3 -> 2 -> 1 -> 3 -> 2 -> 1 -> 5
# Your mission: write a function that conquers this grid and finds the maximum sum path!


def enchanted_forest_max_sum(forest: list[list[int]]) -> int:
    if not forest:
        return 0
    if not forest[0]:
        return 0

    i = j = 0

    height = len(forest)
    width = len(forest[0])

    start = forest[i][j]
    path = [start]

    while i <= height - 1 and j <= width - 1:
        left = forest[i][j + 1] if j + 1 < width else forest[i][j]
        down = forest[i + 1][j] if i + 1 < height else forest[i][j]

        if i == height - 1:
            path.append(left)
            j += 1

        elif j == width - 1:
            path.append(down)
            i += 1

        elif left > down:
            path.append(left)
            if j < width - 1:
                j += 1
        else:
            path.append(down)
            if i < height - 1:
                i += 1

    return sum(path)


# Once you’ve found the path to victory and the maximum sum, report back,
# and the gates to the next part of our thrilling saga shall open wide!


def test_forest_maximum_sum():
    assert enchanted_forest_max_sum(forest) == 19


def test_empty_forest():
    assert enchanted_forest_max_sum([]) == 0


def test_empty_forest_row():
    assert enchanted_forest_max_sum([[]]) == 0


def test_one_tree_forest():
    assert enchanted_forest_max_sum([[1]]) == 1
