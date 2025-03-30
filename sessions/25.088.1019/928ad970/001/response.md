```python
import numpy as np

"""
Draws a rectangular frame on the grid. The frame's color is determined by the 
single contiguous non-gray (5), non-white (0) shape present in the input. 
The frame's position is determined by finding the bounding box of all non-white 
pixels (including the primary shape and any gray pixels), shrinking this bounding 
box inwards by one pixel from all sides, and then drawing the perimeter of this 
shrunk box using the primary shape's color. The frame is drawn only over 
existing white (0) pixels; original non-white pixels along the frame's path 
are preserved.
"""

def find_non_white_pixels(grid):
    """Finds coordinates of all pixels that are not white (0).
    
    Args:
        grid (np.array): The input grid.
    
    Returns:
        list: A list of (row, col) tuples for non-white pixels.
    """
    rows, cols = np.where(grid != 0)
    return list(zip(rows, cols))

def find_primary_color(grid, non_white_pixels):
    """Finds the color of the first non-white, non-gray pixel encountered.
    
    Assumes there is exactly one such color/shape based on task examples.
    
    Args:
        grid (np.array): The input grid.
        non_white_pixels (list): List of (row, col) tuples for non-white pixels.

    Returns:
        int or None: The primary color value, or None if not found.
    """
    for r, c in non_white_pixels:
        color = grid[r, c]
        # Color 0 is excluded by non_white_pixels, check for non-gray
        if color != 5: 
            return color
    return None 

def get_bounding_box(pixels):
    """Calculates the minimum bounding box containing all given pixel coordinates.
    
    Args:
        pixels (list): A list of (row, col) tuples.
        
    Returns:
        tuple or None: (min_row, min_col, max_row, max_col) or None if input is empty.
    """
    if not pixels:
        return None
    rows = [p[0] for p in pixels]
    cols = [p[1] for p in pixels]
    # Adjust max values to be inclusive
    return min(rows), min(cols), max(rows), max(cols)

def transform(input_grid):
    """
    Draws a frame based on the bounding box of all non-white pixels,
    shrunk inwards by one pixel. Frame color matches the primary shape color.
    Only white background pixels are overwritten.

    Args:
        input_grid (np.array): The input grid.

    Returns:
        np.array: The output grid with the frame drawn.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Step 1: Identify the locations of all non-white pixels.
    non_white_pixels = find_non_white_pixels(input_grid)
    if not non_white_pixels:
        # If no non-white pixels, no frame can be determined.
        return output_grid 

    # Step 2: Identify the primary color (non-white, non-gray).
    primary_color = find_primary_color(input_grid, non_white_pixels)
    if primary_color is None:
        # If no primary color shape is found, cannot determine frame color.
        return output_grid 

    # Step 3: Determine the overall bounding box for all non-white pixels.
    bbox = get_bounding_box(non_white_pixels)
    if bbox is None:
         # Should not happen if non_white_pixels is not empty
         return output_grid 

    min_r, min_c, max_r, max_c = bbox

    # Step 4: Calculate the coordinates for the inner, shrunk frame.
    frame_min_r = min_r + 1
    frame_min_c = min_c + 1
    frame_max_r = max_r - 1
    frame_max_c = max_c - 1

    # Step 5: Check if the shrunk frame is valid (has non-negative dimensions).
    # If the bounding box was only 1 or 2 pixels thick/wide, shrinking makes it invalid.
    if frame_min_r > frame_max_r or frame_min_c > frame_max_c:
        # Shrunk box is invalid (e.g., negative width/height).
        return output_grid 

    # Step 6 & 7: Draw the frame perimeter, only overwriting white pixels (0).
    # Ensure drawing stays within grid bounds (although shrinking should guarantee this).
    
    # Draw Top row
    # Check if row index is valid
    if 0 <= frame_min_r < height:
        # Iterate through columns of the top row
        for c in range(max(0, frame_min_c), min(width, frame_max_c + 1)):
            # Check if the original pixel at this location is white
            if input_grid[frame_min_r, c] == 0:
                output_grid[frame_min_r, c] = primary_color

    # Draw Bottom row (avoid double drawing if frame height is 1)
    # Check if row index is valid and different from top row
    if 0 <= frame_max_r < height and frame_max_r != frame_min_r: 
        # Iterate through columns of the bottom row
        for c in range(max(0, frame_min_c), min(width, frame_max_c + 1)):
             # Check if the original pixel at this location is white
            if input_grid[frame_max_r, c] == 0:
                output_grid[frame_max_r, c] = primary_color

    # Draw Left column (excluding corners already drawn by top/bottom row logic)
    # Check if column index is valid
    if 0 <= frame_min_c < width:
        # Iterate through rows between the top and bottom row corners
        for r in range(max(0, frame_min_r + 1), min(height, frame_max_r)):
             # Check if the original pixel at this location is white
            if input_grid[r, frame_min_c] == 0:
                output_grid[r, frame_min_c] = primary_color

    # Draw Right column (excluding corners, avoid double drawing if frame width is 1)
    # Check if column index is valid and different from left column
    if 0 <= frame_max_c < width and frame_max_c != frame_min_c: 
        # Iterate through rows between the top and bottom row corners
       for r in range(max(0, frame_min_r + 1), min(height, frame_max_r)):
            # Check if the original pixel at this location is white
            if input_grid[r, frame_max_c] == 0:
                output_grid[r, frame_max_c] = primary_color

    # Step 8: Return the modified grid
    return output_grid
```