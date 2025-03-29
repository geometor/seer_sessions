
Previous Code:
```python
import numpy as np

"""
Relocates gray (5) objects into the gap defined by static red (2) structures.

The transformation follows these steps:

1.  **Identify Structures**: Locate all red (2) pixels and all gray (5) pixels in the input grid. Red pixels remain fixed.
2.  **Find the Gap**: Analyze the arrangement of red pixels to find the empty space (gap) separating them.
    *   Determine the bounding box of all red pixels.
    *   Check for a contiguous block of empty rows strictly *inside* the vertical span of the red bounding box. If found, this is a horizontal gap (Vertical Separation). Record the gap's top (`gap_min_r`) and bottom (`gap_max_r`) rows.
    *   If no horizontal gap, check for a contiguous block of empty columns strictly *inside* the horizontal span of the red bounding box. If found, this is a vertical gap (Horizontal Separation). Record the gap's leftmost (`gap_min_c`) and rightmost (`gap_max_c`) columns.
3.  **Identify Gray Objects**: Find all distinct connected groups (objects) of gray pixels from the *original* input grid using 8-way connectivity (including diagonals).
4.  **Initialize Output**: Create an output grid containing only the static red pixels, with all other cells set to white (0).
5.  **Relocate Gray Objects**: Move each identified gray object into the determined gap based on the separation type:
    *   **If Vertical Separation (Horizontal Gap):**
        *   For each gray object, determine if its original position was above or below the gap.
        *   If above (`obj_max_r < gap_min_r`), calculate the downward vertical shift (`delta_r`) needed to place the object's bottom edge at row `gap_min_r - 1`.
        *   If below (`obj_min_r > gap_max_r`), calculate the upward vertical shift (`delta_r`) needed to place the object's top edge at row `gap_max_r + 1`.
        *   Apply the shift: For each pixel `(r, c)` in the object, paint the pixel at `(r + delta_r, c)` gray (5) in the output grid. Maintain the object's shape and horizontal position.
    *   **If Horizontal Separation (Vertical Gap):**
        *   For each gray object, determine if its original position was to the left or right of the gap.
        *   If left (`obj_max_c < gap_min_c`), calculate the rightward horizontal shift (`delta_c`) needed to place the object's right edge at column `gap_min_c - 1`.
        *   If right (`obj_min_c > gap_max_c`), calculate the leftward horizontal shift (`delta_c`) needed to place the object's left edge at column `gap_max_c + 1`.
        *   Apply the shift: For each pixel `(r, c)` in the object, paint the pixel at `(r, c + delta_c)` gray (5) in the output grid. Maintain the object's shape and vertical position.
6.  **Return Result**: The output grid containing the static red pixels and the relocated gray objects.
"""

def find_objects(grid, color):
    """
    Finds all connected objects of a specific color in the grid.
    Connectivity includes diagonals (8 neighbors).

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list[set[tuple[int, int]]]: A list where each element is a set
                                      of (row, col) coordinates for one object.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    for r in range(height):
        for c in range(width):
            # If this pixel is the right color and hasn't been visited yet
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = set()
                q = [(r, c)]  # Queue for BFS
                visited[r, c] = True
                while q:
                    row, col = q.pop(0)
                    obj_coords.add((row, col))
                    # Check 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            # Check bounds and if neighbor is the right color and unvisited
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def transform(input_grid_list):
    """
    Relocates gray objects into the gap defined by static red structures.

    Args:
        input_grid_list (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed grid as a list of lists.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    height, width = input_grid.shape

    # --- 1. Identify Structures ---
    red_coords = np.argwhere(input_grid == 2)
    # We need gray objects later, using the original grid

    # --- Initialize Output Grid (Keep red, clear everything else) ---
    output_grid = np.zeros_like(input_grid, dtype=int) # Initialize with white (0)
    if red_coords.size > 0:
        for r, c in red_coords:
            output_grid[r, c] = 2 # Keep red pixels

    # --- 3. Identify Gray Objects ---
    gray_objects = find_objects(input_grid, 5)

    # Handle edge case: no gray objects to move
    if not gray_objects:
        return output_grid.tolist()

    # Handle edge case: no red pixels to define a gap
    if red_coords.size == 0:
        # No gap defined, unclear what to do. Return grid with only red (which is none).
        # Or maybe return the original gray positions? Based on examples, seems red is always present.
        # Let's return the grid with only red (i.e., empty if no red).
         return output_grid.tolist() # Or maybe input_grid.tolist()? Let's stick to the initialized grid.

    # --- 2. Find the Gap ---
    min_r, min_c = red_coords.min(axis=0)
    max_r, max_c = red_coords.max(axis=0)

    separation_axis = None
    gap_min_r, gap_max_r = -1, -1
    gap_min_c, gap_max_c = -1, -1

    # Check for horizontal gap (Vertical Separation)
    h_gap_rows = [r for r in range(min_r + 1, max_r) if not np.any(input_grid[r, min_c:max_c+1] == 2)]
    if h_gap_rows:
        # Find the first contiguous block of gap rows
        start_r = h_gap_rows[0]
        end_r = start_r
        for i in range(1, len(h_gap_rows)):
            if h_gap_rows[i] == end_r + 1:
                end_r = h_gap_rows[i]
            else:
                 break # Stop if the gap rows are not contiguous
        # Check if the gap found is truly internal (not touching the bbox edges implicitly)
        # This is implicitly handled by range(min_r + 1, max_r)
        if end_r >= start_r: # Ensure at least one gap row found
             separation_axis = 'vertical'
             gap_min_r = start_r
             gap_max_r = end_r

    # Check for vertical gap (Horizontal Separation) only if no horizontal gap was found
    if separation_axis is None:
        v_gap_cols = [c for c in range(min_c + 1, max_c) if not np.any(input_grid[min_r:max_r+1, c] == 2)]
        if v_gap_cols:
            # Find the first contiguous block of gap columns
            start_c = v_gap_cols[0]
            end_c = start_c
            for i in range(1, len(v_gap_cols)):
                 if v_gap_cols[i] == end_c + 1:
                     end_c = v_gap_cols[i]
                 else:
                     break # Stop if the gap columns are not contiguous
            # Check if the gap found is truly internal
            if end_c >= start_c: # Ensure at least one gap column found
                 separation_axis = 'horizontal'
                 gap_min_c = start_c
                 gap_max_c = end_c

    # If no gap is found, return the grid with only red pixels
    if separation_axis is None:
        return output_grid.tolist()

    # --- 5. Relocate Gray Objects ---
    for obj_coords in gray_objects:
        if not obj_coords: continue # Skip empty objects if any

        obj_rows = [r for r, c in obj_coords]
        obj_cols = [c for r, c in obj_coords]
        obj_min_r, obj_max_r = min(obj_rows), max(obj_rows)
        obj_min_c, obj_max_c = min(obj_cols), max(obj_cols)

        delta_r = 0
        delta_c = 0

        if separation_axis == 'vertical':
            # Determine if object is above or below the gap and calculate vertical shift
            if obj_max_r < gap_min_r: # Object is above gap
                # Target bottom row of object is gap_min_r - 1
                delta_r = (gap_min_r - 1) - obj_max_r
            elif obj_min_r > gap_max_r: # Object is below gap
                # Target top row of object is gap_max_r + 1
                delta_r = (gap_max_r + 1) - obj_min_r
            else: # Object overlaps gap - behavior undefined? Assume skip or error. Let's skip.
                continue

        elif separation_axis == 'horizontal':
            # Determine if object is left or right of the gap and calculate horizontal shift
            if obj_max_c < gap_min_c: # Object is left of gap
                # Target right col of object is gap_min_c - 1
                delta_c = (gap_min_c - 1) - obj_max_c
            elif obj_min_c > gap_max_c: # Object is right of gap
                # Target left col of object is gap_max_c + 1
                delta_c = (gap_max_c + 1) - obj_min_c
            else: # Object overlaps gap - behavior undefined? Assume skip or error. Let's skip.
                continue

        # Apply the shift to each pixel of the object and paint it on the output grid
        for r, c in obj_coords:
            new_r, new_c = r + delta_r, c + delta_c
            # Check bounds before writing to output grid
            if 0 <= new_r < height and 0 <= new_c < width:
                output_grid[new_r, new_c] = 5
            # else: Pixel moves out of bounds - ignore it? This shouldn't happen if logic is correct for internal gaps.

    # --- 6. Return Result ---
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 2 2 0 0 0
0 0 0 2 0 0 0 0 0 0 0 2 0 5 0
5 5 0 2 0 0 0 0 0 0 0 2 0 5 5
5 5 0 2 0 0 0 0 0 0 0 2 0 5 5
0 0 0 2 0 0 0 0 0 0 0 2 0 5 0
0 0 0 2 2 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 2 2 0 0 0
0 0 0 2 0 0 0 0 0 5 0 2 0 0 0
0 0 0 2 0 5 5 0 5 5 0 2 0 0 0
0 0 0 2 0 5 5 0 5 5 0 2 0 0 0
0 0 0 2 0 0 0 0 0 5 0 2 0 0 0
0 0 0 2 2 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 2 2 0 0 0
0 0 0 2 0 0 0 0 0 0 5 2 0 0 0
0 0 0 5 5 0 0 0 0 0 5 5 0 0 0
0 0 0 5 5 0 0 0 0 0 5 5 0 0 0
0 0 0 2 0 0 0 0 0 0 5 2 0 0 0
0 0 0 2 2 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 20
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 17.77777777777777

## Example 2:
Input:
```
0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 5 2 2 0 0 0 0 0 0 0 0
0 0 2 0 5 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 5 5 5 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 10
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 8.888888888888886

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 2 2 0 0 0 0
0 5 0 2 0 0 0 0 0 0 2 0 5 0 0
5 5 0 2 0 0 0 0 0 0 2 0 5 5 0
0 5 0 2 0 0 0 0 0 0 2 0 0 5 0
0 0 0 2 2 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 2 2 0 0 0 0
0 0 0 2 0 5 0 0 5 0 2 0 0 0 0
0 0 0 2 0 5 5 5 5 0 2 0 0 0 0
0 0 0 2 0 5 0 5 0 0 2 0 0 0 0
0 0 0 2 2 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 2 2 0 0 0 0
0 0 0 2 5 0 0 0 0 5 2 0 0 0 0
0 0 0 5 5 0 0 0 0 5 5 0 0 0 0
0 0 0 2 5 0 0 0 0 0 5 0 0 0 0
0 0 0 2 2 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 16
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 14.222222222222229
**General Assessment**

