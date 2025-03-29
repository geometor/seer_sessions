```python
import numpy as np
from collections import defaultdict
import sys

# Increase recursion depth for deep copies or large structures if necessary
# sys.setrecursionlimit(2000) # Example adjustment, use if needed

"""
Transformation Rule:

1.  **Identify Templates:** Scan the input grid to find all instances of the template pattern: a 3x3 hollow square made entirely of gray (5) pixels (meaning the 8 border pixels are gray). Record the set of coordinates for the 8 gray pixels belonging to each template instance and its top-left corner.
2.  **Determine Template Grid Structure:** Analyze the top-left corners of the found template instances. Determine the number of unique rows (`tr`) and unique columns (`tc`) these templates occupy, effectively defining the dimensions of a "template grid". Create a mapping to easily access the specific template instance corresponding to each logical grid position `(r_idx, c_idx)`, where `0 <= r_idx < tr` and `0 <= c_idx < tc`. If no templates are found, return the input grid unchanged.
3.  **Identify Key Source Pixels:** Create a set of all pixel coordinates `(r, c)` in the input grid that meet three criteria: (a) the color `input_grid[r, c]` is not background (0), (b) the color `input_grid[r, c]` is not gray (5), and (c) the coordinate `(r, c)` is not part of any pixel set belonging to the templates identified in step 1.
4.  **Determine Key Source Bounding Box:** If any key source pixels were found in step 3, calculate the minimum bounding box that encloses all of them. Record its top-left corner `(key_min_r, key_min_c)`, its height `key_h`, and its width `key_w`. If no key source pixels were found, return the input grid unchanged.
5.  **Validate Dimensions:** Check if the template grid height `tr` is equal to the key source bounding box height `key_h`, AND if the template grid width `tc` is equal to the key source bounding box width `key_w`. If these dimensions do not match, return the input grid unchanged.
6.  **Prepare Output Grid:** Create a copy of the input grid to serve as the output grid.
7.  **Apply Transformation:** Iterate through each logical position `(r_idx, c_idx)` of the template grid (from `(0, 0)` to `(tr-1, tc-1)`).
    a.  Check if a template instance exists at this logical position using the mapping from step 2.
    b.  If a template exists:
        i.  Determine the corresponding source coordinate within the key region in the original grid: `src_r = key_min_r + r_idx`, `src_c = key_min_c + c_idx`.
        ii. Retrieve the replacement color from the *original input grid* at `(src_r, src_c)`.
        iii. For every pixel coordinate `(px_r, px_c)` belonging to the 8 gray pixels of the current template instance, update its color in the *output grid* to the retrieved replacement color.
8.  **Return Result:** Return the modified output grid.
"""

def find_template_objects(grid):
    """
    Finds all 3x3 hollow gray square template objects in the grid.
    A template is defined by 8 gray pixels forming the border of a 3x3 square.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, each representing a template object with keys:
              'pixels' (set of (r, c) tuples for the 8 gray pixels),
              'top_left' (tuple: r, c).
    """
    templates = []
    h, w = grid.shape
    gray = 5

    # Iterate up to h-3 and w-3 to allow checking a 3x3 area
    for r in range(h - 2):
        for c in range(w - 2):
            # Check if the 8 border pixels of the 3x3 square starting at (r,c) are gray
            is_template = True
            template_pixels = set()

            # Top row
            if grid[r, c] == gray and grid[r, c+1] == gray and grid[r, c+2] == gray:
                template_pixels.add((r, c))
                template_pixels.add((r, c+1))
                template_pixels.add((r, c+2))
            else:
                is_template = False

            # Middle row (sides)
            if is_template and grid[r+1, c] == gray and grid[r+1, c+2] == gray:
                template_pixels.add((r+1, c))
                template_pixels.add((r+1, c+2))
            elif is_template:
                is_template = False

            # Bottom row
            if is_template and grid[r+2, c] == gray and grid[r+2, c+1] == gray and grid[r+2, c+2] == gray:
                template_pixels.add((r+2, c))
                template_pixels.add((r+2, c+1))
                template_pixels.add((r+2, c+2))
            elif is_template:
                is_template = False

            # If all checks passed, store the template
            if is_template:
                # Double-check pixel count (should be 8)
                if len(template_pixels) == 8:
                    templates.append({
                        'pixels': template_pixels,
                        'top_left': (r, c)
                    })

    return templates

def transform(input_grid_list):
    """
    Applies the transformation rule based on templates and a key source region.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.copy(input_grid)
    h, w = input_grid.shape
    gray = 5
    background = 0

    # 1. Identify Templates
    template_instances = find_template_objects(input_grid)

    # 2. Determine Template Grid Structure & Handle Edge Case (No Templates)
    if not template_instances:
        return output_grid.tolist() # Return original if no templates

    # Extract top-left corners and determine unique rows/cols
    corners = sorted([t['top_left'] for t in template_instances])
    template_rows = sorted(list(set(r for r, c in corners)))
    template_cols = sorted(list(set(c for r, c in corners)))
    tr = len(template_rows) # template grid height
    tc = len(template_cols) # template grid width

    # Create mapping from template grid index (r_idx, c_idx) to the actual object
    template_map = {}
    # Create reverse lookups for rows/cols to indices
    row_map = {row_val: r_idx for r_idx, row_val in enumerate(template_rows)}
    col_map = {col_val: c_idx for c_idx, col_val in enumerate(template_cols)}
    # Build the map using the template instances
    for template_obj in template_instances:
        r_val, c_val = template_obj['top_left']
        if r_val in row_map and c_val in col_map: # Ensure corner belongs to the identified grid
             r_idx = row_map[r_val]
             c_idx = col_map[c_val]
             template_map[(r_idx, c_idx)] = template_obj


    # 3. Identify Key Source Pixels
    all_template_pixels = set().union(*(t['pixels'] for t in template_instances))
    key_source_pixels = []
    for r in range(h):
        for c in range(w):
            color = input_grid[r, c]
            coord = (r, c)
            if color != background and color != gray and coord not in all_template_pixels:
                key_source_pixels.append(coord)

    # 4. Determine Key Source Bounding Box & Handle Edge Case (No Key Pixels)
    if not key_source_pixels:
        return output_grid.tolist() # Return original if no key pixels

    key_min_r = min(r for r, c in key_source_pixels)
    key_min_c = min(c for r, c in key_source_pixels)
    key_max_r = max(r for r, c in key_source_pixels)
    key_max_c = max(c for r, c in key_source_pixels)
    key_h = key_max_r - key_min_r + 1
    key_w = key_max_c - key_min_c + 1

    # 5. Validate Dimensions
    if key_h != tr or key_w != tc:
        return output_grid.tolist() # Return original if dimensions don't match

    # 6. Prepare Output Grid (already done: output_grid = np.copy(input_grid))

    # 7. Apply Transformation
    for r_idx in range(tr):
        for c_idx in range(tc):
            # 7a. Check if a template exists at this logical position
            if (r_idx, c_idx) in template_map:
                template_obj = template_map[(r_idx, c_idx)]

                # 7b. Determine source coordinate and get replacement color
                src_r = key_min_r + r_idx
                src_c = key_min_c + c_idx

                # Bounds check for safety, though dimensions should match
                if 0 <= src_r < h and 0 <= src_c < w:
                    replacement_color = input_grid[src_r, src_c]

                    # 7c. Replace pixels in the output grid
                    for (px_r, px_c) in template_obj['pixels']:
                        # Ensure coordinates are valid (should be)
                        if 0 <= px_r < h and 0 <= px_c < w:
                           # Check if the pixel in the *original* input was gray,
                           # to avoid overwriting something else if templates overlapped (unlikely but safe)
                           # Although, output_grid initially is a copy, so checking output_grid[px_r, px_c] == gray works too.
                           # Let's check the original input for conceptual clarity.
                           if input_grid[px_r, px_c] == gray:
                               output_grid[px_r, px_c] = replacement_color
                # else: Handle case where calculated source coordinate is out of bounds (error condition)
                #      Might indicate flaw in dimension check or key source calculation.
                #      Current logic relies on dimension check passing.

    # 8. Return Result
    return output_grid.tolist()
```