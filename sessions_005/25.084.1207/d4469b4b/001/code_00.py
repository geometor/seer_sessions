import numpy as np

def transform(input_grid):
    """
    Identifies the single non-white color present in the 5x5 input grid.
    Based on this color, returns a predefined 3x3 pattern of gray (5) pixels
    on a white (0) background.
    - Blue (1) maps to a '+' shape.
    - Red (2) maps to a 'T' shape.
    - Green (3) maps to a backward 'L' shape.
    """

    # Define the output patterns as numpy arrays
    pattern_plus = np.array([
        [0, 5, 0],
        [5, 5, 5],
        [0, 5, 0]
    ], dtype=int)

    pattern_t = np.array([
        [5, 5, 5],
        [0, 5, 0],
        [0, 5, 0]
    ], dtype=int)

    pattern_l = np.array([
        [0, 0, 5],
        [0, 0, 5],
        [5, 5, 5]
    ], dtype=int)

    # Convert input grid to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)

    # Find the unique non-white color in the input grid
    non_white_colors = np.unique(input_array[input_array != 0])

    # Ensure there is exactly one non-white color (as per observed pattern)
    if len(non_white_colors) != 1:
        # Handle unexpected input, maybe return an empty or default grid,
        # or raise an error. For now, let's return an empty 3x3 grid.
        print(f"Warning: Expected one non-white color, found {len(non_white_colors)}. Input: {non_white_colors}")
        return np.zeros((3, 3), dtype=int)

    trigger_color = non_white_colors[0]

    # Select the output pattern based on the identified color
    if trigger_color == 1:
        output_grid = pattern_plus
    elif trigger_color == 2:
        output_grid = pattern_t
    elif trigger_color == 3:
        output_grid = pattern_l
    else:
        # Handle unexpected color value
        print(f"Warning: Unexpected trigger color {trigger_color}.")
        output_grid = np.zeros((3, 3), dtype=int) # Default to empty grid

    return output_grid.tolist() # Return as list of lists per requirement