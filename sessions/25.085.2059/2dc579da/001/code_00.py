import numpy as np
from collections import Counter

"""
Identify the single horizontal line and single vertical line that form a cross in the input grid. 
Record their row index (r_cross), column index (c_cross), and color (C_cross).
Identify the single pixel in the grid whose color appears exactly once (unique_pixel). Record its coordinates (r_unique, c_unique).
Determine which of the four quadrants defined by the cross contains the unique_pixel by comparing its coordinates to the cross's intersection point.
Extract the subgrid corresponding to the determined quadrant, excluding the cross lines themselves.
The boundaries for extraction are:
- Top-Left: Rows 0 to r_cross-1, Columns 0 to c_cross-1.
- Top-Right: Rows 0 to r_cross-1, Columns c_cross+1 to Width-1.
- Bottom-Left: Rows r_cross+1 to Height-1, Columns 0 to c_cross-1.
- Bottom-Right: Rows r_cross+1 to Height-1, Columns c_cross+1 to Width-1.
This extracted subgrid is the output.
"""

def transform(input_grid):
    """
    Transforms the input grid by finding a cross shape, locating a unique pixel, 
    and extracting the quadrant containing that unique pixel.
    """
    grid = np.array(input_grid, dtype=int)
    H, W = grid.shape
    
    r_cross = -1
    c_cross = -1
    C_cross = -1

    # 1. Identify_Cross: Find the row and column of the cross
    # Find horizontal line
    for r in range(H):
        if len(np.unique(grid[r, :])) == 1:
            # Check if this line spans the whole width
            # (This check is implicitly true if len(unique)==1 for a full row)
            # Potential horizontal line found
            r_cross_candidate = r
            break # Assume only one such line based on examples
    
    # Find vertical line
    for c in range(W):
         if len(np.unique(grid[:, c])) == 1:
            # Check if this line spans the whole height
            # (Implicitly true if len(unique)==1 for a full column)
            # Potential vertical line found
            c_cross_candidate = c
            break # Assume only one such line
            
    # Confirm cross intersection and color
    if r_cross_candidate != -1 and c_cross_candidate != -1:
         # Check if the colors match at the intersection
         if grid[r_cross_candidate, 0] == grid[0, c_cross_candidate]:
             # Check if the intersection pixel has the same color
             if grid[r_cross_candidate, c_cross_candidate] == grid[r_cross_candidate, 0]:
                r_cross = r_cross_candidate
                c_cross = c_cross_candidate
                C_cross = grid[r_cross, c_cross]
             else:
                 # This handles cases where lines might exist but don't form a consistent cross
                 # based on the problem description, this shouldn't happen for valid inputs.
                 # Fallback logic might be needed if assumptions are wrong.
                 pass 
         else:
            # Colors of candidate lines don't match, invalid cross structure?
            # Based on problem examples, this shouldn't happen.
            pass

    if r_cross == -1 or c_cross == -1:
        # Handle error: Cross not found (shouldn't happen based on examples)
        return [] # Or raise an error


    # 2. Identify_Unique_Pixel: Find the pixel appearing exactly once
    color_counts = Counter(grid.flatten())
    C_unique = -1
    r_unique = -1
    c_unique = -1
    
    for color, count in color_counts.items():
        if count == 1:
            # Found the unique color. Now find its location.
            # Note: The problem statement implies C_unique is different from C_cross and C_bg.
            # We don't explicitly check against C_cross here, but it works for the examples.
            # If C_cross could potentially be unique, this logic needs adjustment.
            C_unique = color
            coords = np.where(grid == C_unique)
            r_unique = coords[0][0]
            c_unique = coords[1][0]
            break

    if r_unique == -1:
        # Handle error: Unique pixel not found (shouldn't happen)
        return [] # Or raise an error

    # 3. Determine_Quadrant: Find which quadrant the unique pixel is in
    # 4. Define_Quadrant_Boundaries & 5. Extract_Subgrid
    output_grid = np.array([[]]) # Initialize

    if r_unique < r_cross and c_unique < c_cross:
        # Top-Left quadrant
        output_grid = grid[0:r_cross, 0:c_cross]
    elif r_unique < r_cross and c_unique > c_cross:
        # Top-Right quadrant
        output_grid = grid[0:r_cross, c_cross + 1:W]
    elif r_unique > r_cross and c_unique < c_cross:
        # Bottom-Left quadrant
        output_grid = grid[r_cross + 1:H, 0:c_cross]
    elif r_unique > r_cross and c_unique > c_cross:
        # Bottom-Right quadrant
        output_grid = grid[r_cross + 1:H, c_cross + 1:W]
    else:
        # Unique pixel is ON the cross line, which contradicts the premise.
        # Handle error or edge case if necessary.
         return [] # Or raise an error

    # Convert output numpy array back to list of lists
    return output_grid.tolist()