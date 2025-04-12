```python
import numpy as np
from collections import deque

"""
Transforms the input grid based on the following rules:
1. Identify a vertical gray line (color 5). This acts as a barrier.
2. Find all distinct contiguous white objects (color 0) located entirely to the 
   left of the gray line.
3. For each white object:
   a. Determine its rightmost column index ('max_c').
   b. Calculate the horizontal shift distance required to move the object rightwards 
      so that its rightmost edge ends up in the column immediately to the left 
      of the gray line ('gray_col' - 1). The shift distance is ('gray_col' - 1) - 'max_c'.
   c. If the shift distance is greater than 0:
      i.  Identify the rows where the object's original rightmost pixels were located. 
          These rows will potentially receive red pixels later.
      ii. In the output grid, change the original pixels of the object to magenta (6).
      iii.In the output grid, draw the object's pixels in their new shifted positions 
          using white (0).
      iv. Determine a width 'W_red'. This is calculated based on the *input* grid: 
          count the number of contiguous columns, starting immediately to the right 
          of the gray line, that consist *entirely* of magenta (6) pixels. 
          Cap this count at a maximum of 4. So, W_red = min(4, count).
      v.  For each row identified in step (i), paint a horizontal segment of red (2) 
          pixels in the output grid. This segment starts at the column immediately 
          to the right of the gray line ('gray_col' + 1) and extends for 'W_red' columns.
4. Pixels not involved in the shifting (the gray line itself, pixels to its right 
   not overwritten by red, background magenta pixels, and white objects that did 
   not need to shift) remain unchanged from the input grid unless overwritten by 
   the shifted white objects during step (iii).
"""

# Color constants
WHITE = 0
RED = 2
GRAY = 5
MAGENTA = 6

def find_objects(grid: np.ndarray, color: int, max_col: int) -> list[list[tuple[int, int]]]:
    """
    Finds connected objects of a specific color strictly to the left of max_col.
    Uses Breadth-First Search (BFS). Returns a list of objects, where each
    object is a list of its (row, col) coordinates.
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
                is_valid_object = True # Assume valid until proven otherwise

                current_obj_visited_in_bfs = set([(r,c)]) # Track visited within this BFS

                while q:
                    row, col = q.popleft()

                    # Check if any part of the object reaches or exceeds max_col
                    if col >= max_col:
                        is_valid_object = False
                        # Continue BFS to mark all connected pixels as visited,
                        # but flag this object as invalid.

                    obj_coords.append((row, col))

                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        neighbor = (nr, nc)
                        
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and \
                           not visited[nr, nc] and \
                           neighbor not in current_obj_visited_in_bfs:
                            
                            # Mark visited globally and for this BFS traversal
                            visited[nr, nc] = True
                            current_obj_visited_in_bfs.add(neighbor)
                            q.append(neighbor)
                
                # Only add objects that are entirely contained left of max_col
                if is_valid_object and obj_coords:
                    objects.append(obj_coords)
                # If !is_valid_object, obj_coords are discarded, but pixels remain 'visited'.

    return objects


def get_object_properties(obj_coords: list[tuple[int, int]]) -> tuple[int, set[int]]:
    """
    Calculates the rightmost column and the set of rows touching that column for an object.
    """
    if not obj_coords:
        return -1, set()

    max_c = -1
    # Find the maximum column index for this object
    for _, c in obj_coords:
        if c > max_c:
            max_c = c

    # Find all rows that have a pixel at this maximum column index
    touching_rows = set()
    for r, c in obj_coords:
        if c == max_c:
            touching_rows.add(r)

    return max_c, touching_rows

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the object shifting and red region painting transformation.
    """
    input_arr = np.array(input_grid, dtype=int)
    # Initialize output as a copy of the input
    output_arr = np.copy(input_arr)
    rows, cols = input_arr.shape

    # --- Step 1: Find the gray line column ---
    gray_col = -1
    for c in range(cols):
        # Assuming the gray line is solid and unique
        if np.all(input_arr[:, c] == GRAY):
            gray_col = c
            break
            
    # If no solid gray line, try finding the first column with *any* gray pixel
    # This is a fallback, might need adjustment if gray appears elsewhere.
    if gray_col == -1:
         for c in range(cols):
             if GRAY in input_arr[:, c]:
                 # Basic check if it's a line-like feature
                 if np.sum(input_arr[:, c] == GRAY) > rows // 2: 
                     gray_col = c
                     break

    # If still no gray line found, return input as we can't proceed
    if gray_col == -1:
        # print("Warning: Gray line column not found. Returning input.")
        return input_grid 

    # --- Step 2: Find white objects strictly left of the gray line ---
    # Pass gray_col as the exclusive upper bound for columns to search/consider
    white_objects = find_objects(input_arr, WHITE, max_col=gray_col)

    # --- Step 3: Determine the width for the red regions ---
    # This is based on contiguous magenta columns in the input grid
    contiguous_magenta_cols = 0
    if gray_col + 1 < cols: # Check if there are columns to the right
        for c_check in range(gray_col + 1, cols):
            # Check if all pixels in this column are magenta
            if np.all(input_arr[:, c_check] == MAGENTA):
                contiguous_magenta_cols += 1
            else:
                break # Stop counting at the first column that's not fully magenta
    # The width is capped at 4, based on observed examples
    w_red = min(4, contiguous_magenta_cols)

    # --- Step 4: Process each white object ---
    rows_to_paint_red = set() # Collect all rows that need red painting
    objects_to_modify = [] # Store info needed for modification steps

    for obj_coords in white_objects:
        if not obj_coords: continue # Skip if an empty object was somehow found

        # Get properties of the object
        max_c, touching_rows = get_object_properties(obj_coords)
        
        # Calculate required shift distance
        shift = (gray_col - 1) - max_c

        # Store information if the object needs to be shifted
        if shift > 0:
            objects_to_modify.append({
                'coords': obj_coords,
                'shift': shift,
                'touching_rows': touching_rows
            })

    # --- Perform modifications in stages to avoid conflicts ---

    # Stage A: Erase original positions of shifted objects
    for obj_data in objects_to_modify:
        for r, c in obj_data['coords']:
            # Check bounds just in case, though coords should be valid
            if 0 <= r < rows and 0 <= c < cols:
                output_arr[r, c] = MAGENTA # Overwrite original with magenta

    # Stage B: Draw shifted objects in new positions
    for obj_data in objects_to_modify:
        shift = obj_data['shift']
        for r, c in obj_data['coords']:
            new_c = c + shift
            # Check bounds for the new position and ensure it's left of gray line
            if 0 <= r < rows and 0 <= new_c < gray_col:
                output_arr[r, new_c] = WHITE # Draw shifted object part

        # Collect the rows that need red painting for this object
        rows_to_paint_red.update(obj_data['touching_rows'])

    # Stage C: Paint red regions if applicable
    if w_red > 0 and rows_to_paint_red:
        red_start_col = gray_col + 1
        # Calculate end column, ensuring it doesn't exceed grid bounds
        red_end_col = min(cols, red_start_col + w_red) 

        for r in rows_to_paint_red:
             # Ensure row is valid and there are columns to paint
             if 0 <= r < rows and red_start_col < red_end_col:
                 output_arr[r, red_start_col:red_end_col] = RED

    # Convert the final NumPy array back to a list of lists
    return output_arr.tolist()
```