import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Identifies 'U' shapes (a 3-wide horizontal bar of a non-zero digit N with two
    vertical legs of N below the ends) in the input grid. For each 'U' shape found,
    places a marker '4' in the last row of the grid, in the column corresponding 
    to the 'gap' of the 'U' (the middle column of the shape). The rest of the 
    output grid remains identical to the input grid.
    """

    # Create a deep copy of the input grid to avoid modifying the original
    output_grid = copy.deepcopy(input_grid)
    
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return output_grid # Handle empty grid case
    width = len(input_grid[0])
    if width == 0:
        return output_grid # Handle empty row case

    # Define the last row index
    last_row_index = height - 1

    # Iterate through each possible top-left corner (r, c) for a U shape
    # We only need to check up to height-2 and width-3 to fit the 3x2 U shape pattern
    for r in range(height - 1): 
        for c in range(width - 2):
            
            # Check for the start of a potential U shape (non-zero digit N)
            n = input_grid[r][c]
            if n != 0:
                # Check if the pattern matches the U shape definition
                # Horizontal bar: (r, c), (r, c+1), (r, c+2) all equal N
                # Vertical legs: (r+1, c), (r+1, c+2) all equal N
                if (input_grid[r][c+1] == n and
                    input_grid[r][c+2] == n and
                    input_grid[r+1][c] == n and
                    input_grid[r+1][c+2] == n):
                    
                    # If a U shape is found, identify the gap column
                    gap_column_index = c + 1
                    
                    # Place the marker '4' in the output grid
                    # Location: last row, gap column
                    if last_row_index >= 0 and 0 <= gap_column_index < width:
                         output_grid[last_row_index][gap_column_index] = 4

    # Return the modified grid
    return output_grid