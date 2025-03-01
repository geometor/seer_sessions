import numpy as np
from typing import List, Tuple

def compare_grids(grid1: np.ndarray, grid2: np.ndarray) -> Tuple[bool, List[Tuple[int, int]], List[Tuple[int, int]]]:
    """
    Compares two grids and returns a boolean indicating if they are identical,
    a list of coordinates where elements are present in grid1 but not in grid2,
    and a list of coordinates where elements are present in grid2 but not in grid1.
    """
    if grid1.shape != grid2.shape:
        return False, [], []

    diff1 = []
    diff2 = []

    for i in range(grid1.shape[0]):
        for j in range(grid1.shape[1]):
            if grid1[i, j] != grid2[i, j]:
                diff1.append((i,j))
                diff2.append((i,j))

    return np.array_equal(grid1, grid2), diff1, diff2

def report(task, results):
    print(f"TASK: {task}")
    for i, (input_grid, expected_output, actual_output) in enumerate(results):
        equal, diff1, diff2 = compare_grids(expected_output, actual_output)
        print(f"  Example {i + 1}:")
        print(f"    Identical: {equal}")
        if not equal:
            print(f"    Mismatched pixels (Expected): {diff1}")
            print(f"    Mismatched pixels (Actual):   {diff2}")

# Example Usage:
# Assuming you have 'results' in the format:
# results = [
#     (input_grid1, expected_output1, actual_output1),
#     (input_grid2, expected_output2, actual_output2),
#     ...
# ]

# Replace this with your actual 'results' variable
results = [] # Replace with actual results after running the code

# Call report to display for all
report("f25ffba3", results)