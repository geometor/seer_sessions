```python
import numpy as np
from collections import deque

"""
Identifies the background color (assumed to be the color of the corners).
Finds all rectangular blocks composed of a single, non-background color (solid blocks).
Selects only those solid blocks that are completely enclosed by a one-pixel thick border of the background color.
Constructs an output grid containing only these selected blocks and their background borders, preserving their relative positions.
The output grid dimensions are adjusted to tightly fit the selected content.
"""

def get_background_color(grid):
    """
    Determines the background color, assuming it's the color of the top-left corner.
    """
    return grid[0][0]

def find_solid_blocks(grid_np, bg_color):
    """
    Finds all contiguous blocks of a single non-background color.

    Args:
        grid_np (np.array): The input grid as a numpy array.
        bg_color (int): The background color.

    Returns:
        list: A list of tuples, where each tuple represents a solid block:
              (color, min_row, max_row, min_col, max_col)
    """
    height, width = grid_np.shape
    visited = np.zeros_like(grid_np, dtype=bool)
    blocks = []

    for r in range(height):
        for c in range(width):
            if not visited[r, c] and grid_np[r, c] != bg_color:
                color = grid_np[r, c]
                min_r, max_r = r, r
                min_c, max_c = c, c
                q = deque([(r, c)])
                visited[r, c] = True
                is_solid = True
                block_pixels = set([(r,c)])

                while q:
                    curr_r, curr_c = q.popleft()
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < height and 0 <= nc < width:
                            if not visited[nr, nc]:
                                if grid_np[nr, nc] == color:
                                    visited[nr, nc] = True
                                    q.append((nr, nc))
                                    block_pixels.add((nr, nc))
                                elif grid_np[nr, nc] != bg_color:
                                    # Found a different non-background color adjacent, not solid?
                                    # Revisit: This BFS finds contiguous areas, need to check rectangular shape later.
                                    pass
                        
                # Check if the found contiguous area forms a solid rectangle
                is_rectangle = True
                if (max_r - min_r + 1) * (max_c - min_c + 1) != len(block_pixels):
                    is_rectangle = False
                else:
                    for br in range(min_r, max_r + 1):
                        for bc in range(min_c, max_c + 1):
                            if grid_np[br, bc] != color:
                                is_rectangle = False
                                break
                        if not is_rectangle:
                            break

                if is_rectangle:
                    blocks.append((color, min_r, max_r, min_c, max_c))
                    # Mark the whole rectangle as visited to avoid redundant checks
                    visited[min_r:max_r+1, min_c:max_c+1] = True


    return blocks


def is_background_bordered(grid_np, bg_color, min_r, max_r, min_c, max_c):
    """
    Checks if a block is surrounded by a 1-pixel border of the background color.

    Args:
        grid_np (np.array): The input grid as a numpy array.
        bg_color (int): The background color.
        min_r, max_r, min_c, max_c (int): Bounding box of the solid block.

    Returns:
        bool: True if the block is properly bordered, False otherwise.
    """
    height, width = grid_np.shape
    
    # Define the border coordinates
    border_min_r = max(0, min_r - 1)
    border_max_r = min(height - 1, max_r + 1)
    border_min_c = max(0, min_c - 1)
    border_max_c = min(width - 1, max_c + 1)

    for r in range(border_min_r, border_max_r + 1):
        for c in range(border_min_c, border_max_c + 1):
            # Skip pixels inside the block itself
            if min_r <= r <= max_r and min_c <= c <= max_c:
                continue
            
            # Check if the border pixel is the background color
            if grid_np[r, c] != bg_color:
                return False
                
    # Ensure the block is not touching the actual grid edge if border check passed
    # This means the border derived above must actually *be* a border
    if min_r == 0 or max_r == height - 1 or min_c == 0 or max_c == width - 1:
         # Check if the border check passed *because* it was at the edge
         # If min_r is 0, border_min_r is 0. We need to ensure the check didn't falsely pass.
         # Re-think: The loop condition correctly handles edges. If a border pixel is checked
         # and it's on the grid boundary, it still must be bg_color. The logic seems correct.
         pass


    return True


def transform(input_grid):
    """
    Filters the input grid to keep only solid blocks surrounded by a background border.
    
    1. Identify the background color.
    2. Find all solid rectangular blocks of non-background colors.
    3. Check each block for a complete 1-pixel background border.
    4. Determine the bounding box of the selected blocks including their borders.
    5. Construct the output grid containing only these bordered blocks.
    """
    
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    
    # 1. Identify background color
    bg_color = get_background_color(input_grid_np)
    
    # 2. Find solid blocks
    solid_blocks = find_solid_blocks(input_grid_np, bg_color)

    # 3. Filter blocks that are background-bordered
    selected_regions = [] # Stores (border_min_r, border_max_r, border_min_c, border_max_c)
    for color, min_r, max_r, min_c, max_c in solid_blocks:
        if is_background_bordered(input_grid_np, bg_color, min_r, max_r, min_c, max_c):
            # Calculate border coordinates, ensuring they stay within grid bounds
            b_min_r = max(0, min_r - 1)
            b_max_r = min(height - 1, max_r + 1)
            b_min_c = max(0, min_c - 1)
            b_max_c = min(width - 1, max_c + 1)
            selected_regions.append((b_min_r, b_max_r, b_min_c, b_max_c))

    # Handle case where no blocks are selected
    if not selected_regions:
        # Returning a 1x1 background pixel grid as a default
        # Adjust if requirements differ (e.g., empty grid, error)
        return [[bg_color]]

    # 4. Determine overall bounding box for the output
    min_overall_r = min(r[0] for r in selected_regions)
    max_overall_r = max(r[1] for r in selected_regions)
    min_overall_c = min(r[2] for r in selected_regions)
    max_overall_c = max(r[3] for r in selected_regions)

    # 5. Construct the output grid
    output_height = max_overall_r - min_overall_r + 1
    output_width = max_overall_c - min_overall_c + 1
    
    # Initialize output grid with background color
    output_grid_np = np.full((output_height, output_width), bg_color, dtype=int)

    # Copy selected regions (including borders) from input to output
    for r1, r2, c1, c2 in selected_regions:
        # Calculate target coordinates in the output grid
        target_r1 = r1 - min_overall_r
        target_r2 = r2 - min_overall_r
        target_c1 = c1 - min_overall_c
        target_c2 = c2 - min_overall_c
        
        # Extract the region from the input grid
        region_to_copy = input_grid_np[r1 : r2 + 1, c1 : c2 + 1]
        
        # Place it into the output grid
        output_grid_np[target_r1 : target_r2 + 1, target_c1 : target_c2 + 1] = region_to_copy

    # Convert numpy array back to list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
```