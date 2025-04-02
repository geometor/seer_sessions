
## train_1

**input:**
```
0 0 0 0 6 0 0 0 0 0 0 6 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 6 6 6 6 6 6 6 6 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 6 0 0 0 6 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 3 0 0 0 0 0 0 0 0 3 0 0 0 0 0
```


**output:**
```
0 0 0 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
```

## Perception

The input consists of a single row (a 1D array or a 1xN grid).
Most pixels in the input row are white (0).
There are exactly two non-white pixels in the input row. These two non-white pixels always share the same color.
The output is also a single row of the same dimensions as the input.
The output row retains the two original non-white pixels from the input.
The key transformation is that all the white pixels located *between* the two non-white pixels in the input are changed to the color of those non-white pixels in the output.
Pixels outside the range defined by the two non-white pixels remain white.

## Facts


```yaml
task_type: fill_segment
components:
  - role: background
    element_type: pixel
    property:
      color: white (0)
  - role: marker
    element_type: pixel
    count: 2
    property:
      color: non-white (any color from 1-9)
      constraint: both markers have the same color in a given input
  - role: segment
    element_type: contiguous_pixels
    definition: the pixels located inclusively between the two marker pixels
    initial_state: may contain white pixels
    final_state: all pixels within the segment adopt the color of the marker pixels
grid_properties:
  dimensionality: 1 (single row)
  size: constant between input and output
transformation:
  operation: fill
  target: the segment defined by the two marker pixels
  fill_color: the color of the marker pixels
relationships:
  - type: spatial
    description: The transformation depends on the relative positions (indices) of the two marker pixels.
```


## Natural Language Program

1.  Identify the color and column indices of the two non-white pixels in the input row. Let the color be `C` and the indices be `index1` and `index2`.
2.  Determine the leftmost index (`start_index = min(index1, index2)`) and the rightmost index (`end_index = max(index1, index2)`).
3.  Create the output row, initially identical to the input row.
4.  Iterate through the columns from `start_index` to `end_index` (inclusive).
5.  For each column index in this range, set the pixel color in the output row to `C`.
6.  The resulting row is the final output.
