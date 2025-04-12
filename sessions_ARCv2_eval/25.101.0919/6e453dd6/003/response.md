```python
import numpy as np
from collections import deque

"""
Transforms the input grid based on object movement and boundary interaction rules:
1.  Identify a vertical gray line (color 5) acting as a barrier.
2.  Calculate the width for potential red regions (`w_red`) based on the number 
    of contiguous all-magenta (color 6) columns immediately to the right of the 
    gray line in the input grid, capped at a maximum width of 4.
3.  Find all distinct contiguous white objects (color 0) located entirely to the 
    left of the gray line.
4.  For each white object:
    a.  Determine its rightmost column (`max_c`).
    b.  Calculate the necessary horizontal shift (`shift`) to move its rightmost 
        edge to the column immediately left of the gray line (`gray_col - 1`).
    c.  If the shift is greater than 0, mark the object's original pixels for 
        erasure (change to magenta).
    d.  Mark the object's pixels for drawing at their new, shifted positions.
    e.  Determine the rows where the object's pixels land in the column 
        `gray_col - 1` after shifting (or originally, if shift is 0).
5.  Apply the erasures and drawings to create an intermediate grid state.
6.  Determine the final set of rows (`R_red`) that should receive red pixels. 
    This step involves a filtering rule applied to the rows identified in step 4e, 
    specifically for objects that required a shift > 0. The exact filtering rule 
    is currently uncertain but is hypothesized to be based on the interaction 
    at the boundary. **(Current implementation uses a placeholder/incorrect rule: 
    includes all rows touched by *shifted* objects at the boundary).**
7.  If `w_red` is greater than 0, paint horizontal red segments (color 2) of 
    width `w_red` starting at column `gray_col + 1` for each row in the 
    final `R_red` set.
"""

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
    """Calculates the width of the red region based on contiguous magenta columns."""
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
    """Finds connected objects of a specific color strictly left of max_col."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        # Only search columns left of the barrier
        for c in range(max_col):
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                is_valid_object = True # Assume valid until proven otherwise
                current_obj_visited_in_bfs = set([(r,c)])

                while q:
                    row, col = q.popleft()

                    # Crucial Check: Ensure the *entire* object is left of max_col
                    if col >= max_col:
                        is_valid_object = False
                        # Continue BFS to mark all connected pixels, but invalidate object
                    
                    obj_coords.append((row, col))

                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        neighbor = (nr, nc)
                        
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and \
                           not visited[nr, nc] and \
                           neighbor not in current_obj_visited_in_bfs:
                            
                            visited[nr, nc] = True
                            current_obj_visited_in_bfs.add(neighbor)
                            q.append(neighbor)
                
                if is_valid_object and obj_coords:
                    objects.append(obj_coords)
                    
    return objects

def get_object_properties(obj_coords: list[tuple[int, int]]) -> tuple[int, set[int]]:
    """Calculates the rightmost column and the set of rows touching that column."""
    if not obj_coords:
        return -1, set()
    max_c = -1
    for _, c in obj_coords:
        max_c = max(max_c, c)
    touching_rows = {r for r, c in obj_coords if c == max_c}
    return max_c, touching_rows

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """Applies the object shifting and red region painting transformation."""
    input_arr = np.array(input_grid, dtype=int)
    output_arr = np.copy(input_arr)
    rows, cols = input_arr.shape

    # --- Step 1: Find the gray line column ---
    gray_col = find_gray_line_col(input_arr)
    if gray_col == -1:
        # Cannot proceed without the barrier
        return input_grid

    # --- Step 2: Calculate red width ---
    w_red = calculate_red_width(input_arr, gray_col)

    # --- Step 3: Find white objects ---
    # Search strictly left of the gray column
    white_objects = find_objects(input_arr, WHITE, max_col=gray_col)

    # --- Step 4 & 5: Prepare modification lists ---
    coords_to_erase = []
    coords_to_draw = []
    # Store info for determining red rows later: (object_index, final_touch_rows, was_shifted)
    boundary_touchers_info = [] 

    for idx, obj_coords in enumerate(white_objects):
        if not obj_coords: continue

        max_c, _ = get_object_properties(obj_coords) # Original touching rows not directly needed here
        
        # Calculate shift
        shift = 0
        if max_c != -1 : # Ensure object exists
             shift = max(0, (gray_col - 1) - max_c)

        final_touch_rows_for_obj = set()
        object_shifted = shift > 0

        # Collect coords for drawing and check final boundary touches
        for r, c in obj_coords:
            new_c = c + shift
            # Ensure drawing happens within bounds and left of gray line
            if 0 <= r < rows and 0 <= new_c < gray_col:
                 coords_to_draw.append((r, new_c))
                 if new_c == gray_col - 1:
                     final_touch_rows_for_obj.add(r)
        
        # Collect coords for erasing if shifted
        if object_shifted:
            coords_to_erase.extend(obj_coords)

        # Store info if object touches boundary in final state
        if final_touch_rows_for_obj:
             boundary_touchers_info.append({
                 'id': idx, 
                 'final_touch_rows': final_touch_rows_for_obj,
                 'shifted': object_shifted
                 })

    # --- Step 6: Apply modifications ---
    # Erase original positions first
    for r, c in coords_to_erase:
        if 0 <= r < rows and 0 <= c < cols: # Boundary check
            output_arr[r, c] = MAGENTA

    # Draw objects in new positions
    for r, c_new in coords_to_draw:
         if 0 <= r < rows and 0 <= c_new < cols: # Boundary check
            output_arr[r, c_new] = WHITE

    # --- Step 7: Determine R_red (rows to paint red) ---
    # !!! Placeholder Logic: Select rows touched by SHIFTED objects only !!!
    # This is known to be incorrect based on test results, but serves as a structure.
    # The correct logic needs to filter `final_touch_rows` based on the unknown rule.
    R_red = set()
    for info in boundary_touchers_info:
        if info['shifted']: # Apply the filter (currently just checks if shifted)
            R_red.update(info['final_touch_rows'])
            
    # --- Step 8: Paint red regions ---
    if w_red > 0 and R_red:
        red_start_col = gray_col + 1
        red_end_col = min(cols, red_start_col + w_red) # Ensure stay within bounds
        
        for r in R_red:
            if 0 <= r < rows and red_start_col < red_end_col: # Check row and col bounds
                 output_arr[r, red_start_col:red_end_col] = RED

    # Convert back to list of lists
    return output_arr.tolist()
```