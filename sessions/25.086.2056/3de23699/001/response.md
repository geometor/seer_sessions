```python
import numpy as np
from collections import Counter

"""
Identifies two non-background colors in the input grid. One color appears exactly four times (marker color), defining a bounding box (ROI). The other color forms the main object. Extracts the part of the main object strictly inside the ROI, changes its color to the marker color, and places it onto a new, smaller grid whose dimensions are determined by the inner size of the ROI.
"""

def find_color_coordinates(grid, color):
    """Finds all coordinates (row, col) of a given color in the grid."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def transform(input_grid):
    """
    Extracts a shape defined by one color within a boundary defined by another color,
    re-colors the shape, and places it on a smaller grid.
    """
    input_grid = np.array(input_grid)
    
    # 1. Find unique non-background colors and their counts
    unique_colors, counts = np.unique(input_grid[input_grid != 0], return_counts=True)
    
    if len(unique_colors) != 2:
        # This case isn't expected based on the examples, but good to consider
        print("Warning: Expected exactly two non-background colors.")
        # Attempt to proceed if possible, otherwise return input or empty grid?
        # For now, let's assume the structure holds based on examples.
        # If counts are not helpful, maybe identify by shape? The examples have 4 single pixels vs one larger object.
        
    # 2. Identify marker color (count == 4) and main object color
    marker_color = 0
    main_object_color = 0
    for color, count in zip(unique_colors, counts):
        if count == 4:
            marker_color = color
        else:
            main_object_color = color
            
    if marker_color == 0 or main_object_color == 0:
        # Handle cases where the expected counts (4 and >4) are not met.
        # Based on the examples, this should not happen.
        print(f"Warning: Could not definitively identify marker ({marker_color}) and main object ({main_object_color}) colors based on counts.")
        # Fallback or error needed? For now, proceed assuming colors were found.

    # 3. Find coordinates of the marker pixels
    marker_coords = find_color_coordinates(input_grid, marker_color)
    
    if len(marker_coords) != 4:
         print(f"Warning: Found {len(marker_coords)} marker pixels, expected 4.")
         # Handle error or attempt best guess

    # 4. Determine the ROI boundaries
    rows = [r for r, c in marker_coords]
    cols = [c for r, c in marker_coords]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    # 5. Calculate output grid dimensions
    output_height = max_row - min_row - 1
    output_width = max_col - min_col - 1
    
    # Handle cases where markers might define a line or point (height/width <= 0)
    if output_height <= 0 or output_width <= 0:
        print(f"Warning: Invalid output dimensions calculated ({output_height}x{output_width}). ROI might be too small.")
        # Return an empty or minimal grid? 
        return np.zeros((1, 1), dtype=int) # Example minimal return

    # 6. Create the output grid, initialized to white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 7. & 8. Iterate through the inner ROI and populate the output grid
    for r in range(min_row + 1, max_row):
        for c in range(min_col + 1, max_col):
            # Check if the pixel in the input grid is the main object color
            if input_grid[r, c] == main_object_color:
                # Calculate corresponding output coordinates
                r_out = r - (min_row + 1)
                c_out = c - (min_col + 1)
                # Set the output pixel color to the marker color
                output_grid[r_out, c_out] = marker_color

    # 9. Return the completed output grid
    return output_grid.tolist() # Return as list of lists per ARC format
```