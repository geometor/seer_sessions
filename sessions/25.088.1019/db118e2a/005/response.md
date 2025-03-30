```python
import numpy as np
from typing import List, Tuple

"""
Transforms the input grid by:
1. Identifying the background color (from corners), frame color (adjacent to background border), and core object pixels (neither background nor frame).
2. Extracting the 'core pattern' defined by the bounding box of the core object pixels.
3. Constructing a 'placed pattern' by adding a border around the 'core pattern'. The border corners use the background color, and the border sides use the frame color.
4. Creating a 15x15 output grid filled with the background color.
5. Placing the 'constructed pattern' onto the output grid twice, at fixed top-left coordinates (2, 2) and (8, 8).
"""

def find_bounding_box(coords: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """Finds the minimum bounding box containing all coordinates."""
    if not coords:
        return 0, 0, -1, -1 # Indicate empty box if no coords
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_r = max(r for r, c in coords)
    max_c = max(c for r, c in coords)
    return min_r, min_c, max_r, max_c

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid: The input grid as a list of lists.

    Returns:
        The transformed 15x15 output grid as a list of lists.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    h, w = input_grid_np.shape

    # --- 1. Identify Input Components ---
    
    # Assume background color is at the corners
    background_color = input_grid_np[0, 0]
    
    # Assume frame color is adjacent to the background border.
    # Check multiple locations in case of thin inputs.
    frame_color = -1 # Initialize with invalid color
    candidates = [(0, 1), (1, 0), (1, 1)]
    for r, c in candidates:
        if 0 <= r < h and 0 <= c < w and input_grid_np[r, c] != background_color:
            frame_color = input_grid_np[r, c]
            break
    # If frame color wasn't found above (e.g., 1xN grid), check further
    if frame_color == -1:
         if h > 1 and w > 1 and input_grid_np[h-1, w-2] != background_color:
             frame_color = input_grid_np[h-1, w-2]
         elif h > 1 and w > 1 and input_grid_np[h-2, w-1] != background_color:
             frame_color = input_grid_np[h-2, w-1]
         # Add more fallbacks if needed, though examples suggest frame is near TL corner

    # Identify core object pixels (not background, not frame)
    core_coords = []
    for r in range(h):
        for c in range(w):
            if input_grid_np[r, c] != background_color and input_grid_np[r, c] != frame_color:
                core_coords.append((r, c))

    # --- 2. Extract Core Pattern ---
    
    if not core_coords:
         # Handle cases with no core objects - based on examples this shouldn't happen,
         # but safest to define behavior. Let's assume a 1x1 core of background color.
         min_r, min_c, max_r, max_c = 0, 0, 0, 0
         core_pattern = np.array([[background_color]], dtype=int) # Default 1x1
    else:
        min_r, min_c, max_r, max_c = find_bounding_box(core_coords)
        core_pattern = input_grid_np[min_r : max_r + 1, min_c : max_c + 1]

    core_h, core_w = core_pattern.shape

    # --- 3. Construct Placed Pattern ---
    
    placed_h = core_h + 2
    placed_w = core_w + 2
    # Initialize with background color, makes border filling easier
    placed_pattern = np.full((placed_h, placed_w), background_color, dtype=int)

    # Place core pattern in the center
    if core_h > 0 and core_w > 0:
        placed_pattern[1:-1, 1:-1] = core_pattern

    # Fill border sides (non-corners) with frame color
    if placed_h > 1: # Fill top/bottom sides
        placed_pattern[0, 1:-1] = frame_color
        placed_pattern[placed_h - 1, 1:-1] = frame_color
    if placed_w > 1: # Fill left/right sides
        placed_pattern[1:-1, 0] = frame_color
        placed_pattern[1:-1, placed_w - 1] = frame_color
        
    # Corners are already background_color due to initialization

    # --- 4. Initialize Output Grid ---
    
    output_h = 15
    output_w = 15
    output_grid = np.full((output_h, output_w), background_color, dtype=int)

    # --- 5. Place Constructed Pattern onto Output ---
    
    loc1_r, loc1_c = 2, 2
    loc2_r, loc2_c = 8, 8

    # Function to safely place a pattern onto a grid
    def place_subgrid(target_grid, subgrid, r_start, c_start):
        target_h, target_w = target_grid.shape
        sub_h, sub_w = subgrid.shape
        
        r_end = min(r_start + sub_h, target_h)
        c_end = min(c_start + sub_w, target_w)
        
        paste_h = r_end - r_start
        paste_w = c_end - c_start
        
        if paste_h > 0 and paste_w > 0:
            target_grid[r_start:r_end, c_start:c_end] = subgrid[:paste_h, :paste_w]

    # Place the first instance
    place_subgrid(output_grid, placed_pattern, loc1_r, loc1_c)

    # Place the second instance (will overwrite if overlap occurs)
    place_subgrid(output_grid, placed_pattern, loc2_r, loc2_c)

    return output_grid.tolist()
```