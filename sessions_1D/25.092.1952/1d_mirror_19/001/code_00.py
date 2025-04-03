"""
1. Interpret the input array as a 14x2 grid.
2. Find the single maroon pixel (9) and its coordinates (R, C).
3. Find the connected object of a color other than white (0) or maroon (9). Determine its color and the coordinates of all its pixels, specifically noting the minimum row index (min_row_obj).
4. Initialize an output grid of the same dimensions (14x2) filled with white (0).
5. Place the maroon pixel in the output grid at coordinates (R, 1).
6. Determine the target starting row for the object based on the maroon pixel's initial column:
   - If the initial column C was 0, the target minimum row (target_min_row) is R + 1.
   - If the initial column C was 1, the target minimum row (target_min_row) is R + 2.
7. Calculate the vertical shift required for the object: shift = target_min_row - min_row_obj.
8. Transfer the object pixels to the output grid, applying the calculated vertical shift: For each original object pixel at (r, c), place it at (r + shift, c) in the output grid using the object's color.
9. Flatten the output grid back into a 1D array.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds all coordinates of pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def find_object_pixels_and_color(grid):
    """Finds the coordinates and color of the non-background, non-marker object."""
    unique_colors = np.unique(grid)
    object_color = -1
    for color in unique_colors:
        if color != 0 and color != 9:
            object_color = color
            break
    if object_color == -1:
        return [], -1 # No object found other than background or marker
        
    object_pixels = find_pixels_by_color(grid, object_color)
    return object_pixels, object_color

def transform(input_grid_flat):
    # --- Grid Setup ---
    # Reshape the flat input array into a 14x2 grid
    input_grid = np.array(input_grid_flat).reshape(14, 2)
    rows, cols = input_grid.shape
    
    # Initialize the output grid with the background color (0)
    output_grid = np.zeros((rows, cols), dtype=int)

    # --- Identify Elements ---
    # Find the marker (maroon pixel, 9)
    marker_coords = find_pixels_by_color(input_grid, 9)
    if not marker_coords:
        # Handle cases where the marker is missing, though not expected based on examples
        return output_grid.flatten().tolist() 
    marker_row, marker_col = marker_coords[0]

    # Find the colored object (not 0 or 9)
    object_pixels, object_color = find_object_pixels_and_color(input_grid)
    if not object_pixels:
         # Handle cases where the object is missing, place only marker and return
         output_grid[marker_row, 1] = 9
         return output_grid.flatten().tolist()

    # Find the minimum row of the object
    min_row_obj = min(r for r, c in object_pixels)

    # --- Apply Transformation Logic ---
    # Place the marker in the output grid (always in the second column)
    output_grid[marker_row, 1] = 9

    # Determine the target minimum row for the object based on the marker's initial column
    if marker_col == 0:
        target_min_row = marker_row + 1
    else: # marker_col == 1
        target_min_row = marker_row + 2

    # Calculate the vertical shift needed
    shift = target_min_row - min_row_obj

    # Place the object in the output grid, shifted vertically
    for r, c in object_pixels:
        new_row = r + shift
        # Check bounds to prevent errors, though not strictly necessary based on examples
        if 0 <= new_row < rows:
            output_grid[new_row, c] = object_color

    # --- Final Output ---
    # Flatten the output grid back to a 1D list
    return output_grid.flatten().tolist()