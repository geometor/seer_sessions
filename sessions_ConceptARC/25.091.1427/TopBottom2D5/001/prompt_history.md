
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0
0 1 1 1 0 2 0 2 0 0
0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 6 0 0 0 0
0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 6 0 0 0 0
0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 7 7 7 0
0 3 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 2 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 2 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0
4 0 4 0 0 0 0 0 0 0
4 4 4 0 0 0 8 8 8 0
3 3 3 0 0 0 8 0 8 0
3 0 3 0 0 0 8 8 8 0
3 3 3 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0 0
3 0 3 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0 0
```

Okay, let's analyze the task based on the provided examples.

**Perception of Task Elements:**

1.  **Input/Output Structure:** Both input and output are grids of pixels with different colors (represented by integers 0-9). White (0) acts as the background.
2.  **Objects:** The non-white pixels form distinct, connected shapes or "objects". In each example, the input grid contains multiple objects of various colors and shapes.
3.  **Transformation:** The transformation involves selectively removing some objects from the input grid to produce the output grid. The objects that remain in the output retain their original color, shape, and position relative to the grid boundaries.
4.  **Selection Criterion:** By comparing the objects present in the input and output across the examples, a pattern emerges related to their vertical position.
    *   In `train_1`, the blue and red objects in the upper part are removed, while the magenta object in the lower part is kept.
    *   In `train_2`, the green, orange, and azure objects are removed, while the red object, which occupies the lowest rows, is kept.
    *   In `train_3`, the yellow and azure objects are removed, while the two green objects, which occupy the lowest rows, are kept.
5.  **Rule:** The rule appears to be: identify all distinct objects in the input. Find the object(s) that extend furthest down (i.e., have pixels in the row with the highest index). Keep only these lowest object(s); remove all others by changing their pixels to white. If multiple objects share the same lowest row extent, all of them are kept.

**YAML Fact Document:**


```yaml
task_description: Identify and keep only the object(s) that extend to the lowest row(s) in the grid, removing all other objects.

elements:
  - element: grid
    description: A 2D array of integers representing pixel colors.
    properties:
      - height: Integer (number of rows)
      - width: Integer (number of columns)
      - pixels: Values from 0 (white) to 9.

  - element: object
    description: A contiguous group of non-white pixels of the same color.
    properties:
      - color: Integer (1-9)
      - pixels: Set of (row, column) coordinates
      - bounding_box: (min_row, min_col, max_row, max_col)
      - lowest_row_index: The maximum row index occupied by any pixel of the object.

relationships:
  - type: spatial
    description: Objects are located at different positions within the grid. Their relative vertical position is key.

actions:
  - action: identify_objects
    description: Find all distinct connected components of non-white pixels in the input grid.
    inputs: input_grid
    outputs: list_of_objects

  - action: find_lowest_extent
    description: For each identified object, determine its lowest_row_index.
    inputs: object
    outputs: lowest_row_index

  - action: find_maximum_lowest_extent
    description: Find the maximum value among the lowest_row_indices of all objects.
    inputs: list_of_lowest_row_indices
    outputs: max_lowest_row

  - action: filter_objects
    description: Select objects whose lowest_row_index equals the max_lowest_row.
    inputs: list_of_objects, max_lowest_row
    outputs: list_of_kept_objects

  - action: generate_output
    description: Create an output grid containing only the pixels of the kept_objects, with all other pixels set to white (0).
    inputs: input_grid_dimensions, list_of_kept_objects
    outputs: output_grid
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct, connected objects composed of non-white pixels in the input grid. If no non-white objects exist, return the original grid.
3.  For each identified object, determine the row index of its lowest pixel (maximum row index).
4.  Find the overall maximum lowest row index among all objects. Let this be `max_lowest_row`.
5.  Iterate through each identified object again.
6.  If an object's lowest row index is less than `max_lowest_row`, change all pixels belonging to that object in the output grid to white (0).
7.  Return the modified output grid.
