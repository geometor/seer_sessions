
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 4
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 2 0 0 2
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 2 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down this task.

**Perception of the Elements:**

1.  **Grid Structure:** The inputs and outputs are grids filled primarily with white pixels (0).
2.  **Objects:** The significant objects are individual pixels of red (2) and yellow (4). There are always multiple red pixels (specifically, two in all examples) and one yellow pixel in the input.
3.  **Transformation:** The transformation involves selective removal of *either* all red pixels *or* the yellow pixel, changing them to white. The other color pixels remain unchanged.
4.  **Determining Factor:** The key is to figure out the condition that decides whether red or yellow pixels are removed. Comparing the examples:
    *   `train_1`: Two red pixels and one yellow pixel, all in the same row. Yellow is removed.
    *   `train_2`: Two red pixels and one yellow pixel, all in the same column. Red pixels are removed.
    *   `train_3`: Two red pixels and one yellow pixel, all aligned diagonally (`r-c` is constant). Red pixels are removed.
    *   `train_4`: Two red pixels and one yellow pixel, not aligned by row, column, or diagonal. Yellow is removed.
5.  **Hypothesis:** The decision seems based on the geometric alignment of *all* the red and yellow pixels combined.
    *   If all colored pixels are in the same row, remove yellow.
    *   If all colored pixels are in the same column, remove red.
    *   If all colored pixels are on the same diagonal, remove red.
    *   Otherwise (no specific alignment), remove yellow.

**YAML Fact Document:**


```yaml
task_description: "Selectively remove either all red (2) or all yellow (4) pixels based on the geometric alignment of all colored pixels."

elements:
  - element: "grid"
    description: "A 2D array of pixels with integer values 0-9 representing colors."
  - element: "pixel"
    description: "A single cell within the grid."
    properties:
      - color: "Integer 0-9 (0=white, 2=red, 4=yellow observed)"
      - position: "(row, column) coordinates"

objects:
  - object: "red_pixels"
    description: "The set of all pixels with color 2 in the input grid."
    properties:
      - count: "Number of red pixels (observed: 2)"
      - positions: "List of (row, column) coordinates"
  - object: "yellow_pixels"
    description: "The set of all pixels with color 4 in the input grid."
    properties:
      - count: "Number of yellow pixels (observed: 1)"
      - positions: "List of (row, column) coordinates"
  - object: "combined_colored_pixels"
    description: "The union of red_pixels and yellow_pixels."
    properties:
      - positions: "List of all (row, column) coordinates of red or yellow pixels"

relationships:
  - relationship: "alignment"
    description: "Geometric collinearity or diagonality of the combined_colored_pixels."
    types:
      - "row_alignment": "All combined colored pixels share the same row index."
      - "column_alignment": "All combined colored pixels share the same column index."
      - "diagonal_alignment": "All combined colored pixels lie on a line where row+column is constant OR row-column is constant."
      - "no_alignment": "None of the above alignments hold true."

actions:
  - action: "identify_pixels"
    description: "Find the coordinates of all pixels of a specific color (red or yellow)."
  - action: "check_alignment"
    description: "Determine if the set of combined_colored_pixels exhibits row, column, or diagonal alignment."
  - action: "remove_pixels"
    description: "Change the color of a specified set of pixels (either all red or all yellow) to white (0)."
  - action: "select_removal_target"
    description: >
      Based on the alignment type, decide which color group (red or yellow) to remove.
      - If row_alignment or no_alignment: Remove yellow.
      - If column_alignment or diagonal_alignment: Remove red.

transformation_logic: "Identify red and yellow pixels. Check their combined alignment. If they are row-aligned or not aligned in any specific way, remove the yellow pixel(s). If they are column-aligned or diagonally-aligned, remove the red pixels."
```


**Natural Language Program:**

1.  Create a copy of the input grid to serve as the output grid.
2.  Identify the locations (row, column pairs) of all red pixels (color 2).
3.  Identify the locations (row, column pairs) of all yellow pixels (color 4).
4.  Combine these locations into a single list of all colored pixel locations.
5.  Examine the combined list of locations:
    a.  Check if all locations share the same row index. If YES, proceed to step 6 (remove yellow).
    b.  Check if all locations share the same column index. If YES, proceed to step 7 (remove red).
    c.  Check if `row + column` is constant for all locations OR if `row - column` is constant for all locations. If YES, proceed to step 7 (remove red).
    d.  If none of the conditions (a, b, c) are met, proceed to step 6 (remove yellow).
6.  **Remove Yellow:** Iterate through the locations identified in step 3 (yellow pixels). For each location, change the pixel color in the output grid to white (0). Stop and return the output grid.
7.  **Remove Red:** Iterate through the locations identified in step 2 (red pixels). For each location, change the pixel color in the output grid to white (0). Stop and return the output grid.
