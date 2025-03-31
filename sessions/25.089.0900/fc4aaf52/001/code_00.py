"""
Transformation Rule:
1. Identify the background color (assumed to be the most frequent color, Azure 8).
2. Find the single contiguous object composed of non-background colors.
3. Determine the anchor pixel of this object, defined as the pixel with the minimum row index, and among those, the minimum column index.
4. Determine the horizontal shift distance (dx) based on the color of the anchor pixel:
   - If the anchor color is white (0), dx = 3.
   - If the anchor color is blue (1), dx = 5.
5. Create a new grid of the same dimensions, filled with the background color.
6. Translate the object horizontally by dx columns: copy each pixel of the original object at (row, col) to the new grid at (row, col + dx).
"""

import numpy as np
from collections import Counter

def find_objects(grid, background_color):
    """
    Finds contiguous objects of non-background colors.
    Returns a list of objects, where each object is a list of (row, col, color) tuples.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color and not visited[r, c]:
                # Found the start of a potential object
                current_object_pixels = []
                q = [(r, c)]
                visited[r, c] = True
                
                while q:
                    row, col = q.pop(0)
                    color = grid[row, col]
                    current_object_pixels.append((row, col, color))

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] != background_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if current_object_pixels:
                     objects.append(current_object_pixels)
                     
    return objects

def find_anchor_pixel(object_pixels):
    """
    Finds the anchor pixel (top-most, then left-most) of an object.
    object_pixels is a list of (row, col, color) tuples.
    Returns the (row, col, color) of the anchor pixel.
    """
    if not object_pixels:
        return None

    min_row = min(p[0] for p in object_pixels)
    top_row_pixels = [p for p in object_pixels if p[0] == min_row]
    min_col = min(p[1] for p in top_row_pixels)
    
    # Find the specific pixel matching min_row and min_col
    for p in top_row_pixels:
        if p[1] == min_col:
            return p # Returns (row, col, color)

    return None # Should not happen if object_pixels is not empty


def get_shift_amount(anchor_color):
    """
    Determines the horizontal shift based on the anchor color.
    """
    if anchor_color == 0: # white
        return 3
    elif anchor_color == 1: # blue
        return 5
    else:
        # Default or error case - return 0 shift if color not mapped
        # Or raise an error if the mapping must be exhaustive
        # For now, assume the provided examples cover the necessary cases
        print(f"Warning: Unhandled anchor color {anchor_color}, returning shift 0.")
        return 0 

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid_np = np.array(input_grid)
    height, width = input_grid_np.shape

    # 1. Identify background color (most frequent)
    colors, counts = np.unique(input_grid_np, return_counts=True)
    background_color = colors[np.argmax(counts)]

    # 2. Find the non-background object
    # Assuming only one relevant object based on examples
    objects = find_objects(input_grid_np, background_color)
    if not objects:
         # Handle case with no object - return original or background grid
         print("Warning: No object found. Returning input grid.")
         return input_grid # Or return a grid filled with background_color
    
    # We assume there's only one major object based on the examples
    source_object_pixels = objects[0] 

    # 3. Find the anchor pixel and its color
    anchor = find_anchor_pixel(source_object_pixels)
    if not anchor:
        print("Warning: Could not find anchor pixel. Returning input grid.")
        return input_grid
        
    anchor_color = anchor[2]

    # 4. Determine the horizontal shift (dx)
    dx = get_shift_amount(anchor_color)

    # 5. Create the output grid, initialized with background color
    output_grid = np.full((height, width), background_color, dtype=int)

    # 6. Translate the object by dx
    for r, c, color in source_object_pixels:
        new_c = c + dx
        # Ensure the new position is within bounds
        if 0 <= new_c < width:
            output_grid[r, new_c] = color
        else:
             # Handle pixels moving out of bounds if necessary 
             # (though not seen in examples)
             print(f"Warning: Pixel at ({r}, {c}) moved out of bounds to ({r}, {new_c}).")


    return output_grid.tolist()