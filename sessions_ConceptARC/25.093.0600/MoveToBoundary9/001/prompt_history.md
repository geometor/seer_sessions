
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 1 1 1 0 0
0 0 2 2 2 0 1 1 1 0 0
0 0 2 2 2 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 1 1 1
2 2 2 0 0 0 0 0 1 1 1
2 2 2 0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 3 0 0 0 4 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 4 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 3 0 0 0 4 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 3 0 3 0 0 0 0 0 0 0 0 0 4 0 4 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 3 0 0 0 0 0 0 0 0 0 4 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 3 0 3 0 0 0 0 0 0 0 0 0 4 0 4 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the transformation.

**Perception:**

The input consists of a grid containing a background of zeros and two distinct groups of non-zero numbers. Each group uses a unique number (e.g., all 2s form one group, all 1s form another in the first example; all 3s form one group, all 4s form another in the second).

The transformation involves moving these two groups horizontally. The group initially positioned further to the left in the input grid is moved so that its leftmost element aligns with the first column (column 0) of the output grid. The group initially positioned further to the right is moved so that its rightmost element aligns with the last column of the output grid.

The internal structure and relative positions of the numbers within each group are preserved. The vertical positions (rows) of all numbers also remain unchanged. The cells that were originally zero remain zero unless overwritten by a moved number.

**YAML Facts:**


```yaml
task_description: "Horizontally shift two distinct non-zero groups to opposite edges of the grid."
elements:
  - element: grid
    description: "A 2D array of integers."
  - element: background
    type: integer
    value: 0
    description: "The default value for grid cells."
  - element: object
    description: "A collection of grid cells sharing the same non-zero integer value."
    properties:
      - value: "The non-zero integer defining the object."
      - coordinates: "A list of (row, column) pairs for cells belonging to the object."
      - horizontal_position: "Determined by the column indices of its coordinates."
      - extent: "Defined by the minimum and maximum row and column indices."
relationships:
  - relationship: "Spatial separation"
    between: [object, object]
    description: "The two non-zero objects are spatially distinct in the input grid, particularly horizontally."
  - relationship: "Left/Right ordering"
    between: [object, object]
    description: "One object can be identified as being 'to the left' of the other based on their minimum column indices."
actions:
  - action: identify_objects
    input: grid
    output: [object1, object2]
    description: "Find all unique non-zero values and group cell coordinates by these values."
  - action: determine_order
    input: [object1, object2]
    output: [left_object, right_object]
    description: "Compare the minimum column indices of the objects to determine which is left and which is right."
  - action: calculate_shifts
    input: [left_object, right_object, grid_width]
    output: [shift_left, shift_right]
    description: >
      Calculate the horizontal shift needed for the left object to align its leftmost point with column 0.
      Calculate the horizontal shift needed for the right object to align its rightmost point with the last column (grid_width - 1).
  - action: apply_shifts
    input: [left_object, right_object, shift_left, shift_right, grid_dimensions]
    output: output_grid
    description: >
      Create a new zero-filled grid.
      Place the cells of the left_object at their original rows and shifted columns (column + shift_left).
      Place the cells of the right_object at their original rows and shifted columns (column + shift_right).
```


**Natural Language Program:**

1.  Initialize an empty output grid with the same dimensions as the input grid, filled with zeros.
2.  Identify the two distinct non-zero values present in the input grid.
3.  For each distinct non-zero value, collect the list of (row, column) coordinates where it appears. These two collections represent the two objects.
4.  Determine which object is the "left object" and which is the "right object" by comparing the minimum column index found within each object's coordinates. The object with the smaller minimum column index is the left object.
5.  Calculate the shift amount for the left object: Find the minimum column index among all coordinates of the left object (`min_col_left`). The required shift is `0 - min_col_left`.
6.  Calculate the shift amount for the right object: Find the maximum column index among all coordinates of the right object (`max_col_right`). Let the width of the grid be `W`. The required shift is `(W - 1) - max_col_right`.
7.  Iterate through the coordinates `(r, c)` of the left object. For each coordinate, set the value in the output grid at `(r, c + shift_left)` to the value of the left object.
8.  Iterate through the coordinates `(r, c)` of the right object. For each coordinate, set the value in the output grid at `(r, c + shift_right)` to the value of the right object.
9.  Return the completed output grid.
