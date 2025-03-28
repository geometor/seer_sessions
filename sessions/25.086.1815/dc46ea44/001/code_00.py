import numpy as np

def find_horizontal_line(grid, color):
    """
    Finds the row index of the first complete horizontal line of a specific color.
    Returns the row index or -1 if no such line is found.
    """
    height, width = grid.shape
    for r in range(height):
        if all(grid[r, c] == color for c in range(width)):
            return r
    return -1

def transform(input_grid):
    """
    The transformation rule involves reflecting the part of the input grid below a
    horizontal yellow line upwards across that line.

    1. Identify the horizontal line composed entirely of yellow (4) pixels. This line
       acts as the axis of reflection.
    2. Create an output grid of the same dimensions as the input, initialized with
       the background color (orange, 7).
    3. Copy the yellow line from the input to the output grid at the same position.
    4. For every pixel in the input grid located *below* the yellow line, calculate
       its corresponding reflection position *above* the yellow line.
    5. Place the color of the input pixel at its calculated reflected position in the
       output grid.
    6. The area below the yellow line in the output grid remains the background color.
    """
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    background_color = 7
    reflection_line_color = 4

    # Initialize output grid with the background color
    output_array = np.full_like(input_array, background_color)

    # Find the row index of the yellow horizontal line
    yellow_row_index = find_horizontal_line(input_array, reflection_line_color)

    if yellow_row_index == -1:
        # Should not happen based on examples, but handle defensively
        print("Warning: Yellow reflection line not found.")
        return input_grid # Or return the background-filled grid

    # Copy the yellow line itself to the output
    output_array[yellow_row_index, :] = input_array[yellow_row_index, :]

    # Iterate through the rows below the yellow line in the input
    for r in range(yellow_row_index + 1, height):
        for c in range(width):
            # Calculate the reflected row index
            # Distance below line = r - yellow_row_index
            # Reflected row = yellow_row_index - (r - yellow_row_index)
            reflected_r = 2 * yellow_row_index - r

            # Ensure the reflected row is within the grid bounds (above or on the line)
            if 0 <= reflected_r < yellow_row_index:
                 # Only copy non-background pixels from below the line
                # Update: The examples show *all* pixels below the line are reflected,
                # including background pixels if they overwrite something else.
                # The background below the line in the output is set by the initial fill.
                output_array[reflected_r, c] = input_array[r, c]
            elif reflected_r == yellow_row_index:
                 # If reflection lands ON the yellow line, only overwrite if the source
                 # pixel is not the background color (to preserve the yellow line).
                 # This case seems unlikely given the reflection logic, but worth considering.
                 # Based on examples, nothing seems to reflect onto the yellow line itself.
                 pass # Do nothing, keep the yellow line pixel


    # Convert the numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid