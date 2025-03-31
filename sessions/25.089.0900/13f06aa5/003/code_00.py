import numpy as np
from collections import Counter

"""
Identify isolated pixels (triggers), replace them with the background color, and project their original color onto a grid edge based on the color. 
A trigger pixel is a non-background pixel where none of its 8 neighbors share its color.
Projection Rules:
- Blue(1) or Green(3) -> Top edge, same column.
- Red(2) -> Left edge, same row.
- Azure(8) -> Right edge, same row.
- Magenta(6) -> Special handling: Fill the entire bottom row with Magenta(6), and place Magenta(6) pixels periodically down the original column below the trigger pixel's location (every 2 rows, starting r+2, stopping before the last row).
Apply standard projections after finding all triggers.
Handle corner intersections: If standard projections land on both Top and Left edges, set top-left (0,0) to White(0). If on Top and Right, set top-right (0, width-1) to White(0).
Pixels not otherwise modified remain unchanged.
"""

def find_background_color(grid_np):
    """Finds the most frequent color in the grid."""
    if grid_np.size == 0:
        return 0 # Default for empty grid
    counts = Counter(grid_np.flatten())
    # If multiple colors have the same max frequency, Counter returns one arbitrarily, which is fine.
    background_color = counts.most_common(1)[0][0]
    return background_color

def transform(input_grid):
    """
    Applies the transformation rule based on isolated trigger pixels and projections.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    height, width = output_grid.shape

    if height == 0 or width == 0:
        return [] # Handle empty grid case

    # Determine the background color
    background_color = find_background_color(input_grid_np)

    # Store details for standard projections
    projections_to_make = []
    # Track which edges received standard projections for intersection checks
    projected_top = False
    projected_left = False
    projected_right = False

    # Iterate through each pixel to find triggers
    for r in range(height):
        for c in range(width):
            C1 = input_grid_np[r, c]

            # Condition 1: Must not be background color
            if C1 == background_color:
                continue

            # Condition 2: Check neighbors - none should match C1
            is_trigger = True
            found_any_neighbor = False # Ensure pixel is not truly isolated in a 1x1 grid situation (unlikely in ARC but good practice)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc

                    # Check if neighbor is within bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        found_any_neighbor = True
                        if input_grid_np[nr, nc] == C1:
                            is_trigger = False
                            break # Found a neighbor with same color, not a trigger
            
            if not found_any_neighbor and (height > 1 or width > 1):
                 # If no neighbors exist (e.g., 1x1 grid) it cannot be isolated *from neighbors*
                 # We only consider pixels with potential neighbors as triggers based on this rule
                 is_trigger = False

            if is_trigger:
                 # If the loop completed without finding a neighbor of color C1, it's a trigger
                
                # Action 1: Replace trigger pixel with background color in output grid
                output_grid[r, c] = background_color

                # Action 2: Determine projection or special action based on C1
                if C1 == 1 or C1 == 3: # Blue (1) or Green (3) -> Top edge
                    target_r, target_c = 0, c
                    projections_to_make.append({'color': C1, 'r': target_r, 'c': target_c})
                    projected_top = True 
                elif C1 == 2: # Red (2) -> Left edge
                    target_r, target_c = r, 0
                    projections_to_make.append({'color': C1, 'r': target_r, 'c': target_c})
                    projected_left = True 
                elif C1 == 8: # Azure (8) -> Right edge
                    target_r, target_c = r, width - 1
                    projections_to_make.append({'color': C1, 'r': target_r, 'c': target_c})
                    projected_right = True 
                elif C1 == 6: # Magenta (6) -> Special rules (apply directly to output_grid)
                    # Fill the entire bottom row
                    if height > 0: 
                        output_grid[height - 1, :] = 6
                    
                    # Place Magenta periodically down the original column 'c'
                    # Start at r+2, step by 2, stop *before* the last row (height-1)
                    for row_idx in range(r + 2, height - 1, 2):
                        # Check col bounds just in case, though 'c' comes from valid coords
                        if 0 <= c < width:
                            output_grid[row_idx, c] = 6

    # Apply the collected standard projections after finding all triggers
    for proj in projections_to_make:
        # Check bounds just in case, though logic should ensure validity
        if 0 <= proj['r'] < height and 0 <= proj['c'] < width:
            output_grid[proj['r'], proj['c']] = proj['color']

    # Handle corner intersections caused by standard projections
    # Check Top-Left corner
    if projected_top and projected_left:
        if height > 0 and width > 0: # Ensure grid is at least 1x1
             output_grid[0, 0] = 0 # White

    # Check Top-Right corner
    if projected_top and projected_right:
        if height > 0 and width > 0: # Ensure grid has a top-right corner index
            output_grid[0, width - 1] = 0 # White

    return output_grid.tolist() # Return as list of lists