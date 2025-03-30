
Previous Code:
```python
import numpy as np
from collections import Counter
import copy

"""
Transforms an input grid based on the following rules:

1.  **Identify Background:** Determine the most frequent color in the input grid, which is considered the background color.
2.  **Find Objects:** Locate all contiguous areas (objects) of pixels that are not the background color. For each object, record its color, the set of pixel coordinates it occupies, its bounding box, and its top-left coordinate.
3.  **Filter Objects:** Select objects for processing based on their color:
    *   Always ignore objects with colors Gray (5), Orange (7), or Maroon (9).
    *   If the background color is Azure (8), additionally ignore objects with color Red (2).
4.  **Sort Objects:** Arrange the filtered (relevant) objects based on their position:
    *   Primary sort key: Row of the top-left coordinate (ascending).
    *   Secondary sort key: Column of the top-left coordinate (ascending).
    *   Conditional Reversal: If the background color is Yellow (4), reverse the order of the sorted objects.
5.  **Determine Output Dimensions:**
    *   Calculate the height (`H_i`) of the bounding box for each relevant object `i`.
    *   The output grid's height (`output_height`) is the sum of all `H_i`.
    *   The output grid's width (`output_width`) is the maximum value among all `H_i`.
6.  **Construct Output Grid:**
    *   Create an output grid with the calculated `output_height` and `output_width`, filled entirely with the background color.
    *   Iterate through the final sorted list of relevant objects. For each object:
        *   Determine its bounding box height `h` and width `w`.
        *   Calculate the horizontal starting position (`start_col`) to center the object's pixels within the `output_width`: `start_col = (output_width - w) // 2`.
        *   For each pixel `(r, c)` belonging to the current object:
            *   Calculate its position relative to the object's bounding box top-left corner (`min_r`, `min_c`): `rel_r = r - min_r`, `rel_c = c - min_c`.
            *   Calculate the target column in the output slice: `target_c = start_col + rel_c`.
            *   Place the object's color at the corresponding position in the output grid slice for this object (row `current_row + rel_r`, column `target_c`).
        *   Advance `current_row` by the object's height `h`.
7.  **Return:** Convert the final NumPy output grid to a list of lists format. If no relevant objects are found after filtering, return an empty grid `[[]]`.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    # Handles empty or invalid input gracefully
    if grid.size == 0:
        return 0 # Default to white/black if grid is empty
    counts = Counter(grid.flatten())
    if not counts:
        return 0 # Should not happen if grid.size > 0, but safe check
    # Background is the most frequent color.
    background_color = counts.most_common(1)[0][0]
    return background_color

