```python
"""
Transforms the input grid based on the following rules:
1.  Create the output grid by copying the input grid.
2.  Locate the vertical gray (5) line and identify its column index, `gray_col`. If no gray line is found, return the initial copy.
3.  Calculate the width for the red regions, `w_red`, by counting the number of consecutive columns starting immediately to the right of the gray line (`gray_col + 1`) in the *input* grid that consist entirely of magenta (6) pixels. The width `w_red` is this count, capped at a maximum of 4.
4.  Identify all distinct contiguous white (0) objects located entirely to the left of the gray line (`gray_col`) in the input grid using 4-connectivity.
5.  For each white object identified:
    a.  Determine its rightmost column index, `max_c`.
    b.  Calculate the horizontal shift distance needed: `shift = max(0, (gray_col - 1) - max_c)`.
    c.  Determine if the object was shifted (`shifted = shift > 0`).
    d.  Find the set of rows (`final_touch_rows`) where the object's pixels will reside in the column `gray_col - 1` in the output grid (after applying the shift).
6.  Perform the object movement on the output grid:
    a.  For every white object that `shifted`, change all its original pixel locations `(r, c)` in the output grid to magenta (6).
    b.  For every white object, draw its pixels at their new locations `(r, c + shift)` in the output grid using white (0), ensuring `c + shift` is less than `gray_col`.
7.  Determine the final set of rows (`R_red`) that will receive red pixels:
    a.  Initialize `R_red` as an empty set.
    b.  For each white object that has a non-empty `final_touch_rows` set (i.e., it touches the boundary column `gray_col - 1` in the output):
        i.  Identify the contiguous vertical segments within its `final_touch_rows`. (e.g., if `final_touch_rows` is `{7, 8, 9, 11}`, the segments are `{7, 8, 9}` and `{11}`).
        ii. For each segment found:
            *   If the segment contains 3 or more rows: Add all rows from that segment to `R_red`, *except* for the smallest (topmost) row index and the largest (bottommost) row index within that segment.
            *   If the segment contains fewer than 3 rows, it contributes nothing to `R_red`.
8.  If the calculated `w_red` is greater than 0, paint the red regions: For each row index `r` in the final `R_red` set, change the pixels in the output grid from column `gray_col + 1` up to (but not including) column `gray_col + 1 + w_red` to red (2). Do not paint outside the grid's boundaries.
9.  Return the modified output grid.
"""

import numpy as np
from collections import deque

# Color constants
WHITE = 0
RED = 2
GRAY = 5
MAGENTA = 6

def find_gray_line_col(grid: np.ndarray) -> int:
    """Finds the column index of the vertical gray line."""
    rows, cols = grid.shape
    for c in range(cols):
        # Prioritize solid gray lines
        if np.all(grid[:, c] == GRAY):
            return c
    # Fallback: find first column with a majority of gray pixels (heuristic)
    for c in range(cols):
         if np.sum(grid[:, c] == GRAY) > rows // 2:
             return c
    return -1 # Indicate not found

def calculate_red_width(grid: np.ndarray, gray_col: int) -> int:
    """Calculates the width of the red region based on contiguous magenta columns in input."""
    rows, cols = grid.shape
    contiguous_magenta_cols = 0
    if gray_col != -1 and gray_col + 1 < cols:
        for c_check in range(gray_col + 1, cols):
            if np.all(grid[:, c_check] == MAGENTA):
                contiguous_magenta_cols += 1
            else:
                break
    # Cap width at 4 based on observations
    return min(4, contiguous_magenta_cols)

def find_objects(grid: np.ndarray, color: int, max_col: int) -> list[list[tuple[int, int]]]:
    """
    Finds connected objects (4-connectivity) of a specific color strictly left of max_col.
    Returns a list of objects, where each object is a list of its (row, col) coordinates.
    Ensures entire object is within bounds.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    for r in range(rows):
        # Only start searching in columns strictly less than max_col
        for c in range(max_col):
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                current_obj_visited = set([(r,c)]) # Track visited within this BFS

                while q:
                    row, col = q.popleft()
                    obj_coords.append((row, col))

                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        neighbor = (nr, nc)

                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and \
                           not visited[nr, nc] and \
                           neighbor not in current_obj_visited:

                            visited[nr, nc] = True
                            current_obj_visited.add(neighbor)
                            q.append(neighbor)

                # Final validity check: Ensure ALL pixels of the found object are < max_col
                final_is_valid = all(obj_c < max_col for _, obj_c in obj_coords)

                if final_is_valid and obj_coords:
                    objects.append(obj_coords)
                else:
                     # If invalid, ensure all explored pixels are marked visited anyway
                     # This prevents re-starting BFS from parts of an invalid object
                     for vr, vc in obj_coords:
                         if 0 <= vr < rows and 0 <= vc < cols:
                            visited[vr,vc] = True
    return objects


def get_object_max_c(obj_coords: list[tuple[int, int]]) -> int:
    """Calculates the rightmost column index for an object."""
    if not obj_coords:
        return -1
    return max(c for _, c in obj_coords)

def get_contiguous_segments(rows_set: set[int]) -> list[list[int]]:
    """ Groups a set of row indices into lists of contiguous segments. """
    if not rows_set:
        return []

    sorted_rows = sorted(list(rows_set))
    segments = []
    current_segment = [sorted_rows[0]]

    for i in range(1, len(sorted_rows)):
        if sorted_rows[i] == sorted_rows[i-1] + 1:
            current_segment.append(sorted_rows[i])
        else:
            segments.append(current_segment)
            current_segment = [sorted_rows[i]]
    segments.append(current_segment) # Add the last segment
    return segments


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """ Applies the object shifting and red region painting transformation based on boundary interactions."""
    
    # Initialize grid
    input_arr = np.array(input_grid, dtype=int)
    output_arr = np.copy(input_arr)
    rows, cols = input_arr.shape

    # --- Step 2: Find the gray line column ---
    gray_col = find_gray_line_col(input_arr)
    if gray_col == -1:
        # Cannot proceed without the barrier
        return input_grid # Return the copy

    # --- Step 3: Calculate red width ---
    w_red = calculate_red_width(input_arr, gray_col)

    # --- Step 4: Find white objects ---
    # Search strictly left of the gray column
    white_objects = find_objects(input_arr, WHITE, max_col=gray_col)

    # --- Step 5 & 6 prep: Calculate shifts and identify boundary interactions ---
    coords_to_erase = []
    coords_to_draw = []
    # Store info needed for red row calculation: (object_index, final_touch_rows)
    boundary_touchers_info = [] 

    for idx, obj_coords in enumerate(white_objects):
        if not obj_coords: continue

        # 5a: Get object's original rightmost column
        max_c = get_object_max_c(obj_coords)
        
        # 5b: Calculate shift
        shift = 0
        if max_c != -1 : # Ensure object exists
             shift = max(0, (gray_col - 1) - max_c)

        # 5c: Determine if shifted
        object_shifted = shift > 0
        
        # 5d: Find rows touching the boundary in the final state
        final_touch_rows_for_obj = set()
        target_coords_for_obj = [] # Collect target coords for drawing later

        for r, c in obj_coords:
            new_c = c + shift
            # Ensure drawing happens within bounds and left of gray line
            if 0 <= r < rows and 0 <= new_c < gray_col:
                 target_coords_for_obj.append((r, new_c))
                 if new_c == gray_col - 1:
                     final_touch_rows_for_obj.add(r)
        
        # Store info for drawing
        coords_to_draw.extend(target_coords_for_obj)
        
        # Store coords for erasing if shifted
        if object_shifted:
            coords_to_erase.extend(obj_coords)

        # Store info if object touches boundary in final state (for red row calculation)
        if final_touch_rows_for_obj:
             boundary_touchers_info.append({
                 'id': idx, 
                 'final_touch_rows': final_touch_rows_for_obj,
                 # 'shifted' status not strictly needed for Hypothesis 12 rule
             })

    # --- Step 6: Apply modifications (object movement) ---
    # Erase original positions first for shifted objects
    for r, c in coords_to_erase:
        if 0 <= r < rows and 0 <= c < cols: # Boundary check
            output_arr[r, c] = MAGENTA

    # Draw objects in new positions (handles shifted and unshifted)
    for r, c_new in coords_to_draw:
         if 0 <= r < rows and 0 <= c_new < cols: # Boundary check
            output_arr[r, c_new] = WHITE

    # --- Step 7: Determine R_red (rows to paint red) using Hypothesis 12 ---
    R_red = set()
    for info in boundary_touchers_info:
        touch_rows = info['final_touch_rows']
        # 7bi: Find contiguous vertical segments
        segments = get_contiguous_segments(touch_rows)
        
        # 7bii: Apply filtering rule based on segment length
        for segment in segments:
            seg_len = len(segment)
            if seg_len >= 3:
                min_r_seg, max_r_seg = min(segment), max(segment)
                # Add all rows except the min and max of the segment
                R_red.update({r for r in segment if r != min_r_seg and r != max_r_seg})

    # --- Step 8: Paint red regions ---
    if w_red > 0 and R_red:
        red_start_col = gray_col + 1
        # Calculate end column, ensuring it doesn't exceed grid bounds
        red_end_col = min(cols, red_start_col + w_red) 
        
        for r in R_red:
             # Ensure row is valid and there are columns to paint
             if 0 <= r < rows and red_start_col < red_end_col: 
                 output_arr[r, red_start_col:red_end_col] = RED

    # --- Step 9: Return final grid ---
    return output_arr.tolist()
```