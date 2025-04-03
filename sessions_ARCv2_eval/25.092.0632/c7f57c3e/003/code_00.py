import numpy as np
from collections import deque

"""
Transforms an input grid based on its background color.

1. Determine the dominant background color.

2. If the background is Yellow (4):
   a. Swap Green (3) and Azure (8), BUT with a modification for Azure blocks:
      - Original Green pixels become Azure.
      - For original Azure blocks:
        - Pixels at the minimum row index within the block become Red (2).
        - Other pixels within the block become Green (3).
   b. Red (2) pixels change to Azure (8) if they are adjacent (including diagonals)
      to an original Green pixel OR adjacent to another Red pixel that is also changing to Azure. This change propagates.

3. If the background is Green (3):
   a. Find the single Magenta (6) trigger pixel and change it to Green (3).
   b. Find all Yellow (4) pixels.
   c. Identify the Yellow pixel with the minimum row index (tie-break with min column index).
   d. Change this target Yellow pixel to Magenta (6).
   e. Change the pixel in the top row (row 0) in the same column as the target Yellow pixel to Magenta (6).
   f. For all *other* Yellow pixels:
      - If the Yellow pixel was isolated (no Yellow neighbors in the input), it remains Yellow.
      - If the Yellow pixel had Yellow neighbors (part of a block in the input), it changes to Green (3).

4. If the background is neither Yellow nor Green, return the input grid unchanged.
"""

def get_background_color(grid):
    """Determines the most frequent color in the grid, assuming it's the background."""
    colors, counts = np.unique(grid, return_counts=True)
    return colors[np.argmax(counts)]

def find_pixels(grid, color):
    """Finds the coordinates (row, col) of all pixels with the given color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def get_neighbors(r, c, height, width, connectivity=8):
    """Gets neighbor coordinates for a pixel (r, c)."""
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            # Skip diagonals if connectivity is 4
            if connectivity == 4 and abs(dr) + abs(dc) > 1:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def find_contiguous_blocks(grid, color):
    """Finds connected components (blocks) of a given color using BFS."""
    height, width = grid.shape
    visited = set()
    blocks = []
    
    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and (r, c) not in visited:
                block = []
                q = deque([(r, c)])
                visited.add((r, c))
                block.append((r, c))
                
                while q:
                    row, col = q.popleft()
                    # Use 8-connectivity for finding blocks
                    for nr, nc in get_neighbors(row, col, height, width, connectivity=8):
                         if grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            block.append((nr, nc))
                if block:
                    blocks.append(block)
    return blocks

def is_isolated(r, c, grid, color):
    """Checks if a pixel (r, c) of a given color has any neighbors of the same color."""
    height, width = grid.shape
    for nr, nc in get_neighbors(r, c, height, width, connectivity=8):
        if grid[nr, nc] == color:
            return False
    return True

def transform(input_grid):
    """
    Applies the transformation rules based on the background color.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # 1. Determine background color
    background_color = get_background_color(input_np)

    if background_color == 4: # Yellow background case
        original_green_locs = find_pixels(input_np, 3)
        original_red_locs = find_pixels(input_np, 2)
        original_azure_blocks = find_contiguous_blocks(input_np, 8)

        # 2a. Change original Green pixels to Azure
        for r, c in original_green_locs:
            output_np[r, c] = 8

        # 2a. Process original Azure blocks
        for block in original_azure_blocks:
            if not block: continue
            min_row = min(r for r, c in block)
            min_row_pixels = [(r, c) for r, c in block if r == min_row]
            
            for r, c in block:
                if (r, c) in min_row_pixels:
                    output_np[r, c] = 2 # Min row pixels become Red
                else:
                    output_np[r, c] = 3 # Other pixels become Green

        # 2b. Propagating Red to Azure change
        red_to_change = set()
        red_locs_set = set(original_red_locs)
        original_green_locs_set = set(original_green_locs)
        
        # Initial set: Reds adjacent to original Greens
        for r, c in original_red_locs:
             for nr, nc in get_neighbors(r, c, height, width, connectivity=8):
                 if (nr, nc) in original_green_locs_set:
                     red_to_change.add((r, c))
                     break # No need to check other neighbors for this red pixel

        # Propagation loop
        while True:
            added_new = False
            newly_added = set()
            
            # Check reds NOT yet marked for change
            candidates = red_locs_set - red_to_change
            
            for r, c in candidates:
                 # Check if adjacent to a red ALREADY marked for change
                 is_adjacent_to_changing_red = False
                 for nr, nc in get_neighbors(r, c, height, width, connectivity=8):
                     if (nr, nc) in red_to_change:
                         is_adjacent_to_changing_red = True
                         break
                 if is_adjacent_to_changing_red:
                     newly_added.add((r, c))
                     added_new = True
            
            if not added_new:
                break # No more propagation
            
            red_to_change.update(newly_added) # Add newly found reds to the set

        # Apply the change for all identified Red pixels
        for r, c in red_to_change:
            output_np[r, c] = 8

    elif background_color == 3: # Green background case
        magenta_locs = find_pixels(input_np, 6)
        yellow_locs = find_pixels(input_np, 4)
        yellow_locs_set = set(yellow_locs)
        
        # 3a. Change trigger Magenta to Green
        if magenta_locs:
            trigger_loc = magenta_locs[0] # Assume single trigger
            output_np[trigger_loc[0], trigger_loc[1]] = 3

        if yellow_locs:
            # 3c. Find target Yellow (min row, then min col)
            target_yellow = min(yellow_locs, key=lambda x: (x[0], x[1]))
            target_r, target_c = target_yellow

            # 3d. Change target Yellow to Magenta
            output_np[target_r, target_c] = 6
            
            # 3e. Change top row pixel in target column to Magenta
            output_np[0, target_c] = 6

            # 3f. Process other Yellow pixels
            for r, c in yellow_locs:
                if (r, c) == target_yellow:
                    continue # Skip the target pixel itself
                
                # Check for yellow neighbors in the *input* grid
                has_yellow_neighbor = False
                for nr, nc in get_neighbors(r, c, height, width, connectivity=8):
                    if (nr, nc) in yellow_locs_set: # Check against original yellow locations
                         has_yellow_neighbor = True
                         break
                
                if has_yellow_neighbor:
                    # Part of a block -> change to Green
                    output_np[r, c] = 3
                else:
                    # Isolated -> remains Yellow (no change needed as output started as copy)
                    pass

    # 4. If background is neither Yellow nor Green, output_np remains a copy of input_np
    return output_np.tolist()