
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 0 0
1 1 0
0 1 0
1 1 1
0 0 1
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0 0 0
0 0 0 2 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 2 2
0 0 2 0
2 2 2 0
2 0 2 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 8 0 0 0 0 0
0 0 0 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 8 0 8 0
8 8 8 8 0
0 0 0 8 8
```

Okay, analyzing the provided examples.

**Perception of Task Elements:**

*   Each input grid contains a single, contiguous object composed of a non-white color (blue, red, or azure in the examples) set against a white background.
*   The object's shape and position vary across the examples.
*   The output grid is significantly smaller than the input grid.
*   The output grid contains only the non-white object from the input, with the surrounding white background removed.
*   The relative arrangement of the colored pixels within the object is preserved in the output.
*   The dimensions of the output grid correspond exactly to the dimensions of the bounding box containing the non-white object in the input grid.

**Facts:**


```yaml
facts:
  - scope: global
    description: Each task involves extracting a non-white object from a mostly white background.
  - scope: input
    objects:
      - name: background
        pixels: All pixels with value 0 (white).
      - name: shape
        pixels: All contiguous pixels with a value > 0 (non-white).
        properties:
          - color: The specific non-white value (e.g., 1, 2, 8).
          - contiguous: All non-white pixels are connected orthogonally or diagonally.
          - unique_color: Only one non-white color exists per input grid.
    relationships:
      - type: containment
        subject: background
        object: shape
        description: The shape is located somewhere within the background grid.
  - scope: output
    objects:
      - name: cropped_shape
        pixels: All pixels corresponding to the 'shape' from the input.
        properties:
          - color: Same as the input 'shape'.
          - relative_positions: The internal spatial arrangement of pixels is identical to the input 'shape'.
          - dimensions: Matches the bounding box of the input 'shape'.
    relationships:
      - type: extraction
        subject: input.shape
        object: output.cropped_shape
        description: The output is created by finding the bounding box of the input shape and extracting only that portion of the grid.
```


**Natural Language Program:**

1.  Identify all non-white pixels in the input grid.
2.  Determine the minimum and maximum row indices (`min_row`, `max_row`) and minimum and maximum column indices (`min_col`, `max_col`) occupied by these non-white pixels. This defines the bounding box of the shape.
3.  Calculate the height (`height = max_row - min_row + 1`) and width (`width = max_col - min_col + 1`) of the bounding box.
4.  Create a new output grid with dimensions `height` x `width`.
5.  Iterate through the rows from `min_row` to `max_row` (inclusive) and columns from `min_col` to `max_col` (inclusive) of the input grid.
6.  For each input pixel at `input[row][col]`, copy its value to the corresponding position in the output grid at `output[row - min_row][col - min_col]`.
7.  Return the newly created output grid.
