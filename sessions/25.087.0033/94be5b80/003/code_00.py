import numpy as np
from collections import defaultdict, Counter

"""
Natural Language Program:

1.  **Identify Objects:** Find all connected components (objects) of non-white pixels in the input grid using 8-neighbor connectivity (including diagonals). For each object, record its color, coordinates, and bounding box.
2.  **Determine Template Shape:** Calculate a shape signature (relative coordinates from the top-left corner) for each object. Group objects by their shape signature. Identify the most frequently occurring shape signature as the `Template Signature`. Record the height (`H`) and width (`W`) of this template shape. Store the objects matching this signature as `Template Objects`.
3.  **Identify Palette Objects & Colors:**
    a. Identify objects whose shape signature does *not* match the `Template Signature`. These are the `Palette Objects`.
    b. If `Palette Objects` exist:
        i. Find the minimum bounding box enclosing *all* pixels of *all* `Palette Objects`.
        ii. Determine the orientation of the palette based on this bounding box: Horizontal if width > height, Vertical if height > width. Handle ties or single-pixel palettes (assume Horizontal if ambiguous or dimensions are equal).
        iii. Extract `Palette Colors` based on orientation:
            - **Horizontal:** Scan columns from left to right within the palette bounding box. For each column, find the top-most pixel belonging to any `Palette Object`. Add its color to the `Palette Colors` list, ensuring uniqueness and preserving the left-to-right order.
            - **Vertical:** Scan rows from top to bottom within the palette bounding box. For each row, find the left-most pixel belonging to any `Palette Object`. Add its color to the `Palette Colors` list, ensuring uniqueness and preserving the top-to-bottom order.
    c. If no `Palette Objects` exist:
        i. Use the `Template Objects` themselves as the source for the palette.
        ii. Sort the `Template Objects` by their top-most row coordinate (`bbox[0]`).
        iii. The `Palette Colors` list consists of the colors of these sorted `Template Objects`, preserving order and uniqueness.
4.  **Identify Anchor Template:** Among the `Template Objects`, find the one with the minimum starting row (top-most). Record its starting row (`min_orig_row`), starting column (`colS` - the left-most column of its bbox), and color (`anchor_color`).
5.  **Find Anchor Index:** Determine the 0-based index (`k`) of `anchor_color` within the ordered `Palette Colors` list. If the anchor color is not found (which shouldn't happen with correct logic, but as a fallback), use `k=0`.
6.  **Calculate Output Stack Start Row:** Compute the starting row (`R_start`) for the stacked output shapes using the formula: `R_start = min_orig_row - (k * H)`.
7.  **Generate Output Grid:** Create a new grid of the same dimensions as the input, initialized with the background color (white, 0). Iterate through the `Palette Colors` list. For each color `ci` at index `i`:
    a. Calculate the top row for placing this instance of the template: `current_row = R_start + (i * H)`.
    b. Using the `Template Signature` (relative coordinates `dr, dc`), draw the template shape onto the output grid at position (`current_row`, `colS`) using color `ci`. Specifically, for each `(dr, dc)` in the signature, set the pixel at `(current_row + dr, colS + dc)` to `ci`, ensuring it's within grid bounds.
8.  Return the generated output grid.
"""

import numpy as np
from collections import defaultdict, Counter

def find_connected_components_8_neighbor(grid):
    """Finds all connected components of non-background pixels using 8-neighbor connectivity."""
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

                objects.append({
                    "coords": frozenset(component_coords), # Use frozenset for hashability
                    "color": color,
                    "bbox": (min_r, min_c, max_r, max_c), # top, left, bottom, right
                })
    return objects

def get_shape_signature(obj):
    """Calculates a shape signature (sorted relative coordinates) and dimensions."""
    min_r, min_c, _, _ = obj['bbox']
    relative_coords = tuple(sorted([(r - min_r, c - min_c) for r, c in obj['coords']]))
    # Calculate height and width based on relative coordinates max values
    height = 0
    width = 0
    if relative_coords:
        height = max(rc[0] for rc in relative_coords) + 1
        width = max(rc[1] for rc in relative_coords) + 1
    return relative_coords, height, width


