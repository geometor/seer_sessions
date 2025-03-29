
Previous Code:
```python
import numpy as np

"""
This module transforms an input grid based on the spatial relationship between static red (2) pixels and mobile gray (5) pixels.

The transformation relocates the gray pixels based on how the red pixel structures are separated:

1.  **Identify Elements**: Locate all red and gray pixels.
2.  **Clear Original Gray**: Create an intermediate grid by setting original gray pixel locations to white (0).
3.  **Analyze Red Separation**: Determine if the red structures are primarily separated by empty vertical columns (horizontal separation) or empty horizontal rows (vertical separation).
    *   Find the bounding box of all red pixels.
    *   Check for rows within the bounding box (excluding top/bottom) that contain no red pixels. If found, assume vertical separation.
    *   Otherwise, check for columns within the bounding box (excluding left/right) that contain no red pixels. If found, assume horizontal separation.
4.  **Apply Transformation**:
    *   **Horizontal Separation**: Find the vertical gap columns between red structures. Find the inner vertical extent (rows) defined by the red pixels adjacent to this gap. Fill the rectangular area defined by the gap columns and the inner rows with gray (5).
    *   **Vertical Separation**: Find the horizontal gap rows between red structures. Identify individual connected gray objects from the input grid. Translate each gray object vertically to fill the gap. Objects above the gap move down to the top of the gap; objects below the gap move up to the bottom of the gap. Their horizontal position and shape are preserved.
5.  **Return Result**: The grid with relocated gray pixels.
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
    Relocates gray pixels based on the spatial arrangement of static red pixels.

    Args:
        input_grid_list (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed grid as a list of lists.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # --- 1. Identify Elements ---
    red_coords = np.argwhere(input_grid == 2)
    gray_coords = np.argwhere(input_grid == 5)

    # Handle edge case: no gray pixels to move
    if gray_coords.size == 0:
        return output_grid.tolist()

    # --- 2. Clear Original Gray ---
    for r, c in gray_coords:
        output_grid[r, c] = 0 # Set to white

    # Handle edge case: no red pixels to guide movement (shouldn't happen based on examples)
    if red_coords.size == 0:
        # Or maybe just return the grid with gray removed? Let's stick to removing gray.
        return output_grid.tolist()

    # --- 3. Analyze Red Separation ---
    min_r, min_c = red_coords.min(axis=0)
    max_r, max_c = red_coords.max(axis=0)

    separation_axis = None
    gap_min_r, gap_max_r = -1, -1
    gap_min_c, gap_max_c = -1, -1

    # Check for horizontal gap (Vertical Separation)
    h_gap_rows = [r for r in range(min_r + 1, max_r) if not np.any(input_grid[r, min_c:max_c+1] == 2)]
    if h_gap_rows:
        separation_axis = 'vertical'
        # Find the contiguous block of gap rows
        # Assume the first block found is the relevant one if multiple exist
        start_r = h_gap_rows[0]
        end_r = start_r
        for i in range(1, len(h_gap_rows)):
            if h_gap_rows[i] == end_r + 1:
                end_r = h_gap_rows[i]
            else:
                 # Stop if the gap rows are not contiguous
                 # This simplistic approach assumes one primary gap.
                 break
        gap_min_r = start_r
        gap_max_r = end_r


    # Check for vertical gap (Horizontal Separation) only if no horizontal gap was found
    if separation_axis is None:
        v_gap_cols = [c for c in range(min_c + 1, max_c) if not np.any(input_grid[min_r:max_r+1, c] == 2)]
        if v_gap_cols:
            separation_axis = 'horizontal'
            # Find the contiguous block of gap columns
            start_c = v_gap_cols[0]
            end_c = start_c
            for i in range(1, len(v_gap_cols)):
                 if v_gap_cols[i] == end_c + 1:
                     end_c = v_gap_cols[i]
                 else:
                     # Stop if the gap columns are not contiguous
                     break
            gap_min_c = start_c
            gap_max_c = end_c

    # --- 4. Apply Transformation ---

    if separation_axis == 'horizontal':
        # Find inner vertical extent based on red pixels adjacent to the gap
        rows_with_adjacent_red = set()
        # Check column left of gap (if exists)
        if gap_min_c > 0:
            for r in range(height):
                 if input_grid[r, gap_min_c - 1] == 2:
                     rows_with_adjacent_red.add(r)
        # Check column right of gap (if exists)
        if gap_max_c < width - 1:
             for r in range(height):
                 if input_grid[r, gap_max_c + 1] == 2:
                     rows_with_adjacent_red.add(r)

        if rows_with_adjacent_red:
             inner_min_r = min(rows_with_adjacent_red)
             inner_max_r = max(rows_with_adjacent_red)
             # Fill the rectangle with gray
             output_grid[inner_min_r : inner_max_r + 1, gap_min_c : gap_max_c + 1] = 5
        else:
            # Fallback or error case: couldn't determine bounds for filling
            # Revert to original state (or just gray removed state)? Keep gray removed.
            pass


    elif separation_axis == 'vertical':
        # Find original gray objects
        gray_objects = find_objects(input_grid, 5)

        for obj_coords in gray_objects:
            if not obj_coords: continue # Skip empty objects if any

            obj_rows = [r for r, c in obj_coords]
            obj_min_r = min(obj_rows)
            obj_max_r = max(obj_rows)
            delta_r = 0

            # Determine if object is above or below the gap and calculate shift
            if obj_max_r < gap_min_r: # Object is above gap
                delta_r = gap_min_r - obj_min_r # Shift down
            elif obj_min_r > gap_max_r: # Object is below gap
                delta_r = gap_max_r - obj_max_r # Shift up

            # Apply the shift to each pixel of the object
            for r, c in obj_coords:
                new_r = r + delta_r
                # Ensure the new position is within bounds (should be if gap logic is correct)
                if 0 <= new_r < height:
                    output_grid[new_r, c] = 5

    # If separation_axis is None, no transformation is applied beyond removing gray.

    # --- 5. Return Result ---
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
0 0 0 2 2 5 5 5 5 5 2 2 0 0 0
0 0 0 2 0 5 5 5 5 5 0 2 0 0 0
0 0 0 2 0 5 5 5 5 5 0 2 0 0 0
0 0 0 2 0 5 5 5 5 5 0 2 0 0 0
0 0 0 2 0 5 5 5 5 5 0 2 0 0 0
0 0 0 2 2 5 5 5 5 5 2 2 0 0 0
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
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

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
0 0 0 2 2 5 5 5 5 2 2 0 0 0 0
0 0 0 2 0 5 5 5 5 0 2 0 0 0 0
0 0 0 2 0 5 5 5 5 0 2 0 0 0 0
0 0 0 2 0 5 5 5 5 0 2 0 0 0 0
0 0 0 2 2 5 5 5 5 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 12
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 10.666666666666657
