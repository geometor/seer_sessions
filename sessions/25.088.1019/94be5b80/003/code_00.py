import numpy as np
from collections import Counter, defaultdict

# --- Constants ---
BACKGROUND_COLOR = 0

# --- Helper Functions: Object Finding ---

def find_objects(grid, colors=None, connectivity=1):
    """
    Finds contiguous objects of specified colors in a grid.

    Args:
        grid (np.array): The input grid.
        colors (set, optional): Set of colors to look for. If None, finds all non-background objects. Defaults to None.
        connectivity (int): 1 for 4-way (adjacent), 2 for 8-way (adjacent + diagonal). Defaults to 1.

    Returns:
        list: A list of dictionaries, each representing an object with:
              'color': The color of the object.
              'pixels': Set of (row, col) tuples belonging to the object.
              'bbox': Tuple (min_row, min_col, max_row, max_col).
              'shape': Frozenset of relative pixel coordinates (dr, dc) from bbox top-left.
              'size': Number of pixels in the object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    if colors is None:
        colors_to_find = set(np.unique(grid)) - {BACKGROUND_COLOR}
    else:
        colors_to_find = set(colors)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] in colors_to_find:
                color = grid[r, c]
                obj_pixels = set()
                q = [(r, c)]
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.pop(0)
                    obj_pixels.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Define neighbors based on connectivity
                    if connectivity == 1:
                        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
                    else: # connectivity == 2 (or default)
                         neighbors = [(dr, dc) for dr in range(row-1, row+2) for dc in range(col-1, col+2) if not (dr==row and dc==col)]

                    for nr, nc in neighbors:
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if obj_pixels:
                    # Ensure consistent sorting for shape signature
                    sorted_pixels = sorted(list(obj_pixels))
                    rel_pixels = frozenset((pr - min_r, pc - min_c) for pr, pc in sorted_pixels)
                    objects.append({
                        'color': color,
                        'pixels': obj_pixels,
                        'bbox': (min_r, min_c, max_r, max_c),
                        'shape': rel_pixels, # Shape relative to bbox top-left
                        'size': len(obj_pixels)
                    })
    return objects

# --- Helper Functions: Drawing ---

def draw_shape(grid, shape_sig, color, top_left_pos):
    """
    Draws a shape defined by its relative pixel signature onto the grid.

    Args:
        grid (np.array): The target grid to draw on.
        shape_sig (frozenset): Set of (dr, dc) relative coordinates defining the shape.
        color (int): The color to draw with.
        top_left_pos (tuple): The (row, col) of the top-left corner where the shape starts.
    """
    min_r, min_c = top_left_pos
    rows, cols = grid.shape
    for dr, dc in shape_sig:
        r, c = min_r + dr, min_c + dc
        if 0 <= r < rows and 0 <= c < cols:
            grid[r, c] = color
        # else: print(f"Warning: Pixel ({r},{c}) out of bounds for grid {grid.shape}") # Optional: for debugging bounds issues

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Transforms the input grid by:
    1. Identifying the largest monochromatic object as the 'template'.
    2. Identifying remaining non-background pixels as the 'palette'.
    3. Determining the vertical sequence of colors in the palette.
    4. Creating an output color sequence: [template color] + [palette sequence].
    5. Stacking copies of the template shape vertically in a new grid, colored according
       to the output color sequence. The vertical offset between shapes equals the
       template's height. The output grid size is adjusted as needed.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    input_rows, input_cols = input_grid_np.shape

    # 1. Identify all distinct objects
    input_objects = find_objects(input_grid_np)

    if not input_objects:
        # No objects found, return empty grid of same size? Or input?
        # Return input seems safer if the premise of template+palette fails.
        return input_grid

    # 2. Identify the template object (largest by pixel count)
    input_objects.sort(key=lambda o: o['size'], reverse=True)
    template_object = input_objects[0]
    template_color = template_object['color']
    template_shape = template_object['shape']
    template_bbox = template_object['bbox']
    template_pixels = template_object['pixels']
    template_min_r, template_min_c, template_max_r, template_max_c = template_bbox
    template_height = template_max_r - template_min_r + 1
    # template_width = template_max_c - template_min_c + 1 # Not needed for offset calc here

    # 3. Identify palette pixels and their colors/positions
    all_input_pixels = set(zip(*np.where(input_grid_np != BACKGROUND_COLOR)))
    palette_pixels_set = all_input_pixels - template_pixels
    
    palette_colors_positions = {} # color -> (r, c) - assuming single pixel per color
    for r, c in palette_pixels_set:
        color = input_grid_np[r, c]
        # Store the first encountered position for each color (or topmost)
        if color not in palette_colors_positions or r < palette_colors_positions[color][0]:
             palette_colors_positions[color] = (r, c)

    # 4. Determine palette sequence (vertical, top to bottom)
    palette_sequence = sorted(palette_colors_positions.keys(), key=lambda c: palette_colors_positions[c][0])

    # 5. Construct the output color sequence
    output_color_sequence = [template_color] + palette_sequence
    num_shapes = len(output_color_sequence)

    # 6. Calculate the vertical offset for stacking
    # Offset is the height of the template bounding box.
    vertical_offset = template_height

    # 7. Calculate required output grid dimensions
    output_cols = input_cols # Width remains the same
    # Calculate the maximum row index needed
    if num_shapes == 0: # Should not happen if template exists, but safeguard
        max_r_occupied = template_max_r
    elif num_shapes == 1:
        max_r_occupied = template_max_r
    else:
        # Row where the last shape *starts* drawing
        last_shape_start_r = template_min_r + (num_shapes - 1) * vertical_offset
        # Max row occupied by the last shape (its bottom edge)
        max_r_occupied = last_shape_start_r + (template_max_r - template_min_r)

    output_rows = max(input_rows, max_r_occupied + 1)

    # 8. Create the output grid
    output_grid = np.full((output_rows, output_cols), BACKGROUND_COLOR, dtype=int)

    # 9. Draw the shapes onto the output grid
    for i, color in enumerate(output_color_sequence):
        # Calculate the top-left position for this shape instance
        # Row = template's original top row + index * offset
        # Col = template's original left col
        pos_r = template_min_r + i * vertical_offset
        pos_c = template_min_c
        
        # Draw the shape
        draw_shape(output_grid, template_shape, color, (pos_r, pos_c))

    return output_grid.tolist()