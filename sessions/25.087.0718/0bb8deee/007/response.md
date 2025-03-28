```python
import numpy as np

"""
Transformation Rule:

1.  **Identify Solid Dividing Lines:**
    a.  Scan the input grid row by row to find any **solid horizontal line**. A solid horizontal line at row `R` consists *entirely* of a single non-white color `C_h` across the full width of the grid.
    b.  Scan the input grid column by column to find any **solid vertical line**. A solid vertical line at column `Col` consists *entirely* of a single non-white color `C_v` across the full height of the grid.
    c.  Find the *unique* pair of a solid horizontal line (row `R`, color `C_h`) and a solid vertical line (column `Col`, color `C_v`) such that their colors match (`C_h == C_v`). Let this common color be the `dividing_color`. If no such unique pair exists, the transformation cannot proceed as defined (return a 6x6 all-white grid).
2.  **Define Quadrants:** Use the dividing line indices (`R`, `Col`) to define four rectangular regions (quadrants) *excluding* the dividing lines themselves:
    *   Top-Left (TL): `grid[0 : R, 0 : Col]`
    *   Top-Right (TR): `grid[0 : R, Col + 1 : width]`
    *   Bottom-Left (BL): `grid[R + 1 : height, 0 : Col]`
    *   Bottom-Right (BR): `grid[R + 1 : height, Col + 1 : width]`
3.  **Extract Content:** For each of the four quadrants:
    a.  Isolate the subgrid corresponding to the quadrant's boundaries.
    b.  Within this subgrid, identify the locations of all pixels whose color is *neither* the background color (0) *nor* the `dividing_color`.
    c.  If no such pixels are found, this quadrant's content is considered empty.
    d.  If such pixels exist, determine the minimal bounding box (smallest rectangle) that encloses *all* of them, relative to the quadrant's top-left corner.
    e.  Extract the subgrid defined by this bounding box. This is the quadrant's `content_grid`.
4.  **Assemble Output:** Create a new 6x6 grid, initialized entirely with the background color (0).
5.  **Place Content:** For each quadrant (TL, TR, BL, BR) and its corresponding extracted `content_grid` (which might be empty):
    a.  Determine the target 3x3 area in the output grid:
        *   TL -> rows 0-2, cols 0-2
        *   TR -> rows 0-2, cols 3-5
        *   BL -> rows 3-5, cols 0-2
        *   BR -> rows 3-5, cols 3-5
    b.  If the `content_grid` is not empty:
        i.  Determine the dimensions (`h`, `w`) of the `content_grid`.
        ii. Calculate the dimensions to copy: `copy_h = min(h, 3)`, `copy_w = min(w, 3)`.
        iii. Copy the top-left `copy_h` x `copy_w` portion of the `content_grid` into the target 3x3 area, starting at the top-left corner (e.g., `output[0:copy_h, 0:copy_w]` for TL). The remaining parts of the 3x3 area stay background color (0).
    c.  If the `content_grid` is empty, the target 3x3 area remains filled with the background color.
6.  **Return:** The final 6x6 assembled grid.
"""


def find_dividing_lines(grid):
    """
    Finds the row index, column index, and color of the intersecting
    SOLID horizontal and SOLID vertical dividing lines.
    A solid line consists entirely of a single non-white color.
    """
    rows, cols = grid.shape
    candidate_rows = {} # Store {row_index: color}
    candidate_cols = {} # Store {col_index: color}

    # Find SOLID candidate horizontal lines
    for r in range(rows):
        line = grid[r, :]
        unique_colors = np.unique(line)
        # Must have exactly one unique color, and it must not be white (0)
        if len(unique_colors) == 1 and unique_colors[0] != 0:
            candidate_rows[r] = unique_colors[0]

    # Find SOLID candidate vertical lines
    for c in range(cols):
        line = grid[:, c]
        unique_colors = np.unique(line)
        # Must have exactly one unique color, and it must not be white (0)
        if len(unique_colors) == 1 and unique_colors[0] != 0:
            candidate_cols[c] = unique_colors[0]

    # Find the unique matching intersection
    found_intersections = []
    for r, h_color in candidate_rows.items():
        for c, v_color in candidate_cols.items():
            # Check if colors match
            # The intersection pixel check (grid[r, c] == h_color) is guaranteed
            # because both the row and column are solid lines of that color.
            if h_color == v_color:
                found_intersections.append((r, c, h_color))

    # Expecting exactly one valid intersection
    if len(found_intersections) == 1:
        # Convert numpy int type to standard python int if needed
        r_idx, c_idx, color = found_intersections[0]
        return int(r_idx), int(c_idx), int(color)
    else:
        # If zero or multiple intersections are found, the rule is ambiguous or fails
        # print(f"Warning/Error: Found {len(found_intersections)} intersections. Expected 1.")
        return -1, -1, -1 # Indicate failure


def extract_quadrant_content(grid, r_start, r_end, c_start, c_end, dividing_color):
    """
    Extracts the minimal bounding box of content from a specified quadrant,
    excluding background (0) and the dividing_color.
    """
    # Ensure boundary indices are valid and define the quadrant slice
    r_start = max(0, r_start)
    r_end = min(grid.shape[0], r_end)
    c_start = max(0, c_start)
    c_end = min(grid.shape[1], c_end)

    # Check for invalid or zero-sized quadrant definitions
    if r_start >= r_end or c_start >= c_end:
        return None

    quadrant = grid[r_start:r_end, c_start:c_end]

    # Find coordinates of relevant content pixels (not background, not dividing color)
    # relative to the quadrant's top-left corner
    content_coords = np.argwhere((quadrant != 0) & (quadrant != dividing_color))

    if content_coords.size == 0:
        # No relevant content found in this quadrant
        return None

    # Determine minimal bounding box relative to the quadrant
    min_r_rel = np.min(content_coords[:, 0])
    max_r_rel = np.max(content_coords[:, 0])
    min_c_rel = np.min(content_coords[:, 1])
    max_c_rel = np.max(content_coords[:, 1])

    # Extract the content using these relative coordinates
    content = quadrant[min_r_rel : max_r_rel + 1, min_c_rel : max_c_rel + 1]
    return content


def place_content(output_grid, content, r_offset, c_offset):
    """
    Places extracted content into a designated 3x3 subgrid of the output grid,
    starting at (r_offset, c_offset). Crops content if larger than 3x3.
    Assumes target area is 3x3.
    """
    target_h, target_w = 3, 3 # Target subgrid size

    if content is None or content.size == 0:
        # No content to place, the target area remains background (already initialized)
        return

    content_h, content_w = content.shape

    # Determine the dimensions of the content to actually copy (crop if needed)
    copy_h = min(content_h, target_h)
    copy_w = min(content_w, target_w)

    # Place the (potentially cropped) content into the output grid's target area
    output_grid[r_offset : r_offset + copy_h, c_offset : c_offset + copy_w] = content[0:copy_h, 0:copy_w]


def transform(input_grid):
    # Convert input list of lists to numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # 1. Identify the solid dividing lines and their intersection
    div_row, div_col, div_color = find_dividing_lines(input_np)

    # Handle case where dividing lines are not found as expected
    if div_row == -1 or div_col == -1:
        # If no unique solid dividing lines are found, return a default 6x6 grid of zeros
        return np.zeros((6, 6), dtype=int).tolist()

    # 2. Define quadrant boundaries (exclusive of the dividing lines)
    tl_r_start, tl_r_end = 0, div_row
    tl_c_start, tl_c_end = 0, div_col

    tr_r_start, tr_r_end = 0, div_row
    tr_c_start, tr_c_end = div_col + 1, cols

    bl_r_start, bl_r_end = div_row + 1, rows
    bl_c_start, bl_c_end = 0, div_col

    br_r_start, br_r_end = div_row + 1, rows
    br_c_start, br_c_end = div_col + 1, cols

    # 3. Extract content from each quadrant, excluding background and dividing color
    content_tl = extract_quadrant_content(input_np, tl_r_start, tl_r_end, tl_c_start, tl_c_end, div_color)
    content_tr = extract_quadrant_content(input_np, tr_r_start, tr_r_end, tr_c_start, tr_c_end, div_color)
    content_bl = extract_quadrant_content(input_np, bl_r_start, bl_r_end, bl_c_start, bl_c_end, div_color)
    content_br = extract_quadrant_content(input_np, br_r_start, br_r_end, br_c_start, br_c_end, div_color)

    # 4. Create the 6x6 output grid, initialized to background color (0)
    output_h, output_w = 6, 6
    output_grid = np.zeros((output_h, output_w), dtype=int)

    # 5. Place extracted content into the corresponding 3x3 output subgrids
    place_content(output_grid, content_tl, 0, 0)          # Top-left section (0:3, 0:3)
    place_content(output_grid, content_tr, 0, 3)          # Top-right section (0:3, 3:6)
    place_content(output_grid, content_bl, 3, 0)          # Bottom-left section (3:6, 0:3)
    place_content(output_grid, content_br, 3, 3)          # Bottom-right section (3:6, 3:6)

    # 6. Return the final grid as a list of lists
    return output_grid.tolist()
```