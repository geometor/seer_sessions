import copy

"""
Identifies a single contiguous horizontal line of a non-white color (1-9) in the input grid (assumed to be 1xN).
Shifts this line 3 positions to the right in the output grid, maintaining its color and length.
The rest of the output grid is filled with the background color (white, 0).
The input line is assumed to start at index 1 based on the training examples.
"""

def find_line_properties(grid_row):
    """
    Finds the start index, color, and length of the first non-white horizontal line segment.

    Args:
        grid_row (list): A list representing the single row of the grid.

    Returns:
        tuple: (start_index, color, length) or (None, None, None) if no line is found.
    """
    start_index = -1
    color = 0
    length = 0
    
    for i, pixel in enumerate(grid_row):
        if pixel != 0:  # Found the start of a potential line
            start_index = i
            color = pixel
            length = 1
            # Continue to find the end of this contiguous segment
            for j in range(i + 1, len(grid_row)):
                if grid_row[j] == color:
                    length += 1
                else:
                    break # End of the line segment
            return start_index, color, length # Return after finding the first line
            
    return None, None, None # No non-white pixel found

def transform(input_grid):
    """
    Transforms the input grid by shifting the horizontal line 3 positions to the right.

    Args:
        input_grid (list): A list of lists representing the input grid (expected 1xN).

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    # Assume input is a 1xN grid
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])
    
    # Initialize output_grid with background color (0)
    # Use deepcopy to ensure the original input_grid isn't modified if we were to copy it
    # output_grid = copy.deepcopy(input_grid) 
    # for r in range(rows):
    #     for c in range(cols):
    #         output_grid[r][c] = 0 
    # More direct initialization:
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]


    # We only expect one row based on examples
    input_row = input_grid[0]
    output_row = output_grid[0]

    # Find the line in the input row
    start_index_input, line_color, line_length = find_line_properties(input_row)

    # Check if a line was found
    if start_index_input is not None:
        # Define the shift amount
        shift_distance = 3
        
        # Calculate the new starting position
        start_index_output = start_index_input + shift_distance

        # Draw the line in the output grid row
        for i in range(line_length):
            current_col = start_index_output + i
            # Ensure we don't write outside the grid boundaries
            if 0 <= current_col < cols:
                output_row[current_col] = line_color
                
    return output_grid