import numpy as np
from collections import defaultdict, Counter

"""
Identify a template shape and a color palette from the input grid. 
Generate an output grid by replicating the template shape vertically, forming a stack. 
The colors of the stacked shapes and their order are determined by the sequence of colors in the palette. 
The stack's position is anchored relative to the topmost instance of the template shape found in the input.

Natural Language Program:

1.  **Identify Objects:** Find all connected components (objects) of non-white pixels using 8-neighbor connectivity. Record each object's color, coordinates, bounding box, and pixel count.
2.  **Group Objects by Shape:** Calculate a canonical shape signature (e.g., sorted relative coordinates from the top-left of the bounding box) for each object. Group objects sharing the same signature.
3.  **Distinguish Palette and Template Candidates:**
    a.  Find all objects and group them by shape signature. Record the pixel count for each shape signature.
    b.  Identify the shape signature associated with the largest individual object pixel count. Assume this signature belongs to the `Template Objects`.
    c.  Designate all objects *not* matching the `Template Signature` as `Palette Components`.
    d.  If no `Palette Components` are found (e.g., all objects have the same shape), use the `Template Objects` themselves as the source for the palette (fallback mechanism).
4.  **Extract Palette Colors:**
    a.  If `Palette Components` exist:
        i.   Collect all pixel coordinates belonging to any `Palette Component`.
        ii.  Determine the bounding box of these collected palette pixels.
        iii. Determine the primary orientation (Horizontal if width >= height, Vertical otherwise).
        iv.  Scan the palette pixels along the primary axis (left-to-right if Horizontal, top-to-bottom if Vertical). For each step along the axis, find the first palette pixel encountered (top-most for horizontal, left-most for vertical) and add its color (from the input grid) to the `Palette Colors` list, ensuring uniqueness while preserving order.
    b.  If using the fallback mechanism (no distinct `Palette Components`):
        i.   Sort the `Template Objects` by their top-most row coordinate (`bbox[0]`).
        ii.  The `Palette Colors` list consists of the unique colors of these sorted `Template Objects`, preserving their order.
5.  **Identify Anchor Template:** Among the confirmed `Template Objects`, find the one with the minimum starting row (top-most). Record its starting row (`min_orig_row`), starting column (`colS` - the left-most column of its bbox), and color (`anchor_color`).
6.  **Find Anchor Index:** Find the 0-based index (`k`) of `anchor_color` in the ordered `Palette Colors` list. If not found, default to `k=0`.
7.  **Calculate Output Stack Start Row:** Compute `R_start = min_orig_row - (k * H)`, where `H` is the height of the `Template Signature`.
8.  **Generate Output Grid:** Create a new grid of the same dimensions as the input, initialized with the background color (white, 0). Iterate through the `Palette Colors` list (index `i`, color `ci`):
    a.  Calculate the draw row: `current_row = R_start + (i * H)`.
    b.  Using the `Template Signature`, draw the template shape at (`current_row`, `colS`) using color `ci`. For each relative coordinate `(dr, dc)` in the signature, set the output grid pixel at `(current_row + dr, colS + dc)` to `ci`, checking grid bounds.
9.  Return the generated output grid.
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
                    "pixel_count": len(component_coords),
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

    # 1. Identify Objects
    all_objects = find_connected_components_8_neighbor(input_np)
    if not all_objects:
        return output_grid.tolist()

    # 2. Group Objects by Shape and calculate properties
    shape_groups = defaultdict(lambda: {"indices": [], "pixel_count": 0})
    obj_details = [] # Store details for each object
    max_pixel_count = 0
    signature_with_max_pixels = None

    for i, obj in enumerate(all_objects):
        signature, h, w = get_shape_signature(obj)
        shape_groups[signature]["indices"].append(i)
        shape_groups[signature]["pixel_count"] = obj["pixel_count"] # Store pixel count per object of this shape
        shape_groups[signature]["height"] = h
        shape_groups[signature]["width"] = w
        obj_details.append({'signature': signature, 'height': h, 'width': w, 'obj': obj, 'id': i})

        # Track the signature corresponding to the largest object found so far
        if obj["pixel_count"] > max_pixel_count:
            max_pixel_count = obj["pixel_count"]
            signature_with_max_pixels = signature

    # 3. Distinguish Palette and Template Candidates
    template_signature = None
    template_objects = []
    palette_components = []

    if signature_with_max_pixels is not None:
        # Assume the signature of the largest object is the template signature
        template_signature = signature_with_max_pixels
        template_height = shape_groups[template_signature]["height"]
        template_width = shape_groups[template_signature]["width"]

        for detail in obj_details:
            if detail['signature'] == template_signature:
                template_objects.append(detail['obj'])
            else:
                palette_components.append(detail['obj'])
    else:
        # Fallback if no objects were found or something went wrong
        return output_grid.tolist()

    # 4. Extract Palette Colors
    palette_colors = []
    seen_colors = set()

    if palette_components:
        # Collect all pixels from palette components
        all_palette_pixels = set()
        min_pr, min_pc = rows, cols
        max_pr, max_pc = -1, -1
        for obj in palette_components:
            all_palette_pixels.update(obj['coords'])
            min_r, min_c, max_r, max_c = obj['bbox']
            min_pr = min(min_pr, min_r)
            min_pc = min(min_pc, min_c)
            max_pr = max(max_pr, max_r)
            max_pc = max(max_pc, max_c)

        if not all_palette_pixels: # Should not happen if palette_components is not empty, but check anyway
             pass # Fallback to using templates below
        else:
            # Create a lookup for palette pixel coordinates to color
            palette_pixel_map = {coord: input_np[coord] for coord in all_palette_pixels}

            # Determine orientation
            palette_bbox_height = max_pr - min_pr + 1
            palette_bbox_width = max_pc - min_pc + 1
            is_horizontal = palette_bbox_width >= palette_bbox_height # Default to horizontal if square

            if is_horizontal:
                # Scan columns L->R
                for c in range(min_pc, max_pc + 1):
                    col_pixels = []
                    for r in range(min_pr, max_pr + 1):
                        if (r, c) in palette_pixel_map:
                            col_pixels.append((r, palette_pixel_map[(r, c)])) # Store (row, color)
                    if col_pixels:
                        col_pixels.sort() # Sort by row (find top-most)
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
                            row_pixels.append((c, palette_pixel_map[(r, c)])) # Store (col, color)
                    if row_pixels:
                        row_pixels.sort() # Sort by col (find left-most)
                        left_color = row_pixels[0][1]
                        if left_color not in seen_colors:
                            palette_colors.append(left_color)
                            seen_colors.add(left_color)

    # Fallback: No separate palette components identified OR palette extraction failed
    if not palette_colors:
        if not template_objects: # No template either, something is wrong
            return output_grid.tolist()
        # Use colors of template objects, sorted by row
        template_objects.sort(key=lambda obj: obj['bbox'][0])
        seen_colors_fallback = set()
        for obj in template_objects:
            if obj['color'] not in seen_colors_fallback:
                 palette_colors.append(obj['color'])
                 seen_colors_fallback.add(obj['color'])

    # Final check for critical components
    if not palette_colors or not template_objects or template_signature is None:
        # Cannot proceed meaningfully
        # print("Warning: Could not determine palette, template shapes, or template signature.")
        return output_grid.tolist()

    # 5. Identify Anchor Template
    template_objects.sort(key=lambda obj: obj['bbox'][0]) # Sort by top row
    anchor_template = template_objects[0]
    min_orig_row, colS, _, _ = anchor_template['bbox']
    anchor_color = anchor_template['color']

    # 6. Find Anchor Index
    try:
        k = palette_colors.index(anchor_color)
    except ValueError:
        # Fallback if anchor color isn't in the derived palette
        # print(f"Warning: Anchor color {anchor_color} not found in derived palette {palette_colors}. Using index 0.")
        k = 0

    # 7. Calculate Output Stack Start Row
    # H is template_height
    R_start = min_orig_row - (k * template_height)

    # 8. Generate Output Grid
    for i, ci in enumerate(palette_colors):
        current_row = R_start + (i * template_height)
        # Draw the template shape using its signature
        for dr, dc in template_signature:
            r_draw, c_draw = current_row + dr, colS + dc
            # Ensure drawing is within grid bounds
            if 0 <= r_draw < rows and 0 <= c_draw < cols:
                output_grid[r_draw, c_draw] = ci

    return output_grid.tolist()