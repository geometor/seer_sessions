import numpy as np
from collections import Counter

"""
Identify pixels completely enclosed by an object of a different color (where the enclosing object's color is not the background color). 
Replace the enclosed pixel with the background color.
Project the original color (C1) of the enclosed pixel onto a specific edge of the grid:
- Blue(1) or Green(3) -> Top edge, same column.
- Red(2) -> Left edge, same row.
- Azure(8) -> Right edge, same row.
- Magenta(6) -> Special handling: Fill the entire bottom row with Magenta(6), and place Magenta(6) pixels periodically down the original column below the enclosed pixel's location (every 2 rows, starting r+2, stopping before the last row).
Apply the projections to the output grid.
If projections land on both the Top and Left edges, set the top-left corner (0, 0) to White(0).
If projections land on both the Top and Right edges, set the top-right corner (0, width-1) to White(0).
Pixels not otherwise modified remain unchanged.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    # Using Counter is slightly more direct for finding the most common element
    counts = Counter(grid.flatten())
    background_color = counts.most_common(1)[0][0]
    return background_color

def find_contained_pixels(grid, background_color):
    """Finds pixels fully enclosed by 8 neighbors of the same non-background color."""
    height, width = grid.shape
    contained = []
    # Iterate only over pixels that *can* have 8 neighbors (1 to height-2, 1 to width-2)
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            center_color = grid[r, c]
            
            # Optimization: If center pixel is background, it cannot be a contained pixel C1
            if center_color == background_color:
                continue

            # Get potential container color C2 from the first neighbor (top-left)
            container_color = grid[r-1, c-1] 

            # C2 cannot be the background color
            if container_color == background_color:
                continue
                
            # C2 cannot be the same as the center color C1
            if container_color == center_color:
                continue

            # Check if all 8 neighbors match the potential container color C2
            all_neighbors_match = True
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    # Inner loop guarantees neighbors are within bounds
                    if grid[r + dr, c + dc] != container_color:
                        all_neighbors_match = False
                        break
                if not all_neighbors_match:
                    break
            
            # If all neighbors match and meet criteria, it's a contained pixel
            if all_neighbors_match:
                # Store C1 (center color) and its location (r, c)
                contained.append({'C1': center_color, 'r': r, 'c': c}) 
                
    return contained

def transform(input_grid):
    """
    Applies the transformation rule based on contained pixels and projections.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    height, width = output_grid.shape

    # Determine the background color
    background_color = find_background_color(input_grid_np)

    # Find all contained pixels
    contained_pixels = find_contained_pixels(input_grid_np, background_color)

    # Store details for standard projections
    projections_to_make = []
    # Track which edges received standard projections for intersection checks
    projected_top = False
    projected_left = False
    projected_right = False

    # Process each contained pixel
    for item in contained_pixels:
        C1, r, c = item['C1'], item['r'], item['c']

        # Step 1: Replace the contained pixel with the background color
        output_grid[r, c] = background_color

        # Step 2: Determine projection target or special actions based on C1
        if C1 == 1 or C1 == 3: # Blue (1) or Green (3) -> Top edge
            target_r, target_c = 0, c
            projections_to_make.append({'color': C1, 'r': target_r, 'c': target_c})
            projected_top = True # Mark that a projection hit the top edge
        elif C1 == 2: # Red (2) -> Left edge
            target_r, target_c = r, 0
            projections_to_make.append({'color': C1, 'r': target_r, 'c': target_c})
            projected_left = True # Mark that a projection hit the left edge
        elif C1 == 8: # Azure (8) -> Right edge
            target_r, target_c = r, width - 1
            projections_to_make.append({'color': C1, 'r': target_r, 'c': target_c})
            projected_right = True # Mark that a projection hit the right edge
        elif C1 == 6: # Magenta (6) -> Special rules
            # Action 1: Fill the entire bottom row with Magenta (6)
            if height > 0: # Check if grid has rows
                output_grid[height - 1, :] = 6
            
            # Action 2: Place Magenta (6) periodically down the original column 'c'
            # Start at r+2, step by 2, stop *before* the last row (height-1)
            for row_idx in range(r + 2, height - 1, 2):
                 # The range ensures row_idx is always < height - 1
                 output_grid[row_idx, c] = 6
            # Note: Magenta doesn't add to projections_to_make and doesn't trigger corner intersections itself

    # Step 3: Apply the standard projections collected earlier
    for proj in projections_to_make:
        # Check bounds just in case, though logic should ensure validity
        if 0 <= proj['r'] < height and 0 <= proj['c'] < width:
            output_grid[proj['r'], proj['c']] = proj['color']

    # Step 4: Handle corner intersections caused by standard projections
    # Check Top-Left corner
    if projected_top and projected_left:
        if 0 < height and 0 < width: # Ensure grid is at least 1x1
             output_grid[0, 0] = 0 # White

    # Check Top-Right corner
    if projected_top and projected_right:
        if 0 < height and width > 0: # Ensure grid has a top-right corner index
            output_grid[0, width - 1] = 0 # White

    return output_grid.tolist() # Return as list of lists