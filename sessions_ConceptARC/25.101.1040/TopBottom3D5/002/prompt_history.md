
## train_1

**input:**
```
0 0 1 1 1 1 1 1 0 0 0 0
0 0 1 1 1 1 1 1 0 0 0 0
0 0 1 1 2 2 2 1 7 7 7 0
0 3 3 3 2 2 2 1 7 7 7 0
0 3 3 3 2 2 2 1 7 7 7 0
0 3 3 3 3 3 1 1 7 7 7 0
0 3 3 3 3 3 1 1 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0
```


**output:**
```
2 2 2
2 2 2
2 2 2
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0
0 9 9 9 9 0 3 3 0
4 9 9 9 9 4 4 4 4
4 9 9 9 9 4 4 4 4
4 9 9 9 9 4 4 4 4
0 9 9 9 9 0 0 0 0
0 9 7 7 7 7 0 0 0
0 0 7 7 7 7 0 0 0
0 0 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
7 7 7 7
7 7 7 7
7 7 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 0 0
0 0 0 0 3 3 3 4 0 0
0 0 0 2 2 2 3 4 0 0
0 0 5 5 5 2 3 0 0 0
0 0 0 5 5 2 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
5 5 5
0 5 5
0 0 5
```

*   **Perception:** The task involves identifying a specific "target" object within a larger input grid based on its color and then extracting a 3x3 representation of that object. The input grids contain multiple objects of different colors and shapes, set against a white background. The output grid is always 3x3 and contains the pixels corresponding to the top-left 3x3 portion of the identified target object's bounding box. If the target object doesn't completely fill this 3x3 area within its bounding box, the remaining cells are white.

*   **Facts:**
    
```yaml
    task_type: object_extraction
    input_grid_properties:
      - contains_multiple_objects: true
      - background_color: white (0)
      - object_colors_present: [blue, red, green, yellow, gray, orange, maroon] # Across examples
    output_grid_properties:
      - size: 3x3
      - content: derived_from_single_input_object
    transformation_logic:
      - step: identify_target_object
        criteria:
          - property: color
          - rule: color is one of [red (2), orange (7), gray (5)] # Based on observed examples
          - assumption: only one such object exists per input grid
      - step: determine_bounding_box
        target: identified_target_object
      - step: extract_subgrid
        source: bounding_box_of_target_object
        subgrid_definition: top_left_3x3_area
      - step: handle_incomplete_fill
        rule: if a cell within the 3x3 subgrid does not correspond to a pixel of the target object (e.g., outside the object but inside its bounding box, or if the bounding box is smaller than 3x3), the output cell value is white (0).
      - step: generate_output
        content: extracted_3x3_subgrid
    ```


*   **Natural Language Program:**
    1.  Scan the input grid to find the object whose color is red (2), orange (7), or gray (5). Assume exactly one such object exists.
    2.  Determine the minimum bounding box containing this target object.
    3.  Create a new 3x3 grid initialized with white (0) pixels.
    4.  Iterate through the cells from row 0 to 2 and column 0 to 2 of the output grid.
    5.  For each output cell at `(row, col)`, find the corresponding cell in the input grid at `(bounding_box_top_row + row, bounding_box_left_col + col)`.
    6.  If this corresponding input cell exists within the bounds of the input grid *and* contains the color of the target object, copy the target object's color to the output cell at `(row, col)`. Otherwise, leave the output cell as white (0).
    7.  Return the generated 3x3 grid.
```python
import collections

"""
Identifies a target object based on its color (red, orange, or gray) within the input grid. 
Determines the bounding box of this target object. 
Extracts the top-left 3x3 area from the input grid corresponding to the target object's bounding box. 
If a cell within this 3x3 area in the input does not belong to the target object (either outside bounds or different color), the corresponding output cell is set to white (0). 
Otherwise, the output cell takes the color of the target object.
"""

def find_connected_pixels(grid, start_r, start_c, target_color):
    """Finds all connected pixels of a target color using BFS."""
    height = len(grid)
    width = len(grid[0])
    q = collections.deque([(start_r, start_c)])
    visited = set([(start_r, start_c)])
    pixels = set([(start_r, start_c)])

    while q:
        r, c = q.popleft()

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # 4-connectivity
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr][nc] == target_color and (nr, nc) not in visited:
                visited.add((nr, nc))
                pixels.add((nr, nc))
                q.append((nr, nc))
    return pixels

def get_bounding_box(pixels):
    """Calculates the bounding box for a set of pixel coordinates."""
    if not pixels:
        return -1, -1, -1, -1 # Or raise error
    min_r = min(r for r, c in pixels)
    min_c = min(c for r, c in pixels)
    max_r = max(r for r, c in pixels)
    max_c = max(c for r, c in pixels)
    return min_r, min_c, max_r, max_c

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by finding a specific colored object (red, orange, or gray)
    and extracting its top-left 3x3 representation.
    """
    height = len(input_grid)
    width = len(input_grid[0])
    target_colors = {2, 7, 5} # red, orange, gray

    found_target_color = -1
    target_pixels = set()
    bbox_top_row = -1
    bbox_left_col = -1

    # 1. Scan the input grid to find the target object
    for r in range(height):
        for c in range(width):
            color = input_grid[r][c]
            if color in target_colors:
                # 2. Once a pixel of a target color is found, find all connected pixels
                found_target_color = color
                target_pixels = find_connected_pixels(input_grid, r, c, found_target_color)
                # 3. Determine the minimum bounding box
                min_r, min_c, _, _ = get_bounding_box(target_pixels)
                bbox_top_row = min_r
                bbox_left_col = min_c
                break # Found the first pixel of the target object, assume only one
        if found_target_color != -1:
            break # Exit outer loop as well

    if found_target_color == -1:
         # Handle case where no target object is found (though problem implies one exists)
         # Returning an empty or default grid might be appropriate, or raise an error.
         # Based on examples, we assume a target is always found.
         # For robustness, let's return a default 3x3 white grid.
         return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


    # 4. Create a new 3x3 grid initialized with white (0) pixels.
    output_grid = [[0 for _ in range(3)] for _ in range(3)]

    # 5. Iterate through the cells of the output grid (0 to 2 for row and col).
    for r_out in range(3):
        for c_out in range(3):
            # 6. Find the corresponding cell in the input grid.
            r_in = bbox_top_row + r_out
            c_in = bbox_left_col + c_out

            # 7. Check if the corresponding input cell exists within bounds
            #    and belongs to the target object (has the target color).
            if 0 <= r_in < height and 0 <= c_in < width and \
               input_grid[r_in][c_in] == found_target_color:
                # Copy the target object's color to the output cell.
                output_grid[r_out][c_out] = found_target_color
            # Otherwise, leave the output cell as white (0) (already initialized).

    # 8. Return the generated 3x3 grid.
    return output_grid
```
