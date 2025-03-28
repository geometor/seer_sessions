import numpy as np
from collections import defaultdict, Counter

"""
Natural Language Program:

1.  **Identify Objects:** Find all connected components (objects) of non-white pixels in the input grid. For each object, record its color, coordinates, and bounding box.
2.  **Determine Template Shape:** Calculate a shape signature (relative coordinates from the top-left corner) for each object. Group objects by their shape signature. Identify the most frequently occurring shape signature as the `Template Signature`. Record the height (`H`) of this template shape. Store the objects matching this signature as `Template Objects`.
3.  **Identify Palette Colors:** Consider all pixels *not* belonging to the `Template Objects` as potential palette pixels. Find the bounding box enclosing all these potential palette pixels. Scan this bounding box column by column, from left to right. For each column, find the first non-white pixel within the bounding box's rows. Add its color to the `Palette Colors` list, ensuring uniqueness and preserving the left-to-right order.
4.  **Identify Anchor Template:** Among the `Template Objects`, find the one with the minimum starting row (top-most). Record its starting row (`min_orig_row`), starting column (`colS`), and color (`anchor_color`). Note: Assume all template objects share the same starting column `colS`.
5.  **Find Anchor Index:** Determine the 0-based index (`k`) of `anchor_color` within the ordered `Palette Colors` list.
6.  **Calculate Output Stack Start Row:** Compute the starting row (`R_start`) for the stacked output shapes using the formula: `R_start = min_orig_row - (k * H)`.
7.  **Generate Output Grid:** Create a new grid of the same dimensions as the input, initialized with the background color (white, 0). Iterate through the `Palette Colors` list. For each color `ci` at index `i`:
    a.  Calculate the top row for placing this instance of the template: `current_row = R_start + (i * H)`.
    b.  Using the `Template Signature` (relative coordinates `dr, dc`), draw the template shape onto the output grid at position (`current_row`, `colS`) using color `ci`. Specifically, for each `(dr, dc)` in the signature, set the pixel at `(current_row + dr, colS + dc)` to `ci`.
8.  Return the generated output grid.
"""