def transform(input_grid):
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    output_grid = np.zeros_like(input_np, dtype=int)

    # 1. Identify Objects (8-neighbor connectivity)
    all_objects = find_connected_components_8_neighbor(input_np)
    if not all_objects:
        return output_grid.tolist() # Return empty grid if no objects

    # 2. Determine Template Shape
    shape_signatures = defaultdict(list)
    obj_details = {}
    for i, obj in enumerate(all_objects):
        signature, h, w = get_shape_signature(obj)
        shape_signatures[signature].append(i)
        obj_details[i] = {'signature': signature, 'height': h, 'width': w, 'obj': obj}

    if not shape_signatures:
         return output_grid.tolist() # Should not happen if all_objects is not empty

    # Find the most frequent signature
    template_signature = max(shape_signatures, key=lambda k: len(shape_signatures[k]))
    template_indices = shape_signatures[template_signature]
    template_height = obj_details[template_indices[0]]['height']
    template_width = obj_details[template_indices[0]]['width']

    template_objects = [all_objects[i] for i in template_indices]
    palette_object_indices = list(set(range(len(all_objects))) - set(template_indices))
    palette_objects = [all_objects[i] for i in palette_object_indices]

    # 3. Identify Palette Objects & Colors
    palette_colors = []
    if palette_objects:
        # Collect all pixels from palette objects
        all_palette_pixels = set()
        min_pr, min_pc = rows, cols
        max_pr, max_pc = -1, -1
        for obj in palette_objects:
            all_palette_pixels.update(obj['coords'])
            min_r, min_c, max_r, max_c = obj['bbox']
            min_pr = min(min_pr, min_r)
            min_pc = min(min_pc, min_c)
            max_pr = max(max_pr, max_r)
            max_pc = max(max_pc, max_c)

        # Create a lookup for palette pixel coordinates to color
        palette_pixel_map = {coord: input_np[coord] for coord in all_palette_pixels}

        # Determine orientation
        palette_bbox_height = max_pr - min_pr + 1
        palette_bbox_width = max_pc - min_pc + 1
        is_horizontal = palette_bbox_width >= palette_bbox_height # Default to horizontal if square or ambiguous

        seen_colors = set()
        if is_horizontal:
            # Scan columns L->R
            for c in range(min_pc, max_pc + 1):
                col_pixels = []
                for r in range(min_pr, max_pr + 1):
                    if (r, c) in palette_pixel_map:
                        col_pixels.append((r, palette_pixel_map[(r, c)]))
                if col_pixels:
                    col_pixels.sort() # Sort by row (top-most)
                    top_color = col_pixels[0][1]
                    if top_color not in seen_colors:
                        palette_colors.append(top_color)
                        seen_colors.add(top_color)
        else:
            # Scan rows T->B
            for r in range(min_pr, max_pr + 1):
                row_pixels = []
                for c in range(min_pc, max_pc + 1):
                    if (r, c) in palette_pixel_map:
                        row_pixels.append((c, palette_pixel_map[(r, c)]))
                if row_pixels:
                    row_pixels.sort() # Sort by col (left-most)
                    left_color = row_pixels[0][1]
                    if left_color not in seen_colors:
                        palette_colors.append(left_color)
                        seen_colors.add(left_color)

    # Fallback: No separate palette objects found
    if not palette_colors:
        # Use colors of template objects, sorted by row
        template_objects.sort(key=lambda obj: obj['bbox'][0])
        seen_colors = set()
        for obj in template_objects:
            if obj['color'] not in seen_colors:
                 palette_colors.append(obj['color'])
                 seen_colors.add(obj['color'])

    # Check if palette or template identification failed
    if not palette_colors or not template_objects:
        # Cannot proceed meaningfully
        # print("Warning: Could not determine palette or template shapes.")
        return output_grid.tolist()

    # 4. Identify Anchor Template
    template_objects.sort(key=lambda obj: obj['bbox'][0]) # Sort by top row
    anchor_template = template_objects[0]
    min_orig_row, colS, _, _ = anchor_template['bbox']
    anchor_color = anchor_template['color']

    # 5. Find Anchor Index
    try:
        k = palette_colors.index(anchor_color)
    except ValueError:
        # Fallback if anchor color isn't in the derived palette
        # print(f"Warning: Anchor color {anchor_color} not found in derived palette {palette_colors}. Using index 0.")
        k = 0 # Use index 0 as a fallback

    # 6. Calculate Output Stack Start Row
    R_start = min_orig_row - (k * template_height)

    # 7. Generate Output Grid
    for i, ci in enumerate(palette_colors):
        current_row = R_start + (i * template_height)
        # Draw the template shape using its signature
        for dr, dc in template_signature:
            r_draw, c_draw = current_row + dr, colS + dc
            # Ensure drawing is within grid bounds
            if 0 <= r_draw < rows and 0 <= c_draw < cols:
                output_grid[r_draw, c_draw] = ci

    return output_grid.tolist()