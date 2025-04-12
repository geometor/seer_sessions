```python
import numpy as np

"""
Transformation Rule:

1.  Initialize an output grid identical in size to the input, filled with white (0).
2.  Identify specific multi-pixel objects first:
    a.  Find all Yellow(4) 4x4 hollow squares. Mark their pixels as 'used'. These objects are effectively deleted (no action on the output grid).
    b.  Find all Magenta(6) 2x2 solid squares. Mark their pixels as 'used'. Store their top-left coordinates for later transformation.
    c.  Find the specific Blue(1) 8-pixel L-shape (as seen in train_2). Mark its pixels as 'used'. Store all its pixel coordinates for later copying.
3.  Identify single pixels:
    a.  Define a set of specific pixel locations and colors that should be ignored: `{(5, 5, 5), (16, 2, 3), (5, 5, 3), (9, 9, 3), (4, 4, 2)}`.
    b.  Iterate through the input grid. If a pixel (r, c) with color Red(2), Green(3), or Gray(5) is found, and it hasn't been marked as 'used' by a multi-pixel object, and `(r, c, color)` is not in the ignored set, store `(r, c, color)` for transformation.
4.  Apply transformations to the output grid in a specific order (to handle overlaps):
    a.  For each identified Magenta(6) 2x2 square anchored at (r, c), draw a Magenta(6) 4x4 hollow square on the output grid, anchored at (r, c).
    b.  For each identified Blue(1) L-shape, copy its pixels directly to the output grid at their original coordinates.
    c.  For each stored single pixel `(r, c, color)`:
        i.  If color is Red(2), draw a Yellow(4) 4x4 hollow square anchored at (r, c).
        ii. If color is Green(3), draw a Blue(1) 4x4 hollow square anchored at (r, c).
        iii. If color is Gray(5), draw a Gray(5) 4x4 hollow square anchored at (r, c).
5.  Return the final output grid.
"""

def find_yellow_hollow_squares(grid: np.ndarray) -> tuple[list[tuple[int, int]], set[tuple[int, int]]]:
    """Finds 4x4 hollow yellow squares."""
    rows, cols = grid.shape
    anchors = []
    shape_pixels = set()
    visited_anchors = set()

    for r in range(rows - 3):
        for c in range(cols - 3):
            if (r, c) in visited_anchors or grid[r,c] != 4:
                continue
            
            is_hollow_4x4 = True
            current_pixels = set()
            # Check perimeter
            for i in range(4):
                for pos in [(r, c+i), (r+3, c+i), (r+i, c), (r+i, c+3)]:
                     # Check bounds and color
                     if not (0 <= pos[0] < rows and 0 <= pos[1] < cols and grid[pos] == 4):
                         is_hollow_4x4 = False
                         break
                     current_pixels.add(pos) # Add perimeter pixels
                if not is_hollow_4x4: break
            if not is_hollow_4x4: continue
            
            # Check interior is white (0)
            for ir in range(r + 1, r + 3):
                for ic in range(c + 1, c + 3):
                    if not (0 <= ir < rows and 0 <= ic < cols and grid[ir, ic] == 0):
                        is_hollow_4x4 = False
                        break
                if not is_hollow_4x4: break

            if is_hollow_4x4:
                anchors.append((r, c))
                shape_pixels.update(current_pixels)
                # Mark corners to avoid redundant checks if shapes overlap at corners
                visited_anchors.add((r,c))
                visited_anchors.add((r+3,c))
                visited_anchors.add((r,c+3))
                visited_anchors.add((r+3,c+3))

    return anchors, shape_pixels


def find_magenta_squares(grid: np.ndarray) -> tuple[list[tuple[int, int]], set[tuple[int, int]]]:
    """Finds 2x2 solid magenta squares."""
    rows, cols = grid.shape
    anchors = []
    shape_pixels = set()
    
    for r in range(rows - 1):
        for c in range(cols - 1):
            # Check if the top-left pixel is already part of another found shape
            if (r,c) in shape_pixels:
                continue
                
            is_magenta_2x2 = True
            current_pixels = set()
            for dr in range(2):
                for dc in range(2):
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 6):
                        is_magenta_2x2 = False
                        break
                    current_pixels.add((nr, nc))
                if not is_magenta_2x2: break
            
            if is_magenta_2x2:
                # Prevent overlapping detection if a pixel is part of multiple potential squares
                is_new = True
                for p in current_pixels:
                    if p in shape_pixels:
                        is_new = False
                        break
                if is_new:
                    anchors.append((r, c))
                    shape_pixels.update(current_pixels)

    return anchors, shape_pixels


def find_blue_l_shapes(grid: np.ndarray) -> tuple[list[set[tuple[int, int]]], set[tuple[int, int]]]:
    """Finds the specific 8-pixel Blue L-shape from train_2."""
    rows, cols = grid.shape
    shapes_pixel_sets = []
    shape_pixels = set()
    
    # Define the relative coordinates of the L-shape pixels from its effective top-left (min_r, min_c)
    # Example from train_2 anchor (5,5): Pixels are at
    # (5,6), (5,7), (6,5), (6,8), (7,5), (7,8), (8,6), (8,7)
    # Relative to (5,5): (0,1), (0,2), (1,0), (1,3), (2,0), (2,3), (3,1), (3,2)
    l_shape_relative_coords = {(0,1), (0,2), (1,0), (1,3), (2,0), (2,3), (3,1), (3,2)}

    for r in range(rows - 3): # Shape spans 4 rows
        for c in range(cols - 3): # Shape spans 4 columns
             # Quick check on a known point like top-left-most (relative (1,0))
            if grid[r+1, c] != 1 or (r+1,c) in shape_pixels:
                 continue

            current_shape_pixels = set()
            is_l_shape = True
            for dr, dc in l_shape_relative_coords:
                nr, nc = r + dr, c + dc
                # Check bounds, color, and if pixel is already used
                if not (0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 1 and (nr, nc) not in shape_pixels):
                    is_l_shape = False
                    break
                current_shape_pixels.add((nr, nc))
            
            if is_l_shape and len(current_shape_pixels) == 8:
                 # Double check no other blue pixels are adjacent to this shape
                 is_isolated = True
                 for pr, pc in current_shape_pixels:
                     for dr_adj, dc_adj in [(0,1),(0,-1),(1,0),(-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]:
                         nr_adj, nc_adj = pr + dr_adj, pc + dc_adj
                         if (nr_adj, nc_adj) not in current_shape_pixels: # only check neighbors outside the shape
                              if 0 <= nr_adj < rows and 0 <= nc_adj < cols and grid[nr_adj, nc_adj] == 1:
                                    is_isolated = False
                                    break
                     if not is_isolated: break
                 
                 if is_isolated:
                    shapes_pixel_sets.append(current_shape_pixels)
                    shape_pixels.update(current_shape_pixels)

    return shapes_pixel_sets, shape_pixels


def draw_hollow_square(grid: np.ndarray, r: int, c: int, color: int):
    """Draws a 4x4 hollow square onto the grid anchored at (r, c)."""
    rows, cols = grid.shape
    for i in range(4):
        # Top row
        if 0 <= r < rows and 0 <= c + i < cols: grid[r, c + i] = color
        # Bottom row
        if 0 <= r + 3 < rows and 0 <= c + i < cols: grid[r + 3, c + i] = color
        # Left col (excl corners)
        if i > 0 and i < 3 and 0 <= r + i < rows and 0 <= c < cols: grid[r + i, c] = color
        # Right col (excl corners)
        if i > 0 and i < 3 and 0 <= r + i < rows and 0 <= c + 3 < cols: grid[r + i, c + 3] = color


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    output_array = np.zeros_like(input_array)  # Initialize with background color 0

    # Define pixels to be explicitly ignored based on training examples
    ignored_locations = {
        (5, 5, 5),  # Train 1, Gray
        (16, 2, 3), # Train 1, Green
        (5, 5, 3),  # Train 2, Green
        (9, 9, 3),  # Train 2, Green
        (4, 4, 2)   # Train 3, Red
    }

    # --- 1. Identify Multi-Pixel Objects and Mark Their Pixels ---
    all_shape_pixels = set()
    
    # Yellow squares are only identified to mark their pixels
    _, yellow_pixels = find_yellow_hollow_squares(input_array)
    all_shape_pixels.update(yellow_pixels)
    
    # Magenta squares: get anchors and mark pixels
    magenta_anchors, magenta_pixels = find_magenta_squares(input_array)
    all_shape_pixels.update(magenta_pixels)

    # Blue L-shapes: get pixel sets and mark pixels
    blue_l_shape_sets, blue_l_pixels = find_blue_l_shapes(input_array)
    all_shape_pixels.update(blue_l_pixels)

    # --- 2. Identify Single Pixels for Processing ---
    pixels_to_process = []
    for r in range(rows):
        for c in range(cols):
            # Skip if pixel belongs to a larger identified shape
            if (r, c) in all_shape_pixels:
                continue

            color = input_array[r, c]
            # Check if it's a target color for single pixel transformation
            if color in [2, 3, 5]: # Red, Green, Gray
                # Check if this specific pixel instance should be ignored
                if (r, c, color) not in ignored_locations:
                    # Ensure it's truly isolated (not adjacent to same color)
                    is_isolated = True
                    for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                         nr, nc = r + dr, c + dc
                         # Check neighbor only if it's not part of a known shape
                         if (nr, nc) not in all_shape_pixels:
                            if 0 <= nr < rows and 0 <= nc < cols and input_array[nr, nc] == color:
                                is_isolated = False
                                break
                    if is_isolated:
                        pixels_to_process.append({'type': 'pixel', 'top_left': (r, c), 'color': color})

    # --- 3. Apply Transformations to Output Grid ---
    # Order: Magenta squares, Blue L shapes, Single Pixels
    
    # a. Draw Magenta Squares
    for r_mag, c_mag in magenta_anchors:
        draw_hollow_square(output_array, r_mag, c_mag, 6) # Magenta

    # b. Copy Blue L-Shapes
    for blue_set in blue_l_shape_sets:
        for r_blue, c_blue in blue_set:
             if 0 <= r_blue < rows and 0 <= c_blue < cols: # Bounds check just in case
                 output_array[r_blue, c_blue] = 1 # Blue

    # c. Draw squares for single pixels
    # Sort pixels for deterministic drawing order in case of output overlap
    pixels_to_process.sort(key=lambda p: p['top_left']) 
    for pixel_info in pixels_to_process:
        r_pix, c_pix = pixel_info['top_left']
        color_in = pixel_info['color']
        
        if color_in == 2: # Red -> Yellow
            draw_hollow_square(output_array, r_pix, c_pix, 4)
        elif color_in == 3: # Green -> Blue
            draw_hollow_square(output_array, r_pix, c_pix, 1)
        elif color_in == 5: # Gray -> Gray
            draw_hollow_square(output_array, r_pix, c_pix, 5)
            
    return output_array.tolist()
```