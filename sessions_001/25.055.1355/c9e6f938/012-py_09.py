"""
Identifies all contiguous blocks of orange (7) pixels in the input grid.
Expands them, doubling their width or height based on examples.
Shifts other color pixels accordingly.
"""

import numpy as np

def find_objects(grid):
    """
    Finds all contiguous objects (blocks of same color) in a grid.
    Returns a list of objects.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, pixels):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        pixels.append((row, col))
        dfs(row + 1, col, color, pixels)
        dfs(row - 1, col, color, pixels)
        dfs(row, col + 1, color, pixels)
        dfs(row, col - 1, color, pixels)

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                color = grid[row, col]
                pixels = []
                dfs(row, col, color, pixels)
                if pixels:
                    # find top_left, bottom_right
                    pixels_array = np.array(pixels)
                    min_row, min_col = np.min(pixels_array, axis=0)
                    max_row, max_col = np.max(pixels_array, axis=0)
                    objects.append({
                        "color": color,
                        "pixels": pixels,
                        "top_left": (min_row, min_col),
                        "bottom_right": (max_row, max_col)
                    })
    return objects

def determine_expansion_direction(examples):
    """
    Determines if expansion is horizontal or vertical by comparing input/output pairs.
    """
    for input_grid, output_grid in examples:
        input_grid = np.array(input_grid)
        output_grid = np.array(output_grid)
        if input_grid.shape[0] != output_grid.shape[0]:
            return "vertical"  # Height changed
        if input_grid.shape[1] != output_grid.shape[1]:
            return "horizontal"  # Width changed
    return "horizontal"  # Default to horizontal if no change is detected

def transform(input_grid, examples=None): #added examples arg
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find all objects
    objects = find_objects(input_grid)

    # Determine expansion direction
    expansion_direction = determine_expansion_direction(examples)


    if expansion_direction == "horizontal":
        # Calculate maximum expansion needed
        max_expansion = 0
        for obj in objects:
            if obj["color"] == 7:
                width = obj["bottom_right"][1] - obj["top_left"][1] + 1
                max_expansion = max(max_expansion, width)

        # Initialize output grid
        output_grid = np.zeros((input_grid.shape[0], input_grid.shape[1] + max_expansion), dtype=int)

        # shift tracking
        shifts = {}

        # Copy and expand, shift
        for obj in objects:
            if obj["color"] == 7:
                original_width = obj["bottom_right"][1] - obj["top_left"][1] + 1
                expansion_amount = original_width

                for row, col in obj["pixels"]:
                    #calculate shift for this row
                    shift = shifts.get(row,0)
                    output_grid[row, col + shift] = 7  # Original position
                    output_grid[row, col + shift + expansion_amount] = 7  # Expanded position

                # update shifts for rows below orange objects
                for r in range(input_grid.shape[0]):
                    orange_cols_in_row = 0
                    for c in range(input_grid.shape[1]):
                        if input_grid[r,c] == 7:
                            orange_object = None
                            for o in objects:
                                if o['color'] == 7 and (r,c) in o['pixels']:
                                    orange_object = o
                                    break

                            if orange_object is not None:
                                 original_width = orange_object["bottom_right"][1] - orange_object["top_left"][1] + 1
                                 orange_cols_in_row = original_width
                                 break #found orange in row
                    shifts[r] = shifts.get(r,0) + orange_cols_in_row #update shift

            else:
                # copy non-orange
                for row, col in obj["pixels"]:
                    #calculate shift
                    shift = shifts.get(row, 0)
                    output_grid[row, col + shift] = obj["color"]

    elif expansion_direction == "vertical":
        # Calculate maximum expansion needed
        max_expansion = 0
        for obj in objects:
            if obj["color"] == 7:
                height = obj["bottom_right"][0] - obj["top_left"][0] + 1
                max_expansion = max(max_expansion, height)

        # Initialize output grid
        output_grid = np.zeros((input_grid.shape[0] + max_expansion, input_grid.shape[1]), dtype=int)

        # shift tracking
        shifts = {}  # Track shifts per column

        for obj in objects:
            if obj["color"] == 7:
                # Calculate original height
                original_height = obj["bottom_right"][0] - obj["top_left"][0] + 1
                expansion_amount = original_height

                # Place original and expanded copies
                for row, col in obj["pixels"]:
                    shift = shifts.get(col, 0)
                    output_grid[row + shift, col] = 7
                    output_grid[row + shift + expansion_amount, col] = 7

                 #update shift
                for c in range(input_grid.shape[1]):
                    orange_rows_in_col = 0
                    for r in range(input_grid.shape[0]):
                        if input_grid[r,c] == 7:
                            orange_object = None
                            for o in objects:
                                if o['color'] == 7 and (r,c) in o['pixels']:
                                    orange_object = o
                                    break

                            if orange_object is not None:
                                original_height = orange_object['bottom_right'][0] - orange_object['top_left'][0] + 1
                                orange_rows_in_col = original_height
                                break
                    shifts[c] = shifts.get(c,0) + orange_rows_in_col

            else:
                # Copy other color pixels
                for row, col in obj["pixels"]:
                    shift = shifts.get(col, 0)
                    output_grid[row + shift, col] = obj["color"]
    return output_grid