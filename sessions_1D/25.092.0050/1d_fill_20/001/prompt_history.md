
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 3 0 0 0 0 3 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 3 3 3 3 3 3 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
5 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Perception
The input and output are single-row grids (1D arrays).
Each input grid contains exactly two pixels of the same non-white color, with all other pixels being white (0).
The output grid is formed by filling the space *between* these two non-white pixels (inclusive) with the same non-white color.
The pixels outside this filled range remain white.

## Facts

```yaml
task_type: fill_segment
dimensionality: 1D
input_elements:
  - type: background
    color: white (0)
  - type: markers
    count: 2
    color: non-white (varies per example: orange, green, gray)
    properties:
      - location: index within the row
      - relationship: define the start and end points of a segment
output_elements:
  - type: background
    color: white (0)
    properties:
      - location: outside the segment defined by input markers
  - type: filled_segment
    color: same as the input markers
    properties:
      - location: spans from the index of the first marker to the index of the second marker (inclusive)
transformation:
  - action: identify_markers
    inputs: input grid
    outputs: indices and color of the two non-white pixels
  - action: determine_range
    inputs: indices of the markers
    outputs: minimum and maximum index (start and end of the segment)
  - action: fill_range
    inputs: input grid, start index, end index, marker color
    outputs: output grid (copy of input with the range filled)
```


## Natural Language Program

1.  Identify the non-white color present in the input grid.
2.  Find the indices of the two pixels that have this non-white color.
3.  Determine the minimum and maximum of these two indices. Let these be `start_index` and `end_index`.
4.  Create the output grid, initially identical to the input grid.
5.  Iterate from `start_index` to `end_index` (inclusive). For each index in this range, set the pixel value in the output grid to the identified non-white color.
6.  Return the modified output grid.
