
## train_1

**input:**
```
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 9 9 6 6 6 6
6 6 6 6 6 6 9 9 6 6 6 6
6 6 6 6 0 0 6 6 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 0 0 6 6 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 0 0 6 6 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 7 7 6 6 6 6
6 6 6 6 6 6 7 7 6 6 6 6
```


**output:**
```
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 7 7 6 6 6 6
6 6 6 6 6 6 7 7 6 6 6 6
6 6 6 6 0 0 2 2 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 0 0 2 2 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 0 0 2 2 0 0 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6
```


## train_2

**input:**
```
6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6
6 6 6 0 6 0 6 6
6 6 6 0 6 0 6 6
6 7 6 6 6 6 6 9
6 6 6 0 6 0 6 6
6 6 6 0 6 0 6 6
6 6 6 6 6 6 6 6
```


**output:**
```
6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6
6 6 6 0 6 0 6 6
6 6 6 0 6 0 6 6
6 6 6 2 6 2 6 7
6 6 6 0 6 0 6 6
6 6 6 0 6 0 6 6
6 6 6 6 6 6 6 6
```


## train_3

**input:**
```
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 6 6 6 9 9 6 6 6 6 6 6 7 7 6 6
6 6 6 6 9 9 6 6 6 6 6 6 7 7 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
```


**output:**
```
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 6 6 6 7 7 6 2 6 6 2 6 6 6 6 6
6 6 6 6 7 7 6 2 6 6 2 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 0 6 0 6 0 6 0 6 6 0 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
```

Okay, let's analyze the provided examples for this task.

**Perception of Elements:**

1.  **Colors:** The primary colors involved are Magenta (6) as the background, Maroon (9), Orange (7), White (0), and Red (2). Red only appears in the output.
2.  **Objects:**
    *   There is always exactly one Maroon (9) object and one Orange (7) object in the input. These objects can be single pixels or small rectangles.
    *   There are White (0) objects, often appearing as pairs of identical blocks/pixels, either horizontally or vertically aligned with each other.
    *   The Magenta (6) color forms the background.
3.  **Transformation:**
    *   The Magenta background remains unchanged.
    *   The Maroon (9) object disappears.
    *   The Orange (7) object moves to occupy the exact location previously held by the Maroon (9) object.
    *   Red (2) pixels appear in the output. Their placement seems dependent on the relative positions of the Maroon, Orange, and White objects.
4.  **Spatial Relationships:** The relative alignment (horizontal vs. vertical) of the Maroon and Orange objects appears crucial. The placement of White objects, particularly when they form pairs on the same row(s), also influences the output, specifically the location of the Red pixels.

**Analysis of Alignment and Red Pixel Placement:**

*   **Horizontal Alignment (train_2, train_3):** When the Maroon and Orange objects are on the same row(s), the Red pixels replace any White pixels found *between* the column span of the Maroon object and the column span of the Orange object, but *only* on the shared row(s).
*   **Vertical Alignment (train_1):** When the Maroon and Orange objects are in the same column(s), the Red pixels appear on rows that contain pairs of horizontally separated White blocks. Specifically, Red pixels appear in two columns on these rows: the column corresponding to the right edge of the Maroon/Orange objects and the column corresponding to the left edge of the *rightmost* White block on that row. These Red pixels replace the background Magenta pixels.

**YAML Facts:**


```yaml
task_description: Replace a Maroon object with an Orange object and add Red pixels based on alignment and White pixel locations.
background_color: Magenta (6)
objects:
  - type: Maroon_Object
    color: 9
    count: 1
    input_action: Removed
  - type: Orange_Object
    color: 7
    count: 1
    input_action: Relocated
    output_action: Replaces Maroon_Object location
  - type: White_Object
    color: 0
    count: variable
    input_action: Some are potentially replaced by Red (horizontal case), others trigger Red placement (vertical case)
    output_action: Some remain, some replaced by Red (horizontal case)
  - type: Red_Pixel
    color: 2
    count: variable
    input_action: None (does not exist in input)
    output_action: Created based on rules
relationships:
  - type: Alignment
    between: [Maroon_Object, Orange_Object]
    values: [Horizontal, Vertical]
    effect: Determines the rule for placing Red_Pixels
  - type: Position
    of: White_Objects
    relative_to: [Maroon_Object, Orange_Object]
    effect: Influences Red_Pixel placement (location or replacement)
```


