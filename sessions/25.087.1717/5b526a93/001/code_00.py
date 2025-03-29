import numpy as np

"""
Identify all occurrences of the 3x3 blue (1) hollow square pattern 
(center is white (0)) in the input grid. Collect the unique row and 
column indices of the top-left corners of these patterns. Generate all 
possible top-left coordinates by taking the Cartesian product of the unique 
row and column sets. For each generated coordinate, if a blue pattern 
does not start at that location in the input grid, draw a 3x3 azure (8) 
hollow square pattern (center white (0)) at that location in the output grid. 
The output grid is initialized as a copy of the input grid.
"""

def find_pattern_locations(grid, pattern):
    """
    Finds all occurrences of a given pattern in the grid.

    Args:
        grid (np.array): The grid to search within.
        pattern (np.array): The pattern to search for.

    Returns:
        set: A set of (row, col) tuples representing the top-left corner
             of each found pattern instance.
    """
    locations = set()
    p_rows, p_cols = pattern.shape
    g_rows, g_cols = grid.shape
    
    for r in range(g_rows - p_rows + 1):
        for c in range(g_cols - p_cols + 1):
            subgrid = grid[r:r+p_rows, c:c+p_cols]
            if np.array_equal(subgrid, pattern):
                locations.add((r, c))
    return locations

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Identifies blue hollow squares, determines a target grid of locations based
    on their row/col coordinates, and fills empty target locations with
    azure hollow squares.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    
    # Define the source (blue) and target (azure) patterns
    # Note: The center is white (0), not the primary color.
    source_pattern = np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ], dtype=int)
    
    derived_pattern = np.array([
        [8, 8, 8],
        [8, 0, 8],
        [8, 8, 8]
    ], dtype=int)
    
    pattern_rows, pattern_cols = source_pattern.shape

    # 1. Identify all occurrences of the source blue pattern
    source_locations = find_pattern_locations(input_np, source_pattern)

    if not source_locations: # Handle case with no source patterns
        return input_grid 

    # 2. Record the unique row and column coordinates
    unique_rows = set(r for r, c in source_locations)
    unique_cols = set(c for r, c in source_locations)

    # 3. Generate all possible coordinate pairs (Cartesian product)
    target_locations = set()
    for r in unique_rows:
        for c in unique_cols:
            target_locations.add((r, c))
            
    # 4. Initialize output grid (already done with np.copy)

    # 5. Iterate through target locations and draw derived patterns if needed
    for r, c in target_locations:
        # Check if a source pattern already exists at this location
        if (r, c) not in source_locations:
            # Ensure the pattern fits within the grid boundaries
            if r + pattern_rows <= output_np.shape[0] and c + pattern_cols <= output_np.shape[1]:
                # Draw the derived (azure) pattern
                # Be careful only to overwrite pixels corresponding to the pattern's non-zero parts
                for i in range(pattern_rows):
                    for j in range(pattern_cols):
                         # Only change if the derived pattern pixel is not the background (0)
                         # This handles the hollow center correctly.
                        if derived_pattern[i, j] != 0: 
                           output_np[r + i, c + j] = derived_pattern[i, j]


    # Convert back to list of lists for the required output format
    output_grid = output_np.tolist()
    
    return output_grid
