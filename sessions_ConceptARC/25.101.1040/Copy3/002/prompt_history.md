
## train_1

**input:**
```
0 0 4 4 4 0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 1 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 4 4 4 0 0 0 0
```


**output:**
```
0 0 4 4 4 0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 4 0 0 0 0
0 0 1 0 1 0 1 0 0 1 0 1 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 3 3 3 3 3 0 0
0 0 0 0 4 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 4 0 0 0 0
0 0 4 4 4 0 0 0 0 4 4 4 0 0 0 0
```


## train_2

**input:**
```
6 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 7 0 0 0 0 0 0 0 0 0 0
3 4 7 0 0 0 6 6 0 0 0 0 0
3 0 7 0 0 0 0 0 0 0 0 0 0
3 4 7 0 0 0 0 0 7 0 0 0 0
4 0 0 0 0 0 0 0 7 0 0 0 0
0 4 0 0 0 0 0 0 7 0 0 0 0
0 0 6 6 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 7 0 0 0 0 0 0 0 0 0 0
3 4 7 0 0 0 6 6 0 0 0 0 0
3 0 7 0 0 0 0 0 0 0 0 0 0
3 4 7 0 0 0 3 0 7 0 0 0 0
4 0 0 0 0 0 3 4 7 0 0 0 0
0 4 0 0 0 0 3 0 7 0 0 0 0
0 0 6 6 0 0 3 4 7 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples to understand the transformation rule.

## Perception

1.  **Grid Structure**: Both examples involve transforming a grid into another grid of the *same dimensions*.
2.  **Example 1 (train_1)**:
    *   The input grid has a width of 16 (even).
    *   Various patterns (yellow 'L' shapes, a blue dotted line, a green bar, small yellow dots/lines) exist, mostly concentrated on the left half (columns 0-7).
    *   The output grid appears to be created by taking the left half of the input grid (columns 0-7) and copying it onto the right half (columns 8-15), overwriting the original content of the right half. The left half remains unchanged.
3.  **Example 2 (train_2)**:
    *   The input grid has a width of 13 (odd).
    *   It contains several distinct objects/patterns: magenta rectangles, a complex shape made of green, yellow, and orange pixels ('Object A') on the left, and scattered orange pixels and magenta rectangles on the right.
    *   The output grid shows that 'Object A' from the left side (specifically, the content within the bounding box from row 2, col 0 to row 7, col 2) has been copied to a new location starting at row 5, col 6.
    *   The original content at the destination location (mostly white space, but including some orange pixels) is overwritten by the copied pattern. Other elements, like the magenta rectangles, remain in their original positions.
4.  **Key Difference**: The transformation logic seems to differ based on some property of the input grid. In train_1 (even width, no magenta), a simple half-grid copy occurs. In train_2 (odd width, contains magenta), a specific complex pattern is identified and copied to a location possibly determined by a magenta marker object. The copy destination in train_2 appears related to the magenta `6 6` block at (3, 6) in the input, with the copy starting 2 rows below it.

## Facts


```yaml
task_description: Copy patterns within the grid based on grid properties or specific markers.

example_1:
  input_grid_properties:
    height: 11
    width: 16
    colors_present: [white, yellow, blue, green]
    contains_magenta: false
  objects:
    - id: left_half
      description: Columns 0 through 7 of the grid.
      contains_patterns: [yellow_L_top, blue_dotted_line, green_bar, misc_yellow]
    - id: right_half
      description: Columns 8 through 15 of the grid.
      contains_patterns: [yellow_L_top, empty_space]
  action:
    type: copy
    source: left_half
    destination: right_half
    overwrite: true
  output_grid_properties:
    identical_dimensions: true
    content: Left half is unchanged, right half is identical to the left half.

example_2:
  input_grid_properties:
    height: 15
    width: 13
    colors_present: [white, magenta, green, orange, yellow]
    contains_magenta: true
  objects:
    - id: pattern_A
      description: Complex pattern composed of green, yellow, orange pixels.
      location: Bounding box (rows 2-7, cols 0-2)
    - id: marker_1
      description: Magenta 1x2 rectangle
      location: (0, 0)
    - id: marker_2
      description: Magenta 1x2 rectangle
      location: (3, 6) # Seems relevant for destination
    - id: marker_3
      description: Magenta 1x2 rectangle
      location: (8, 2)
    - id: marker_4
      description: Magenta 1x2 rectangle
      location: (11, 8)
    - id: other_pixels
      description: Scattered orange pixels on the right side.
  action:
    type: copy
    source: pattern_A (content of its bounding box)
    destination_anchor: marker_2 at (3, 6)
    destination_top_left: Calculated as (marker_2.row + 2, marker_2.col) = (5, 6)
    overwrite: true
  output_grid_properties:
    identical_dimensions: true
    content: pattern_A is copied starting at (5, 6), overwriting original content. Other markers and pixels remain unchanged.

