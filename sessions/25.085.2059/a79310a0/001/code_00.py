import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. Initialize the output grid as a copy of the input grid, but replace all azure (8) pixels with white (0) pixels.
    2. Identify all pixels in the input grid that have the color azure (8).
    3. For each identified azure pixel at coordinates (row, column):
        a. Calculate the new row coordinate by adding 1 to the original row coordinate (row + 1).
        b. Ensure the new row coordinate is within the bounds of the grid height.
        c. If the new position (row + 1, column) is within the grid bounds, change the color of the pixel at this position in the output grid to red (2).
    """

    # Convert input_grid to a numpy array for easier manipulation
    np_input = np.array(input_grid, dtype=int)
    height, width = np_input.shape

    # Create an output grid initialized with the background color (white, 0)
    # We will copy non-azure pixels first, then draw the transformed azure pixels
    output_grid = np.zeros_like(np_input)

    # Store the locations and new color for the moved pixels
    pixels_to_draw = []

    # Iterate through the input grid
    for r in range(height):
        for c in range(width):
            # Get the color of the current pixel
            color = np_input[r, c]

            # Check if the pixel is azure (8)
            if color == 8:
                # Calculate the new row position (move down by 1)
                new_r = r + 1
                # Check if the new position is within the grid bounds
                if new_r < height:
                    # Add the new position and color (red, 2) to the list
                    pixels_to_draw.append(((new_r, c), 2))
            else:
                # If the pixel is not azure, copy its color to the output grid
                output_grid[r, c] = color

    # Draw the moved and recolored pixels onto the output grid
    # This ensures they overwrite any background pixels at the target locations
    for pos, color in pixels_to_draw:
        output_grid[pos] = color

    # Convert the numpy array back to a list of lists before returning
    return output_grid.tolist()