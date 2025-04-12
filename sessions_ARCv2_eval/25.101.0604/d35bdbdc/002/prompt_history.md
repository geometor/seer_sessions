
## train_1

**input:**
```
0 0 0 0 0 0 0 3 3 3
0 0 5 5 5 5 5 3 4 3
0 5 0 0 0 0 0 3 3 3
0 5 4 4 4 0 0 0 0 0
5 0 4 2 4 0 0 6 6 6
0 5 4 4 4 0 5 6 1 6
0 5 5 5 5 5 0 6 6 6
0 0 1 1 1 0 0 0 0 0
0 0 1 3 1 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 3 3 3
0 0 5 5 5 5 5 3 2 3
0 5 0 0 0 0 0 3 3 3
0 5 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 6 6 6
0 5 0 0 0 0 5 6 3 6
0 5 5 5 5 5 0 6 6 6
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
2 2 2 0 0 0 3 3 3 0
2 6 2 0 0 0 3 2 3 0
2 2 2 0 5 0 3 3 3 0
0 0 0 5 0 5 5 5 5 0
8 8 8 0 5 0 0 1 1 1
8 3 8 0 0 5 0 1 4 1
8 8 8 0 5 0 0 1 1 1
0 5 0 5 4 4 4 0 0 0
0 5 5 0 4 8 4 0 0 0
0 0 0 0 4 4 4 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 5 0 5 5 5 5 0
8 8 8 0 5 0 0 1 1 1
8 2 8 0 0 5 0 1 8 1
8 8 8 0 5 0 0 1 1 1
0 5 0 5 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
1 1 1 0 0 0 0 4 4 4
1 2 1 0 0 0 0 4 3 4
1 1 1 0 0 5 0 4 4 4
0 5 0 0 5 0 5 0 0 0
0 5 0 5 3 3 3 5 0 0
0 0 5 0 3 6 3 0 5 0
0 0 0 0 3 3 3 0 5 0
2 2 2 0 0 0 0 7 7 7
2 9 2 0 0 0 0 7 4 7
2 2 2 0 0 0 0 7 7 7
```


**output:**
```
1 1 1 0 0 0 0 0 0 0
1 9 1 0 0 0 0 0 0 0
1 1 1 0 0 5 0 0 0 0
0 5 0 0 5 0 5 0 0 0
0 5 0 5 0 0 0 5 0 0
0 0 5 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 7 3 7
0 0 0 0 0 0 0 7 7 7
```

Okay, let's break down the transformation logic for this task.

**Perception of Elements:**

1.  **Grid Structure:** The input and output are 2D grids of digits (0-9). The digit 0 typically represents a background color.
2.  **Objects:** The non-zero digits form various shapes or objects. A recurring pattern is a 3x3 square where the 8 border cells share one non-zero color (the "frame") and the center cell contains a different non-zero color (the "interior" or "center"). Other non-zero shapes also exist, sometimes connected, sometimes isolated.
3.  **Transformation Focus:** The core transformation appears to target these specific "3x3 framed objects". Other shapes and background cells seem unaffected *unless* they are part of a targeted 3x3 framed object that gets removed.
4.  **Conditional Logic:** Whether a framed object is modified or removed depends entirely on the specific pair of colors: the frame color (C1) and the center color (C2).
5.  **Modification vs. Removal:**
    *   Some (C1, C2) pairs cause the center cell C2 to change to a new color C3, while the frame C1 remains untouched.
    *   Other (C1, C2) pairs cause the *entire* 3x3 object (frame and center) to be removed (replaced with the background color 0).

**YAML Facts:**