The provided code attempts to relocate gray objects into a gap defined by static red structures. The results indicate that while the code correctly identifies the red structures, the gray objects, and the general orientation of the gap (horizontal or vertical), it fails to place the gray objects in their correct final positions in all three training examples.

The core issue appears to be the calculation of the target position for the gray objects relative to the identified gap boundaries. The current logic places the objects adjacent to the gap but *outside* of it (e.g., at `gap_min_r - 1` or `gap_max_c + 1`). Examination of the expected outputs suggests the objects should be moved so their nearest edge aligns *with* the first row/column of the gap itself (e.g., at `gap_min_r` or `gap_max_c`).

The strategy will be to:
1.  Re-analyze the input/output pairs, focusing on the precise relationship between the gray objects and the gap boundaries in the expected output.
2.  Gather detailed metrics on object positions and gap boundaries.
3.  Update the YAML facts and natural language program to reflect the corrected placement logic.

**Gather Metrics**


*code_execution:*
```python
import numpy as np

# --- Data from the failed run ---

# Example 1
input_1 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,2,2,0,0,0,0,0,2,2,0,0,0],
    [0,0,0,2,0,0,0,0,0,0,0,2,0,5,0],
    [5,5,0,2,0,0,0,0,0,0,0,2,0,5,5],
    [5,5,0,2,0,0,0,0,0,0,0,2,0,5,5],
    [0,0,0,2,0,0,0,0,0,0,0,2,0,5,0],
    [0,0,0,2,2,0,0,0,0,0,2,2,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
], dtype=int)

expected_output_1 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,2,2,0,0,0,0,0,2,2,0,0,0],
    [0,0,0,2,0,0,0,0,0,5,0,2,0,0,0],
    [0,0,0,2,0,5,5,0,5,5,0,2,0,0,0],
    [0,0,0,2,0,5,5,0,5,5,0,2,0,0,0],
    [0,0,0,2,0,0,0,0,0,5,0,2,0,0,0],
    [0,0,0,2,2,0,0,0,0,0,2,2,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
], dtype=int)

transformed_output_1 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,2,2,0,0,0,0,0,2,2,0,0,0],
    [0,0,0,2,0,0,0,0,0,0,5,2,0,0,0], # transformed has 5@ (6,10) vs expected (6,9)
    [0,0,0,5,5,0,0,0,0,0,5,5,0,0,0], # transformed has 5s @ (7,3),(7,4) vs expected (7,5),(7,6) and 5s @ (7,10),(7,11) vs expected (7,8),(7,9)
    [0,0,0,5,5,0,0,0,0,0,5,5,0,0,0], # transformed has 5s @ (8,3),(8,4) vs expected (8,5),(8,6) and 5s @ (8,10),(8,11) vs expected (8,8),(8,9)
    [0,0,0,2,0,0,0,0,0,0,5,2,0,0,0], # transformed has 5@ (9,10) vs expected (9,9)
    [0,0,0,2,2,0,0,0,0,0,2,2,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
], dtype=int)

# Example 2
input_2 = np.array([
    [0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,2,2,2,2,2,0,0,0,0,0,0,0,0],
    [0,0,2,0,0,0,2,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,2,0,0,0,2,0,0,0,0,0,0,0,0],
    [0,0,2,2,2,2,2,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,5,5,5,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
], dtype=int)

expected_output_2 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,2,2,2,2,2,0,0,0,0,0,0,0,0],
    [0,0,2,0,0,0,2,0,0,0,0,0,0,0,0],
    [0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,5,5,5,0,0,0,0,0,0,0,0,0],
    [0,0,2,0,0,0,2,0,0,0,0,0,0,0,0],
    [0,0,2,2,2,2,2,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
], dtype=int)

transformed_output_2 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,2,2,5,2,2,0,0,0,0,0,0,0,0], # transformed has 5 @ (3,4) vs expected (5,4)
    [0,0,2,0,5,0,2,0,0,0,0,0,0,0,0], # transformed has 5 @ (4,4) vs expected (6,4)
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,2,5,5,5,2,0,0,0,0,0,0,0,0], # transformed has 5s @ (10,3),(10,4),(10,5) vs expected (9,3),(9,4),(9,5)
    [0,0,2,2,2,2,2,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
], dtype=int)

# Example 3
input_3 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,2,2,0,0,0,0,2,2,0,0,0,0],
    [0,5,0,2,0,0,0,0,0,0,2,0,5,0,0],
    [5,5,0,2,0,0,0,0,0,0,2,0,5,5,0],
    [0,5,0,2,0,0,0,0,0,0,2,0,0,5,0],
    [0,0,0,2,2,0,0,0,0,2,2,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
], dtype=int)

expected_output_3 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,2,2,0,0,0,0,2,2,0,0,0,0],
    [0,0,0,2,0,5,0,0,5,0,2,0,0,0,0],
    [0,0,0,2,0,5,5,5,5,0,2,0,0,0,0],
    [0,0,0,2,0,5,0,5,0,0,2,0,0,0,0],
    [0,0,0,2,2,0,0,0,0,2,2,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
], dtype=int)

transformed_output_3 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,2,2,0,0,0,0,2,2,0,0,0,0],
    [0,0,0,2,5,0,0,0,0,5,2,0,0,0,0], # transformed 5s @ (5,4), (5,9) vs expected (5,5), (5,8)
    [0,0,0,5,5,0,0,0,0,5,5,0,0,0,0], # transformed 5s @ (6,3),(6,4) vs expected (6,5),(6,6),(6,7),(6,8) and 5s @ (6,9),(6,10)
    [0,0,0,2,5,0,0,0,0,0,5,0,0,0,0], # transformed 5s @ (7,4), (7,10) vs expected (7,5), (7,7)
    [0,0,0,2,2,0,0,0,0,2,2,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
], dtype=int)

# --- Helper Function ---
def analyze_example(input_grid, expected_grid, transformed_grid):
    report = {}
    report['shape_input'] = input_grid.shape
    report['shape_expected'] = expected_grid.shape
    report['shape_transformed'] = transformed_grid.shape
    report['shape_match'] = expected_grid.shape == transformed_grid.shape

    input_colors, input_counts = np.unique(input_grid, return_counts=True)
    expected_colors, expected_counts = np.unique(expected_grid, return_counts=True)
    transformed_colors, transformed_counts = np.unique(transformed_grid, return_counts=True)

    report['palette_match'] = set(expected_colors) == set(transformed_colors)
    report['colors_input'] = dict(zip(input_colors, input_counts))
    report['colors_expected'] = dict(zip(expected_colors, expected_counts))
    report['colors_transformed'] = dict(zip(transformed_colors, transformed_counts))

    # Count specific colors (0=white, 2=red, 5=gray)
    count_colors = [0, 2, 5]
    for color in count_colors:
        report[f'count_input_{color}'] = report['colors_input'].get(color, 0)
        report[f'count_expected_{color}'] = report['colors_expected'].get(color, 0)
        report[f'count_transformed_{color}'] = report['colors_transformed'].get(color, 0)

    # Gap analysis (simplified based on visual inspection and previous code logic)
    red_coords = np.argwhere(input_grid == 2)
    gap_info = {'type': 'None', 'min': -1, 'max': -1}
    if red_coords.size > 0:
        min_r, min_c = red_coords.min(axis=0)
        max_r, max_c = red_coords.max(axis=0)
        # Check horizontal gap
        h_gap_rows = [r for r in range(min_r + 1, max_r) if not np.any(input_grid[r, min_c:max_c+1] == 2)]
        if h_gap_rows:
             start_r = h_gap_rows[0]
             end_r = start_r
             for i in range(1, len(h_gap_rows)):
                if h_gap_rows[i] == end_r + 1: end_r = h_gap_rows[i]
                else: break
             if end_r >= start_r:
                 gap_info = {'type': 'Horizontal Gap (Vertical Separation)', 'min_row': start_r, 'max_row': end_r, 'col_range':(min_c, max_c)}

        # Check vertical gap if no horizontal found
        elif gap_info['type'] == 'None':
            v_gap_cols = [c for c in range(min_c + 1, max_c) if not np.any(input_grid[min_r:max_r+1, c] == 2)]
            if v_gap_cols:
                start_c = v_gap_cols[0]
                end_c = start_c
                for i in range(1, len(v_gap_cols)):
                    if v_gap_cols[i] == end_c + 1: end_c = v_gap_cols[i]
                    else: break
                if end_c >= start_c:
                     gap_info = {'type': 'Vertical Gap (Horizontal Separation)', 'min_col': start_c, 'max_col': end_c, 'row_range':(min_r, max_r)}
    report['gap'] = gap_info

    # Gray object info (original position)
    gray_coords = np.argwhere(input_grid == 5)
    gray_objects = []
    if gray_coords.size > 0:
         # This is simplified - assumes objects don't merge, just gets bounding boxes
         visited = set()
         for r_init, c_init in gray_coords:
             if (r_init, c_init) in visited: continue
             q = [(r_init, c_init)]
             visited.add((r_init, c_init))
             current_obj_coords = [(r_init, c_init)]
             while q:
                 r, c = q.pop(0)
                 for dr in [-1, 0, 1]:
                     for dc in [-1, 0, 1]:
                         if dr == 0 and dc == 0: continue
                         nr, nc = r + dr, c + dc
                         if 0 <= nr < input_grid.shape[0] and 0 <= nc < input_grid.shape[1] and \
                            input_grid[nr, nc] == 5 and (nr, nc) not in visited:
                             visited.add((nr, nc))
                             q.append((nr, nc))
                             current_obj_coords.append((nr, nc))
             if current_obj_coords:
                 rows = [r for r,c in current_obj_coords]
                 cols = [c for r,c in current_obj_coords]
                 gray_objects.append({'min_r': min(rows), 'max_r': max(rows), 'min_c': min(cols), 'max_c': max(cols)})

    report['gray_objects_input_bbox'] = gray_objects

    # Placement comparison (qualitative based on visual inspection)
    report['placement_error'] = "Object placed adjacent *outside* gap instead of adjacent *inside* gap." if not np.array_equal(expected_grid, transformed_grid) else "None"

    return report

# --- Analyze Examples ---
report_1 = analyze_example(input_1, expected_output_1, transformed_output_1)
report_2 = analyze_example(input_2, expected_output_2, transformed_output_2)
report_3 = analyze_example(input_3, expected_output_3, transformed_output_3)

print("--- Example 1 Analysis ---")
print(report_1)
print("\n--- Example 2 Analysis ---")
print(report_2)
print("\n--- Example 3 Analysis ---")
print(report_3)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Example 1 Analysis ---
{'shape_input': (15, 15), 'shape_expected': (15, 15), 'shape_transformed': (15, 15), 'shape_match': True, 'palette_match': True, 'colors_input': {np.int64(0): np.int64(199), np.int64(2): np.int64(16), np.int64(5): np.int64(10)}, 'colors_expected': {np.int64(0): np.int64(199), np.int64(2): np.int64(16), np.int64(5): np.int64(10)}, 'colors_transformed': {np.int64(0): np.int64(203), np.int64(2): np.int64(12), np.int64(5): np.int64(10)}, 'count_input_0': np.int64(199), 'count_expected_0': np.int64(199), 'count_transformed_0': np.int64(203), 'count_input_2': np.int64(16), 'count_expected_2': np.int64(16), 'count_transformed_2': np.int64(12), 'count_input_5': np.int64(10), 'count_expected_5': np.int64(10), 'count_transformed_5': np.int64(10), 'gap': {'type': 'Vertical Gap (Horizontal Separation)', 'min_col': 5, 'max_col': 9, 'row_range': (np.int64(5), np.int64(10))}, 'gray_objects_input_bbox': [{'min_r': np.int64(6), 'max_r': np.int64(9), 'min_c': np.int64(13), 'max_c': np.int64(14)}, {'min_r': np.int64(7), 'max_r': np.int64(8), 'min_c': np.int64(0), 'max_c': np.int64(1)}], 'placement_error': 'Object placed adjacent *outside* gap instead of adjacent *inside* gap.'}

--- Example 2 Analysis ---
{'shape_input': (15, 15), 'shape_expected': (15, 15), 'shape_transformed': (15, 15), 'shape_match': True, 'palette_match': True, 'colors_input': {np.int64(0): np.int64(206), np.int64(2): np.int64(14), np.int64(5): np.int64(5)}, 'colors_expected': {np.int64(0): np.int64(206), np.int64(2): np.int64(14), np.int64(5): np.int64(5)}, 'colors_transformed': {np.int64(0): np.int64(207), np.int64(2): np.int64(13), np.int64(5): np.int64(5)}, 'count_input_0': np.int64(206), 'count_expected_0': np.int64(206), 'count_transformed_0': np.int64(207), 'count_input_2': np.int64(14), 'count_expected_2': np.int64(14), 'count_transformed_2': np.int64(13), 'count_input_5': np.int64(5), 'count_expected_5': np.int64(5), 'count_transformed_5': np.int64(5), 'gap': {'type': 'Horizontal Gap (Vertical Separation)', 'min_row': 5, 'max_row': 9, 'col_range': (np.int64(2), np.int64(6))}, 'gray_objects_input_bbox': [{'min_r': np.int64(0), 'max_r': np.int64(1), 'min_c': np.int64(4), 'max_c': np.int64(4)}, {'min_r': np.int64(13), 'max_r': np.int64(13), 'min_c': np.int64(3), 'max_c': np.int64(5)}], 'placement_error': 'Object placed adjacent *outside* gap instead of adjacent *inside* gap.'}

--- Example 3 Analysis ---
{'shape_input': (15, 15), 'shape_expected': (15, 15), 'shape_transformed': (15, 15), 'shape_match': True, 'palette_match': True, 'colors_input': {np.int64(0): np.int64(203), np.int64(2): np.int64(14), np.int64(5): np.int64(8)}, 'colors_expected': {np.int64(0): np.int64(203), np.int64(2): np.int64(14), np.int64(5): np.int64(8)}, 'colors_transformed': {np.int64(0): np.int64(206), np.int64(2): np.int64(11), np.int64(5): np.int64(8)}, 'count_input_0': np.int64(203), 'count_expected_0': np.int64(203), 'count_transformed_0': np.int64(206), 'count_input_2': np.int64(14), 'count_expected_2': np.int64(14), 'count_transformed_2': np.int64(11), 'count_input_5': np.int64(8), 'count_expected_5': np.int64(8), 'count_transformed_5': np.int64(8), 'gap': {'type': 'Vertical Gap (Horizontal Separation)', 'min_col': 5, 'max_col': 8, 'row_range': (np.int64(4), np.int64(8))}, 'gray_objects_input_bbox': [{'min_r': np.int64(5), 'max_r': np.int64(7), 'min_c': np.int64(0), 'max_c': np.int64(1)}, {'min_r': np.int64(5), 'max_r': np.int64(7), 'min_c': np.int64(12), 'max_c': np.int64(13)}], 'placement_error': 'Object placed adjacent *outside* gap instead of adjacent *inside* gap.'}

```
**YAML Facts**


