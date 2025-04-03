
## train_1

**input:**
```
0 2 2 2 2 0 0 0 0 0
```


**output:**
```
0 2 0 0 2 0 0 0 0 0
```


## train_2

**input:**
```
4 4 4 0 0 0 0 0 0 0
```


**output:**
```
4 0 4 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 7 7 7 0
```


**output:**
```
0 0 0 0 0 0 7 0 7 0
```

## Perception

The input and output are single-row grids (1x10).
The input contains contiguous horizontal segments of non-white pixels surrounded by white pixels.
The transformation modifies these non-white segments.
Specifically, within each non-white segment, the first and last pixels retain their original color, while all the pixels between the first and last are changed to white (0).
Segments of length 1 or 2 would remain unchanged by this rule, although the examples only show segments of length 3 or 4.
The white pixels outside the segments remain unchanged.

## Facts


```yaml
task_type: object_transformation
grid_dimensionality: 1D # Effectively 1D rows within a 2D grid representation
objects:
  - type: segment
    description: Contiguous horizontal sequence of non-white pixels.
    properties:
      - color: The uniform color of the pixels in the segment (e.g., red, yellow, orange).
      - length: The number of pixels in the segment.
      - start_index: The column index of the first pixel in the segment.
      - end_index: The column index of the last pixel in the segment.
relationships:
  - type: spatial
    description: Segments are separated by one or more white (0) pixels.
actions:
  - name: hollow_segment
    input: non-white segment
    condition: segment length must be 3 or greater.
    output: modified segment
    process:
      - Identify the first pixel (at start_index) and the last pixel (at end_index) of the segment.
      - Keep the color of the first and last pixels unchanged.
      - Change the color of all pixels between the start_index and end_index to white (0).
transformation_scope: Applies independently to each row and each identified segment within that row.
background_pixels: White (0) pixels remain unchanged unless they are part of the interior of a segment being hollowed.
```


## Natural Language Program

1.  Iterate through each row of the input grid.
2.  Within the current row, identify all contiguous horizontal segments of pixels that are not white (0).
3.  For each identified segment:
    a.  Determine the length of the segment.
    b.  If the length is 3 or greater:
        i.  Keep the color of the first pixel in the segment.
        ii. Keep the color of the last pixel in the segment.
        iii. Change the color of all pixels located *between* the first and last pixels to white (0).
4.  Pixels not part of any segment (original white pixels) and pixels in segments shorter than 3 remain unchanged.
5.  Construct the output grid based on these modifications.
