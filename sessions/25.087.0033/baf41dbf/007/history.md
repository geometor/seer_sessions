
Previous Code:
```python
import numpy as np
from collections import deque

"""
Transforms the input grid by finding the main green (3) frame object, resizing it based on the positions of external magenta (6) markers, and drawing the resized frame on a new grid along with the original markers.

1. Identifies all magenta markers and stores their coordinates.
2. Identifies all connected green objects (potential frames).
3. If green objects exist, determines the "main" green object based on the largest bounding box area. Ties are broken by the top-left corner position (min_row, then min_col).
4. Calculates the initial bounding box of this main green object.
5. Finds magenta markers located strictly outside the main object's initial bounding box.
6. Calculates a target bounding box based on these external markers:
    - Top boundary extends towards the lowest marker above, stopping one step before it.
    - Bottom boundary extends towards the highest marker below, stopping one step before it.
    - Left boundary extends towards the rightmost marker to the left, stopping one step before it.
    - Right boundary extends towards the leftmost marker to the right, stopping one step before it.
7. Determines the final new bounding box as the union of the initial box and the target expansion area. Coordinates are clamped to grid bounds.
8. Creates an output grid initialized to white (0).
9. Draws a hollow green rectangle representing the perimeter of the new bounding box on the output grid.
10. Redraws all original magenta markers at their initial positions on the output grid.
"""

def find_objects(grid, color):
    """
    Finds all connected components of a given color in the grid using Breadth-First Search.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to search for.

    Returns:
        list: A list of sets, where each set contains the (row, col) tuples
              of pixels belonging to a connected object. Objects are connected
              cardinally (up, down, left, right). Returns an empty list if no
              objects of the specified color are found.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                obj_coords.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check 4 cardinal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            obj_coords.add((nr, nc))
                            q.append((nr, nc))
                
                if obj_coords: # ensure we found something
                    objects.append(obj_coords)
    return objects

def get_bounding_box(obj_coords):
    """
    Calculates the bounding box (min_row, min_col, max_row, max_col) for a set of coordinates.

    Args:
        obj_coords (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) inclusive.
               Returns None if obj_coords is empty.
    """
    if not obj_coords:
        return None
    
    min_row = min(r for r, c in obj_coords)
    min_col = min(c for r, c in obj_coords)
    max_row = max(r for r, c in obj_coords)
    max_col = max(c for r, c in obj_coords)
    
    return min_row, min_col, max_row, max_col

def get_bbox_area(bbox):
    """Calculates the area of a bounding box."""
    if not bbox:
        return 0
    min_r, min_c, max_r, max_c = bbox
    return (max_r - min_r + 1) * (max_c - min_c + 1)

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    # Initialize output grid with white (0)
    output_grid = np.zeros_like(input_np) 

    # --- Step 1: Find Magenta Markers ---
    magenta_markers = []
    for r in range(rows):
        for c in range(cols):
            if input_np[r, c] == 6:
                magenta_markers.append((r, c))

    # --- Step 2: Find Green Objects ---
    green_objects = find_objects(input_np, 3)
    
    main_green_object = None
    if green_objects:
        # --- Step 3: Identify Main Green Object ---
        max_area = -1
        best_bbox_top_left = (rows, cols) # Initialize with max possible values

        for obj_coords in green_objects:
            bbox = get_bounding_box(obj_coords)
            if not bbox: continue
            
            area = get_bbox_area(bbox)
            min_r, min_c, _, _ = bbox
            
            if area > max_area:
                max_area = area
                main_green_object = obj_coords
                best_bbox_top_left = (min_r, min_c)
            elif area == max_area:
                # Tie-breaking: choose the one with the top-most, then left-most corner
                if (min_r, min_c) < best_bbox_top_left:
                    main_green_object = obj_coords
                    best_bbox_top_left = (min_r, min_c)

    # --- Process the main frame if found ---
    if main_green_object:
        # --- Step 4: Calculate initial bounding box ---
        initial_bbox = get_bounding_box(main_green_object)
        if not initial_bbox: # Should not happen if main_green_object is valid
             # Draw only markers if frame finding failed unexpectedly
             for r, c in magenta_markers:
                 if 0 <= r < rows and 0 <= c < cols:
                     output_grid[r, c] = 6
             return output_grid.tolist()

        initial_min_r, initial_min_c, initial_max_r, initial_max_c = initial_bbox

        # --- Step 5: Find external markers ---
        external_markers = [
            (m_r, m_c) for m_r, m_c in magenta_markers 
            if not (initial_min_r <= m_r <= initial_max_r and initial_min_c <= m_c <= initial_max_c)
        ]

        # --- Step 6: Calculate target boundaries based on external markers ---
        target_min_r = rows # Default: grid height (no markers above)
        target_max_r = -1   # Default: -1 (no markers below)
        target_min_c = cols # Default: grid width (no markers left)
        target_max_c = -1   # Default: -1 (no markers right)

        markers_above = [m_r for m_r, m_c in external_markers if m_r < initial_min_r]
        markers_below = [m_r for m_r, m_c in external_markers if m_r > initial_max_r]
        markers_left  = [m_c for m_r, m_c in external_markers if m_c < initial_min_c]
        markers_right = [m_c for m_r, m_c in external_markers if m_c > initial_max_c]

        if markers_above:
            # Lowest marker above defines target top row (+1 because boundary stops before marker)
            target_min_r = min(markers_above) + 1 
        if markers_below:
            # Highest marker below defines target bottom row (-1 because boundary stops before marker)
            target_max_r = max(markers_below) - 1
        if markers_left:
            # Rightmost marker left defines target left col (+1) - use max coord
            target_min_c = max(markers_left) + 1 
        if markers_right:
            # Leftmost marker right defines target right col (-1) - use min coord
            target_max_c = min(markers_right) - 1

        # --- Step 7: Determine final new bounding box ---
        # Union of initial box and target expansion area
        new_min_r = min(initial_min_r, target_min_r)
        new_max_r = max(initial_max_r, target_max_r)
        new_min_c = min(initial_min_c, target_min_c)
        new_max_c = max(initial_max_c, target_max_c)
        
        # --- Step 8: Clamp bounds to grid dimensions ---
        new_min_r = max(0, new_min_r)
        new_max_r = min(rows - 1, new_max_r)
        new_min_c = max(0, new_min_c)
        new_max_c = min(cols - 1, new_max_c)

        # --- Step 9 & 10: Draw hollow green rectangle ---
        # Check if the calculated box has valid dimensions before drawing
        if new_min_r <= new_max_r and new_min_c <= new_max_c:
            # Draw top border
            output_grid[new_min_r, new_min_c:new_max_c+1] = 3
            # Draw bottom border
            output_grid[new_max_r, new_min_c:new_max_c+1] = 3
            # Draw left border (excluding corners already drawn)
            if new_max_r > new_min_r: # Avoid index error for single row boxes
                 output_grid[new_min_r+1:new_max_r, new_min_c] = 3
            # Draw right border (excluding corners already drawn)
            if new_max_r > new_min_r and new_max_c > new_min_c: # Avoid index error and overdraw for single row/col boxes
                 output_grid[new_min_r+1:new_max_r, new_max_c] = 3
            
    # --- Step 11: Redraw Magenta Markers ---
    # This happens regardless of whether a green frame was found/processed
    for r, c in magenta_markers:
        # Ensure marker is within bounds before drawing (should always be)
        if 0 <= r < rows and 0 <= c < cols:
            output_grid[r, c] = 6

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0 0 0
0 6 0 0 3 0 3 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0 0 0 0
0 6 3 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0 0 0 0
0 6 3 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0
0 3 0 3 0 0 3 0 0 0 0 6 0 0 0 0 0
0 3 0 3 0 0 3 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 3 0 3 0 0 0 0 0 0 3 6 0 0 0 0 0
0 3 0 3 0 0 0 0 0 0 3 0 0 0 0 0 0
0 3 0 3 0 0 0 0 0 0 3 0 0 0 0 0 0
0 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 3 6 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0
0 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 3
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 4.411764705882348

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 3 0 0 0 0 0
0 0 0 0 3 0 0 3 0 3 0 0 6 0 0
0 0 0 0 3 3 3 3 3 3 0 0 0 0 0
0 6 0 0 3 0 0 3 0 3 0 0 0 0 0
0 0 0 0 3 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 0 0 0 0 3 0 0 0 3 6 0 0
0 0 3 3 3 3 3 3 3 3 3 3 0 0 0
0 6 3 0 0 0 0 3 0 0 0 3 0 0 0
0 0 3 0 0 0 0 3 0 0 0 3 0 0 0
0 0 3 0 0 0 0 3 0 0 0 3 0 0 0
0 0 3 0 0 0 0 3 0 0 0 3 0 0 0
0 0 3 0 0 0 0 3 0 0 0 3 0 0 0
0 0 3 0 0 0 0 3 0 0 0 3 0 0 0
0 0 3 0 0 0 0 3 0 0 0 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 0 0 0 0 0 0 0 0 3 6 0 0
0 0 3 0 0 0 0 0 0 0 0 3 0 0 0
0 6 3 0 0 0 0 0 0 0 0 3 0 0 0
0 0 3 0 0 0 0 0 0 0 0 3 0 0 0
0 0 3 0 0 0 0 0 0 0 0 3 0 0 0
0 0 3 0 0 0 0 0 0 0 0 3 0 0 0
0 0 3 0 0 0 0 0 0 0 0 3 0 0 0
0 0 3 0 0 0 0 0 0 0 0 3 0 0 0
0 0 3 0 0 0 0 0 0 0 0 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 16
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 14.222222222222229
**Correction:** My manual analysis of Example 3 was incorrect regarding the number of green objects. The `find_objects` function identifies *all* connected green pixels as a single object if they touch cardinally. In Example 3, the two apparent rectangles are connected by pixels like (5,4) and (6,4), forming one large object. The code output confirms this: "Number of Green Objects: 1", with BBox `(3, 4, 7, 9)`. This simplifies the "main object" selection as there's only one. The rest of the analysis holds.

The metrics confirm the initial bounding boxes and external markers used in the previous logic. The core issue remains the handling of the *content* within the frame during resizing.

## General Assessment

The provided code successfully identifies the main green frame object and calculates the correct expanded bounding box based on external magenta markers in all examples. Example 1 succeeded because the original frame was hollow, so drawing only the new border was sufficient. Examples 2 and 3 failed because the original frames contained internal patterns (non-green pixels) which were discarded by the code. The code only drew the *new* hollow green frame and the magenta markers, omitting the original content.

The strategy to resolve this is to modify the transformation process:
1.  Identify the main green frame and its initial bounding box (`initial_bbox`).
2.  Identify external magenta markers and calculate the new bounding box (`new_bbox`).
3.  Create an empty output grid.
4.  Copy the rectangular region defined by `initial_bbox` from the input grid to the same coordinates in the output grid.
5.  Draw the *perimeter* of the `new_bbox` onto the output grid using the green color (color 3). This will overwrite any pixels from the previous step that fall on the new border.
6.  Draw all original magenta markers onto the output grid at their original positions.

## Metrics

| Example | Input Shape | Output Shape | Main Green Initial BBox | External Markers | Pixels Off (Previous Code) | Failure Reason                                     |
| :------ | :---------- | :----------- | :---------------------- | :--------------- | :------------------------- | :------------------------------------------------- |
| 1       | 11x15       | 11x15        | (2, 4, 4, 6)            | [(3, 1), (9, 5)] | 0                          | N/A (Success)                                      |
| 2       | 8x17        | 8x17         | (1, 1, 4, 6)            | [(2, 11), (6, 4)] | 3                          | Original frame content (white pixels) not copied.  |
| 3       | 15x15       | 15x15        | (3, 4, 7, 9)            | [(4, 12), (6, 1), (14, 7)] | 16                         | Original frame content (white pixels) not copied. |

*Note: The BBoxes are (min_row, min_col, max_row, max_col), inclusive.*
*Note: The code analysis confirmed only one green object was found in Example 3, with BBox (3, 4, 7, 9).*

## Facts


```yaml
task_description: "Resize a green frame based on the location of external magenta markers, preserving the original content within the frame's initial area."

