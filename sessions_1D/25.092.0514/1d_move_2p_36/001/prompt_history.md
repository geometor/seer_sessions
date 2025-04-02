
## train_1

**input:**
```
2 2 2 2 2 2 2 2 2 2 2 0 0 0 0
```


**output:**
```
0 0 2 2 2 2 2 2 2 2 2 2 2 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 1 1 1 1 1 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 1 1 1 1 1 0 0
```


## train_3

**input:**
```
0 5 5 5 5 5 5 5 5 5 0 0 0 0 0
```


**output:**
```
0 0 0 5 5 5 5 5 5 5 5 5 0 0 0
```

Okay, let's analyze the provided examples.

**Perception of Elements:**

*   The input and output data are represented as 1D arrays or single-row grids.
*   Each example contains a single contiguous block of a non-white color (red, blue, or gray) surrounded by white pixels (0).
*   The size of the array remains constant between the input and output.
*   The block of non-white pixels retains its color and length in the output.
*   The primary transformation appears to be a positional shift of the non-white block within the array.
*   In all three examples, the non-white block moves two positions to the right.

**YAML Facts:**


```yaml
task_type: array_transformation_1d
components:
  - type: background
    properties:
      color: white (0)
      role: padding
  - type: object
    properties:
      shape: contiguous_block_1d
      color: non-white (1, 2, 5 observed)
      size: variable_length
      count: 1
actions:
  - type: shift
    target: object
    properties:
      direction: right
      magnitude: 2 positions
relationships:
  - input_output:
      preserves:
        - array_length
        - object_color
        - object_length
      modifies:
        - object_position
        - background_padding_distribution
```


**Natural Language Program:**

1.  Identify the contiguous sequence of non-white pixels within the input 1D array.
2.  Determine the starting index of this sequence.
3.  Create a new 1D array of the same total length as the input, filled initially with white pixels (0).
4.  Calculate the target starting index for the sequence in the output array by adding 2 to the original starting index.
5.  Copy the identified sequence of non-white pixels into the new array, beginning at the calculated target starting index.
6.  The resulting array is the output.
