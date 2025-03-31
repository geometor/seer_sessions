import numpy as np

def find_horizontal_line(grid, color):
    """Finds the row index of a horizontal line of a specific color."""
    for r in range(grid.shape[0]):
        if np.all(grid[r, :] == color):
            return r
    return -1 # Indicate not found, though task examples guarantee it exists

def transform(input_grid):
    """
    Reflects the grid content vertically across the horizontal yellow line.
    The portion above the yellow line moves below it, and the portion below
    the yellow line moves above it. The yellow line itself remains in place.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Define the color of the reflection line
    reflection_line_color = 4 # yellow

    # Find the row index of the yellow horizontal line
    line_row_index = find_horizontal_line(input_array, reflection_line_color)
    
    # If no line is found (should not happen based on examples), return input
    if line_row_index == -1:
        # Or raise an error, depending on expected behavior for invalid inputs
        print("Warning: Reflection line not found.")
        return input_grid 

    # Extract the parts of the grid relative to the line
    # Part above the line
    grid_above = input_array[:line_row_index, :]
    # The line itself
    grid_line = input_array[line_row_index:line_row_index+1, :]
    # Part below the line
    grid_below = input_array[line_row_index+1:, :]

    # Construct the output grid by swapping the 'above' and 'below' parts
    # Place the 'below' part first (at the top of the output)
    # Then place the 'line'
    # Finally, place the 'above' part (at the bottom of the output)
    output_array = np.vstack((grid_below, grid_line, grid_above))

    # Convert the numpy array back to a list of lists for the required output format
    output_grid = output_array.tolist()

    return output_grid