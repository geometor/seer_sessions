
## train_1

**input:**
```
0 0 7 7 7 0 0 0 0 9 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 7 7 7 0 0 0 9 9 9 0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 2 2 2 0 0 8 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 2 2 0 8 8 8 0 0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 8 8 8 0 0 0 2 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 8 8 8 0 0 2 2 2 0 0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze this task.

**Perception:**

The input and output are single rows (1D arrays represented as strings).
The input contains sequences of white pixels (0) interspersed with colored pixels.
Some colored pixels appear individually (like the maroon 9 and the second orange 7 in `train_1`), while others form horizontal blocks (like the first orange 777 block in `train_1`).

Observing the transformation:
1.  The existing horizontal block of orange pixels `7 7 7` remains unchanged in the output.
2.  The single maroon pixel `9` at index 9 in the input is replaced by a `9 9 9` block in the output, centered around the original position (indices 8, 9, 10).
3.  The single orange pixel `7` at index 13 in the input is replaced by a `7 7 7` block in the output, centered around the original position (indices 12, 13, 14).
4.  All white pixels (0) remain white unless overwritten by the expansion of a single colored pixel.

The core transformation seems to be the identification of isolated colored pixels and their expansion into a 1x3 horizontal block of the same color. Pixels already part of a horizontal block (of size > 1) are not affected.

**Facts YAML:**


```yaml
task_description: Expand isolated single colored pixels into 1x3 horizontal blocks.
elements:
  - type: grid
    dimensionality: 1 # Effectively 1D since it's a single row
    content:
      - type: background
        color: white (0)
      - type: object
        description: Blocks or single pixels of non-white color.
objects:
  - type: single_pixel
    description: A colored pixel with white pixels (or grid boundaries) as horizontal neighbors.
    properties:
      color: non-white (1-9)
      location: original index in the row
    action:
      type: expand
      direction: horizontal
      size: 1x3
      center: original location
      color: same as original pixel
  - type: block
    description: A horizontal sequence of 2 or more identical colored pixels.
    properties:
      color: non-white (1-9)
      location: range of indices
      size: >1 pixel wide
    action:
      type: none # Blocks remain unchanged
relationships:
  - type: adjacency
    description: Used to determine if a colored pixel is single (horizontally adjacent to white/boundary) or part of a block (horizontally adjacent to the same color).
constraints:
  - Expansion happens horizontally only.
  - Expansion overwrites background pixels.
  - Expansion is centered on the original single pixel's position.
  - Only single pixels are expanded; existing blocks are preserved.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each pixel of the input row at index `i`.
3.  If the pixel at index `i` is a colored pixel (not white, value > 0):
    a.  Check its horizontal neighbors (at `i-1` and `i+1`, handling boundary conditions).
    b.  If both neighbors are white (0) or out of bounds, then the pixel at `i` is an "isolated single pixel".
    c.  If it is an isolated single pixel:
        i.  Get its color `C`.
        ii. If `i > 0`, set the pixel at index `i-1` in the output grid to color `C`.
        iii. Set the pixel at index `i` in the output grid to color `C`.
        iv. If `i` is not the last index, set the pixel at index `i+1` in the output grid to color `C`.
4.  Pixels that are part of existing blocks (have at least one horizontal neighbor of the same color) or are background pixels are already correctly placed in the output grid by the initial copy and are not modified further by the expansion logic.
5.  Return the modified output grid.
