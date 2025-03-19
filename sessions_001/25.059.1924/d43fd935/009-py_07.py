import numpy as np

def compare_grids(grid1, grid2):
    """Compares two grids and returns metrics."""
    correct_pixels = np.sum(grid1 == grid2)
    incorrect_pixels = np.sum(grid1 != grid2)
    diff_colors = {}

    for color in np.unique(np.concatenate((grid1, grid2))):
        diff = np.sum(grid1 == color) - np.sum(grid2 == color)
        if diff != 0:
            diff_colors[color] = diff

    return correct_pixels, incorrect_pixels, diff_colors

# Example usage (replace with actual grids)
# Assuming 'output_grid' is from the 'transform' function and 'expected_grid' is the correct output
# correct, incorrect, diffs = compare_grids(output_grid, expected_grid)
# print(f"Correct Pixels: {correct}, Incorrect Pixels: {incorrect}, Differences: {diffs}")