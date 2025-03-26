
## train_1

**input:**
```
2 1
3 1
```


**output:**
```
2 2 1 1
2 2 1 1
3 3 1 1
3 3 1 1
```


## train_2

**input:**
```
0 5 1
5 5 5
2 5 0
```


**output:**
```
0 0 5 5 1 1
0 0 5 5 1 1
5 5 5 5 5 5
5 5 5 5 5 5
2 2 5 5 0 0
2 2 5 5 0 0
```


## train_3

**input:**
```
2 0 3 0
2 1 3 0
0 0 3 3
0 0 3 5
```


**output:**
```
2 2 0 0 3 3 0 0
2 2 0 0 3 3 0 0
2 2 1 1 3 3 0 0
2 2 1 1 3 3 0 0
0 0 0 0 3 3 3 3
0 0 0 0 3 3 3 3
0 0 0 0 3 3 5 5
0 0 0 0 3 3 5 5
```

## Perception

The task involves transforming an input grid into a larger output grid. In all provided examples, the output grid's dimensions (height and width) are exactly double those of the input grid. Observing the color patterns, each individual pixel (cell) in the input grid appears to be expanded into a 2x2 block of the same color in the output grid. The relative positions of these expanded blocks correspond to the relative positions of the original pixels.

## Facts


```yaml
Input Grid:
  - Type: 2D array of integers (colors)
  - Size: Variable height (H) and width (W)

Output Grid:
  - Type: 2D array of integers (colors)
  - Size: Fixed relationship to input size - Height = 2 * H, Width = 2 * W

Transformation:
  - Type: Scaling / Expansion
  - Operation: Each pixel at position (r, c) in the input grid is replaced by a 2x2 block of the same color in the output grid.
  - Mapping:
    - Input pixel at (r, c) with color X maps to:
      - Output pixel at (2*r, 2*c) with color X
      - Output pixel at (2*r+1, 2*c) with color X
      - Output pixel at (2*r, 2*c+1) with color X
      - Output pixel at (2*r+1, 2*c+1) with color X
  - Objects: Individual pixels are treated as units.
  - Properties: The color of each pixel is preserved during expansion.
  - Relationships: The spatial relationship between adjacent pixels in the input is maintained in the output through the adjacency of the corresponding 2x2 blocks.
```


## Natural Language Program

1.  Determine the height (H) and width (W) of the input grid.
2.  Create a new output grid with height 2*H and width 2*W.
3.  Iterate through each pixel in the input grid, using its row index `r` (from 0 to H-1) and column index `c` (from 0 to W-1).
4.  For each input pixel at position (`r`, `c`), get its color value.
5.  In the output grid, fill the 2x2 block of pixels starting at position (`2*r`, `2*c`) with this color value. Specifically, set the color of the output pixels at (`2*r`, `2*c`), (`2*r + 1`, `2*c`), (`2*r`, `2*c + 1`), and (`2*r + 1`, `2*c + 1`) to the input pixel's color.
6.  Return the completed output grid.
