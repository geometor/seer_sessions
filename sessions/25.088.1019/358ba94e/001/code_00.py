import numpy as np

"""
Identify the primary non-white color in the input grid. 
Iterate through all possible 5x5 subgrids within the input grid. 
For each 5x5 subgrid, count the number of pixels matching the primary non-white color. 
Select the 5x5 subgrid that contains the maximum count of these primary non-white pixels. 
If multiple subgrids share the maximum count, the one encountered first during a top-to-bottom, left-to-right scan is chosen.
Output the selected 5x5 subgrid.
"""

def find_primary_color(grid):
    """Finds the first non-zero color in the grid."""
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                return grid[r, c]
    return 0 # Should not happen based on examples, but handles all-zero case

def transform(input_grid):
    """
    Extracts the 5x5 subgrid from the input grid that contains the 
    highest count of the primary non-white color.
    """
    # Convert input to numpy array for easier slicing and calculations
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # Check if grid is large enough to contain a 5x5 subgrid
    if height < 5 or width < 5:
        # Cannot extract a 5x5 grid, return empty or handle as error
        # Based on examples, input is always larger. Returning None for now.
        return None 

    # Identify the primary non-white color used in the patterns
    primary_color = find_primary_color(grid)
    if primary_color == 0:
         # Handle case where only background color is present
         # Return a 5x5 grid of zeros? Or None? Let's assume valid input.
         # Based on examples, a primary color always exists.
         # For robustness, maybe return a 5x5 zero grid if desired.
         # Let's stick to the assumption derived from examples.
         pass


    # Initialize variables to track the best subgrid found so far
    max_count = -1  # Start with -1 to ensure any valid count is higher
    best_subgrid = None

    # Iterate through all possible top-left corners (r, c) of a 5x5 subgrid
    for r in range(height - 4):  # Max row index is height - 5
        for c in range(width - 4):  # Max col index is width - 5
            
            # Extract the current 5x5 subgrid
            subgrid = grid[r:r+5, c:c+5]
            
            # Count the number of primary color pixels in this subgrid
            current_count = np.sum(subgrid == primary_color)
            
            # If this subgrid has more primary color pixels than the best one found so far
            if current_count > max_count:
                # Update the maximum count
                max_count = current_count
                # Store this subgrid as the new best
                best_subgrid = subgrid

    # Return the 5x5 subgrid that had the highest count of the primary color
    # If best_subgrid is still None (e.g., input smaller than 5x5 or no primary color found)
    # this would return None. However, based on task constraints and examples, 
    # a valid best_subgrid should always be found.
    return best_subgrid.tolist() # Convert back to list of lists if required by framework