```yaml
task_context:
  description: Relocate gray objects into a central gap defined by static red structures.
  colors:
    - red: 2 (static structure)
    - gray: 5 (mobile objects)
    - white: 0 (background, gap space)
  connectivity: 8-way (for finding gray objects)

input_features:
  - red_pixels: Form one or more static structures.
  - gray_pixels: Form one or more distinct objects.
  - gap: An empty rectangular area (containing only white pixels) separating parts of the red structure(s). The gap can be oriented horizontally (vertical separation) or vertically (horizontal separation).
    - identification: Find the bounding box of all red pixels. A horizontal gap is a contiguous block of all-white rows strictly *within* the red bounding box's vertical span. A vertical gap is a contiguous block of all-white columns strictly *within* the red bounding box's horizontal span.
    - properties:
        - horizontal_gap: defined by `gap_min_r`, `gap_max_r` (first and last rows of the gap).
        - vertical_gap: defined by `gap_min_c`, `gap_max_c` (first and last columns of the gap).
  - gray_objects: Identified as connected components of gray pixels.
    - properties:
        - location: Bounding box (`obj_min_r`, `obj_max_r`, `obj_min_c`, `obj_max_c`).
        - position_relative_to_gap: Each gray object is located either entirely above/below a horizontal gap, or entirely left/right of a vertical gap.

transformation:
  - goal: Move each gray object into the gap, placing it adjacent to the inner boundary of the red structure that defines the gap, while preserving the object's shape and relative position if multiple objects are on the same side.
  - steps:
      1. Identify red pixels and find the gap (determine type, min/max rows or columns).
      2. Identify all distinct gray objects from the original input.
      3. Initialize the output grid with only the static red pixels.
      4. For each gray object:
         a. Determine its original position relative to the gap.
         b. Calculate the necessary shift (delta_r or delta_c) to move it into the gap.
            - **Vertical Gap (Horizontal Separation):**
                - Object left of gap (`obj_max_c < gap_min_c`): Target the object's rightmost pixel column to be `gap_min_c`. Calculate `delta_c = gap_min_c - obj_max_c`.
                - Object right of gap (`obj_min_c > gap_max_c`): Target the object's leftmost pixel column to be `gap_max_c`. Calculate `delta_c = gap_max_c - obj_min_c`.
            - **Horizontal Gap (Vertical Separation):**
                - Object above gap (`obj_max_r < gap_min_r`): Target the object's bottommost pixel row to be `gap_min_r`. Calculate `delta_r = gap_min_r - obj_max_r`.
                - Object below gap (`obj_min_r > gap_max_r`): Target the object's topmost pixel row to be `gap_max_r`. Calculate `delta_r = gap_max_r - obj_min_r`.
         c. Apply the calculated shift to all pixels of the gray object and place them onto the output grid.

output_features:
  - grid: Contains the original red static structures and the relocated gray objects within the gap area. The original positions of gray objects are now white.

edge_cases:
  - No red pixels: The gap cannot be defined. (Behavior: Output grid contains no pixels / is all white).
  - No gray pixels: No objects to move. (Behavior: Output grid contains only red pixels).
  - No gap found between red structures: No defined space to move objects into. (Behavior: Output grid contains only red pixels).
  - Gray objects overlapping gap in input: This scenario is not observed in examples; assume objects are always outside the gap initially.
```


