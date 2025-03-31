import numpy as np
from collections import deque
import math

"""
Transformation Rule Description:

1.  Initialize an output grid with the same dimensions as the input, filled with the background color (orange, 7).
2.  Identify all connected objects (groups of same-colored pixels) in the input grid that are not the background color.
3.  For each `input_object`:
    a. Determine its color `C_in`, its pixels `pixels_in`, and the top-left corner of its bounding box (`r_min`, `c_min`).
    b. Map the input color `C_in` to the output color `C_out`: Swap Red(2) and Blue(1); keep other non-background colors (Gray(5), Maroon(9), Azure(8), Yellow(4)) the same.
    c. Calculate the transposed top-left reference point: `P_t = (c_min, r_min)`. Let `r_t = c_min` and `c_t = r_min`.
    d. Calculate the output reference point `P_out = (r_out, c_out_ref)` by applying a color-dependent coordinate transformation `T(C_in)` to `P_t`:
        *   If `C_in` is Maroon (9): `r_out = r_t + 3`, `c_out_ref = c_t + 3`. (Confirmed Ex 2)
        *   If `C_in` is Gray (5): `r_out = r_t + math.floor(r_t / 4) - 4`, `c_out_ref = c_t - 3`. (Confirmed Ex 2)
        *   If `C_in` is Red (2), Blue (1), Azure (8), or Yellow (4): Use a placeholder rule `r_out = r_t`, `c_out_ref = c_t`, as the correct placement transformation is unknown.
    e. Based on `C_in`, determine the output shape `S_out` and draw it relative to `P_out` using `C_out`:
        *   If `C_in` is Maroon (9): Draw a horizontal line of length 5 starting at `P_out`.
        *   If `C_in` is Gray (5): Draw a single pixel at `P_out`.
        *   If `C_in` is Red (2): Draw a 3x3 Blue plus sign centered at `P_out` (Placeholder/Guess).
        *   If `C_in` is Blue (1), Azure (8), or Yellow (4): Draw the *transposed* version of the original object's pixels relative to `P_out`. (Placeholder - correct shape generation needed, especially for Blue->L/Staircase and Yellow->Scatter).
4.  Return the completed `output_grid`.
"""

# --- Helper Functions ---

def find_objects(grid, background_color):
    """
    Finds connected components (objects) of the same non-background color in the grid.

    Args:
        grid (np.ndarray): The input grid.
        background_color (int): The color to ignore.

    Returns:
        list: A list of objects. Each object is a dictionary containing:
              'color': The color of the object.
              'pixels': A set of (row, col) tuples for the object's pixels.
              'bbox': A tuple (min_row, min_col, max_row, max_col).
    """
    objects = []
    visited = np.zeros(grid.shape, dtype=bool)
    rows, cols = grid.shape

    for r in range(rows):
        for c in range(cols):
            # If pixel is not background and not visited, start BFS
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                # Breadth-First Search to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    # Update bounding box coordinates
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, visited status, and color match
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Store the found object
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return objects

def draw_pixel(grid, r, c, color):
    """ Safely draws a pixel onto the grid if coordinates are valid. """
    rows, cols = grid.shape
    if 0 <= r < rows and 0 <= c < cols:
        grid[r, c] = color

def draw_horizontal_line(grid, r, c, length, color):
    """ Safely draws a horizontal line starting at (r, c). """
    for i in range(length):
        draw_pixel(grid, r, c + i, color)
        
def draw_transposed_object(grid, obj_pixels, r_out_ref, c_out_ref, r_in_ref, c_in_ref, color):
    """ 
    Placeholder shape drawing: Draws the object transposed relative to the output reference point.
    Calculates relative positions from input reference point, transposes the relative coordinates (swap row/col offset), 
    and applies them to the output reference point.
    """
    for r_in, c_in in obj_pixels:
        rel_r = r_in - r_in_ref # Relative row offset in input
        rel_c = c_in - c_in_ref # Relative col offset in input
        # Transpose relative coordinates (swap roles of row/col offsets)
        # Apply transposed relative offset to output reference point
        draw_pixel(grid, r_out_ref + rel_c, c_out_ref + rel_r, color)

def draw_plus(grid, r_center, c_center, color):
    """ Draws a 3x3 plus sign centered at (r_center, c_center). """
    # Draw vertical bar
    for dr in [-1, 0, 1]:
        draw_pixel(grid, r_center + dr, c_center, color)
    # Draw horizontal bar (center pixel is already drawn)
    for dc in [-1, 1]:
        draw_pixel(grid, r_center, c_center + dc, color)

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the transformation rule to the input grid based on object properties,
    transposition, and color-dependent shape/placement rules. Includes known
    rules for Maroon(9)/Gray(5) and placeholders for others.
    """
    background_color = 7
    
    # 1. Initialize output grid with background color
    output_grid = np.full(input_grid.shape, background_color, dtype=int)
    
    # 2. Find all input objects
    objects = find_objects(input_grid, background_color)

    # 3. Process each object
    for obj in objects:
        c_in = obj['color']             # Input color
        pixels_in = obj['pixels']       # Set of (r, c) tuples for the object
        r_min, c_min, _, _ = obj['bbox'] # Top-left corner of input bounding box

        # 3a. Determine output color based on input color
        if c_in == 2: c_out = 1      # Red -> Blue
        elif c_in == 1: c_out = 2    # Blue -> Red
        else: c_out = c_in           # 5->5, 9->9, 8->8, 4->4 remain unchanged

        # 3b. Calculate transposed reference point (top-left)
        r_t, c_t = c_min, r_min # Swap row and column from input top-left

        # 3c. Calculate output reference point P_out = (r_out, c_out_ref) 
        #     by applying a color-dependent transformation T(C_in) to P_t
        if c_in == 9: # Maroon (Rule derived and confirmed from Ex 2)
            r_out, c_out_ref = r_t + 3, c_t + 3
        elif c_in == 5: # Gray (Rule derived and confirmed from Ex 2)
            # This rule correctly maps (5,5)->(2,2) and (9,5)->(7,2)
            r_out, c_out_ref = r_t + math.floor(r_t / 4) - 4, c_t - 3
        else: # Placeholder transformation for other colors (Red, Blue, Yellow, Azure)
            # Default to using the transposed coordinate directly as the output ref point.
            # This is likely incorrect and needs refinement based on further analysis.
            r_out, c_out_ref = r_t, c_t 

        # 3d. Draw the output shape S_out relative to the calculated P_out
        if c_in == 9: # Input Maroon -> Output Horizontal Line Length 5
            draw_horizontal_line(output_grid, r_out, c_out_ref, 5, c_out)
        elif c_in == 5: # Input Gray -> Output Single Pixel
            draw_pixel(output_grid, r_out, c_out_ref, c_out)
        elif c_in == 2: # Input Red -> Output Blue Plus Sign (Placeholder shape/positioning)
            # Guessing the output shape is a 3x3 plus centered at P_out
            draw_plus(output_grid, r_out, c_out_ref, c_out) 
        # Placeholder for other input shapes: Blue(1), Yellow(4), Azure(8)
        else: 
            # Default shape generation: Draw the transposed original shape relative to P_out.
            # This is needed for Blue->L/Staircase, Yellow->Scatter, Azure->Corner repositioning.
            draw_transposed_object(output_grid, pixels_in, r_out, c_out_ref, r_min, c_min, c_out)
             
    # 4. Return the final grid
    return output_grid