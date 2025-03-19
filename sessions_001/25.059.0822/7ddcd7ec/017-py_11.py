import numpy as np

def find_2x2_square(grid, color):
    """Finds the top-left corner of a 2x2 square of the given color."""
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if (grid[r, c] == color and
                grid[r + 1, c] == color and
                grid[r, c + 1] == color and
                grid[r + 1, c + 1] == color):
                return (r, c)
    return None

def find_orange_blocks(grid):
    """Finds all contiguous orange blocks and their bounding boxes."""
    orange_pixels = (grid == 7)
    labeled_array, num_features = ndimage.label(orange_pixels)
    blocks = []
    for i in range(1, num_features + 1):
        coords = np.where(labeled_array == i)
        min_row, min_col = np.min(coords, axis=1)
        max_row, max_col = np.max(coords, axis=1)
        blocks.append({
            'min_row': min_row,
            'min_col': min_col,
            'max_row': max_row,
            'max_col': max_col,
            'height': max_row - min_row + 1,
            'width': max_col - min_col + 1
        })
    return blocks

def analyze_example(input_grid, output_grid):
    """Analyzes a single example pair."""
    square_coords = find_2x2_square(input_grid, 7)
    input_blocks = find_orange_blocks(input_grid)
    output_blocks = find_orange_blocks(output_grid)

    print("2x2 Orange Square Coordinates (Top-Left):", square_coords)
    print("Input Orange Blocks:", input_blocks)
    print("Output Orange Blocks:", output_blocks)
    print("-" * 20)


# The provided example data from the prompt:
example_data = [
    # Example 1
    (np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 7, 7, 0, 0, 0],
        [0, 0, 0, 0, 7, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([
        [0, 0, 0, 0, 0, 0, 7, 0, 0],
        [0, 0, 0, 0, 0, 0, 7, 0, 0],
        [0, 0, 0, 0, 7, 7, 0, 0, 0],
        [0, 0, 0, 0, 7, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]])),
    # Example 2
    (np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 7, 7, 0, 0, 0],
        [0, 0, 0, 0, 7, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 7, 7, 0, 0, 0],
        [0, 0, 0, 0, 7, 7, 0, 0, 0],
        [0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]])),
    # Example 3
    (np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 7, 7, 0, 0, 0, 0],
        [0, 0, 0, 7, 7, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 7, 0, 0],
        [0, 0, 0, 0, 0, 0, 7, 0, 0],
        [0, 0, 0, 7, 7, 0, 0, 0, 0],
        [0, 0, 0, 7, 7, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]])),
]

from scipy import ndimage

for i, (input_grid, output_grid) in enumerate(example_data):
    print(f"Training Example {i + 1}:")
    analyze_example(input_grid, output_grid)