**Natural Language Program**

1.  **Identify Static Structures and Gap:**
    *   Locate all red (2) pixels in the input grid. These remain unchanged in the output.
    *   Determine the bounding box of all red pixels (`min_r`, `max_r`, `min_c`, `max_c`).
    *   Search for a contiguous block of empty (white, 0) rows strictly between `min_r` and `max_r` (i.e., from `min_r + 1` to `max_r - 1`) that span at least from `min_c` to `max_c`. If found, this is a **horizontal gap**. Record its first (`gap_min_r`) and last (`gap_max_r`) rows.
    *   If no horizontal gap is found, search for a contiguous block of empty (white, 0) columns strictly between `min_c` and `max_c` (i.e., from `min_c + 1` to `max_c - 1`) that span at least from `min_r` to `max_r`. If found, this is a **vertical gap**. Record its first (`gap_min_c`) and last (`gap_max_c`) columns.
    *   If neither gap is found, proceed to step 6 with an output grid containing only red pixels.

2.  **Identify Mobile Objects:**
    *   Find all distinct connected groups (objects) of gray (5) pixels in the *original* input grid using 8-way connectivity. Record the coordinates of each pixel belonging to each object.

3.  **Initialize Output:**
    *   Create an output grid of the same dimensions as the input, initially filled with white (0).
    *   Copy all red (2) pixels from the input grid to their corresponding locations in the output grid.

