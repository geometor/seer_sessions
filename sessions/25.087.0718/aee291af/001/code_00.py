"""
Find all square subgrids within the input grid that meet specific criteria:
1. The border of the square subgrid must consist entirely of Azure (8) pixels.
2. All pixels within the square subgrid (including the border) must be either Azure (8) or Red (2).
Return the unique pattern found among these qualifying subgrids.
"""

import numpy as np

def check_pattern(grid):
    """
    Checks if a given grid meets the required pattern criteria.
    - Border must be all Azure (8).
    - Content must be only Azure (8) or Red (2).
    """
    rows, cols = grid.shape
    if rows != cols or rows < 2:  # Must be a square of at least size 2x2
        return False

    # Check border
    # Top row
    if not np.all(grid[0, :] == 8):
        return False
    # Bottom row
    if not np.all(grid[-1, :] == 8):
        return False
    # Left column (excluding corners already checked)
    if not np.all(grid[1:-1, 0] == 8):
        return False
    # Right column (excluding corners already checked)
    if not np.all(grid[1:-1, -1] == 8):
        return False

    # Check content (all pixels must be 8 or 2)
    allowed_colors = {8, 2}
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] not in allowed_colors:
                return False

    return True

def transform(input_grid):
    """
    Finds the unique square subgrid pattern meeting border and content criteria.
    """
    input_grid_np = np.array(input_grid)
    height, width = input_grid_np.shape
    qualifying_patterns = []

    # Iterate through possible square sizes (from min size 2 up to min dimension)
    for size in range(2, min(height, width) + 1):
        # Iterate through all possible top-left starting positions
        for r in range(height - size + 1):
            for c in range(width - size + 1):
                # Extract the candidate subgrid
                candidate_subgrid = input_grid_np[r:r+size, c:c+size]

                # Check if the candidate meets the criteria
                if check_pattern(candidate_subgrid):
                    # Store the found pattern (convert back to list of lists for consistency if needed later)
                    # Since examples suggest all found patterns are identical, we might optimize
                    # but storing all and picking first is safer for now.
                    qualifying_patterns.append(candidate_subgrid.tolist()) 

                    # Optimization: Based on the observation that all qualifying patterns
                    # within a single input are identical, we can potentially return
                    # the first one found. Let's stick to finding all first.
                    # If we find one, we can likely return it immediately.
                    # return candidate_subgrid.tolist() # Uncomment for immediate return

    # After checking all possibilities, return the first qualifying pattern found.
    # The problem implies there will be at least one, and all found will be identical.
    if qualifying_patterns:
        # You could add a check here to ensure all found patterns are indeed identical
        # assert all(np.array_equal(np.array(p), np.array(qualifying_patterns[0])) for p in qualifying_patterns)
        return qualifying_patterns[0]
    else:
        # Should not happen based on examples, but return empty or original as fallback?
        # Returning an empty list might be appropriate.
        return [] # Or handle error appropriately
