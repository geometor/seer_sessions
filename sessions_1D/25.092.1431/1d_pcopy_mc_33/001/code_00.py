import copy

"""
Transforms a single-row grid by identifying pixels of a non-white color C that are horizontally surrounded by white pixels (0 C 0). 
Each such identified pattern (0 C 0) is replaced in the output by a sequence of three pixels of color C (C C C). 
Pixels not involved in this specific replacement pattern are copied directly from the input to the output.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid. 
                                     Expected to have only one row.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    # Ensure the input is a list of lists (grid format)
    if not isinstance(input_grid, list) or not all(isinstance(row, list) for row in input_grid):
        raise TypeError("Input grid must be a list of lists.")
        
    # Expecting a single row grid based on examples
    if len(input_grid) != 1:
         # Or handle multi-row grids if needed, but examples suggest 1 row
        print("Warning: Expected single-row grid based on examples.") # Or raise error
        # For now, process only the first row if multiple exist
        # return input_grid # Or specific error handling

    input_row = input_grid[0]
    width = len(input_row)

    # Initialize output_row as a copy of the input_row
    # We modify this copy based on the patterns found in the *original* input_row
    output_row = list(input_row) 

    # Iterate through the input row, checking for the pattern (0, C, 0)
    # We need to look at triplets, so iterate from index 1 up to width-2
    for i in range(1, width - 1):
        # Get the triplet from the original input row
        p1 = input_row[i-1]
        p2 = input_row[i]
        p3 = input_row[i+1]

        # Check for the pattern: white, non-white, white
        if p1 == 0 and p2 != 0 and p3 == 0:
            # If the pattern is found, modify the output_row
            # Set the triplet in the output to be (C, C, C) where C is p2
            output_row[i-1] = p2
            output_row[i]   = p2
            output_row[i+1] = p2

    # Return the modified row wrapped in a list to match the grid format
    return [output_row]
