# Example: Analyzing the first training pair (assuming input_grid and expected_output_grid are defined)
import numpy as np

def analyze_differences(input_grid, expected_output_grid):
    differences = np.where(input_grid != expected_output_grid)
    diff_coords = list(zip(differences[0], differences[1]))

    print("Differences found at coordinates:", diff_coords)
    for row, col in diff_coords:
      print(f"  Input:  ({row}, {col}) = {input_grid[row, col]}")
      print(f"  Output: ({row}, {col}) = {expected_output_grid[row, col]}")

def find_pixels_by_color(grid, color):
    return np.argwhere(grid == color)

#  example usage using first example pair
#  analyze_differences(training_examples[0][0], training_examples[0][1])