general_rule_hypothesis:
  condition: Check if magenta (color 6) is present in the input grid.
  case_no_magenta:
    condition: Grid width W is even. (Assumption based on example 1)
    action: Copy columns 0 to W/2 - 1 to columns W/2 to W - 1.
  case_magenta_present:
    condition: Grid width W is odd. (Assumption based on example 2)
    action:
      1. Identify the largest connected component group containing colors other than white and magenta ('source pattern'). Get its bounding box.
      2. Identify potential 'marker' objects (magenta rectangles/pixels).
      3. Select the relevant marker (e.g., based on proximity below/after the source pattern). Let its top-left be (r_mark, c_mark).
      4. Calculate the destination top-left as (r_mark + 2, c_mark).
      5. Copy the source pattern (content of its bounding box) to the calculated destination.
```


## Natural Language Program

1.  Examine the input grid to determine if any pixels have the color magenta (6).
2.  **If no magenta pixels are present**:
    a. Determine the width `W` of the grid.
    b. Define the left half of the grid as columns from 0 to `W/2 - 1`.
    c. Define the right half of the grid as columns from `W/2` to `W - 1`.
    d. Create the output grid by copying the input grid.
    e. For each row `r` from 0 to `height - 1`:
        i. For each column `c` from 0 to `W/2 - 1`:
            - Set the pixel value at `(r, c + W/2)` in the output grid to the value of the pixel at `(r, c)` in the input grid.
3.  **If magenta pixels are present**:
    a. Identify all connected components of non-white pixels. Find the component `P` that is the "main pattern" (heuristic: largest bounding box area containing non-magenta colors, as seen in example 2). Determine the bounding box of `P`: `(min_row_P, min_col_P)` to `(max_row_P, max_col_P)`.
    b. Identify all magenta objects/pixels. Find the specific "marker" magenta object `M` (heuristic: the top-most magenta object whose column is greater than `max_col_P` and whose row is closest to `min_row_P`, as seen in example 2). Let the top-left corner of `M` be `(row_M, col_M)`.
    c. Calculate the destination top-left corner `(dest_row, dest_col)` as `(row_M + 2, col_M)`.
    d. Create the output grid by copying the input grid.
    e. Iterate through the pixels within the bounding box of the source pattern `P`. For each source pixel at `(r_src, c_src)` within the bounding box (where `r_src` ranges from `min_row_P` to `max_row_P`, and `c_src` ranges from `min_col_P` to `max_col_P`):
        i. Calculate the corresponding destination coordinates: `(r_dest, c_dest) = (dest_row + (r_src - min_row_P), dest_col + (c_src - min_col_P))`.
        ii. If `(r_dest, c_dest)` is within the grid boundaries, set the pixel value at `(r_dest, c_dest)` in the output grid to the value of the pixel at `(r_src, c_src)` in the input grid.
4.  Return the modified output grid.
```python
import copy
import collections

"""
This function transforms an input grid based on the presence or absence of magenta pixels (color 6).

1. Checks if magenta (color 6) is present in the input grid.

2. If no magenta is present:
   - Assumes the grid width `W` is even.
   - Copies the left half of the grid (columns 0 to W/2 - 1) to the right half (columns W/2 to W - 1), overwriting the original content of the right half.
   - The left half remains unchanged.

3. If magenta is present:
   - Identifies connected components of non-white pixels.
   - Filters these components to find the "main pattern" `P`: the component with the largest bounding box area that does *not* contain only magenta pixels.
   - Identifies magenta pixels/components. Finds the "marker" magenta component `M`: the top-most, left-most magenta component whose minimum column index is greater than the maximum column index of the main pattern `P`.
   - Calculates a destination top-left corner `(dest_row, dest_col)` based on the marker's top-left corner `(row_M, col_M)` using the formula `(row_M + 2, col_M)`.
   - Copies the content of the bounding box of the main pattern `P` to the calculated destination area in the output grid, overwriting existing content.
   - All other parts of the grid remain unchanged from the input.
"""

