import numpy as np
from scipy.ndimage import label, find_objects

"""
Identify the largest hollow rectangular object (the "frame") in the input grid. 
Identify all other distinct objects (content objects) in the grid.
For each content object, determine if it lies entirely within the inner area bounded by the frame.
Create the output grid by copying the input grid.
In the output grid, change the color of all pixels belonging to content objects strictly inside the frame 
to the background color (white/0). Leave the frame and objects outside the frame unchanged.
"""

def find_largest_object(grid):
    """Finds the object (connected component of non-background pixels)
       with the most pixels. Returns its color, coordinates, and count.
    """
    unique_colors = np.unique(grid[grid != 0])
    if len(unique_colors) == 0:
        return -1, None, 0 # No non-background objects

    largest_object_coords = None
    largest_object_color = -1
    max_pixels = 0

    for color in unique_colors:
        # Find connected components for the current color
        labeled_array, num_labels = label(grid == color)
        if num_labels > 0:
            # Iterate through each component found for this color
            for i in range(1, num_labels + 1):
                coords = np.argwhere(labeled_array == i)
                num_pixels = len(coords)
                # Check if this component is the largest found so far
                if num_pixels > max_pixels:
                    max_pixels = num_pixels
                    largest_object_color = color
                    largest_object_coords = coords
                    
    return largest_object_color, largest_object_coords, max_pixels

def get_bounding_box(coords):
    """Calculates the bounding box (min_row, min_col, max_row, max_col) for a set of coordinates."""
    if coords is None or len(coords) == 0:
        return None
    min_row, min_col = np.min(coords, axis=0)
    max_row, max_col = np.max(coords, axis=0)
    return min_row, min_col, max_row, max_col


def transform(input_grid):
    """
    Removes objects located strictly inside the largest hollow rectangular frame.

    1. Identifies the largest connected non-background object, assuming it's the frame.
    2. Determines the bounding box of this frame.
    3. Iterates through the pixels *inside* the frame's bounding box.
    4. If an inside pixel belongs to an object other than the frame (i.e., its color is not the frame color
       and not the background color 0), it changes that pixel's color to background (0).
    5. Returns the modified grid.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    background_color = 0

    # Find the largest object, assumed to be the frame
    frame_color, frame_coords, _ = find_largest_object(input_grid)

    # If no frame is found (e.g., grid is all background or empty), return original
    if frame_color == -1 or frame_coords is None:
        return output_grid

    # Get the bounding box of the frame
    frame_bbox = get_bounding_box(frame_coords)
    if frame_bbox is None:
         return output_grid # Should not happen if frame_coords is not None, but safe check
        
    min_row, min_col, max_row, max_col = frame_bbox

    # Define the inner region (strictly inside the frame's bounding box)
    # Loop ranges exclude the max values, so max_row and max_col work directly
    inner_min_row = min_row + 1
    inner_max_row = max_row 
    inner_min_col = min_col + 1
    inner_max_col = max_col

    # Iterate through the pixels within the inner region
    for r in range(inner_min_row, inner_max_row):
        for c in range(inner_min_col, inner_max_col):
            # Check boundaries just in case, though ranges should handle this
            if 0 <= r < height and 0 <= c < width:
                pixel_color = input_grid[r, c]
                # If the pixel is inside the bounds and is NOT the frame color and NOT background,
                # set it to background color in the output.
                if pixel_color != frame_color and pixel_color != background_color:
                    output_grid[r, c] = background_color

    return output_grid