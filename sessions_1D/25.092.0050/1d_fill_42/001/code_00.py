import numpy as np

"""
Identify the non-white color present in the input grid. 
Find the leftmost and rightmost indices of this color.
Create an output grid of the same size, initially white.
Fill the segment between the leftmost and rightmost indices (inclusive) in the output grid with the identified non-white color.
"""

def transform(input_grid):
    """
    Fills the segment between two marker pixels of the same color in a 1D grid.

    Args:
        input_grid (list): A list representing a single row grid.

    Returns:
        list: The transformed grid with the segment filled.
    """
    # Convert input to numpy array for easier manipulation
    # Assuming input_grid is a list of lists representing rows, 
    # but for this task, it's effectively a single row.
    input_row = np.array(input_grid[0])
    
    # Initialize output_grid as a list of lists with the same dimensions, filled with white (0)
    rows, cols = 1, len(input_row) # Get dimensions from the input row
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)] # Create the base output grid structure
    output_row = np.array(output_grid[0]) # Work with the numpy array representation

    # 1. Identify the non-white color
    fill_color = 0
    for pixel in input_row:
        if pixel != 0:
            fill_color = pixel
            break # Found the color, no need to continue

    # Check if a non-white color was found (handles edge case of all white input)
    if fill_color == 0:
        return output_grid # Return the all-white grid if no non-white pixel found

    # 2. Find the indices of the fill_color
    indices = [i for i, pixel in enumerate(input_row) if pixel == fill_color]

    # Check if exactly two markers were found as per task description
    if len(indices) < 2:
         # If only one marker, just copy it to output (or handle as per ambiguity, copying seems reasonable)
         if len(indices) == 1:
             output_row[indices[0]] = fill_color
             output_grid[0] = output_row.tolist()
             return output_grid
         else: # No markers found (already handled by fill_color check, but good practice)
            return output_grid


    # 3. Find the leftmost (start) and rightmost (end) indices
    start_index = min(indices)
    end_index = max(indices)

    # 4. Fill the segment in the output row
    # Iterate from start_index to end_index (inclusive)
    for i in range(start_index, end_index + 1):
        output_row[i] = fill_color

    # Update the output_grid list structure with the modified row
    output_grid[0] = output_row.tolist()

    # 5. Return the modified output grid
    return output_grid