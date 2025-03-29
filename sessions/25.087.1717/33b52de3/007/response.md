```python
import numpy as np
from collections import defaultdict

"""
Transformation Rule:

1.  Initialize: Create a copy of the input grid to serve as the output grid.
2.  Identify Templates: Scan the input grid to find all instances of the "template" pattern: a 3x3 area where the 8 border pixels are gray (5) and the center pixel is *not* gray. For each template found, record the set of coordinates for its 8 gray border pixels and the coordinate of its top-left corner.
3.  Handle No Templates: If no template instances are found, return the initial output grid (the unchanged copy of the input).
4.  Determine Template Grid Structure:
    a.  Collect the top-left corner coordinates of all found template instances.
    b.  Determine the sorted list of unique row indices and unique column indices from these corners.
    c.  The number of unique rows is the template grid height (`tr`).
    d.  The number of unique columns is the template grid width (`tc`).
    e.  Create a mapping (e.g., a dictionary) where keys are logical grid indices `(r_idx, c_idx)` (from `(0,0)` to `(tr-1, tc-1)`) and values are the corresponding template objects found at that logical position in the grid.
5.  Identify Key Region Anchor:
    a.  Create a set containing the coordinates of all gray pixels belonging to *any* identified template instance.
    b.  Scan the input grid row by row, column by column, to find the first pixel `(r, c)` that meets all the following criteria:
        i.  Its color is not background (0).
        ii. Its color is not gray (5).
        iii. Its coordinate `(r, c)` is not in the set of template pixels identified in step 5a.
    c.  Record the coordinate `(r, c)` of this first matching pixel as the key region anchor `(key_min_r, key_min_c)`.
6.  Handle No Anchor: If no anchor pixel is found (meaning there are no non-background, non-gray pixels outside the templates), return the initial output grid.
7.  Apply Transformation: Iterate through each logical position `(r_idx, c_idx)` of the template grid (from `(0, 0)` up to `(tr-1, tc-1)`).
    a.  Check if a template instance exists at this logical position using the mapping created in step 4e.
    b.  If a template exists at `(r_idx, c_idx)`:
        i.  Calculate the corresponding source coordinate within the key region in the original input grid: `src_r = key_min_r + r_idx`, `src_c = key_min_c + c_idx`.
        ii. Retrieve the replacement color from the *original input grid* at `(src_r, src_c)`. Handle potential out-of-bounds access if `src_r` or `src_c` fall outside the input grid dimensions.
        iii. Retrieve the set of 8 gray pixel coordinates associated with the current template instance `(r_idx, c_idx)`.
        iv. For each coordinate `(px_r, px_c)` in this set, update the color of the pixel at `(px_r, px_c)` in the *output grid* to the retrieved replacement color.
8.  Return Result: Return the modified output grid.
"""

def find_template_objects(grid):
    """
    Finds all 3x3 hollow gray square template objects in the grid.
    A template is defined by 8 gray pixels forming the border of a 3x3 square,
    and the center pixel NOT being gray.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, each representing a template object with keys:
              'pixels' (set of (r, c) tuples for the 8 gray border pixels),
              'top_left' (tuple: r, c).
    """
    templates = []
    h, w = grid.shape
    gray = 5

    # Iterate up to h-3 and w-3 to allow checking a 3x3 area
    for r in range(h - 2):
        for c in range(w - 2):
            # Check if the 8 border pixels of the 3x3 square starting at (r,c) are gray
            is_template_border = True
            template_pixels = set()

            # Coordinates of the 8 border pixels relative to (r, c)
            border_coords_relative = [
                (0, 0), (0, 1), (0, 2),
                (1, 0),         (1, 2),
                (2, 0), (2, 1), (2, 2)
            ]

            for dr, dc in border_coords_relative:
                pr, pc = r + dr, c + dc
                if grid[pr, pc] == gray:
                    template_pixels.add((pr, pc))
                else:
                    is_template_border = False
                    break

            # If border is gray, check center pixel is NOT gray
            is_hollow = False
            if is_template_border:
                 center_r, center_c = r + 1, c + 1
                 # Check bounds for center (should be fine given loop limits)
                 if 0 <= center_r < h and 0 <= center_c < w and grid[center_r, center_c] != gray:
                     is_hollow = True

            # If all checks passed (gray border, non-gray center, 8 pixels), store the template
            if is_template_border and is_hollow:
                 # Double-check pixel count (should be 8)
                if len(template_pixels) == 8:
                    templates.append({
                        'pixels': template_pixels,
                        'top_left': (r, c)
                    })

    return templates

def transform(input_grid_list):
    """
    Applies the transformation rule based on templates and a key source region
    defined by an anchor point and template grid dimensions.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    # 1. Initialize output grid
    output_grid = np.copy(input_grid)
    h, w = input_grid.shape
    gray = 5
    background = 0

    # 2. Identify Templates
    template_instances = find_template_objects(input_grid)

    # 3. Handle No Templates
    if not template_instances:
        return output_grid.tolist() # Return original if no templates found

    # 4. Determine Template Grid Structure
    corners = sorted([t['top_left'] for t in template_instances])
    # Determine unique rows and columns from template corners
    template_rows = sorted(list(set(r for r, c in corners)))
    template_cols = sorted(list(set(c for r, c in corners)))
    tr = len(template_rows) # template grid height
    tc = len(template_cols) # template grid width

    # Create mapping from logical grid index (r_idx, c_idx) to the actual template object
    template_map = {}
    # Create reverse lookups for rows/cols to logical indices
    row_map = {row_val: r_idx for r_idx, row_val in enumerate(template_rows)}
    col_map = {col_val: c_idx for c_idx, col_val in enumerate(template_cols)}
    # Build the map using the template instances
    for template_obj in template_instances:
        r_val, c_val = template_obj['top_left']
        # Ensure the corner belongs to the grid structure derived from unique rows/cols
        if r_val in row_map and c_val in col_map:
             r_idx = row_map[r_val]
             c_idx = col_map[c_val]
             template_map[(r_idx, c_idx)] = template_obj

    # 5. Identify Key Region Anchor
    # 5a. Get all gray pixels belonging to any template
    all_template_pixels = set().union(*(t['pixels'] for t in template_instances))
    key_region_anchor = None
    # 5b. Scan grid for the anchor pixel
    for r in range(h):
        for c in range(w):
            color = input_grid[r, c]
            coord = (r, c)
            # Check criteria: not background, not gray, not part of a template's gray pixels
            if color != background and color != gray and coord not in all_template_pixels:
                key_region_anchor = coord # Found the top-leftmost anchor
                break # Exit inner loop
        if key_region_anchor:
            break # Exit outer loop

    # 6. Handle No Anchor
    if key_region_anchor is None:
        # No suitable anchor pixel found, return the original grid
        return output_grid.tolist()

    key_min_r, key_min_c = key_region_anchor

    # 7. Apply Transformation
    # Iterate through logical template grid positions
    for r_idx in range(tr):
        for c_idx in range(tc):
            # 7a. Check if a template exists at this logical position
            if (r_idx, c_idx) in template_map:
                template_obj = template_map[(r_idx, c_idx)]

                # 7b. Determine source coordinate and get replacement color
                src_r = key_min_r + r_idx
                src_c = key_min_c + c_idx

                # Check if source coordinate is within the input grid bounds
                if 0 <= src_r < h and 0 <= src_c < w:
                    replacement_color = input_grid[src_r, src_c]

                    # 7c. Get the 8 gray pixels for this template
                    pixels_to_replace = template_obj['pixels']

                    # 7d. Replace pixels in the output grid
                    for (px_r, px_c) in pixels_to_replace:
                        # Ensure target coordinates are valid (should be, as they came from template finding)
                        if 0 <= px_r < h and 0 <= px_c < w:
                            # Replace the color in the output grid
                            output_grid[px_r, px_c] = replacement_color
                # else: source coordinate is out of bounds. This indicates an issue
                #       either with anchor finding or template grid calculation.
                #       Silently ignore for now, or could raise an error/warning.

    # 8. Return Result
    return output_grid.tolist()
```