grid_properties:
  - size: Variable (up to 30x30)
  - background_color: white (0)

objects:
  - type: frame
    color: green (3)
    definition: A connected component of green pixels. May be hollow or contain other colors.
    properties:
      - bounding_box: The smallest rectangle enclosing the object.
      - main_frame: If multiple green objects exist, the one with the largest bounding box area. Ties broken by top-most, then left-most bounding box corner. (In observed examples, only one green object exists).
  - type: marker
    color: magenta (6)
    definition: Single pixels of magenta color.
    properties:
      - location: (row, col) coordinates.
      - classification:
          - internal: Located within or on the border of the main_frame's initial bounding box.
          - external: Located strictly outside the main_frame's initial bounding box.

actions:
  - 1_find_markers: Identify the coordinates of all magenta markers.
  - 2_find_frame: Identify all connected green objects and determine the main_frame and its initial bounding box (`initial_bbox`).
  - 3_classify_markers: Identify which magenta markers are external to `initial_bbox`.
  - 4_calculate_new_bbox: Determine the target expansion boundaries based on external markers:
      - target_top: Row below the lowest external marker above `initial_bbox`.
      - target_bottom: Row above the highest external marker below `initial_bbox`.
      - target_left: Column right of the rightmost external marker left of `initial_bbox`.
      - target_right: Column left of the leftmost external marker right of `initial_bbox`.
      - The final new bounding box (`new_bbox`) is the union of `initial_bbox` and the area defined by the target boundaries, clamped to grid dimensions.
  - 5_create_output: Initialize an output grid of the same size as the input, filled with white (0).
  - 6_copy_content: Copy the rectangular region defined by `initial_bbox` from the input grid to the output grid at the same coordinates.
  - 7_draw_new_frame: Draw a hollow rectangle using green (3) along the perimeter defined by `new_bbox` onto the output grid.
  - 8_draw_markers: Draw all original magenta markers (both internal and external) onto the output grid at their original coordinates.