def find_objects(grid, background_color):
    """Finds all contiguous objects of non-background colors using Breadth-First Search."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != background_color:
                color = grid[r, c]
                obj_pixels = set()
                q = [(r, c)]
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                processed_in_current_object = set([(r,c)]) # Track nodes added to queue

                while q:
                    row, col = q.pop(0)
                    obj_pixels.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            # Check if already queued for this object to prevent duplicates
                           if (nr, nc) not in processed_in_current_object:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                processed_in_current_object.add((nr,nc))

                if obj_pixels:
                    bounding_box = (min_r, min_c, max_r, max_c)
                    height = max_r - min_r + 1
                    width = max_c - min_c + 1
                    objects.append({
                        'color': color,
                        'pixels': obj_pixels,
                        'bbox': bounding_box,
                        'top_left': (min_r, min_c),
                        'height': height,
                        'width': width
                    })
    return objects

def filter_objects(objects, background_color):
    """Filters objects based on color rules."""
    ignored_colors = {5, 7, 9} # Gray, Orange, Maroon
    relevant_objects = []
    for obj in objects:
        color = obj['color']
        # Rule 1: Ignore specific colors
        if color in ignored_colors:
            continue
        # Rule 2: Ignore Red if background is Azure
        if background_color == 8 and color == 2:
            continue
        relevant_objects.append(obj)
    return relevant_objects

def transform(input_grid):
    """
    Transforms the input grid by extracting, filtering, sorting, and stacking shapes
    based on the specified rules.
    """
    input_np = np.array(input_grid, dtype=int)

    # 1. Determine background color
    background_color = find_background_color(input_np)

    # 2. Find all objects
    all_objects = find_objects(input_np, background_color)

    # 3. Filter objects
    relevant_objects = filter_objects(all_objects, background_color)

    # 4. Handle case with no relevant objects
    if not relevant_objects:
        return [[]] # Return empty grid as per requirement analysis

    # 5. Sort objects by top-left (row, then column)
    # Sorting key is a tuple (row, column)
    sorted_objects = sorted(relevant_objects, key=lambda obj: obj['top_left'])

    # 6. Conditional reverse if background is Yellow (4)
    if background_color == 4:
        sorted_objects.reverse()

    final_ordered_objects = sorted_objects

    # 7. Determine output grid dimensions
    output_height = 0
    max_object_height = 0
    if final_ordered_objects: # Ensure list is not empty before calculating max
      max_object_height = max(obj['height'] for obj in final_ordered_objects)

    output_width = max_object_height # Output width is the max height of relevant objects
    for obj in final_ordered_objects:
        output_height += obj['height']

    # Ensure valid dimensions, at least 1x1 if objects exist
    if output_height <= 0 or output_width <= 0:
         return [[]] # Or potentially a 1x1 background grid? Empty seems safer.

    # 8. Construct the output grid
    output_grid = np.full((output_height, output_width), background_color, dtype=int)

    current_row = 0
    # 9. Iterate through sorted objects and place them in the output grid
    for obj in final_ordered_objects:
        h = obj['height']
        w = obj['width']
        min_r, min_c, _, _ = obj['bbox']
        obj_color = obj['color']
        pixels = obj['pixels']

        # Calculate starting column for horizontal centering
        start_col = (output_width - w) // 2

        # Place the object's pixels onto the output grid slice
        for r, c in pixels:
            rel_r = r - min_r  # Relative row within the object's bounding box
            rel_c = c - min_c  # Relative col within the object's bounding box

            target_r = current_row + rel_r
            target_c = start_col + rel_c

            # Check bounds (should be safe with centering if width calc is right, but good practice)
            if 0 <= target_r < output_height and 0 <= target_c < output_width:
                output_grid[target_r, target_c] = obj_color

        # Move to the starting row for the next object
        current_row += h

    # 10. Return as list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 5 2 2 2 2 2 2 2 2 2 2 2 2 2 5 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 4 4 2 2 2 8 8 2 2 2 2 2 2 2 2 2 2
2 2 4 2 2 4 2 8 2 2 8 2 3 3 2 2 2 2 2 2
2 4 2 2 2 2 4 5 2 2 2 8 2 2 3 2 2 2 2 2
2 4 2 9 2 2 4 2 2 2 3 8 2 9 2 3 2 2 2 2
2 2 4 2 2 4 2 8 2 2 8 2 2 2 2 3 2 2 2 2
2 2 2 4 4 2 2 2 8 8 2 3 2 2 3 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 3 3 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 5 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
5 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
```
Expected Output:
```
2 2 4 4 2 2
2 4 2 2 4 2
4 2 2 2 2 4
4 2 2 2 2 4
2 4 2 2 4 2
2 2 4 4 2 2
2 2 8 8 2 2
2 8 2 2 8 2
8 2 2 2 2 8
8 2 2 2 2 8
2 8 2 2 8 2
2 2 8 8 2 2
2 2 3 3 2 2
2 3 2 2 3 2
3 2 2 2 2 3
3 2 2 2 2 3
2 3 2 2 3 2
2 2 3 3 2 2
```
Transformed Output:
```
4 4
8 8
4 2
4 2
8 2
8 2
3 3
4 2
4 2
4 2
4 2
8 2
8 2
3 2
3 2
3 2
3 2
4 2
4 2
8 2
8 2
4 4
8 8
3 2
3 2
3 3
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None

## Example 2:
Input:
```
3 3 3 3 3 3 3 3 3 3
5 3 3 4 4 3 3 3 3 3
3 3 4 3 8 4 3 3 3 3
3 4 3 8 3 3 4 3 3 3
3 4 8 1 3 3 4 8 3 3
3 1 4 3 1 4 3 8 3 3
1 3 3 4 4 1 8 3 3 3
1 3 5 3 8 8 3 3 3 3
3 1 3 3 1 3 3 3 3 3
3 3 1 1 3 3 5 3 3 3
```
Expected Output:
```
3 3 4 4 3 3
3 4 3 3 4 3
4 3 3 3 3 4
4 3 3 3 3 4
3 4 3 3 4 3
3 3 4 4 3 3
3 3 8 8 3 3
3 8 3 3 8 3
8 3 3 3 3 8
8 3 3 3 3 8
3 8 3 3 8 3
3 3 8 8 3 3
3 3 1 1 3 3
3 1 3 3 1 3
1 3 3 3 3 1
1 3 3 3 3 1
3 1 3 3 1 3
3 3 1 1 3 3
```
Transformed Output:
```
4 4
4 3
8 3
4 3
4 3
4 3
8 3
4 3
4 3
8 3
1 3
8 3
8 3
1 3
4 3
1 3
4 3
1 3
1 3
4 4
1 3
8 3
8 8
1 3
1 3
1 1
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None

## Example 3:
Input:
```
4 4 4 4 4 5 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 7 4
4 4 2 2 4 4 4 4 4 4 4 4 4
4 2 4 4 2 4 4 4 4 4 4 4 4
2 4 4 7 4 2 4 4 4 4 4 4 4
2 4 4 4 4 8 8 4 4 5 4 4 4
4 2 4 4 8 4 4 8 4 4 4 4 4
4 4 2 8 4 4 4 4 8 4 4 4 4
4 4 4 8 4 4 4 4 3 3 4 4 4
4 4 4 4 8 4 4 3 4 4 3 4 4
4 5 4 4 4 8 3 4 4 4 4 3 4
4 4 7 4 4 4 3 4 4 5 4 3 4
4 4 4 4 4 4 4 3 4 4 3 4 4
```
Expected Output:
```
4 4 3 3 4 4
4 3 4 4 3 4
3 4 4 4 4 3
3 4 4 4 4 3
4 3 4 4 3 4
4 4 3 3 4 4
4 4 8 8 4 4
4 8 4 4 8 4
8 4 4 4 4 8
8 4 4 4 4 8
4 8 4 4 8 4
4 4 8 8 4 4
4 4 2 2 4 4
4 2 4 4 2 4
2 4 4 4 4 2
2 4 4 4 4 2
4 2 4 4 2 4
4 4 2 2 4 4
```
Transformed Output:
```
3 4
3 4
3 4
3 4
3 4
3 4
8 4
3 4
3 4
8 4
3 3
8 4
8 4
8 4
2 4
8 4
8 4
2 4
8 8
2 4
2 4
2 4
2 4
2 4
2 2
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None

## Example 4:
Input:
```
8 8 8 8 8 8 8 8 5 8
8 8 8 8 8 8 8 8 8 8
8 8 8 4 4 8 3 3 8 8
8 8 4 8 8 4 8 8 3 8
8 4 2 8 3 8 4 8 8 3
8 4 8 8 3 8 4 8 8 3
8 8 4 8 8 4 8 8 3 8
8 8 8 4 4 8 3 3 8 8
8 5 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 8 8
```
Expected Output:
```
8 8 4 4 8 8
8 4 8 8 4 8
4 8 8 8 8 4
4 8 8 8 8 4
8 4 8 8 4 8
8 8 4 4 8 8
8 8 3 3 8 8
8 3 8 8 3 8
3 8 8 8 8 3
3 8 8 8 8 3
8 3 8 8 3 8
8 8 3 3 8 8
```
Transformed Output:
```
4 4
3 3
4 8
4 8
3 8
4 8
4 8
3 8
3 8
4 8
4 8
3 8
3 8
4 8
4 8
3 8
4 4
3 3
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None
