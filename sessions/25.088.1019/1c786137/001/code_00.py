import numpy as np

"""
Scan the input grid to identify all possible rectangular frames. 
A frame is defined as a rectangular border of pixels, exactly one pixel thick, 
all having the same single non-white color (C). This border encloses an inner 
rectangular region where all pixels must *not* have the color C. The frame 
(including border) must be at least 3x3. Calculate the area of the inner 
region for each valid frame. Select the frame with the largest inner area. 
Extract the subgrid corresponding to the inner region of the selected largest 
frame. This extracted subgrid is the final output.
"""

def _is_valid_frame(grid, r1, c1, r2, c2):
    """
    Checks if the rectangle defined by (r1, c1) and (r2, c2) forms a valid frame.

    A valid frame:
    1. Has dimensions at least 3x3.
    2. Has a border exactly one pixel thick.
    3. The border pixels all have the same non-white color (frame_color).
    4. All interior pixels (if any) do *not* have the frame_color.
    """
    rows, cols = grid.shape
    
    # Check bounds
    if not (0 <= r1 < r2 < rows and 0 <= c1 < c2 < cols):
        return False, -1

    # Check minimum size
    height = r2 - r1 + 1
    width = c2 - c1 + 1
    if height < 3 or width < 3:
        return False, -1

    # Get potential frame color (must be non-white)
    frame_color = grid[r1, c1]
    if frame_color == 0: 
        return False, -1

    # Check top border
    if not np.all(grid[r1, c1:c2+1] == frame_color):
        return False, -1
        
    # Check bottom border
    if not np.all(grid[r2, c1:c2+1] == frame_color):
        return False, -1
        
    # Check left border (excluding corners already checked)
    if not np.all(grid[r1+1:r2, c1] == frame_color):
        return False, -1
        
    # Check right border (excluding corners already checked)
    if not np.all(grid[r1+1:r2, c2] == frame_color):
        return False, -1

    # Check interior (if it exists)
    interior_height = height - 2
    interior_width = width - 2
    if interior_height > 0 and interior_width > 0:
        interior = grid[r1+1:r2, c1+1:c2]
        if np.any(interior == frame_color):
            return False, -1
            
    # If all checks pass, it's a valid frame
    interior_area = interior_height * interior_width
    return True, interior_area

def transform(input_grid):
    """
    Finds the largest valid frame in the input grid and extracts its interior.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    
    largest_frame_info = {'area': -1, 'r1': -1, 'c1': -1, 'r2': -1, 'c2': -1}

    # Iterate through all possible top-left corners (r1, c1)
    for r1 in range(rows - 2):
        for c1 in range(cols - 2):
            # Iterate through all possible bottom-right corners (r2, c2)
            # Ensure minimum size 3x3
            for r2 in range(r1 + 2, rows):
                for c2 in range(c1 + 2, cols):
                    # Check if this rectangle forms a valid frame
                    is_valid, area = _is_valid_frame(input_grid, r1, c1, r2, c2)
                    
                    if is_valid:
                        # If it's the largest valid frame found so far, store its info
                        # Note: No explicit tie-breaking needed based on examples, 
                        # assuming a unique largest frame. If tie-breaking is needed,
                        # rules like top-most, then left-most could be added here.
                        if area > largest_frame_info['area']:
                            largest_frame_info = {'area': area, 'r1': r1, 'c1': c1, 'r2': r2, 'c2': c2}

    # If no valid frame was found (should not happen based on examples)
    if largest_frame_info['area'] == -1:
        # Return an empty grid or handle error appropriately
        # Based on task structure, a frame is expected.
        # Returning the input might be a fallback, but extraction is the goal.
        # Let's raise an error for clarity if this unexpected case occurs.
         raise ValueError("No valid frame found in the input grid.")

    # Extract the interior of the largest frame
    r1 = largest_frame_info['r1']
    c1 = largest_frame_info['c1']
    r2 = largest_frame_info['r2']
    c2 = largest_frame_info['c2']
    
    output_grid = input_grid[r1+1:r2, c1+1:c2]

    return output_grid.tolist() # Convert back to list of lists for standard ARC format