```yaml
task_description: Modify or remove specific 3x3 patterns within a grid based on the colors of the frame and center.

definitions:
  - object: Framed Object
    properties:
      - structure: A 3x3 area in the grid.
      - frame_color: The single non-zero color (C1) occupying all 8 border cells of the 3x3 area.
      - center_color: The non-zero color (C2) in the center cell of the 3x3 area.
      - condition: Frame color (C1) must be different from center color (C2). Both C1 and C2 must be non-zero.
  - background_color: 0

actions:
  - name: Identify Framed Objects
    description: Scan the grid to find all instances matching the 'Framed Object' definition.
  - name: Classify Framed Objects
    description: Based on the specific pair of (frame_color C1, center_color C2), classify the object for modification or removal.
    rules:
      - category: Keep and Modify Center
        pairs: # (C1, C2) -> New C2
          - [3, 4, 2] # Frame=3, Center=4 -> New Center=2
          - [6, 1, 3] # Frame=6, Center=1 -> New Center=3
          - [8, 3, 2] # Frame=8, Center=3 -> New Center=2
          - [1, 4, 8] # Frame=1, Center=4 -> New Center=8
          - [1, 2, 9] # Frame=1, Center=2 -> New Center=9
          - [7, 4, 3] # Frame=7, Center=4 -> New Center=3
      - category: Remove Object
        pairs: # (C1, C2)
          - [1, 3]
          - [2, 6]
          - [3, 2]
          - [4, 8]
          - [4, 3]
          - [3, 6]
          - [2, 9]
  - name: Apply Transformations
    description: Create the output grid by applying the classified actions.
    steps:
      - Copy the input grid to the output grid.
      - For 'Keep and Modify Center' objects, update the center cell in the output grid with the new color.
      - For 'Remove Object' objects, set all 9 cells (frame and center) of the object in the output grid to the background color (0).
    precedence: Removals potentially override modifications if a modified center cell is part of a removed frame.

relationships:
  - The fate of a framed object (modification or removal) is determined solely by the combination of its frame color and its center color.
  - Cells not part of any identified framed object remain unchanged in the output.
```

**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Create a list to store coordinates and new values for modifications (`modifications`).
3.  Create a set to store coordinates of cells to be removed (`removals`).
4.  Iterate through each cell `(r, c)` of the input grid that could be the center of a 3x3 object (i.e., where `1 <= r < height-1` and `1 <= c < width-1`).
5.  For each potential center `(r, c)`:
    a.  Check if all 8 neighboring cells have the same non-zero color, `C1`.
    b.  Check if the center cell `(r, c)` has a non-zero color, `C2`, such that `C1 != C2`.
    c.  If both conditions (a) and (b) are true, a "Framed Object" is found with frame `C1` and center `C2`.
    d.  Check the pair `(C1, C2)`:
        i.  If `(C1, C2)` is one of `(3,4)`, `(6,1)`, `(8,3)`, `(1,4)`, `(1,2)`, or `(7,4)`, determine the corresponding new center color (`2`, `3`, `2`, `8`, `9`, or `3` respectively) and add the modification `(r, c, new_color)` to the `modifications` list.
        ii. If `(C1, C2)` is one of `(1,3)`, `(2,6)`, `(3,2)`, `(4,8)`, `(4,3)`, `(3,6)`, or `(2,9)`, add the coordinates of all 9 cells of the 3x3 object (center `(r, c)` and its 8 neighbors) to the `removals` set.
