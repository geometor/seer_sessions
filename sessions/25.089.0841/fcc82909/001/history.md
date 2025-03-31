
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 4 8 0 0 0 0 0 0
0 0 9 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 1 0 0
0 0 0 0 0 0 1 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 4 8 0 0 0 0 0 0
0 0 9 4 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0
0 0 3 3 0 0 2 1 0 0
0 0 3 3 0 0 1 2 0 0
0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 4 0 0 0
0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 3 3 0 0 8 4 0 0 0
0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 3 3 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 2 4 0 0 9 8 0 0
0 0 6 7 0 0 8 9 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 6 0 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 2 4 0 0 9 8 0 0
0 0 6 7 0 0 8 9 0 0
0 0 3 3 0 0 3 3 0 0
0 0 3 3 0 0 3 3 0 0
0 0 3 3 7 6 0 0 0 0
0 0 3 3 6 6 0 0 0 0
0 0 0 0 3 3 0 0 0 0
0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Perception:**

The input grids contain a white background (0) and one or more distinct 2x2 squares composed of various non-white pixels. The output grids retain the original 2x2 squares and add a new 2x2 square filled entirely with green (3) pixels immediately below each original 2x2 square. The transformation identifies these 2x2 non-white blocks and essentially "extrudes" or copies a green version downwards by two rows.

**Facts:**


```yaml
Input Grid:
  - type: grid
  - background_color: white (0)
  - contains:
      - objects:
          - type: square
          - size: 2x2
          - composition: non-white pixels (1-9)
          - quantity: variable (1 or more)
          - position: variable

Output Grid:
  - type: grid
  - background_color: white (0)
  - transformation: based on input grid
  - contains:
      - original_objects:
          - copied from: input grid's 2x2 non-white squares
          - properties: unchanged position and colors
      - new_objects:
          - type: square
          - size: 2x2
          - composition: green (3) pixels only
          - quantity: equal to the number of original_objects
          - position:
              - relationship: directly below an original_object
              - rule: If original object's top-left corner is (row, col), new object's top-left corner is (row + 2, col).
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through all possible 2x2 areas within the input grid. Check each 2x2 area starting from the top-left corner (row `r`, column `c`) up to `height-2` and `width-2`.
3.  For each 2x2 area, verify if all four pixels (`grid[r, c]`, `grid[r, c+1]`, `grid[r+1, c]`, `grid[r+1, c+1]`) are non-white (not equal to 0).
4.  If a 2x2 area consists entirely of non-white pixels:
    a.  Identify the corresponding location in the output grid two rows below the identified area. This target area will cover rows `r+2` and `r+3`, and columns `c` and `c+1`.
    b.  Check if this target area is within the bounds of the grid (i.e., `r+3` is less than the grid height).
    c.  If within bounds, fill the 2x2 target area in the *output* grid with green (3) pixels:
        i.  `output[r+2, c] = 3`
        ii. `output[r+2, c+1] = 3`
        iii. `output[r+3, c] = 3`
        iv. `output[r+3, c+1] = 3`
5.  Return the modified output grid.
