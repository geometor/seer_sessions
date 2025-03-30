import numpy as np
from typing import List, Tuple

"""
Transforms the input grid by:
1. Identifying the background color (from corners) and frame color (adjacent to border).
2. Identifying 'object' pixels (neither background nor frame).
3. Determining a central point:
    - If object pixels exist, the center is the middle of their bounding box.
    - If no object pixels exist, the center is the geometric middle of the input grid.
4. Extracting a 3x3 'core pattern' from the input grid, centered at the determined point.
5. Constructing a 5x5 'placed pattern':
    - The center 3x3 area is the extracted 'core pattern'.
    - The border sides (non-corners) are filled with the frame color.
    - The border corners are filled with the background color.
6. Creating a 15x15 output grid filled with the background color.
7. Placing the 5x5 'placed pattern' onto the output grid twice, at fixed top-left coordinates (2, 2) and (8, 8).
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

def place_subgrid(target_grid: np.ndarray, subgrid: np.ndarray, r_start: int, c_start: int):
    """Safely places a subgrid onto a target grid, handling boundary clipping."""
    target_h, target_w = target_grid.shape
    sub_h, sub_w = subgrid.shape
    
    r_end = min(r_start + sub_h, target_h)
    c_end = min(c_start + sub_w, target_w)
    
    paste_h = r_end - r_start
    paste_w = c_end - c_start
    
    if paste_h > 0 and paste_w > 0:
        target_grid[r_start:r_end, c_start:c_end] = subgrid[:paste_h, :paste_w]


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

    # --- 1. Identify Colors ---
    background_color = input_grid_np[0, 0]
    
    # Find frame color (look adjacent to background border)
    frame_color = -1 
    possible_frame_coords = []
    if h > 1:
        possible_frame_coords.extend([(1, c) for c in range(w)])
        possible_frame_coords.extend([(h-2, c) for c in range(w)])
    if w > 1:
        possible_frame_coords.extend([(r, 1) for r in range(h)])
        possible_frame_coords.extend([(r, w-2) for r in range(h)])
    # Special case for 1xN or Nx1 near corners
    if h>1 and w > 1:
        possible_frame_coords.extend([(1,1), (1,w-2), (h-2,1), (h-2, w-2)])
    elif h>1:
        possible_frame_coords.extend([(1,0)])
    elif w>1:
         possible_frame_coords.extend([(0,1)])
        
    for r, c in possible_frame_coords:
         # Ensure coords are valid (might be duplicates or outside for small grids)
         if 0 <= r < h and 0 <= c < w:
             pixel = input_grid_np[r, c]
             if pixel != background_color:
                 frame_color = pixel
                 break
                 
    # Fallback if frame color still not found (e.g. input is solid background)
    # Use a default distinct color like -1, though this shouldn't happen based on examples
    if frame_color == -1:
         # This case is unlikely given the problem structure, but safest to handle.
         # We can assume the frame color is the same as the background in this edge case.
         frame_color = background_color


    # --- 2. Identify Object Pixels ---
    object_coords = []
    for r in range(h):
        for c in range(w):
            if input_grid_np[r, c] != background_color and input_grid_np[r, c] != frame_color:
                object_coords.append((r, c))

    # --- 3. Determine Center for Core Extraction ---
    center_r, center_c = 0, 0
    if object_coords:
        min_r, min_c, max_r, max_c = find_bounding_box(object_coords)
        # Calculate the center of the bounding box
        center_r = (min_r + max_r) // 2
        center_c = (min_c + max_c) // 2
    else:
        # Use the geometric center of the grid
        center_r = (h - 1) // 2
        center_c = (w - 1) // 2
        
    # --- 4. Extract 3x3 Core Pattern ---
    # Calculate the top-left corner for the 3x3 slice
    core_start_r = center_r - 1
    core_start_c = center_c - 1
    
    # Extract the 3x3 pattern, ensuring indices stay within bounds
    # We assume the 3x3 region exists fully within the input based on examples.
    # A more robust solution might pad, but let's stick to direct slicing first.
    core_pattern = input_grid_np[core_start_r : core_start_r + 3, core_start_c : core_start_c + 3]
    
    # Ensure core_pattern is exactly 3x3, handling edge cases where slicing might yield smaller.
    # This shouldn't be necessary if the center guarantees a full 3x3 slice.
    if core_pattern.shape != (3, 3):
         # This indicates an issue with center calculation or assumption.
         # For now, create a default 3x3 if extraction failed.
         # Using frame_color as a placeholder default fill.
         print(f"Warning: Core pattern extraction failed for center ({center_r}, {center_c}), shape={core_pattern.shape}. Defaulting.")
         core_pattern = np.full((3, 3), frame_color, dtype=int)


    # --- 5. Construct 5x5 Placed Pattern ---
    placed_pattern = np.full((5, 5), background_color, dtype=int)
    # Place core in the center
    placed_pattern[1:4, 1:4] = core_pattern
    # Fill border sides
    placed_pattern[0, 1:4] = frame_color  # Top
    placed_pattern[4, 1:4] = frame_color  # Bottom
    placed_pattern[1:4, 0] = frame_color  # Left
    placed_pattern[1:4, 4] = frame_color  # Right

    # --- 6. Create Output Grid ---
    output_h = 15
    output_w = 15
    output_grid = np.full((output_h, output_w), background_color, dtype=int)

    # --- 7. Place Pattern ---
    loc1_r, loc1_c = 2, 2
    loc2_r, loc2_c = 8, 8

    place_subgrid(output_grid, placed_pattern, loc1_r, loc1_c)
    place_subgrid(output_grid, placed_pattern, loc2_r, loc2_c)

    return output_grid.tolist()