
## train_1

**input:**
```
0 0 0 0 0 0 4 4 4 4 4 4 4 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 4 4 4 4 4 4 4 0 0 0
```


## train_2

**input:**
```
0 5 5 5 5 5 5 5 5 5 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 9 0 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 1 1 1 1 1 1 1 1 1 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 1 1 1 1 1 1 1 1 1 0 0 0 0
```

**Perception**

1.  **Input/Output Format:** The input and output are single rows (1xN grids) of pixels.
2.  **Key Elements:** Each grid contains:
    *   Background pixels (white, 0).
    *   A single unique 'pivot' pixel (maroon, 9).
    *   A single contiguous block of identical colored pixels (yellow, gray, or blue in the examples), which are neither white nor maroon.
3.  **Transformation:** The core transformation involves moving the contiguous colored block. In the input, this block always appears *before* the maroon pixel. In the output, this block is moved to the position immediately *after* the maroon pixel.
4.  **Structure Preservation:** The relative order of all other pixels (white background pixels and the maroon pivot pixel) is preserved. The dimensions of the grid remain unchanged.

**Facts**


```yaml
task_type: rearrangement
grid_dimensionality: 1D (represented as 1xN)
objects:
  - id: background
    color: white (0)
    role: fills empty space
  - id: pivot
    color: maroon (9)
    count: 1
    role: defines the target location for rearrangement
  - id: colored_block
    color: any color except white (0) or maroon (9)
    count: 1
    properties:
      - contiguous sequence of identical pixels
    role: the object being moved
relationship:
  - type: spatial order (input)
    description: The 'colored_block' appears somewhere before the 'pivot' pixel in the linear sequence.
  - type: spatial order (output)
    description: The 'colored_block' appears immediately after the 'pivot' pixel in the linear sequence.
action:
  - type: move
    target: colored_block
    details: The block is extracted from its original position and reinserted immediately after the pivot pixel. All other pixels maintain their relative order.
constraints:
  - Exactly one pivot pixel exists.
  - Exactly one contiguous block of a single color (not white or maroon) exists.
  - The colored block initially precedes the pivot pixel.
```


**Natural Language Program**

1.  Identify the index (position) of the single maroon (9) pixel in the input row.
2.  Identify the contiguous block of pixels that are neither white (0) nor maroon (9). Record the sequence of pixels forming this block and their start and end indices in the input row.
3.  Create a new sequence (list) of pixels by removing the identified colored block from the input row.
4.  Find the index of the maroon (9) pixel within this new, shorter sequence.
5.  Insert the recorded colored block sequence immediately after the maroon pixel's position in the new sequence.
6.  The resulting sequence is the final output row.
