
## train_1

**input:**
```
0 6 6 6 0 0 0 6 0 0 0 0 0 6 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 6 6 6 0 0 6 6 6 0 0 0 6 6 6 0 0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 7 7 7 0 0 0 0 7 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 7 7 7 0 0 0 7 7 7 0 0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 9 9 9 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 9 9 9 0 0 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples.

**Perception of Task Elements:**

1.  **Grid Structure:** The inputs and outputs appear to be 1-dimensional arrays or single rows from a larger grid. All examples have the same length (33).
2.  **Colors:** Each example uses white (0) as the background color and one other dominant color: magenta (6) in the first, orange (7) in the second, and maroon (9) in the third.
3.  **Input Patterns:** The inputs contain blocks of the dominant color (e.g., `6 6 6`, `7 7 7`, `9 9 9`) and isolated instances of the dominant color surrounded by white pixels (e.g., `0 6 0`, `0 7 0`, `0 9 0`).
4.  **Output Patterns:** In the outputs, the initial blocks of the dominant color remain unchanged. However, the isolated instances of the dominant color seem to be expanded into a block of three. Specifically, a pattern `0 C 0` (where `C` is the dominant color) in the input becomes `C C C` in the output, centered at the original position of `C`.
5.  **Transformation:** The core transformation identifies isolated pixels of the dominant color (pixels with white neighbors on both the left and right) and replaces the pixel itself and its immediate left and right neighbors with the dominant color. Pixels that are already part of a horizontal sequence of the dominant color are not considered isolated and are left unchanged. The transformation preserves the grid dimensions.

**Facts (YAML):**


```yaml
task_type: pattern_replacement
grid_dimensionality: 1D (or row-wise 2D)
colors:
  - background: white (0)
  - foreground: variable (magenta=6, orange=7, maroon=9 in examples)
objects:
  - type: pixel
    properties:
      - color
      - position (index)
      - left_neighbor_color
      - right_neighbor_color
  - type: pattern
    properties:
      - constituent_pixels
      - sequence (e.g., '0 C 0', 'C C C')
input_features:
  - presence of isolated foreground pixels (pattern '0 C 0')
  - presence of contiguous blocks of foreground pixels (e.g., 'C C C')
output_features:
  - isolated foreground pixels ('0 C 0') are replaced by a block ('C C C')
  - contiguous blocks ('C C C') remain unchanged
transformation:
  - name: expand_isolated_pixel
  - description: Replaces a sequence '0 C 0' with 'C C C', where C is the foreground color.
  - condition: Applies only if a pixel has the foreground color AND its immediate left and right neighbors are white (0).
  - scope: Operates horizontally. Requires index bounds checking (i-1, i, i+1 must be valid).
relationship: horizontal_adjacency
invariance:
  - grid_size
  - background_pixels not involved in the direct replacement
  - foreground pixels that are not isolated horizontally
```


**Natural Language Program:**

1.  Create a copy of the input grid to serve as the initial output grid.
2.  Identify the single non-white (foreground) color `C` present in the input grid.
3.  Iterate through the input grid horizontally, examining each pixel from the second position up to the second-to-last position (index `i` from 1 to length-2).
4.  For each examined pixel at index `i`:
    a.  Check if the pixel at `input[i]` has color `C`.
    b.  Check if the pixel at `input[i-1]` has color white (0).
    c.  Check if the pixel at `input[i+1]` has color white (0).
5.  If all three conditions (4a, 4b, 4c) are true, then this pixel is an "isolated foreground pixel". Modify the *output* grid by setting the pixels at indices `i-1`, `i`, and `i+1` to color `C`.
6.  After iterating through all applicable pixels, return the final output grid.
