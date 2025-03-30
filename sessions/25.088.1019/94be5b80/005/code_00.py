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
        # Find all non-background colors present in the grid
        unique_colors = set(np.unique(grid)) - {BACKGROUND_COLOR}
        if not unique_colors: # Handle case of empty or all-background grid
            return []
        colors_to_find = unique_colors
    else:
        colors_to_find = set(colors)

    # Prioritize objects based on position (top-left) for tie-breaking in size
    sorted_coords = sorted([(r, c) for r in range(rows) for c in range(cols) if grid[r,c] in colors_to_find])

    for r, c in sorted_coords:
        if not visited[r, c] and grid[r, c] in colors_to_find:
            color = grid[r, c]
            obj_pixels = set()
            q = [(r, c)]
            visited[r, c] = True
            min_r, min_c = r, c
            max_r, max_c = r, c

            processed_in_this_object = set([(r,c)]) # Track pixels added to queue for this object

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
                       not visited[nr, nc] and grid[nr, nc] == color and \
                       (nr, nc) not in processed_in_this_object: # Check if already queued/visited for this object
                        visited[nr, nc] = True
                        q.append((nr, nc))
                        processed_in_this_object.add((nr,nc))
                
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
    start_r, start_c = top_left_pos
    rows, cols = grid.shape
    for dr, dc in shape_sig:
        r, c = start_r + dr, start_c + dc
        if 0 <= r < rows and 0 <= c < cols:
            grid[r, c] = color
        # else: print(f"Warning: Pixel ({r},{c}) out of bounds for grid {grid.shape}") # Optional: for debugging bounds issues

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. Identify all distinct contiguous objects (non-background color).
    2. Select the object with the largest area (pixel count) as the 'template'. If there's a tie in size, the one whose bounding box starts further up (minimum row) and then further left (minimum column) is chosen.
    3. Identify all non-background pixels that *do not* belong to the template object. These are the 'palette' pixels.
    4. Determine the color sequence from the palette pixels by reading them primarily from top to bottom, and secondarily from left to right. Extract the unique colors in this order.
    5. Determine the starting position for stacking:
        - The starting column is the leftmost column of the template object's bounding box.
        - The starting row is the topmost row containing any palette pixel.
    6. Calculate the vertical offset for stacking: This is the height of the template object's bounding box.
    7. Calculate the required output grid dimensions:
        - Width is the same as the input grid width.
        - Height is determined by the starting row, the number of shapes to stack (length of the palette color sequence), and the vertical offset. It must be at least as tall as the input grid.
    8. Create the output grid initialized with the background color.
    9. Draw copies of the template shape vertically onto the output grid:
        - Start at the calculated starting position (row, col).
        - Use the colors from the determined palette sequence, in order.
        - Stack subsequent shapes directly below the previous one, using the calculated vertical offset.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    input_rows, input_cols = input_grid_np.shape

    # 1. & 2. Identify all objects and select the template
    input_objects = find_objects(input_grid_np)

    if not input_objects:
        # Handle empty input or input with only background
        return input_grid # Return input as is

    # Sort objects: Primarily by size (desc), secondarily by min_row (asc), thirdly by min_col (asc)
    input_objects.sort(key=lambda o: (-o['size'], o['bbox'][0], o['bbox'][1]))
    template_object = input_objects[0]
    template_shape = template_object['shape']
    template_bbox = template_object['bbox']
    template_pixels = template_object['pixels']
    template_min_r, template_min_c, template_max_r, template_max_c = template_bbox
    template_height = template_max_r - template_min_r + 1

    # 3. Identify palette pixels
    all_colored_pixels = set(zip(*np.where(input_grid_np != BACKGROUND_COLOR)))
    palette_pixels_set = all_colored_pixels - template_pixels

    if not palette_pixels_set:
         # If no palette pixels, maybe just draw the template in its original color and position?
         # Or follow the logic assuming an empty sequence (draw nothing new)?
         # Let's assume the task implies a palette always exists if transformation occurs.
         # If not, maybe return the input? For now, proceed, resulting sequence will be empty.
         # Revisit: The examples imply a palette. Let's try returning input if no palette.
         return input_grid # No palette found, transformation rule might not apply.


    # 4. Determine palette sequence
    # Sort palette pixels: top-to-bottom, then left-to-right
    sorted_palette_pixels = sorted(list(palette_pixels_set), key=lambda p: (p[0], p[1]))
    
    palette_color_sequence = []
    seen_colors = set()
    palette_min_row = input_rows # Initialize high to find minimum

    for r, c in sorted_palette_pixels:
        color = input_grid_np[r, c]
        palette_min_row = min(palette_min_row, r) # Update the minimum row found for palette pixels
        if color not in seen_colors:
            palette_color_sequence.append(color)
            seen_colors.add(color)
            
    # Handle case where palette_min_row wasn't updated (no palette pixels found - redundant check)
    if not palette_color_sequence:
        return input_grid # Should have been caught earlier, but safe check

    # 5. Determine stacking start position
    start_col = template_min_c
    start_row = palette_min_row # Use the topmost row of any palette pixel

    # 6. Vertical offset is template height (already calculated)
    vertical_offset = template_height

    # 7. Calculate output grid dimensions
    num_shapes = len(palette_color_sequence)
    output_cols = input_cols

    # Calculate the maximum row index needed for the last shape
    if num_shapes == 0:
         # This case should ideally not be reached if we return input grid when no palette
         max_r_occupied = template_max_r # Or maybe 0? Depends on desired output for edge case.
    elif num_shapes == 1:
         max_r_occupied = start_row + (template_max_r - template_min_r) # Bottom edge of the single shape
    else:
         last_shape_start_r = start_row + (num_shapes - 1) * vertical_offset
         max_r_occupied = last_shape_start_r + (template_max_r - template_min_r) # Bottom edge of the last shape

    output_rows = max(input_rows, max_r_occupied + 1)

    # 8. Create output grid
    output_grid = np.full((output_rows, output_cols), BACKGROUND_COLOR, dtype=int)

    # 9. Draw the shapes
    for i, color in enumerate(palette_color_sequence):
        # Calculate top-left position for this instance
        current_start_r = start_row + i * vertical_offset
        current_start_c = start_col
        
        # Draw the shape
        draw_shape(output_grid, template_shape, color, (current_start_r, current_start_c))

    return output_grid.tolist()