**Natural Language Program:**

1.  Identify the unique Maroon (9) object and the unique Orange (7) object in the input grid.
2.  Determine if the Maroon and Orange objects share common rows (Horizontal Alignment) or common columns (Vertical Alignment).
3.  Create the output grid by copying the input grid.
4.  Modify the output grid by replacing the pixels originally occupied by the Maroon object with the Orange (7) color.
5.  **If Horizontal Alignment:**
    a.  Find the row(s) shared by the Maroon and Orange objects.
    b.  Determine the minimum and maximum column indices spanned by the Maroon and Orange objects combined.
    c.  For each shared row, iterate through the columns strictly *between* the minimum and maximum column indices.
    d.  If the pixel at a given `(row, column)` position in the *input* grid is White (0), change the corresponding pixel in the *output* grid to Red (2).
6.  **If Vertical Alignment:**
    a.  Find the column(s) shared by the Maroon and Orange objects. Determine the rightmost shared column index (`maroon_orange_right_col`).
    b.  Identify all rows in the input grid that contain at least two distinct, horizontally separated White (0) objects (these are `target_rows`).
    c.  For each `target_row`:
        i.  Find the rightmost White (0) object on that row. Determine the column index of its leftmost edge (`right_white_left_col`).
        ii. Change the pixels in the *output* grid at coordinates `(target_row, maroon_orange_right_col)` and `(target_row, right_white_left_col)` to Red (2), overwriting the existing background color (Magenta 6).
