import numpy as np

def calculate_difference(predicted_output, expected_output):
    """Calculates the pixel-wise difference between two grids."""
    return predicted_output - expected_output

def compare_grids(grid1, grid2):
    """Compares two grids and returns a grid with differences highlighted.

    0: identical
    1: different
    """
    return (grid1 != grid2).astype(int)

# Example Usage (assuming we have predicted_output and expected_output for a case):
# difference_grid = calculate_difference(predicted_output, expected_output)
# print(difference_grid)

# input_grid
i0 = np.array([
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,3,0,0,0,0],
    [0,0,0,0,3,0,0,0,0],
    [0,0,0,0,3,0,0,0,0],
    [0,3,3,3,3,3,3,3,0],
    [0,0,0,0,3,2,0,0,0],
    [0,0,0,0,3,0,0,0,0],
    [0,0,0,0,3,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]])

# expected output
o0 = np.array([
    [0,0,0,0,3,0,0,0,0],
    [0,0,0,0,3,0,0,0,0],
    [0,0,0,0,3,0,0,0,0],
    [0,3,3,3,3,3,3,3,0],
    [0,3,3,3,3,3,3,3,0],
    [0,3,3,3,3,2,3,3,0],
    [0,3,3,3,3,0,3,3,0],
    [0,3,3,3,3,3,3,3,0],
    [0,0,0,0,3,0,0,0,0]])

# input
i1 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,3,0,0,0,0,0],
    [0,0,0,0,0,3,0,0,0,0,0],
    [0,0,0,0,0,3,0,0,0,0,0],
    [0,0,0,0,0,3,0,0,0,0,0],
    [0,0,3,3,3,3,3,3,3,3,0],
    [0,0,0,0,0,3,2,0,0,0,0],
    [0,0,0,0,0,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0]])

# expected
o1 = np.array([
    [0,0,0,0,0,3,0,0,0,0,0],
    [0,0,0,0,0,3,0,0,0,0,0],
    [0,0,0,0,0,3,0,0,0,0,0],
    [0,0,0,0,0,3,0,0,0,0,0],
    [0,0,3,3,3,3,3,3,3,3,0],
    [0,0,3,3,3,3,3,3,3,3,0],
    [0,0,3,3,3,3,2,3,3,3,0],
    [0,0,3,3,3,3,3,3,3,3,0],
    [0,0,0,0,0,3,0,0,0,0,0]])

# input
i2 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,0,0,0,0,0],
    [0,0,0,3,3,3,3,3,3,3,3,3,0],
    [0,0,0,0,0,0,0,3,2,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0]])

# expected
o2 = np.array([
    [0,0,0,0,0,0,0,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,0,0,0,0,0],
    [0,0,0,0,0,0,0,3,0,0,0,0,0],
    [0,0,0,3,3,3,3,3,3,3,3,3,0],
    [0,0,0,3,3,3,3,3,3,3,3,3,0],
    [0,0,0,3,3,3,3,3,2,3,3,3,0],
    [0,0,0,0,0,0,0,3,0,0,0,0,0]])

p0 = transform(i0)
p1 = transform(i1)
p2 = transform(i2)

diff0 = compare_grids(p0, o0)
diff1 = compare_grids(p1, o1)
diff2 = compare_grids(p2, o2)


print("Difference 0:\n", diff0)
print("Difference 1:\n", diff1)
print("Difference 2:\n", diff2)