def find_connected_components(grid):
    """Finds all connected components of non-background pixels."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                component_coords = set()
                q = [(r, c)]
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.pop(0)
                    component_coords.add((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                # Check orthogonal neighbors only if diagonal fails
                if not component_coords: # Should not happen with initial pixel
                     continue
                
                q = [(r, c)]
                visited_ortho = np.zeros_like(grid, dtype=bool)
                visited_ortho[r,c] = True
                component_coords_ortho = set()
                min_r_ortho, max_r_ortho = r, r
                min_c_ortho, max_c_ortho = c, c

                while q:
                    row, col = q.pop(0)
                    component_coords_ortho.add((row, col))
                    min_r_ortho = min(min_r_ortho, row)
                    max_r_ortho = max(max_r_ortho, row)
                    min_c_ortho = min(min_c_ortho, col)
                    max_c_ortho = max(max_c_ortho, col)
                    
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                         nr, nc = row + dr, col + dc
                         if 0 <= nr < rows and 0 <= nc < cols and \
                            grid[nr, nc] == color and not visited_ortho[nr, nc]:
                            visited_ortho[nr, nc] = True
                            visited[nr,nc] = True # Mark as visited globally
                            q.append((nr, nc))

                objects.append({
                    "coords": component_coords_ortho,
                    "color": color,
                    "bbox": (min_r_ortho, min_c_ortho, max_r_ortho, max_c_ortho) # top, left, bottom, right
                })
                # Mark all found coords as visited to avoid reprocessing
                # for cr, cc in component_coords_ortho:
                #     visited[cr, cc] = True


    return objects

def get_shape_signature(obj):
    """Calculates a shape signature (sorted relative coordinates) and dimensions."""
    min_r, min_c, max_r, max_c = obj['bbox']
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    
    relative_coords = tuple(sorted([(r - min_r, c - min_c) for r, c in obj['coords']]))
    return relative_coords, height, width

def transform(input_grid):
    """
    Transforms the input grid based on identifying a palette and template shapes,
    then stacking instances of the template shape colored according to the palette order.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    output_grid = np.zeros_like(input_np, dtype=int)

    # 1. Identify Objects
    all_objects = find_connected_components(input_np)
    if not all_objects:
        return output_grid.tolist() # Return empty grid if no objects

    # 2. Determine Template Shape
    shape_signatures = defaultdict(list)
    obj_signatures = {}
    for i, obj in enumerate(all_objects):
        signature, h, w = get_shape_signature(obj)
        shape_signatures[signature].append(i)
        obj_signatures[i] = {'signature': signature, 'height': h, 'width': w}

    if not shape_signatures:
         return output_grid.tolist() # Should not happen if all_objects is not empty

    # Find the most frequent signature
    template_signature = max(shape_signatures, key=lambda k: len(shape_signatures[k]))
    template_indices = shape_signatures[template_signature]
    template_height = obj_signatures[template_indices[0]]['height'] # Get height from first template obj

    template_objects = [all_objects[i] for i in template_indices]
    palette_object_indices = set(range(len(all_objects))) - set(template_indices)

    # 3. Identify Palette Colors
    palette_pixels = []
    if palette_object_indices:
        min_pr, min_pc, max_pr, max_pc = rows, cols, -1, -1
        for i in palette_object_indices:
            obj = all_objects[i]
            for r, c in obj['coords']:
                palette_pixels.append({'coord': (r, c), 'color': obj['color']})
                min_pr = min(min_pr, r)
                min_pc = min(min_pc, c)
                max_pr = max(max_pr, r)
                max_pc = max(max_pc, c)

        # Extract palette colors by scanning the bounding box L->R
        palette_colors = []
        if palette_pixels: # Check if palette exists
             processed_cols = set()
             sorted_palette_pixels = sorted(palette_pixels, key=lambda p: (p['coord'][1], p['coord'][0])) # sort by col, then row
             
             current_col_colors = []
             last_col = -1
             unique_col_colors = []

             for p in sorted_palette_pixels:
                 r,c = p['coord']
                 color = p['color']
                 if c != last_col:
                     if current_col_colors:
                          # Take the first color encountered in the previous column (lowest row)
                          if unique_col_colors and unique_col_colors[-1] != current_col_colors[0]:
                             unique_col_colors.append(current_col_colors[0])
                          elif not unique_col_colors:
                               unique_col_colors.append(current_col_colors[0])

                     current_col_colors = []
                     last_col = c
                 
                 if color not in current_col_colors:
                     current_col_colors.append(color)

             # Add colors from the last column processed
             if current_col_colors:
                  if unique_col_colors and unique_col_colors[-1] != current_col_colors[0]:
                      unique_col_colors.append(current_col_colors[0])
                  elif not unique_col_colors:
                       unique_col_colors.append(current_col_colors[0])

             palette_colors = unique_col_colors
             
        # Fallback if palette identification failed but templates exist
        if not palette_colors and template_objects: 
             # Use colors of template objects as palette, sorted by row
             template_objects.sort(key=lambda obj: obj['bbox'][0])
             palette_colors = [obj['color'] for obj in template_objects]


    else: # No separate palette objects found, assume template colors are the palette
        template_objects.sort(key=lambda obj: obj['bbox'][0]) # sort by row
        palette_colors = []
        seen_colors = set()
        for obj in template_objects:
            if obj['color'] not in seen_colors:
                 palette_colors.append(obj['color'])
                 seen_colors.add(obj['color'])


    if not palette_colors or not template_objects:
        # If still no palette or templates, cannot proceed
         print("Warning: Could not determine palette or template shapes.")
         return output_grid.tolist()


    # 4. Identify Anchor Template
    template_objects.sort(key=lambda obj: obj['bbox'][0]) # Sort by top row
    anchor_template = template_objects[0]
    min_orig_row, colS, _, _ = anchor_template['bbox']
    anchor_color = anchor_template['color']

    # Verify common starting column (optional but good check)
    # for obj in template_objects:
    #     if obj['bbox'][1] != colS:
    #         print(f"Warning: Template objects do not share the same start column. Expected {colS}, found {obj['bbox'][1]}")
            # Decide how to handle: maybe use the anchor's colS, or majority? Using anchor's colS.


    # 5. Find Anchor Index
    try:
        k = palette_colors.index(anchor_color)
    except ValueError:
        # Anchor color not in derived palette? This indicates an issue.
        # Maybe the palette logic needs refinement, or the anchor is wrong.
        # As a fallback, perhaps just use index 0 or try matching based on position?
        print(f"Warning: Anchor color {anchor_color} not found in derived palette {palette_colors}. Using index 0.")
        k = 0 # Fallback

    # 6. Calculate Output Stack Start Row
    # Need template height H, which we got during signature calculation
    R_start = min_orig_row - (k * template_height)

    # 7. Generate Output Grid
    for i, ci in enumerate(palette_colors):
        current_row = R_start + (i * template_height)
        # Draw the template shape
        for dr, dc in template_signature:
            r_draw, c_draw = current_row + dr, colS + dc
            # Ensure drawing is within grid bounds
            if 0 <= r_draw < rows and 0 <= c_draw < cols:
                output_grid[r_draw, c_draw] = ci

    return output_grid.tolist()