edge_cases:
  - No green frame found: Output should contain only the magenta markers on a white background.
  - No external markers found: The frame is not resized (`new_bbox` equals `initial_bbox`). Content is copied, frame border is redrawn (potentially changing internal green pixels to border green pixels if the original wasn't hollow), markers are drawn.
  - Markers only on some sides: Frame expands only in the directions indicated by external markers.
```


## Natural Language Program

1.  Initialize an output grid of the same dimensions as the input grid, filled with the background color (white, 0).
2.  Find all coordinates of magenta (6) pixels (markers).
3.  Find all connected components of green (3) pixels. If multiple components exist, identify the "main" component as the one with the largest bounding box area (breaking ties by selecting the component whose bounding box has the minimum row index, then minimum column index). If no green component exists, skip to step 7.
4.  Calculate the initial bounding box (`initial_bbox`) of the main green component.
5.  Copy the rectangular region defined by `initial_bbox` from the input grid to the corresponding region in the output grid.
6.  Determine the "new" bounding box (`new_bbox`):
    a.  Identify magenta markers that lie strictly outside `initial_bbox`.
    b.  Calculate target expansion boundaries based on these external markers:
        i.  The top boundary expands upwards towards the lowest external marker *above* the `initial_bbox`, stopping one row below it.
        ii. The bottom boundary expands downwards towards the highest external marker *below* the `initial_bbox`, stopping one row above it.
        iii.The left boundary expands leftwards towards the rightmost external marker *left* of the `initial_bbox`, stopping one column to its right.
        iv. The right boundary expands rightwards towards the leftmost external marker *right* of the `initial_bbox`, stopping one column to its left.
    c.  `new_bbox` is the union of `initial_bbox` and the target expansion area (defined by the calculated boundaries), ensuring coordinates stay within the grid limits. If there are no external markers in a given direction (e.g., no markers above), the boundary does not expand in that direction.
    d.  Draw the perimeter of `new_bbox` on the output grid using green (3), overwriting any pixels previously copied in step 5 that fall on this perimeter.
7.  Draw all magenta markers found in step 2 onto the output grid at their original coordinates, overwriting any existing pixels at those locations.
8.  Return the final output grid.## General Assessment

The previous code successfully identified the primary green object (frame) and the external magenta markers, correctly calculating the dimensions and position of the resized frame based on these markers. The code worked for Example 1 where the original frame content was effectively hollow or irrelevant. However, it failed on Examples 2 and 3 because it only drew the *new* frame's border and markers, neglecting to preserve the content that was originally inside the frame's initial bounding box.

The core issue is the omission of copying the original frame's content area into the new grid before drawing the resized frame border. The strategy is to insert a step where the content within the original frame's bounding box is copied to the output grid, *then* draw the new, potentially larger, frame border, and finally redraw the markers.

## Metrics

Metrics gathered using `tool_code` confirm the analysis:

| Example | Input Shape | Output Shape | Main Green Initial BBox | External Markers           | Pixels Off (Previous Code) | Failure Reason (Previous Code)                     |
| :------ | :---------- | :----------- | :---------------------- | :------------------------- | :------------------------- | :------------------------------------------------- |
| 1       | 11x15       | 11x15        | (2, 4, 4, 6)            | [(3, 1), (9, 5)]           | 0                          | N/A (Success)                                      |
| 2       | 8x17        | 8x17         | (1, 1, 4, 6)            | [(2, 11), (6, 4)]          | 3                          | Original frame content (white pixels) not copied.  |
| 3       | 15x15       | 15x15        | (3, 4, 7, 9)            | [(4, 12), (6, 1), (14, 7)] | 16                         | Original frame content (white pixels) not copied. |

*Note: BBoxes are (min_row, min_col, max_row, max_col), inclusive.*
*Note: In Example 3, although visually appearing as two rectangles, the green pixels form a single connected component.*

## Facts


```yaml
task_description: "Resize a green frame based on the location of external magenta markers, preserving the original content within the frame's initial area."

grid_properties:
  - size: Variable (up to 30x30)
  - background_color: white (0)

objects:
  - type: frame
    color: green (3)
    definition: A connected component of green pixels. May contain pixels of other colors within its bounding box.
    properties:
      - bounding_box: The smallest rectangle enclosing all the object's green pixels (`initial_bbox`).
      - main_frame: If multiple disjoint green objects exist, the one with the largest `initial_bbox` area. Ties broken by top-most, then left-most corner of `initial_bbox`. (In observed examples, only one connected green object exists).
      - content_area: The rectangular region defined by `initial_bbox`.
  - type: marker
    color: magenta (6)
    definition: Single pixels of magenta color.
    properties:
      - location: (row, col) coordinates.
      - classification:
          - internal: Located within or on the border of the `initial_bbox`.
          - external: Located strictly outside the `initial_bbox`.

actions:
  - 1_find_markers: Identify the coordinates of all magenta markers.
  - 2_find_frame: Identify all connected green objects. If any exist, determine the `main_frame` and its `initial_bbox`. If no green frame exists, proceed to step 8.
  - 3_classify_markers: Identify which magenta markers are `external` relative to `initial_bbox`.
  - 4_calculate_new_bbox: Determine the target expansion boundaries based on `external` markers:
      - target_top_boundary: Row index `r` such that `r = min(marker_row) + 1` for all external markers with `marker_row < initial_bbox.min_row`. Default is `initial_bbox.min_row`.
      - target_bottom_boundary: Row index `r` such that `r = max(marker_row) - 1` for all external markers with `marker_row > initial_bbox.max_row`. Default is `initial_bbox.max_row`.
      - target_left_boundary: Column index `c` such that `c = max(marker_col) + 1` for all external markers with `marker_col < initial_bbox.min_col`. Default is `initial_bbox.min_col`.
      - target_right_boundary: Column index `c` such that `c = min(marker_col) - 1` for all external markers with `marker_col > initial_bbox.max_col`. Default is `initial_bbox.max_col`.
      - The final new bounding box (`new_bbox`) encompasses the area from `min(initial_bbox.min_row, target_top_boundary)` to `max(initial_bbox.max_row, target_bottom_boundary)` and `min(initial_bbox.min_col, target_left_boundary)` to `max(initial_bbox.max_col, target_right_boundary)`, clamped to grid dimensions (0 to rows-1, 0 to cols-1).
  - 5_create_output: Initialize an output grid of the same size as the input, filled with white (0).
  - 6_copy_content: Copy the rectangular region defined by `initial_bbox` from the input grid to the output grid, placing it at the same `(row, col)` coordinates.
  - 7_draw_new_frame_border: Draw a hollow rectangle using green (3) along the perimeter defined by `new_bbox` onto the output grid. This overwrites any pixels previously copied in step 6 that lie on this new perimeter.
  - 8_draw_markers: Draw all magenta markers (found in step 1) onto the output grid at their original coordinates, overwriting any existing pixels.

edge_cases:
  - No green frame found: Output grid contains only the original magenta markers on a white background.
  - No external markers found: `new_bbox` equals `initial_bbox`. The content is copied, the frame border is redrawn with green (potentially overwriting original non-border green pixels if the frame wasn't hollow), and markers are drawn.
  - Markers only on some sides: Frame expands only in the directions indicated by external markers.
```


## Natural Language Program

1.  Create an output grid with the same dimensions as the input grid, initialized with white (0) pixels.
2.  Locate all magenta (6) pixels in the input grid and store their coordinates.
3.  Identify all distinct connected components of green (3) pixels in the input grid.
4.  If no green components are found, proceed directly to step 9.
5.  If one or more green components are found, determine the "main" green component: select the component whose bounding box has the largest area. If there's a tie in area, select the component whose bounding box has the minimum top-row index; if there's still a tie, select the one with the minimum left-column index. Let the bounding box of this main component be `initial_bbox`.
6.  Copy the rectangular region defined by `initial_bbox` (from `initial_bbox.min_row` to `initial_bbox.max_row`, and `initial_bbox.min_col` to `initial_bbox.max_col`) from the input grid to the *same corresponding region* in the output grid.
7.  Identify the subset of magenta markers that lie strictly *outside* the `initial_bbox`.
8.  Calculate the boundaries of a new bounding box, `new_bbox`, based on the `initial_bbox` and the locations of these *external* markers:
    *   The top edge of `new_bbox` is the minimum of `initial_bbox.min_row` and `r+1` for the lowest external marker above the box (where `r` is the marker's row). If no markers are above, the top edge is `initial_bbox.min_row`.
    *   The bottom edge of `new_bbox` is the maximum of `initial_bbox.max_row` and `r-1` for the highest external marker below the box (where `r` is the marker's row). If no markers are below, the bottom edge is `initial_bbox.max_row`.
    *   The left edge of `new_bbox` is the minimum of `initial_bbox.min_col` and `c+1` for the rightmost external marker left of the box (where `c` is the marker's column). If no markers are left, the left edge is `initial_bbox.min_col`.
    *   The right edge of `new_bbox` is the maximum of `initial_bbox.max_col` and `c-1` for the leftmost external marker right of the box (where `c` is the marker's column). If no markers are right, the right edge is `initial_bbox.max_col`.
    *   Ensure all `new_bbox` coordinates are clamped within the grid's bounds (0 to height-1, 0 to width-1).
    *   Draw the perimeter (top, bottom, left, right edges) of this `new_bbox` onto the output grid using the green (3) color. This overwrites any pixels previously copied at these border locations.
9.  Iterate through the stored coordinates of *all* magenta markers (from step 2) and set the corresponding pixels in the output grid to magenta (6), overwriting any color previously present at those locations.
10. Return the completed output grid.
