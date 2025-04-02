
## train_1

**input:**
```
0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0
```


## train_2

**input:**
```
0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0
```


## train_3

**input:**
```
0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0
```

**Perception of Task Elements:**

The input and output data are presented as one-dimensional arrays (or 1xN grids) of integers representing colors. Each example features a single contiguous block of a non-white color (red, orange, or gray) surrounded by white pixels (0). The core transformation observed across all examples is a spatial shift of this colored block. The length of the array and the color/length of the block remain unchanged; only its position within the array is altered. Specifically, the colored block moves three positions to the right. The white pixels effectively flow around the shifted block, maintaining the overall array length.

**YAML Facts:**


```yaml
Data:
  Type: 1-dimensional array (or 1xN grid)
  Format: Integers representing colors (0-9)
  Background_Color: white (0)

Objects:
  - Type: Contiguous_Block
    Properties:
      - Color: Non-white (varies per example: red(2), orange(7), gray(5))
      - Shape: Linear segment
      - Count: 1 per grid
    Relationship_to_Background: Surrounded by white pixels

Transformation:
  Action: Spatial_Shift
  Target: Contiguous_Block (non-white)
  Direction: Right
  Magnitude: 3 positions
  Effect_on_Background: White pixels fill the vacated space on the left and are displaced on the right, maintaining array length.
  Invariants:
    - Grid dimensions (length)
    - Color of the block
    - Length of the block
```


**Natural Language Program:**

1.  Identify the contiguous block of non-white pixels within the input array.
2.  Determine the starting and ending indices of this block.
3.  Create a new array of the same length as the input, initialized with white pixels (0).
4.  Copy the identified non-white block into the new array, shifting its starting position 3 indices to the right compared to its position in the input array.
5.  The resulting array is the output.
