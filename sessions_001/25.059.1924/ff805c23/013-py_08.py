import numpy as np
from typing import List, Tuple

def find_inner_bounding_box(grid):
    """
    Finds the inner bounding box defined by the region of interest (ROI)
    within the area bounded by magenta (color 6).
    """
    rows, cols = grid.shape
    
    # Find outermost magenta pixels
    outer_min_row, outer_min_col, outer_max_row, outer_max_col = find_bounding_box(grid, 6)

    # Find top boundary of ROI (looking downwards from the outermost top magenta)
    top_row = outer_min_row
    while top_row <= outer_max_row:
        if all(grid[top_row, outer_min_col:outer_max_col+1] != 6):
            break
        top_row += 1
    top_row -=1 #adjust

    # Find bottom boundary of ROI (looking upwards from the outermost bottom magenta)
    bottom_row = outer_max_row
    while bottom_row >= outer_min_row:
        if all(grid[bottom_row, outer_min_col:outer_max_col+1] != 6):
            break
        bottom_row -= 1
    bottom_row += 1 #adjust

    # Find left boundary of ROI (looking rightwards from the outermost left magenta)
    left_col = outer_min_col
    while left_col <= outer_max_col:
        if all(grid[outer_min_row:outer_max_row+1, left_col] != 6):
            break
        left_col += 1
    left_col -=1 #adjust

    # Find right boundary of ROI (looking leftwards from the outermost right magenta)
    right_col = outer_max_col
    while right_col >= outer_min_col:
        if all(grid[outer_min_row:outer_max_row+1, right_col] != 6):
             break
        right_col -= 1
    right_col += 1
        
    return top_row, left_col, bottom_row, right_col

def find_bounding_box(grid, color):
    rows, cols = grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                min_row = min(min_row, r)
                min_col = min(min_col, c)
                max_row = max(max_row, r)
                max_col = max(max_col, c)

    return min_row, min_col, max_row, max_col

def transform(input_grid):
    # Find the inner bounding box (ROI).
    top_row, left_col, bottom_row, right_col = find_inner_bounding_box(input_grid)

    # Calculate height and width of the ROI.
    height = bottom_row - top_row + 1
    width = right_col - left_col + 1
    
    # Initialize output grid with the calculated dimensions, filled with 6s.
    output_grid = np.full((height, width), 6, dtype=int)

    # Copy color 0 pixels from the input ROI to the output grid.
    for r in range(height):
        for c in range(width):
            input_row = top_row + r
            input_col = left_col + c
            if input_grid[input_row, input_col] == 0:
                output_grid[r, c] = input_grid[input_row, input_col]

    return output_grid

def compare_grids(grid1, grid2):
    return np.array_equal(grid1, grid2)


# Example data (replace with actual data from the task)
train_pairs = [
    ([
        [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
        [6, 1, 1, 1, 1, 8, 8, 8, 8, 8, 1, 6],
        [6, 1, 1, 1, 1, 8, 8, 8, 8, 8, 1, 6],
        [6, 1, 1, 1, 1, 8, 8, 8, 8, 8, 1, 6],
        [6, 1, 1, 1, 1, 0, 0, 0, 8, 8, 1, 6],
        [6, 1, 1, 1, 1, 8, 8, 0, 8, 8, 1, 6],
        [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
    ],
     [
        [6, 6, 6, 6, 6, 6],
        [6, 8, 8, 8, 8, 6],
        [6, 8, 8, 8, 8, 6],
        [6, 8, 8, 8, 8, 6],
        [6, 0, 0, 0, 8, 6],
        [6, 8, 8, 0, 8, 6]
    ]),
    ([
        [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
        [6, 1, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8, 1, 6],
        [6, 1, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8, 1, 6],
        [6, 1, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8, 1, 6],
        [6, 1, 1, 1, 1, 8, 8, 8, 0, 0, 8, 8, 1, 6],
        [6, 1, 1, 1, 1, 8, 8, 8, 0, 0, 8, 8, 1, 6],
        [6, 1, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8, 1, 6],
        [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
    ],
     [
        [6, 6, 6, 6, 6, 6, 6, 6],
        [6, 8, 8, 8, 8, 8, 8, 6],
        [6, 8, 8, 8, 8, 8, 8, 6],
        [6, 8, 8, 8, 0, 0, 8, 6],
        [6, 8, 8, 8, 0, 0, 8, 6],
        [6, 8, 8, 8, 8, 8, 8, 6],
        [6, 6, 6, 6, 6, 6, 6, 6]
    ]),
    ([
        [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
        [6, 6, 6, 1, 1, 8, 8, 8, 6, 6],
        [6, 6, 6, 1, 1, 8, 8, 8, 6, 6],
        [6, 6, 6, 1, 1, 8, 0, 8, 6, 6],
        [6, 6, 6, 1, 1, 8, 8, 8, 6, 6],
        [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
    ],
    [
        [6, 6, 6, 6],
        [6, 8, 8, 6],
        [6, 8, 0, 6],
        [6, 8, 8, 6],
        [6, 6, 6, 6]
    ]),
     ([
        [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
        [6, 1, 1, 1, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8, 1, 6],
        [6, 1, 1, 1, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8, 1, 6],
        [6, 1, 1, 1, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8, 1, 6],
        [6, 1, 1, 1, 1, 1, 1, 8, 8, 8, 0, 0, 0, 8, 1, 6],
        [6, 1, 1, 1, 1, 1, 1, 8, 8, 8, 0, 0, 0, 8, 1, 6],
        [6, 1, 1, 1, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8, 1, 6],
        [6, 1, 1, 1, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8, 1, 6],
        [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
    ],
     [
        [6, 6, 6, 6, 6, 6, 6, 6, 6],
        [6, 8, 8, 8, 8, 8, 8, 8, 6],
        [6, 8, 8, 8, 8, 8, 8, 8, 6],
        [6, 8, 8, 8, 0, 0, 0, 8, 6],
        [6, 8, 8, 8, 0, 0, 0, 8, 6],
        [6, 8, 8, 8, 8, 8, 8, 8, 6],
        [6, 8, 8, 8, 8, 8, 8, 8, 6],
        [6, 6, 6, 6, 6, 6, 6, 6, 6]
    ]),
]


for i, (input_grid, expected_output) in enumerate(train_pairs):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    predicted_output = transform(input_grid)
    is_correct = compare_grids(predicted_output, expected_output)
    top_row, left_col, bottom_row, right_col = find_inner_bounding_box(input_grid)
    
    print(f"Example {i+1}:")
    print(f"  Input Grid Shape: {input_grid.shape}")
    print(f"  Expected Output Shape: {expected_output.shape}")
    print(f"  Predicted Output Shape: {predicted_output.shape}")
    print(f"  Bounding Box: top={top_row}, left={left_col}, bottom={bottom_row}, right={right_col}")
    print(f"  Correct: {is_correct}")
    print("-" * 20)