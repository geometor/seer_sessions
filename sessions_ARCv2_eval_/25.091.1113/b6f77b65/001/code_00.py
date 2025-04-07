import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by conditionally shifting its content based on the color of the top-left pixel.

    1. Identifies the color (C) of the pixel at [0, 0].
    2. Determines a vertical (delta_row) and horizontal (delta_col) shift based on C:
        - Maroon (9): (0, 0) shift
        - Yellow (4): (3, 2) shift (down 3, right 2)
        - Magenta (6): (3, 1) shift (down 3, right 1)
        - Orange (7): (3, 1) shift (down 3, right 1)
        - Other colors: (0, 0) shift (default)
    3. Initializes an output grid of the same size, filled with background color (0).
    4. Places the original top-left pixel color C at [0, 0] in the output grid.
    5. Iterates through all other pixels in the input grid.
    6. If a pixel is not background color, calculates its new position by adding the shift vector.
    7. If the new position is within the grid bounds, copies the pixel color to the output grid at the new position.
    8. Returns the transformed output grid.
    """
    
    input_grid_np = np.array(input_grid)
    height, width = input_grid_np.shape

    # Initialize output grid with background color (0)
    output_grid = np.zeros_like(input_grid_np)

    # Get the color of the control pixel at [0, 0]
    control_color = input_grid_np[0, 0]

    # Determine the shift vector based on the control color
    delta_row, delta_col = 0, 0
    if control_color == 9:  # Maroon
        delta_row, delta_col = 0, 0
    elif control_color == 4:  # Yellow
        delta_row, delta_col = 3, 2
    elif control_color == 6:  # Magenta
        delta_row, delta_col = 3, 1
    elif control_color == 7:  # Orange
        delta_row, delta_col = 3, 1
    # Default shift is (0, 0) for any other color, handled by initialization

    # Place the control pixel in the output grid (it doesn't move)
    output_grid[0, 0] = control_color

    # Iterate through the input grid to shift other non-background pixels
    for r in range(height):
        for c in range(width):
            # Skip the control pixel itself as it's already placed
            if r == 0 and c == 0:
                continue

            input_color = input_grid_np[r, c]

            # Only shift non-background pixels
            if input_color != 0:
                # Calculate the new position
                new_r = r + delta_row
                new_c = c + delta_col

                # Check if the new position is within the grid bounds
                if 0 <= new_r < height and 0 <= new_c < width:
                    # Place the pixel color in the output grid at the new position
                    output_grid[new_r, new_c] = input_color

    return output_grid.tolist()