4.  **Calculate Relocation Shift for Each Gray Object:**
    *   For each gray object identified in step 2:
        *   Determine its bounding box (`obj_min_r`, `obj_max_r`, `obj_min_c`, `obj_max_c`).
        *   Initialize shift amounts: `delta_r = 0`, `delta_c = 0`.
        *   **If a horizontal gap was found (Vertical Separation):**
            *   If the object is entirely above the gap (`obj_max_r < gap_min_r`): Calculate the downward shift required to align the object's bottom edge with the gap's top edge: `delta_r = gap_min_r - obj_max_r`.
            *   If the object is entirely below the gap (`obj_min_r > gap_max_r`): Calculate the upward shift required to align the object's top edge with the gap's bottom edge: `delta_r = gap_max_r - obj_min_r`.
        *   **Else if a vertical gap was found (Horizontal Separation):**
            *   If the object is entirely to the left of the gap (`obj_max_c < gap_min_c`): Calculate the rightward shift required to align the object's right edge with the gap's left edge: `delta_c = gap_min_c - obj_max_c`.
            *   If the object is entirely to the right of the gap (`obj_min_c > gap_max_c`): Calculate the leftward shift required to align the object's left edge with the gap's right edge: `delta_c = gap_max_c - obj_min_c`.

5.  **Apply Shift and Paint Objects:**
    *   For each gray object and its calculated (`delta_r`, `delta_c`):
        *   Iterate through each original pixel coordinate `(r, c)` of the object.
        *   Calculate the new coordinate: `new_r = r + delta_r`, `new_c = c + delta_c`.
        *   If the `new_r` and `new_c` are within the grid boundaries, set the pixel at `(new_r, new_c)` in the output grid to gray (5).

6.  **Return Result:**
    *   Return the completed output grid.