def find_connected_components(grid: list[list[int]], ignore_color: int = 0) -> list[dict]:
    """
    Finds all connected components in the grid, ignoring a specific color (usually white background).

    Args:
        grid: The input grid (list of lists of integers).
        ignore_color: The color value to ignore (treat as background).

    Returns:
        A list of dictionaries, where each dictionary represents a component and contains:
        - 'coords': A set of (row, col) tuples belonging to the component.
        - 'colors': A set of color values present in the component.
        - 'bounding_box': A tuple (min_row, min_col, max_row, max_col).
        - 'bounding_box_area': The area of the bounding box.
    """
    height = len(grid)
    width = len(grid[0])
    visited = set()
    components = []

    for r in range(height):
        for c in range(width):
            if grid[r][c] != ignore_color and (r, c) not in visited:
                component_coords = set()
                component_colors = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    component_coords.add((row, col))
                    component_colors.add(grid[row][col])
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr][nc] != ignore_color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))

                bbox = (min_r, min_c, max_r, max_c)
                bbox_area = (max_r - min_r + 1) * (max_c - min_c + 1)
                components.append({
                    'coords': component_coords,
                    'colors': component_colors,
                    'bounding_box': bbox,
                    'bounding_box_area': bbox_area
                })
    return components

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on magenta presence.

    Args:
        input_grid: The input grid (list of lists of integers).

    Returns:
        The transformed output grid (list of lists of integers).
    """
    height = len(input_grid)
    width = len(input_grid[0])
    output_grid = copy.deepcopy(input_grid)
    magenta_color = 6
    white_color = 0

    # Check for magenta presence
    has_magenta = any(magenta_color in row for row in input_grid)

    if not has_magenta:
        # Case 1: No magenta - Copy left half to right half
        if width % 2 == 0: # Ensure width is even as per observation
            mid_col = width // 2
            for r in range(height):
                for c in range(mid_col):
                    # Copy pixel from left half (r, c) to right half (r, c + mid_col)
                    output_grid[r][c + mid_col] = input_grid[r][c]
        # If width is odd and no magenta, the rule is undefined by examples. Return input copy.
        # Update: Example 2 has odd width *and* magenta. Example 1 has even width *and* no magenta.
        # Assume the condition is just 'no magenta' leads to mirroring if width is even.
        # If width is odd and no magenta, based on current examples, do nothing.
        
    else:
        # Case 2: Magenta is present - Find pattern, marker, and copy
        components = find_connected_components(input_grid, ignore_color=white_color)

        # Identify the main pattern P (largest non-magenta-only component by bbox area)
        main_pattern = None
        max_area = -1
        non_magenta_components = [comp for comp in components if not (comp['colors'] == {magenta_color})]
        
        if not non_magenta_components: # Should not happen based on example 2, but handle edge case
             return output_grid # Or raise error? Return copy for now.

        # Heuristic: Find the component with the largest bounding box area among those not solely magenta
        for comp in non_magenta_components:
             if comp['bounding_box_area'] > max_area:
                 max_area = comp['bounding_box_area']
                 main_pattern = comp
             # Tie-breaking: if areas are equal, maybe prefer top-most, then left-most?
             # For now, first one encountered with max area is chosen.
             elif comp['bounding_box_area'] == max_area:
                 if main_pattern is None or comp['bounding_box'][0] < main_pattern['bounding_box'][0] or \
                    (comp['bounding_box'][0] == main_pattern['bounding_box'][0] and comp['bounding_box'][1] < main_pattern['bounding_box'][1]):
                     main_pattern = comp


        if not main_pattern:
            # No suitable pattern found
            return output_grid 

        # Identify magenta components
        magenta_components = [comp for comp in components if magenta_color in comp['colors']]

        if not magenta_components:
             # Magenta pixels exist but not forming components? Or logic error.
             return output_grid # Return copy

        # Identify the marker M (top-most, left-most magenta component starting after pattern P ends horizontally)
        pattern_min_r, pattern_min_c, pattern_max_r, pattern_max_c = main_pattern['bounding_box']
        
        relevant_markers = []
        for comp in magenta_components:
            marker_min_r, marker_min_c, _, _ = comp['bounding_box']
            # Condition: marker starts to the right of the pattern
            if marker_min_c > pattern_max_c:
                relevant_markers.append(comp)

        if not relevant_markers:
            # No marker found to the right of the pattern
            return output_grid # Return copy

        # Sort relevant markers: primary key = min_row (top-most), secondary key = min_col (left-most)
        relevant_markers.sort(key=lambda comp: (comp['bounding_box'][0], comp['bounding_box'][1]))
        
        marker_component = relevant_markers[0] # Select the top-most, left-most
        marker_min_r, marker_min_c, _, _ = marker_component['bounding_box']


        # Calculate destination top-left corner
        dest_row_start = marker_min_r + 2
        dest_col_start = marker_min_c

        # Copy the pattern P's bounding box content to the destination
        pattern_height = pattern_max_r - pattern_min_r + 1
        pattern_width = pattern_max_c - pattern_min_c + 1

        for r_offset in range(pattern_height):
            for c_offset in range(pattern_width):
                src_r, src_c = pattern_min_r + r_offset, pattern_min_c + c_offset
                dest_r, dest_c = dest_row_start + r_offset, dest_col_start + c_offset

                # Check if source pixel is part of the actual component (not just bbox)
                # and destination is within grid bounds
                # Note: We copy the *entire bounding box content* as per example 2.
                # If we only wanted to copy the component shape, we'd check `(src_r, src_c) in main_pattern['coords']`
                if 0 <= dest_r < height and 0 <= dest_c < width:
                    output_grid[dest_r][dest_c] = input_grid[src_r][src_c]

    return output_grid
```
