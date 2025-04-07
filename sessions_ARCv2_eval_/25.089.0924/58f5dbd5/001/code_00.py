import numpy as np
from typing import List, Tuple, Dict, Set

"""
Identify solid 5x5 rectangles of a single non-background color within the input grid.
Determine the bounding box encompassing all identified 5x5 rectangles.
Create an output grid by cropping the input grid based on this bounding box, expanded by a 1-pixel border (using the background color).
Within this output grid, locate the positions corresponding to the original 5x5 rectangles.
Modify these rectangles by changing their inner 3x3 core to the background color, leaving only a 1-pixel thick frame of the original color.
The background color is determined from the top-left corner pixel of the input grid.
"""

def find_solid_5x5_rectangles(grid: np.ndarray, background_color: int) -> List[Tuple[int, int, int]]:
    """
    Finds all solid 5x5 rectangles of a single non-background color.

    Args:
        grid: The input numpy array grid.
        background_color: The background color to ignore.

    Returns:
        A list of tuples, where each tuple contains (row, col, color)
        for the top-left corner of a found 5x5 rectangle.
    """
    target_rectangles = []
    height, width = grid.shape
    
    # Iterate through possible top-left corners of 5x5 squares
    for r in range(height - 4):
        for c in range(width - 4):
            # Get the color of the potential top-left corner
            color = grid[r, c]
            
            # Skip if it's the background color
            if color == background_color:
                continue
                
            # Extract the 5x5 subgrid
            subgrid = grid[r:r+5, c:c+5]
            
            # Check if all pixels in the subgrid have the same color
            if np.all(subgrid == color):
                target_rectangles.append((r, c, color))
                
    return target_rectangles

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by finding solid 5x5 rectangles, cropping around them,
    and hollowing them out.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape

    # 1. Determine the background color (assume top-left pixel)
    background_color = grid_np[0, 0]

    # 2. Identify all solid 5x5 target rectangles
    target_rectangles = find_solid_5x5_rectangles(grid_np, background_color)

    # If no target rectangles are found, return a minimal grid or handle as appropriate.
    # Based on examples, target rectangles seem guaranteed. Let's assume at least one exists.
    if not target_rectangles:
        # Return a 1x1 grid with background color if none found (or consider other error handling)
        # This scenario is not present in the training examples.
        # The examples imply cropping will always happen based on found objects.
        # If the input *only* contained the background color, what would happen?
        # Let's adhere to the observed pattern: if targets exist, crop. If not, maybe return empty or minimal bg grid.
        # For now, assume targets exist as per examples.
         # Based on test case behavior, an empty list or equivalent might be expected
         # if the core logic doesn't find anything to crop around.
         # Let's stick to the main logic first. If this function gets called
         # with an input yielding no targets, the min/max logic below will fail.
         # Add a check here.
         # Returning an empty list might cause issues downstream. 
         # Let's return a 1x1 grid with the background color as a placeholder.
         # Example 2 shows cropping only the top part, suggesting non-target shapes below are ignored.
        if height > 0 and width > 0:
             return [[background_color]] 
        else:
             return [[]] # Handle empty input case


    # 4. Find the minimum bounding box encompassing all target rectangles
    min_r = height
    max_r = -1
    min_c = width
    max_c = -1

    for r, c, _ in target_rectangles:
        min_r = min(min_r, r)
        max_r = max(max_r, r + 4) # bottom row index of the 5x5 square
        min_c = min(min_c, c)
        max_c = max(max_c, c + 4) # rightmost column index of the 5x5 square

    # 5. Define the region for the output grid (expand bounding box by 1 pixel)
    out_r_start = max(0, min_r - 1)
    out_r_end = min(height - 1, max_r + 1) # inclusive index
    out_c_start = max(0, min_c - 1)
    out_c_end = min(width - 1, max_c + 1) # inclusive index

    # 6. Create the output grid by copying the pixels from the input grid
    # Slicing in numpy is exclusive of the end index, so add 1
    output_grid_np = grid_np[out_r_start : out_r_end + 1, out_c_start : out_c_end + 1].copy()

    # 7. Hollow out the target rectangles within the output grid
    for r, c, color in target_rectangles:
        # Calculate the top-left position relative to the output grid
        out_r = r - out_r_start
        out_c = c - out_c_start
        
        # Check if the rectangle is fully within the bounds of the output grid 
        # (it should be by definition of the crop, but good practice)
        if out_r + 4 < output_grid_np.shape[0] and out_c + 4 < output_grid_np.shape[1]:
            # Modify the inner 3x3 area to the background color
            # Row indices: out_r+1, out_r+2, out_r+3
            # Col indices: out_c+1, out_c+2, out_c+3
            # Slicing needs +4 for rows and +4 for columns to include index +3
            output_grid_np[out_r + 1 : out_r + 4, out_c + 1 : out_c + 4] = background_color

    # Convert the final numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid