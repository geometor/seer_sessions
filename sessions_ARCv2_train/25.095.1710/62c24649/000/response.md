**Perception:**

The task takes a square grid of numbers as input and produces a larger square grid as output. The output grid's dimensions are double the input grid's dimensions in both height and width. The output grid is constructed by tiling four versions of the input grid:
1.  The original input grid in the top-left quadrant.
2.  A horizontally flipped version of the input grid in the top-right quadrant.
3.  A vertically flipped version of the input grid in the bottom-left quadrant.
4.  A version flipped both horizontally and vertically (or rotated 180 degrees) in the bottom-right quadrant.

**Facts:**


```yaml
Input:
  type: object
  properties:
    grid:
      type: 2D array of integers
      description: A square grid of numbers.
      rows: N
      columns: N
Output:
  type: object
  properties:
    grid:
      type: 2D array of integers
      description: A larger square grid derived from the input.
      rows: 2N
      columns: 2N
Transformation:
  - name: Construct Output Grid
    description: Creates a 2N x 2N grid by combining transformations of the N x N input grid.
    steps:
      - action: Place Original
        source: input grid
        target_quadrant: top-left (rows 0 to N-1, cols 0 to N-1)
        details: The input grid is placed directly into the top-left quadrant of the output grid.
      - action: Flip Horizontal
        source: input grid
        target_quadrant: top-right (rows 0 to N-1, cols N to 2N-1)
        details: The input grid is flipped horizontally and placed into the top-right quadrant.
      - action: Flip Vertical
        source: input grid
        target_quadrant: bottom-left (rows N to 2N-1, cols 0 to N-1)
        details: The input grid is flipped vertically and placed into the bottom-left quadrant.
      - action: Flip Horizontal and Vertical
        source: input grid
        target_quadrant: bottom-right (rows N to 2N-1, cols N to 2N-1)
        details: The input grid is flipped both horizontally and vertically and placed into the bottom-right quadrant.
Relationships:
  - The output grid dimensions are double the input grid dimensions.
  - Each quadrant of the output grid is a specific transformation (identity, horizontal flip, vertical flip, or both flips) of the input grid.
```


**Natural Language Program:**

1.  Define the input grid as `I`. Let `N` be the number of rows (and columns) in `I`.
2.  Create a new output grid `O` with dimensions `2N x 2N`.
3.  Copy the input grid `I` into the top-left quadrant of `O` (from row 0 to `N-1`, column 0 to `N-1`).
4.  Create a horizontally flipped version of `I`, let's call it `I_hflip`.
5.  Copy `I_hflip` into the top-right quadrant of `O` (from row 0 to `N-1`, column `N` to `2N-1`).
6.  Create a vertically flipped version of `I`, let's call it `I_vflip`.
7.  Copy `I_vflip` into the bottom-left quadrant of `O` (from row `N` to `2N-1`, column 0 to `N-1`).
8.  Create a version of `I` flipped both horizontally and vertically, let's call it `I_hvflip`. (This is equivalent to flipping `I_hflip` vertically or `I_vflip` horizontally).
9.  Copy `I_hvflip` into the bottom-right quadrant of `O` (from row `N` to `2N-1`, column `N` to `2N-1`).
10. Return the output grid `O`.