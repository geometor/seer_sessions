
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 3 0 0 0 3 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 3 0
```


## train_3

**input:**
```
0 0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 7 0 7 0 0 0 0 0 0 0 0 0 0 0 0
```

## Perception

The input and output grids are single rows (1D arrays).
The input grids contain segments of non-white pixels (e.g., green '3' or orange '7') surrounded by white pixels ('0').
The transformation focuses on these contiguous segments of non-white pixels.
In the output grid, only the start and end pixels of each contiguous non-white segment from the input are retained. All pixels *between* the start and end pixels of the segment are changed to white ('0').
Segments of length 1 or 2 would remain unchanged by this rule, although no examples are provided for this specific case. The examples show segments of length 3, 4, and 5.
The background white pixels remain unchanged.

## Facts


```yaml
task_type: array_transformation
dimensionality: 1D # Effectively 1D, presented as single-row 2D arrays
grid_properties:
  - single_row
objects:
  - type: segment
    definition: A contiguous sequence of one or more non-white pixels.
    properties:
      - color: The color of the pixels in the segment (e.g., green, orange).
      - length: The number of pixels in the segment.
      - start_index: The index of the first pixel in the segment.
      - end_index: The index of the last pixel in the segment.
  - type: background
    definition: Pixels with value 0 (white).
relationships:
  - segments are surrounded by background pixels or grid boundaries.
actions:
  - identify: Locate all contiguous segments of non-white pixels in the input row.
  - modify: For each identified segment:
      - If the segment length is greater than 2:
          - Change the color of all pixels between the start_index and end_index (exclusive) to white (0).
      - Retain the original color of the pixels at the start_index and end_index.
  - preserve: Keep all background (white) pixels unchanged.
invariance:
  - The color of the non-white segment does not affect the transformation logic.
  - The position of the segment within the row does not affect the transformation logic, only its internal structure.
  - The overall length of the row remains the same.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through the input grid to identify contiguous segments of non-white pixels. A segment starts when a non-white pixel is encountered after a white pixel (or at the beginning of the grid) and ends when a white pixel is encountered after a non-white pixel (or at the end of the grid).
3.  For each identified segment:
    a.  Determine the start index and end index of the segment.
    b.  Calculate the length of the segment (end index - start index + 1).
    c.  If the length of the segment is greater than 2:
        i.  Iterate through the indices strictly between the start index and the end index (i.e., from `start_index + 1` to `end_index - 1`).
        ii. Set the value of the corresponding pixels in the *output* grid to white (0).
4.  Return the modified output grid.