7.  Return the modified output grid.
```python
import numpy as np
from typing import List, Tuple, Dict, Set

# Color mapping for clarity (optional, but helpful)
COLOR_MAP = {
    0: "white", 1: "blue", 2: "red", 3: "green", 4: "yellow",
    5: "gray", 6: "magenta", 7: "orange", 8: "azure", 9: "maroon",
}
MAGENTA = 6
MAROON = 9
ORANGE = 7
WHITE = 0
RED = 2

def find_colored_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates of pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def get_bounding_box(coords: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """Calculates the min_row, max_row, min_col, max_col for a set of coordinates."""
    if not coords:
        return -1, -1, -1, -1 # Indicate no object found
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    return min(rows), max(rows), min(cols), max(cols)

def find_white_segments_on_row(row_slice: np.ndarray) -> List[Tuple[int, int]]:
    """Finds contiguous segments of White (0) on a single row slice.
       Returns a list of (start_col, end_col) tuples for each segment.
    """
    segments = []
    in_segment = False
    start_col = -1
    for c, color in enumerate(row_slice):
        if color == WHITE and not in_segment:
            in_segment = True
            start_col = c
        elif color != WHITE and in_segment:
            in_segment = False
            segments.append((start_col, c - 1))
    # Handle segment ending at the edge
    if in_segment:
        segments.append((start_col, len(row_slice) - 1))
    return segments

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid based on the following rules:
    1. Identify the unique Maroon (9) and Orange (7) objects.
    2. Determine if they are primarily horizontally or vertically aligned based on overlapping rows or columns.
    3. Create the output grid by copying the input.
    4. Replace the Maroon object's location with Orange.
    5. If Horizontally aligned:
       - On the shared row(s), replace White (0) pixels located strictly between the column spans of the two objects with Red (2).
    6. If Vertically aligned:
       - Identify rows containing at least two distinct horizontal segments of White (0).
       - For each such row, find the rightmost White segment.
       - Place Red (2) pixels at two locations on that row in the output:
         - One in the rightmost column shared by the original Maroon/Orange objects.
         - One in the leftmost column of the rightmost White segment found on that row.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # --- Find Objects and Bounds ---
    maroon_coords = find_colored_pixels(input_grid, MAROON)
    orange_coords = find_colored_pixels(input_grid, ORANGE)

    if not maroon_coords or not orange_coords:
        # Should not happen based on examples, but handle defensively
        return output_grid 

    maroon_min_r, maroon_max_r, maroon_min_c, maroon_max_c = get_bounding_box(maroon_coords)
    orange_min_r, orange_max_r, orange_min_c, orange_max_c = get_bounding_box(orange_coords)

    # --- Determine Alignment ---
    rows_overlap = max(maroon_min_r, orange_min_r) <= min(maroon_max_r, orange_max_r)
    cols_overlap = max(maroon_min_c, orange_min_c) <= min(orange_max_c, orange_max_c)

    is_horizontal_alignment = False
    is_vertical_alignment = False

    # Prioritize horizontal if both overlap (e.g., single pixel objects on same row/col)
    # Or if only rows overlap significantly
    if rows_overlap and not cols_overlap:
         is_horizontal_alignment = True
    elif cols_overlap and not rows_overlap:
         is_vertical_alignment = True
    elif rows_overlap and cols_overlap:
         # If bounds perfectly overlap, could be either. Check relative position.
         # If they share rows but not columns -> horizontal
         # If they share columns but not rows -> vertical
         # If they share both rows and columns (contained or identical position) - Treat as Horizontal seems safer based on train_3 edge case where they touch.
         # Let's refine: if number of shared rows > number of shared columns -> likely Horizontal
         # Let's use the simple overlap for now, seems sufficient for examples
         # Check if center points indicate alignment better?
         maroon_center_r = (maroon_min_r + maroon_max_r) / 2
         maroon_center_c = (maroon_min_c + maroon_max_c) / 2
         orange_center_r = (orange_min_r + orange_max_r) / 2
         orange_center_c = (orange_min_c + orange_max_c) / 2
         
         # If centers are much closer horizontally than vertically
         if abs(maroon_center_r - orange_center_r) <= abs(maroon_center_c - orange_center_c) :
             # More aligned vertically or equally, but let's check row span first
             if maroon_min_r == orange_min_r and maroon_max_r == orange_max_r:
                 is_horizontal_alignment = True # Same row(s) -> horizontal
             else: # Different rows but same cols
                 is_vertical_alignment = True
         else: # More aligned horizontally
             if maroon_min_c == orange_min_c and maroon_max_c == orange_max_c:
                 is_vertical_alignment = True # Same col(s) -> vertical
             else:
                is_horizontal_alignment = True

    # Fallback if no clear alignment from overlap (shouldn't occur with 1 obj each)
    if not is_horizontal_alignment and not is_vertical_alignment:
         # Default to horizontal if unsure, or handle error
         # Based on examples, one must be true.
         # Let's re-evaluate based purely on shared rows/cols
         if rows_overlap:
             is_horizontal_alignment = True # Train 2 & 3
         elif cols_overlap:
             is_vertical_alignment = True # Train 1


    # --- Perform Base Transformation (Move Orange to Maroon position) ---
    # Clear original Maroon location in output
    for r, c in maroon_coords:
        output_grid[r, c] = MAGENTA # Assuming magenta is background

    # Place Orange color at Maroon's original location
    for r, c in maroon_coords:
        output_grid[r, c] = ORANGE


    # --- Apply Alignment-Specific Rules ---
    if is_horizontal_alignment:
        # Find shared rows
        shared_rows = range(max(maroon_min_r, orange_min_r), min(maroon_max_r, orange_max_r) + 1)
        
        # Find column span between the objects
        obj1_min_c, obj1_max_c = maroon_min_c, maroon_max_c
        obj2_min_c, obj2_max_c = orange_min_c, orange_max_c

        start_col = min(obj1_max_c, obj2_max_c) + 1
        end_col = max(obj1_min_c, obj2_min_c) # Exclusive end

        # Ensure start_col is actually less than end_col
        if start_col < end_col:
             for r in shared_rows:
                 for c in range(start_col, end_col):
                      # Check original input grid for white
                      if input_grid[r, c] == WHITE:
                          output_grid[r, c] = RED

    elif is_vertical_alignment:
        # Find shared columns and the rightmost one
        shared_cols = range(max(maroon_min_c, orange_min_c), min(maroon_max_c, orange_max_c) + 1)
        if not shared_cols: # Should have overlap if vertical alignment detected
            return output_grid # Error or unexpected case
            
        rightmost_shared_col = max(shared_cols)

        # Iterate through rows to find those with >= 2 white segments
        for r in range(height):
            row_slice = input_grid[r, :]
            white_segments = find_white_segments_on_row(row_slice)

            if len(white_segments) >= 2:
                # Find the rightmost white segment (max start col)
                rightmost_segment = max(white_segments, key=lambda seg: seg[0])
                right_white_left_col = rightmost_segment[0] # Leftmost column of the rightmost segment

                # Place Red pixels
                # Check bounds before writing
                if 0 <= r < height and 0 <= rightmost_shared_col < width:
                     output_grid[r, rightmost_shared_col] = RED
                if 0 <= r < height and 0 <= right_white_left_col < width:
                     output_grid[r, right_white_left_col] = RED

    return output_grid

```
```python
import numpy as np
from typing import List, Tuple, Set
from skimage.measure import label

# Define color constants
MAGENTA = 6
MAROON = 9
ORANGE = 7
WHITE = 0
RED = 2

def find_colored_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates (row, col) of pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def get_bounding_box(coords: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """Calculates the min_row, max_row, min_col, max_col for a set of coordinates."""
    if not coords:
        # Return invalid box if no coordinates
        return -1, -1, -1, -1 
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    return min(rows), max(rows), min(cols), max(cols)

def find_objects(grid: np.ndarray, color: int) -> List[List[Tuple[int, int]]]:
    """Finds connected components of a specified color.
       Uses 4-way connectivity. Returns a list of objects, where each object
       is a list of its (row, col) coordinates.
    """
    binary_grid = (grid == color)
    # connectivity=1 means 4-way adjacency (von Neumann neighborhood)
    labeled_grid, num_labels = label(binary_grid, connectivity=1, background=0, return_num=True) 
    objects = []
    for label_id in range(1, num_labels + 1):
        coords = list(zip(*np.where(labeled_grid == label_id)))
        if coords:
            objects.append(coords)
    return objects

def find_white_segments_on_row(row_slice: np.ndarray) -> List[Tuple[int, int]]:
    """Finds contiguous segments of White (0) on a single row slice.
       Returns a list of (start_col, end_col) tuples for each segment.
    """
    segments = []
    in_segment = False
    start_col = -1
    width = len(row_slice)
    for c, color in enumerate(row_slice):
        if color == WHITE and not in_segment:
            in_segment = True
            start_col = c
        elif color != WHITE and in_segment:
            in_segment = False
            segments.append((start_col, c - 1))
    # Handle segment ending at the edge
    if in_segment:
        segments.append((start_col, width - 1))
    return segments

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid according to the following rules:
    1. Identifies the unique Maroon (9) and Orange (7) objects and their coordinates.
    2. Creates an output grid initialized with the background color (Magenta 6), 
       copying non-Maroon/Orange elements from the input.
    3. Places the Orange (7) color in the output grid at the original location of the Maroon object.
    4. Determines if the Maroon and Orange objects were primarily horizontally or vertically aligned
       based on overlap of their bounding boxes in the input grid.
    5. If Horizontally aligned:
       a. Finds the row(s) shared by the bounding boxes.
       b. Defines a column range strictly between the Maroon and Orange objects.
       c. Identifies all White (0) objects from the input grid that lie entirely within this 'between' column range.
       d. Collects the column indices occupied by these White objects.
       e. Places Red (2) pixels in the output grid on the shared row(s) at the collected column indices.
    6. If Vertically aligned:
       a. Finds the column(s) shared by the bounding boxes and identifies the leftmost shared column.
       b. Identifies rows in the input grid containing at least two distinct horizontal segments of White (0).
       c. For each such row, finds the leftmost column of the rightmost White segment.
       d. Places Red (2) pixels in the output grid at two locations on that row:
          - One in the leftmost column shared by the original Maroon/Orange objects.
          - One in the column immediately to the left of the rightmost White segment's start.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # --- Find Objects and Coordinates ---
    maroon_coords = find_colored_pixels(input_grid, MAROON)
    orange_coords = find_colored_pixels(input_grid, ORANGE)

    # Handle cases where one or both objects might be missing (though not expected per examples)
    if not maroon_coords or not orange_coords:
        return output_grid 

    # --- Perform Base Transformation ---
    # Clear original Maroon location in output grid (set to background)
    for r, c in maroon_coords:
        output_grid[r, c] = MAGENTA 

    # Clear original Orange location in output grid (set to background)
    for r, c in orange_coords:
         if output_grid[r, c] == ORANGE: # Avoid clearing if it overlaps with where maroon was
             output_grid[r, c] = MAGENTA

    # Place Orange color at Maroon's original location
    for r, c in maroon_coords:
        output_grid[r, c] = ORANGE

    # --- Get Bounding Boxes for Alignment Check ---
    maroon_min_r, maroon_max_r, maroon_min_c, maroon_max_c = get_bounding_box(maroon_coords)
    orange_min_r, orange_max_r, orange_min_c, orange_max_c = get_bounding_box(orange_coords)

    # --- Determine Alignment ---
    rows_overlap = max(maroon_min_r, orange_min_r) <= min(maroon_max_r, orange_max_r)
    cols_overlap = max(maroon_min_c, orange_min_c) <= min(maroon_max_c, orange_max_c)

    is_horizontal_alignment = False
    is_vertical_alignment = False

    # Determine alignment based on shared rows/columns
    # Prioritize horizontal if rows are identical, vertical if columns are identical
    if maroon_min_r == orange_min_r and maroon_max_r == orange_max_r:
        is_horizontal_alignment = True
    elif maroon_min_c == orange_min_c and maroon_max_c == orange_max_c:
        is_vertical_alignment = True
    # Fallback based on simple overlap (covers cases where one dim overlaps but not identical spans)
    elif rows_overlap and not cols_overlap:
        is_horizontal_alignment = True
    elif cols_overlap and not rows_overlap:
        is_vertical_alignment = True
    # If both overlap but aren't identical spans, default to horizontal (matches example 3 logic implicitly)
    elif rows_overlap and cols_overlap:
         is_horizontal_alignment = True # Default preference or could add more complex logic

    # --- Apply Alignment-Specific Red Pixel Rules ---
    if is_horizontal_alignment:
        # Find shared rows using bounding boxes
        shared_rows = list(range(max(maroon_min_r, orange_min_r), min(maroon_max_r, orange_max_r) + 1))
        
        # Define the column range strictly *between* the objects
        between_start_col = min(maroon_max_c, orange_max_c) + 1
        between_end_col = max(maroon_min_c, orange_min_c) # Exclusive end

        target_cols = set()
        if between_start_col < between_end_col: # Check if there is actually space between
            # Find all white objects in the input
            white_objects = find_objects(input_grid, WHITE)
            
            # Filter for white objects completely within the 'between' columns
            for obj_coords in white_objects:
                w_min_r, w_max_r, w_min_c, w_max_c = get_bounding_box(obj_coords)
                if w_min_c >= between_start_col and w_max_c < between_end_col:
                    # Collect the columns occupied by these objects
                    for r_w, c_w in obj_coords:
                        target_cols.add(c_w)

        # Place Red pixels on shared rows in the target columns
        for r in shared_rows:
            for c in target_cols:
                # Check bounds just in case, though target_cols should be valid
                if 0 <= r < height and 0 <= c < width:
                    output_grid[r, c] = RED

    elif is_vertical_alignment:
        # Find shared columns and the leftmost one
        shared_cols = list(range(max(maroon_min_c, orange_min_c), min(maroon_max_c, orange_max_c) + 1))
        if not shared_cols: 
             # This case indicates alignment detection might be flawed, but proceed assuming vertical
             leftmost_shared_col = min(maroon_min_c, orange_min_c) # Best guess
        else:
             leftmost_shared_col = min(shared_cols)


        # Iterate through rows to find those with >= 2 white segments
        for r in range(height):
            row_slice = input_grid[r, :]
            white_segments = find_white_segments_on_row(row_slice)

            if len(white_segments) >= 2:
                # Find the rightmost white segment (one with the largest start column)
                rightmost_segment = max(white_segments, key=lambda seg: seg[0])
                right_white_left_col = rightmost_segment[0] # Leftmost column of the rightmost segment
                col_left_of_right_white = right_white_left_col - 1

                # Place Red pixel at leftmost shared column
                if 0 <= r < height and 0 <= leftmost_shared_col < width:
                     output_grid[r, leftmost_shared_col] = RED
                     
                # Place Red pixel at column left of the rightmost white segment start
                if 0 <= r < height and 0 <= col_left_of_right_white < width:
                     output_grid[r, col_left_of_right_white] = RED

    return output_grid
```
