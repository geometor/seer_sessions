import numpy as np

train = [
    (np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
 [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
 [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
 [5, 5, 2, 0, 5, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 5, 5, 5],
 [5, 5, 0, 0, 5, 0, 0, 5, 5, 5, 0, 0, 0, 5, 0, 5, 5, 5],
 [5, 5, 0, 0, 5, 0, 0, 5, 5, 5, 0, 0, 0, 5, 0, 5, 5, 5],
 [5, 5, 0, 0, 5, 0, 0, 5, 5, 5, 0, 0, 0, 5, 0, 5, 5, 5],
 [5, 5, 0, 0, 5, 0, 0, 5, 5, 5, 0, 0, 0, 5, 0, 5, 5, 5]]),
 np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 2, 1, 0, 2, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])),
    (np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
 [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
 [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
 [5, 5, 5, 5, 2, 2, 0, 5, 5, 5, 5, 5, 5, 5, 5],
 [5, 5, 5, 5, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5],
 [5, 5, 5, 5, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5],
 [5, 5, 5, 5, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5],
 [5, 5, 5, 5, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5]]),
 np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])),
    (np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
 [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
 [5, 5, 5, 5, 5, 2, 0, 0, 5, 5, 5, 5, 5, 5],
 [5, 5, 5, 5, 5, 0, 0, 0, 5, 5, 5, 5, 5, 5],
 [5, 5, 5, 5, 5, 0, 0, 0, 5, 5, 5, 5, 5, 5],
 [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
 np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 2, 1, 1, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]))
]

def get_red_positions(grid):
    return np.array(np.where(grid == 2)).T

def get_transformed_region_bounds(grid):
     #find the bounding box of all red pixels
    red_positions = get_red_positions(grid)
    if len(red_positions) == 0:
        return None  # No red pixels

    min_row = np.min(red_positions[:, 0])
    max_row = np.max(red_positions[:, 0])
    min_col = np.min(red_positions[:, 1])
    max_col = np.max(red_positions[:, 1])

    return min_row, max_row, min_col, max_col

def analyze_examples(train):
    for i, (input_grid, expected_output) in enumerate(train):
        print(f"Example {i+1}:")

        # Red positions
        red_positions = get_red_positions(input_grid)
        print(f"  Red Pixel Positions: {red_positions.tolist()}")

        # Transformed region bounds
        bounds = get_transformed_region_bounds(input_grid)
        if bounds:
            min_row, max_row, min_col, max_col = bounds
            print(f"  Transformed Region Bounds: row=({min_row}, {max_row}), col=({min_col}, {max_col})")

            #find the blue pixels
            blue_pos_input = np.array(np.where(input_grid == 1)).T
            blue_pos_output = np.array(np.where(expected_output == 1)).T

            print(f"  Blue output: {blue_pos_output.tolist()}")

            # find the white pixels that transform to blue in the output
            white_to_blue_pixels = []
            for r in range(min_row, max_row + 1):
               for c in range(min_col, max_col+1):
                  if input_grid[r,c] == 0 and expected_output[r,c] == 1:
                     white_to_blue_pixels.append( (r,c))
            print(f"  White to Blue Pixels: {white_to_blue_pixels}")

        else:
            print("  No red pixels found.")
        print("-" * 40)
analyze_examples(train)