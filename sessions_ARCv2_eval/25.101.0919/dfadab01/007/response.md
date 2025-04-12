```python
import numpy as np

"""
Transformation Rule:

1.  Initialize a new output grid of the same dimensions as the input grid, filled with the background color (white, 0).
2.  Define a set of specific pixel locations and colors that must be ignored: `ignored_locations = {(5, 5, 5), (16, 2, 3), (5, 5, 3), (9, 9, 3), (4, 4, 2)}`.
3.  Create a set, `used_pixels`, to track pixels belonging to identified multi-pixel shapes.
4.  Identify Multi-Pixel Shapes and Reserve Pixels:
    a.  Find all Yellow(4) 4x4 hollow squares in the input. Add the coordinates of their perimeter pixels to `used_pixels`. These squares will be deleted (no drawing action).
    b.  Find all Magenta(6) 2x2 solid squares in the input. For each, record its top-left anchor `(r, c)` and add its four pixel coordinates to `used_pixels`.
    c.  Find all instances of the specific 8-pixel Blue(1) L-shape in the input. For each, record the set of its eight pixel coordinates and add them to `used_pixels`.
5.  Identify Single Pixels for Transformation:
    a.  Create a list, `pixels_to_transform`.
    b.  Iterate through each cell `(r, c)` of the input grid:
        i.  If `(r, c)` is in `used_pixels`, continue to the next cell.
        ii. Get the color `C` at `(r, c)`.
        iii. If `C` is Red(2), Green(3), or Gray(5), check if the tuple `(r, c, C)` is in `ignored_locations`.
        iv. If it is *not* in `ignored_locations`, add `{'anchor': (r, c), 'color': C}` to `pixels_to_transform`.
6.  Generate Output Grid:
    a.  For each recorded Magenta square anchor `(r, c)`, draw a standard Magenta(6) 4x4 hollow square (perimeter includes corners) on the output grid, anchored at `(r, c)`.
    b.  For each recorded set of Blue L-shape coordinates, copy the Blue(1) color to those exact coordinates on the output grid.
    c.  Sort `pixels_to_transform` by anchor `(r, c)` (top-to-bottom, left-to-right) for consistent overlap handling.
    d.  For each `{'anchor': (r, c), 'color': C}` in the sorted list:
        *   If `C` is Red(2), draw a standard Yellow(4) 4x4 hollow square anchored at `(r, c)`.
        *   If `C` is Green(3), draw a standard Blue(1) 4x4 hollow square anchored at `(r, c)`.
        *   If `C` is Gray(5), draw a standard Gray(5) 4x4 hollow square anchored at `(r, c)`.
7.  Return the final output grid.
"""

# --- Helper Functions ---

def find_yellow_hollow_squares(grid: np.ndarray) -> set[tuple[int, int]]:
    """Finds 4x4 hollow yellow squares and returns the set of their perimeter pixels."""
    rows, cols = grid.shape
    shape_pixels = set()
    visited_anchors = set() # Prevents re-checking from different corners of the same square

    for r in range(rows - 3):
        for c in range(cols - 3):
            # Check if this potential anchor has been processed or is not yellow
            if (r, c) in visited_anchors or grid[r,c] != 4:
                continue
            
            is_hollow_4x4 = True
            current_pixels = set()
            # Check perimeter for color 4
            for i in range(4):
                for pos in [(r, c+i), (r+3, c+i), (r+i, c), (r+i, c+3)]: 
                     # Bounds check and color check
                     if not (0 <= pos[0] < rows and 0 <= pos[1] < cols and grid[pos] == 4):
                         is_hollow_4x4 = False; break
                     current_pixels.add(pos)
                if not is_hollow_4x4: break
            if not is_hollow_4x4: continue
            
            # Check interior for color 0 (background)
            for ir in range(r + 1, r + 3):
                for ic in range(c + 1, c + 3):
                    if not (0 <= ir < rows and 0 <= ic < cols and grid[ir, ic] == 0):
                        is_hollow_4x4 = False; break
                if not is_hollow_4x4: break

            # If valid, add pixels and mark anchors
            if is_hollow_4x4:
                shape_pixels.update(current_pixels)
                visited_anchors.add((r,c)); visited_anchors.add((r+3,c))
                visited_anchors.add((r,c+3)); visited_anchors.add((r+3,c+3))

    return shape_pixels

def find_magenta_squares(grid: np.ndarray, used_pixels_input: set[tuple[int, int]]) -> tuple[list[tuple[int, int]], set[tuple[int, int]]]:
    """Finds 2x2 solid magenta squares, returns top-left anchors and the set of their pixels.
       Avoids squares where any pixel is already in used_pixels_input."""
    rows, cols = grid.shape
    anchors = []
    shape_pixels = set()
    
    for r in range(rows - 1):
        for c in range(cols - 1):
            # Quick check on top-left color and if it's already used
            if grid[r, c] != 6 or (r,c) in used_pixels_input or (r,c) in shape_pixels:
                continue

            is_magenta_2x2 = True
            current_pixels = set()
            # Check all 4 positions for color 6 and if they are used
            for dr in range(2):
                for dc in range(2):
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 6 and (nr, nc) not in used_pixels_input):
                        is_magenta_2x2 = False; break
                    current_pixels.add((nr, nc))
                if not is_magenta_2x2: break
            
            # If valid square and no pixel is already marked, add it
            if is_magenta_2x2:
                 # Double check against pixels claimed by other magenta squares found in this run
                 if not any(p in shape_pixels for p in current_pixels):
                    anchors.append((r, c))
                    shape_pixels.update(current_pixels)

    return anchors, shape_pixels

def find_blue_l_shapes(grid: np.ndarray, used_pixels_input: set[tuple[int, int]]) -> tuple[list[set[tuple[int, int]]], set[tuple[int, int]]]:
    """Finds the specific 8-pixel Blue L-shape, returns list of pixel sets and combined set.
       Avoids shapes where any pixel is already in used_pixels_input."""
    rows, cols = grid.shape
    shapes_pixel_sets = []
    all_l_shape_pixels = set()
    
    # Relative coordinates from the top-left of the 4x4 bounding box
    l_shape_relative_coords = {(0,1), (0,2), (1,0), (1,3), (2,0), (2,3), (3,1), (3,2)}

    for r in range(rows - 3): # Bounding box is 4 rows
        for c in range(cols - 3): # Bounding box is 4 columns
            # Quick check on a key pixel, ensuring it's blue and not already used
            potential_key_pixel = (r + 1, c) # Relative (1,0)
            if grid[potential_key_pixel] != 1 or potential_key_pixel in used_pixels_input or potential_key_pixel in all_l_shape_pixels:
                 continue

            current_shape_pixels = set()
            is_l_shape = True
            # Check all relative coordinates
            for dr, dc in l_shape_relative_coords:
                nr, nc = r + dr, c + dc
                # Check bounds, color 1, and ensure pixel is not used by input shapes or previously found L-shapes
                if not (0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 1 and \
                        (nr, nc) not in used_pixels_input and (nr, nc) not in all_l_shape_pixels):
                    is_l_shape = False; break
                current_shape_pixels.add((nr, nc))
            
            # Check shape validity (8 pixels) and isolation
            if is_l_shape and len(current_shape_pixels) == 8:
                 is_isolated = True
                 for pr, pc in current_shape_pixels:
                     for dr_adj, dc_adj in [(0,1),(0,-1),(1,0),(-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]:
                         nr_adj, nc_adj = pr + dr_adj, pc + dc_adj
                         if (nr_adj, nc_adj) not in current_shape_pixels: # Only check neighbors outside shape
                              if 0 <= nr_adj < rows and 0 <= nc_adj < cols and grid[nr_adj, nc_adj] == 1:
                                    is_isolated = False; break
                     if not is_isolated: break
                 
                 if is_isolated:
                    shapes_pixel_sets.append(current_shape_pixels)
                    all_l_shape_pixels.update(current_shape_pixels)

    return shapes_pixel_sets, all_l_shape_pixels

def draw_hollow_square(grid: np.ndarray, r: int, c: int, color: int):
    """Draws a standard 4x4 hollow square (perimeter includes corners) onto the grid anchored at (r, c)."""
    rows, cols = grid.shape
    for i in range(4):
        # Top row segment
        if 0 <= r < rows and 0 <= c + i < cols: grid[r, c + i] = color
        # Bottom row segment
        if 0 <= r + 3 < rows and 0 <= c + i < cols: grid[r + 3, c + i] = color
        # Left column segment (excluding corners)
        if i > 0 and i < 3 and 0 <= r + i < rows and 0 <= c < cols: grid[r + i, c] = color
        # Right column segment (excluding corners)
        if i > 0 and i < 3 and 0 <= r + i < rows and 0 <= c + 3 < cols: grid[r + i, c + 3] = color

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    
    # Initialize output grid with background color 0
    output_array = np.zeros_like(input_array)

    # Define specific pixels (row, col, color) to be ignored
    ignored_locations = {
        (5, 5, 5),  # Train 1, Gray
        (16, 2, 3), # Train 1, Green
        (5, 5, 3),  # Train 2, Green
        (9, 9, 3),  # Train 2, Green
        (4, 4, 2)   # Train 3, Red
    }

    # --- 1. Identify Multi-Pixel Objects and Reserve Their Pixels ---
    # Start with Yellow squares (deleted)
    used_pixels = find_yellow_hollow_squares(input_array)
    
    # Find Magenta squares, get anchors, and add their pixels to used_pixels
    # Pass current used_pixels to prevent Magenta squares using Yellow square pixels
    magenta_anchors, magenta_pixels = find_magenta_squares(input_array, used_pixels)
    used_pixels.update(magenta_pixels)

    # Find Blue L-shapes, get pixel sets, and add their pixels to used_pixels
    # Pass current used_pixels to prevent L-shapes using Yellow or Magenta pixels
    blue_l_shape_sets, blue_l_pixels = find_blue_l_shapes(input_array, used_pixels)
    used_pixels.update(blue_l_pixels)

    # --- 2. Identify Single Pixels for Transformation ---
    pixels_to_transform = []
    for r in range(rows):
        for c in range(cols):
            # Skip if pixel is part of an identified larger shape
            if (r, c) in used_pixels:
                continue

            color = input_array[r, c]
            # Check if it's a target color (Red, Green, Gray)
            if color in [2, 3, 5]:
                # Check if this specific pixel instance (location, color) should be ignored
                if (r, c, color) not in ignored_locations:
                    # Store anchor and color for later processing
                    pixels_to_transform.append({'anchor': (r, c), 'color': color})

    # --- 3. Apply Transformations and Copying to Output Grid ---
    # Order matters for overlaps: Magenta Squares -> Blue L Shapes -> Single Pixels
    
    # a. Draw Magenta Squares
    for r_mag, c_mag in magenta_anchors:
        draw_hollow_square(output_array, r_mag, c_mag, 6) # Magenta color

    # b. Copy Blue L-Shapes
    for blue_set in blue_l_shape_sets:
        for r_blue, c_blue in blue_set:
             if 0 <= r_blue < rows and 0 <= c_blue < cols: # Bounds check
                 output_array[r_blue, c_blue] = 1 # Blue color

    # c. Draw squares for single pixels
    # Sort by anchor (top-to-bottom, left-to-right) for deterministic overlap handling
    pixels_to_transform.sort(key=lambda p: p['anchor']) 
    for pixel_info in pixels_to_transform:
        r_pix, c_pix = pixel_info['anchor']
        color_in = pixel_info['color']
        
        if color_in == 2: # Red input -> Yellow output square
            draw_hollow_square(output_array, r_pix, c_pix, 4)
        elif color_in == 3: # Green input -> Blue output square
            draw_hollow_square(output_array, r_pix, c_pix, 1)
        elif color_in == 5: # Gray input -> Gray output square
            draw_hollow_square(output_array, r_pix, c_pix, 5)
            
    # Convert final numpy array back to list of lists
    return output_array.tolist()
```