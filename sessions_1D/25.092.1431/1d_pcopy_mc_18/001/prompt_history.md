
## train_1

**input:**
```
0 9 9 9 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 9 9 9 0 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 8 8 8 0 0 0 9 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 8 8 8 0 0 9 9 9 0 0 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 3 3 3 0 0 5 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 3 3 3 0 5 5 5 0 0 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Perception

The input and output are both single-row grids (1D arrays) of pixels. The grids contain segments of non-white colors separated by white (0) pixels.

Observing the examples:
1.  **Segments of three identical non-white pixels:** These segments appear unchanged in the output grid at the same position (e.g., `9 9 9` in `train_1`, `8 8 8` in `train_2`, `3 3 3` in `train_3`).
2.  **Single non-white pixels:** These pixels are isolated, meaning they have white pixels immediately to their left and right. In the output, each single pixel seems to expand into a segment of three pixels of the *same color*, centered at the original pixel's location. This expansion overwrites the original single pixel and its immediate left and right neighbors.
    *   In `train_1`, the single `8` at index 6 causes indices 5, 6, and 7 in the output to become `8`.
    *   In `train_2`, the single `9` at index 8 causes indices 7, 8, and 9 in the output to become `9`. The single `9` at index 13 causes indices 12, 13, and 14 to become `9`.
    *   In `train_3`, the single `5` at index 7 causes indices 6, 7, and 8 to become `5`. The single `5` at index 13 causes indices 12, 13, and 14 to become `5`.
3.  **White pixels:** White pixels (0) generally remain white, unless they are overwritten by the expansion of a nearby single non-white pixel.

The core transformation identifies isolated non-white pixels and expands them horizontally into a 3-pixel segment, replacing the original pixel and its immediate neighbors. Segments already of length 3 are preserved.

## Facts


```yaml
task_context:
  grid_dimensionality: 1D (single row)
  colors_used:
    - 0 (white): background/separator
    - 1-9: various foreground colors

objects:
  - id: single_pixel
    description: A non-white pixel P at index `i` where the pixel at `i-1` is white (0) and the pixel at `i+1` is white (0). Boundary conditions might need consideration if such pixels occur at index 0 or grid_width-1, but examples show them mid-grid.
    properties:
      - color: The color value (1-9) of the pixel.
      - index: The position `i` in the row.
  - id: segment_len3
    description: A contiguous sequence of exactly three identical non-white pixels.
    properties:
      - color: The color value (1-9) of the pixels in the segment.
      - indices: The starting, middle, and ending indices of the segment.
  - id: background
    description: White pixels (0).

relationships:
  - type: adjacency
    description: Pixels are evaluated based on their immediate left and right neighbors.
  - type: isolation
    description: A property of `single_pixel`, defined by white neighbors.

actions_on_input:
  - action: identify_single_pixels
    description: Scan the input grid to find all pixels matching the `single_pixel` definition. Record their index and color.
  - action: identify_preserved_elements
    description: Identify `segment_len3` and `background` pixels that are *not* adjacent (left or right) to an identified `single_pixel`.

transformation:
  - based_on: identified `single_pixel` at input index `i` with color `c`.
  - action: expand_pixel
    target: output grid
    effect: Set the pixels at output indices `i-1`, `i`, and `i+1` to color `c`.
  - based_on: identified `preserved_elements`.
  - action: copy_pixel
    target: output grid
    effect: Copy the color of the preserved element from the input grid to the corresponding index in the output grid.

processing_notes:
  - The identification of single pixels must happen based entirely on the input grid state *before* any transformations are applied to the output grid.
  - The output grid is constructed by first potentially copying the input, then applying the `expand_pixel` transformation for all identified single pixels. This overwrites the original single pixel and its neighbors (which could be background or part of another segment).
```


## Natural Language Program

1.  Create a new output grid of the same dimensions as the input grid, initially copying all values from the input grid.
2.  Iterate through the input grid from the second pixel (index 1) up to the second-to-last pixel (index `width - 2`).
3.  For each pixel at index `i` in the input grid:
    a.  Check if the pixel's color is non-white (not 0).
    b.  Check if the pixel to its left (at index `i-1`) is white (0).
    c.  Check if the pixel to its right (at index `i+1`) is white (0).
    d.  If all three conditions (non-white current pixel, white left neighbor, white right neighbor) are true, then this pixel is an "isolated single pixel".
    e.  If an isolated single pixel with color `c` is found at index `i` in the input grid:
        i.  Modify the **output** grid: Set the pixel at index `i-1` to color `c`.
        ii. Modify the **output** grid: Set the pixel at index `i` to color `c`.
        iii. Modify the **output** grid: Set the pixel at index `i+1` to color `c`.
4.  After checking all relevant pixels in the input grid and performing all necessary modifications on the output grid, the resulting output grid is the final result. (Pixels not part of a 3-pixel expansion centered on an isolated single pixel retain their original copied value).
