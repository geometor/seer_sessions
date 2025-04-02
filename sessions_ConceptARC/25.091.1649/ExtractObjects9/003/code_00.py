"""
Identifies the background color (0), a frame color (major non-background color near the edge), and inner color(s) (other colors).
Finds the bounding box of all pixels matching the inner color(s).
Refines this bounding box by iteratively trimming edges (bottom, right, top, left) if they consist entirely of the frame color.
Extracts the subgrid defined by the final bounding box from the input.
Replaces any pixels matching the frame color within the extracted subgrid with the background color.
Returns the resulting subgrid.
"""

import numpy as np

def find_bounding_box(grid, target_colors):
    """
    Finds the minimum bounding box containing any of the target colors.
    
    Args:
        grid (np.array): The input grid.
        target_colors (set): A set of colors to find the bounding box for.

    Returns:
        list or None: A list [min_r, max_r, min_c, max_c] or None if no target pixels found.
    """
    rows, cols = np.where(np.isin(grid, list(target_colors)))
    if rows.size == 0:
        return None  # No target pixels found
    min_r, max_r = np.min(rows), np.max(rows)
    min_c, max_c = np.min(cols), np.max(cols)
    # Return as a mutable list for easier modification during refinement
    return [int(min_r), int(max_r), int(min_c), int(max_c)] 

def transform(input_grid):
    """
    Transforms the input grid by extracting an inner object, refining its
    bounding box by trimming frame-colored edges, and replacing frame color 
    remnants within the final box with the background color.
    """
    grid = np.array(input_grid, dtype=int)
    
    if grid.size == 0:
        return [] # Handle empty input
        
    # 1. Identify Colors
    background_color = 0
    unique_colors = np.unique(grid)
    non_background_colors = set(unique_colors) - {background_color}

    # Heuristic for frame color: check grid[1,1] if possible and not background
    frame_color = -1 
    if grid.shape[0] > 1 and grid.shape[1] > 1:
        candidate_frame = grid[1, 1]
        if candidate_frame != background_color:
            frame_color = candidate_frame

    # Fallback/Alternative: If grid[1,1] failed, try another near-border point or common color logic
    # For this task, grid[1,1] seems sufficient for the examples provided. 
    # If not identified, maybe pick the most frequent non-background?
    if frame_color == -1 and non_background_colors:
         # A more robust heuristic might be needed for general cases.
         # Example 2: grid[1,1] is 0, but grid[1,3] is 3 (frame).
         # Let's refine: Check (1,1), then maybe iterate along row 1 or col 1?
         # Or, use the most frequent non-background color. Let's try that as a fallback.
         if non_background_colors:
              counts = {c: np.sum(grid == c) for c in non_background_colors}
              if counts:
                   frame_color = max(counts, key=counts.get) # Assume most frequent non-bg is frame
    
    # If still no frame color found (e.g., only background), return empty or handle as error
    if frame_color == -1:
         # If only background exists, return empty? Or original? Assume empty based on task pattern.
         return []

    inner_colors = non_background_colors - {frame_color}

    if not inner_colors:
        # No inner colors found, which contradicts the examples' patterns.
         return [] 

    # 2. Find Inner Region Bounding Box
    bbox = find_bounding_box(grid, inner_colors)

    if bbox is None:
        # No inner pixels actually found
        return [] 

    # 3. Refine Bounding Box by trimming pure frame-color edges
    # bbox = [min_r, max_r, min_c, max_c]
    refined = True
    while refined:
        refined = False
        min_r, max_r, min_c, max_c = bbox

        # Check bottom row (if valid box)
        if min_r <= max_r and min_c <= max_c:
            bottom_row_slice = grid[max_r, min_c:max_c+1]
            if np.all(bottom_row_slice == frame_color):
                bbox[1] -= 1 # max_r decreases
                refined = True
                if bbox[1] < bbox[0]: break # Box became invalid

        # Check right column (if valid box)
        if bbox[0] <= bbox[1] and bbox[2] <= bbox[3]: # Re-check bounds after potential row trim
             right_col_slice = grid[bbox[0]:bbox[1]+1, bbox[3]]
             if np.all(right_col_slice == frame_color):
                 bbox[3] -= 1 # max_c decreases
                 refined = True
                 if bbox[3] < bbox[2]: break # Box became invalid

        # Check top row (if valid box)
        if bbox[0] <= bbox[1] and bbox[2] <= bbox[3]: # Re-check bounds
            top_row_slice = grid[bbox[0], bbox[2]:bbox[3]+1]
            if np.all(top_row_slice == frame_color):
                bbox[0] += 1 # min_r increases
                refined = True
                if bbox[0] > bbox[1]: break # Box became invalid
        
        # Check left column (if valid box)
        if bbox[0] <= bbox[1] and bbox[2] <= bbox[3]: # Re-check bounds
             left_col_slice = grid[bbox[0]:bbox[1]+1, bbox[2]]
             if np.all(left_col_slice == frame_color):
                 bbox[2] += 1 # min_c increases
                 refined = True
                 if bbox[2] > bbox[3]: break # Box became invalid

    # Check if refinement made the box invalid
    if bbox[0] > bbox[1] or bbox[2] > bbox[3]:
         return [] # Return empty if refinement eliminated the box

    # 4. Extract Subgrid based on final bounding box
    min_r, max_r, min_c, max_c = bbox
    output_grid = grid[min_r:max_r+1, min_c:max_c+1].copy()

    # 5. Clean Up: Replace Frame color with Background color in the extracted grid
    output_grid[output_grid == frame_color] = background_color

    # 6. Output
    return output_grid.tolist()