6.  Apply the removals: Iterate through all coordinates `(rr, cc)` in the `removals` set and set the corresponding cell in the output grid to `0`.
7.  Apply the modifications: Iterate through each modification `(r, c, new_color)` in the `modifications` list. If the coordinate `(r, c)` is *not* present in the `removals` set, update the cell `(r, c)` in the output grid to `new_color`.
8.  Return the final output grid.
```python
import copy

"""
The transformation identifies specific 3x3 patterns ("Framed Objects") in the input grid.
A Framed Object consists of a non-zero center cell (color C2) surrounded by 8 cells of the same, different, non-zero color (C1).
Based on the specific pair of (C1, C2), the object is either:
1. Modified: The center cell C2 is changed to a new color C3, while the frame C1 remains.
2. Removed: The entire 3x3 object (frame C1 and center C2) is replaced with the background color 0.
Cells not part of any identified Framed Object remain unchanged. Removals take precedence over modifications if coordinates overlap (though this specific rule set doesn't seem to create overlaps between removed frames and modified centers).

Modification Rules (Frame C1, Center C2) -> New Center C3:
- (3, 4) -> 2
- (6, 1) -> 3
- (8, 3) -> 2
- (1, 4) -> 8
- (1, 2) -> 9
- (7, 4) -> 3

Removal Rules (Frame C1, Center C2):
- (1, 3)
- (2, 6)
- (3, 2)
- (4, 8)
- (4, 3)
- (3, 6)
- (2, 9)
"""

# Define the modification and removal rules based on (frame_color, center_color) pairs
MODIFICATION_RULES = {
    (3, 4): 2,
    (6, 1): 3,
    (8, 3): 2,
    (1, 4): 8,
    (1, 2): 9,
    (7, 4): 3,
}

REMOVAL_RULES = {
    (1, 3),
    (2, 6),
    (3, 2),
    (4, 8),
    (4, 3),
    (3, 6),
    (2, 9),
}

def _is_framed_object(grid: list[list[int]], r: int, c: int) -> tuple[bool, int | None, int | None]:
    """
    Checks if the cell at (r, c) is the center of a valid Framed Object.
    A Framed Object has a non-zero center (C2) and 8 surrounding cells
    of the same, different, non-zero color (C1).

    Returns:
        tuple[bool, int | None, int | None]: (is_object, frame_color, center_color)
    """
    height = len(grid)
    width = len(grid[0])

    # Center must be within bounds allowing for a 3x3 neighborhood
    if not (0 < r < height - 1 and 0 < c < width - 1):
        return False, None, None

    center_color = grid[r][c]
    # Center color must be non-zero
    if center_color == 0:
        return False, None, None

    frame_color = -1 # Use -1 to indicate frame color not yet determined

    # Check the 8 neighbors
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the center cell itself
            if dr == 0 and dc == 0:
                continue

            nr, nc = r + dr, c + dc
            neighbor_color = grid[nr][nc]

            # Frame cells must be non-zero
            if neighbor_color == 0:
                return False, None, None

            # Initialize frame_color with the first neighbor's color
            if frame_color == -1:
                frame_color = neighbor_color
            # Check if subsequent neighbors match the established frame_color
            elif neighbor_color != frame_color:
                return False, None, None

    # After checking all neighbors:
    # Ensure a valid frame color was found (should be non-zero and consistent)
    if frame_color == -1 or frame_color == 0:
         return False, None, None # Should not happen if neighbors loop worked, but defensive

    # Frame color must be different from center color
    if frame_color == center_color:
        return False, None, None

    # If all checks pass, it's a valid framed object
    return True, frame_color, center_color


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies transformations to a grid based on identifying and processing
    specific 3x3 "Framed Objects".
    """
    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    height = len(input_grid)
    width = len(input_grid[0])

    # Store planned modifications and removals to apply them correctly later
    modifications_to_apply = [] # List of tuples: (r, c, new_color)
    coords_to_remove = set()    # Set of tuples: (r, c) for cells to be set to 0

    # Iterate through potential center cells of 3x3 objects
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            # Check if the current cell is the center of a framed object
            is_object, frame_color, center_color = _is_framed_object(input_grid, r, c)

            if is_object:
                # We have found a valid framed object with frame C1 and center C2
                rule_key = (frame_color, center_color)

                # Check if this object type should be removed
                if rule_key in REMOVAL_RULES:
                    # Add all 9 coordinates of the 3x3 object to the removal set
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            coords_to_remove.add((r + dr, c + dc))
                # Check if this object type's center should be modified
                elif rule_key in MODIFICATION_RULES:
                    new_center_color = MODIFICATION_RULES[rule_key]
                    # Add the modification instruction
                    modifications_to_apply.append((r, c, new_center_color))

    # Apply removals first
    for rr, cc in coords_to_remove:
        # Check bounds just in case, though logic should ensure they are valid
        if 0 <= rr < height and 0 <= cc < width:
             output_grid[rr][cc] = 0

    # Apply modifications, ensuring the cell wasn't part of a removed object
    for r_mod, c_mod, new_color in modifications_to_apply:
        if (r_mod, c_mod) not in coords_to_remove:
            # Check bounds just in case
             if 0 <= r_mod < height and 0 <= c_mod < width:
                output_grid[r_mod][c_mod] = new_color

    return output_grid
```
