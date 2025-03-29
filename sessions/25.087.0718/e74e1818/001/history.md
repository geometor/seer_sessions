
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 0 0 0
0 0 0 0 2 0 2 0 2 0 0 0 0
0 0 0 0 0 2 0 2 0 0 0 0 0
0 0 0 3 0 0 3 0 0 3 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0 0
0 0 0 0 1 1 1 1 1 0 0 0 0
0 0 0 0 1 0 0 0 1 0 0 0 0
0 0 0 0 1 1 1 1 1 0 0 0 0
0 0 0 0 4 4 0 4 4 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 2 0 0 0 0 0
0 0 0 0 2 0 2 0 2 0 0 0 0
0 0 0 2 2 2 2 2 2 2 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0 0
0 0 0 3 0 0 3 0 0 3 0 0 0
0 0 0 0 1 1 1 1 1 0 0 0 0
0 0 0 0 1 0 0 0 1 0 0 0 0
0 0 0 0 1 1 1 1 1 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 4 4 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 0 0
0 0 0 1 1 0 1 1 0 0 0
0 0 0 8 8 8 8 8 0 0 0
0 0 0 5 0 5 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 5 5 5 5 0 0 0
0 0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0
0 0 0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 0 1 1 0 0 0
0 0 1 1 1 1 1 1 1 0 0
0 0 0 8 8 8 8 8 0 0 0
0 0 0 5 5 5 5 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 5 0 5 0 0 0
0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0
0 0 0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0
0 0 9 9 9 0 0
0 9 0 9 0 9 0
0 0 4 4 4 0 0
0 3 3 3 3 3 0
0 0 0 3 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0
0 9 0 9 0 9 0
0 0 9 9 9 0 0
0 0 4 4 4 0 0
0 0 0 3 0 0 0
0 3 3 3 3 3 0
0 0 0 0 0 0 0
```

Okay, let's break down this ARC task.

**Perception of Task Elements:**

1.  **Input/Output Structure:** Both input and output are grids of pixels represented by numbers 0-9 (colors). The background is consistently white (0).
2.  **Objects:** The non-white pixels form distinct connected components or "objects" of various shapes and colors. In the examples, we see shapes resembling letters ('H', 'U', 'T') and simple rectangles. Each object has a single color.
3.  **Transformation:** The core transformation appears to involve manipulating the rows associated with each object. Comparing inputs and outputs, the vertical order of the rows that contain parts of an object seems to be reversed.
4.  **Object Integrity:** The shapes of the objects themselves are not altered (no rotation, scaling, or color change), only the vertical arrangement of their constituent horizontal slices (rows) is modified.
5.  **Spatial Relationship:** Objects maintain their original horizontal positioning within the grid. The vertical flipping happens within the vertical range occupied by the object.
6.  **Independence:** The transformation is applied independently to each object. Objects do not interact with each other.
7.  **Background:** The white background pixels remain white unless they are part of a row that gets swapped and contains part of an object. However, the rule seems to operate on entire rows within the object's vertical span.

**YAML Facts:**


```yaml
task_context:
  grid_representation: 2D array of integers (0-9) representing colors.
  background_color: white (0).
  object_definition: Connected component of non-background pixels of the same color.

objects:
  - id: object_1
    description: A connected component of non-white pixels.
    properties:
      - color: Any color except white (1-9).
      - connectivity: Pixels are connected horizontally or vertically.
      - location: Defined by the set of coordinates it occupies.
      - vertical_extent: The range of row indices spanned by the object (min_row to max_row).

actions:
  - name: identify_objects
    description: Find all distinct connected components of non-white pixels in the input grid.
    inputs: input_grid
    outputs: list_of_objects

  - name: determine_vertical_extent
    description: For a given object, find the minimum and maximum row index it occupies.
    inputs: object
    outputs: min_row, max_row

  - name: extract_row_slice
    description: Get the horizontal rows from the input grid corresponding to the vertical extent of an object.
    inputs: input_grid, min_row, max_row
    outputs: row_slice (a list or array of rows)

  - name: reverse_row_order
    description: Reverse the order of rows within the extracted slice.
    inputs: row_slice
    outputs: reversed_row_slice

  - name: place_reversed_slice
    description: Place the reversed row slice into the output grid at the original vertical extent.
    inputs: output_grid, reversed_row_slice, min_row, max_row
    outputs: modified_output_grid

relationships:
  - type: spatial
    description: Objects occupy specific rows and columns in the grid.
  - type: processing
    description: Each identified object is processed independently. The transformation on one object does not affect others directly.
  - type: input_output_mapping
    description: The output grid is constructed by applying the row-reversal transformation for each object's vertical extent onto an initially white grid.

goal:
  description: Vertically flip the rows within the vertical bounds of each distinct object found in the input grid.
```


**Natural Language Program:**

1.  Create a new output grid with the same dimensions as the input grid, initially filled entirely with the background color (white, 0).
2.  Identify all distinct connected groups (objects) of non-white pixels in the input grid. Ensure each pixel is assigned to only one object.
3.  For each identified object:
    a.  Determine the minimum row index (`min_row`) and the maximum row index (`max_row`) occupied by any pixel of that object.
    b.  Extract the segment of the *input* grid consisting of all rows from `min_row` to `max_row`, inclusive. Let's call this the `input_row_slice`.
    c.  Reverse the order of the rows within the `input_row_slice`. For example, the row at index `min_row` in the input becomes the row at index `max_row` in the reversed slice, the row at `min_row + 1` becomes the row at `max_row - 1`, and so on.
    d.  Copy this reversed sequence of rows into the *output* grid, placing them back into the rows from `min_row` to `max_row`, inclusive.
4.  After processing all objects, return the final output grid.
