```python
"""
Transforms an input grid based on the following rules:
1. Initialize an empty 10x10 output grid filled with zeros.
2. Identify all unique non-zero integer values (colors) present in the input grid.
3. Ignore the color '5'.
4. For each remaining unique color:
    a. Find the coordinates (row, column) of all cells in the input grid containing this color.
    b. Determine the bounding box (minimum/maximum row and column) encompassing these cells.
    c. Calculate the integer center coordinates (center_row, center_col) of the bounding box.
    d. Draw a 3x3 square filled with the current color onto the output grid, centered at (center_row, center_col). Ensure the square stays within the grid boundaries.
5. Return the final output grid.
"""

import numpy as np

def find_color_coords(grid, color):
    """Finds all coordinates (row, col) of a given color in the grid."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def get_bounding_box(coords):
    """Calculates the bounding box (min_r, max_r, min_c, max_c) for a list of coordinates."""
    if not coords:
        return None
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    return min(rows), max(rows), min(cols), max(cols)

def calculate_center(bbox):
    """Calculates the center coordinates (row, col) from a bounding box."""
    min_r, max_r, min_c, max_c = bbox
    center_r = (min_r + max_r) // 2
    center_c = (min_c + max_c) // 2
    return center_r, center_c

def draw_square(grid, center_r, center_c, color):
    """Draws a 3x3 square of a given color onto the grid, centered at (center_r, center_c)."""
    rows, cols = grid.shape
    # Iterate through the 3x3 area centered at (center_r, center_c)
    for r_offset in range(-1, 2):
        for c_offset in range(-1, 2):
            r = center_r + r_offset
            c = center_c + c_offset
            # Check if the coordinates are within the grid bounds
            if 0 <= r < rows and 0 <= c < cols:
                grid[r, c] = color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid)
    rows, cols = input_np.shape

    # Initialize output_grid with zeros
    output_grid = np.zeros_like(input_np)

    # Find unique non-zero colors in the input grid
    unique_colors = np.unique(input_np)
    
    # Process each color, excluding 0 (background) and 5 (ignored color)
    for color in unique_colors:
        if color == 0 or color == 5:
            continue

        # Find all coordinates of the current color
        coords = find_color_coords(input_np, color)
        
        # If the color exists in the grid
        if coords:
            # Determine the bounding box
            bbox = get_bounding_box(coords)
            
            # Calculate the center of the bounding box
            center_r, center_c = calculate_center(bbox)
            
            # Draw the 3x3 square on the output grid
            draw_square(output_grid, center_r, center_c, color)

    # Return the output grid (converting back to list of lists if necessary, 
    # although numpy array is often preferred)
    return output_grid.tolist() 
```