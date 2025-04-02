import numpy as np
from collections import Counter

"""
Identify the background color (typically 0). 
Identify the 'frame' color, assumed to be the dominant non-background color forming a large outer shape (heuristically taken as the color at grid[1,1] if available).
Identify 'inner' color(s) as any other non-background, non-frame colors.
Find the bounding box enclosing all pixels of the 'inner' color(s).
Refine the bounding box by trimming rows/columns from the edges (bottom, right, top, left) if they consist entirely of the 'frame' color within the bounding box's current extent.
Extract the subgrid defined by the final bounding box.
In the extracted subgrid, replace all pixels matching the 'frame' color with the 'background' color.
Return the modified subgrid.
"""

def find_bounding_box(grid, target_colors):
    """Finds the minimum bounding box containing any of the target colors."""
    rows, cols = np.where(np.isin(grid, list(target_colors)))
    if rows.size == 0:
        return None  # No target pixels found
    min_r, max_r = np.min(rows), np.max(rows)
    min_c, max_c = np.min(cols), np.max(cols)
    return [min_r, max_r, min_c, max_c] # Return mutable list

def transform(input_grid):
    """
    Transforms the input grid based on extracting an inner object,
    refining its bounding box, and replacing frame color remnants.
    """
    grid = np.array(input_grid, dtype=int)
    
    if grid.size == 0:
        return []
        
    # 1. Identify Colors
    background_color = 0
    
    # Heuristic: Assume frame color is at [1, 1] if grid is large enough and not background
    # This assumes a border of background color exists.
    frame_color = -1 # Default invalid color
    if grid.shape[0] > 1 and grid.shape[1] > 1:
        candidate_frame = grid[1, 1]
        if candidate_frame != background_color:
             frame_color = candidate_frame
             
    # Fallback or refinement: Find unique non-background colors. If frame_color is still -1 or invalid,
    # determine frame/inner based on frequency or other properties.
    # For now, rely on the grid[1,1] heuristic which works for provided examples.
    unique_colors = np.unique(grid)
    non_background_colors = set(unique_colors) - {background_color}

    if frame_color == -1:
         # If grid[1,1] wasn't helpful, implement alternative logic.
         # E.g., If only one non_background_color, maybe it's inner? Or frame? Task dependent.
         # E.g., If two, maybe most frequent is frame? 
         # For this specific task's examples, grid[1,1] works.
         # If no frame color identifiable, perhaps return original or empty?
         # Let's assume grid[1,1] works based on examples.
         if len(non_background_colors) > 0:
             # Simple fallback: pick the smallest non-background color as frame
             # This is arbitrary and likely wrong for general cases.
             frame_color = min(non_background_colors)
         else: # Only background color present
              return grid.tolist() # Or return empty list? Based on examples, returning original seems unlikely.

    inner_colors = non_background_colors - {frame_color}

    if not inner_colors:
        # No inner colors found, maybe the task is just to crop the frame?
        # Based on examples, we expect inner colors. Return empty grid?
         return [] # Or handle as per potential new examples

    # 2. Locate Inner Object(s) and get Initial Bounding Box
    bbox = find_bounding_box(grid, inner_colors)

    if bbox is None:
        # No inner pixels found
        return [] # Return empty grid

    # 3. Adjust BoundingBox (Trim)
    # Mutable bbox: [min_r, max_r, min_c, max_c]
    refined = True
    while refined:
        refined = False
        
        # Check bottom row
        if bbox[0] <= bbox[1]: # Ensure valid row range
            bottom_row_slice = grid[bbox[1], bbox[2]:bbox[3]+1]
            if np.all(bottom_row_slice == frame_color):
                bbox[1] -= 1
                refined = True
                if bbox[1] < bbox[0]: break # Box became invalid

        # Check right column
        if bbox[2] <= bbox[3] and bbox[0] <= bbox[1]: # Ensure valid col/row range
             right_col_slice = grid[bbox[0]:bbox[1]+1, bbox[3]]
             if np.all(right_col_slice == frame_color):
                 bbox[3] -= 1
                 refined = True
                 if bbox[3] < bbox[2]: break # Box became invalid

        # Check top row
        if bbox[0] <= bbox[1] and bbox[2] <= bbox[3]: # Ensure valid row/col range
            top_row_slice = grid[bbox[0], bbox[2]:bbox[3]+1]
            if np.all(top_row_slice == frame_color):
                bbox[0] += 1
                refined = True
                if bbox[0] > bbox[1]: break # Box became invalid
        
        # Check left column
        if bbox[2] <= bbox[3] and bbox[0] <= bbox[1]: # Ensure valid col/row range
             left_col_slice = grid[bbox[0]:bbox[1]+1, bbox[2]]
             if np.all(left_col_slice == frame_color):
                 bbox[2] += 1
                 refined = True
                 if bbox[2] > bbox[3]: break # Box became invalid

    # Check if refinement made the box invalid
    if bbox[0] > bbox[1] or bbox[2] > bbox[3]:
         return [] # Return empty if refinement eliminated the box

    # 4. Extract Subgrid
    min_r, max_r, min_c, max_c = bbox
    output_grid = grid[min_r:max_r+1, min_c:max_c+1].copy()

    # 5. Apply Color Replacement
    output_grid[output_grid == frame_color] = background_color

    # 6. Final Output
    return output_grid.tolist()