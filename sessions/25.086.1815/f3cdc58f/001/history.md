
## train_1

**input:**
```
0 0 0 0 0 4 0 3 3 0
0 1 3 0 0 0 3 0 0 0
0 0 0 0 1 0 0 1 0 4
3 0 0 0 2 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0 0
0 3 0 0 0 4 3 2 0 0
0 0 0 1 0 0 0 0 3 0
0 0 4 0 0 4 0 1 0 1
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
1 0 3 0 0 0 0 0 0 0
1 0 3 0 0 0 0 0 0 0
1 2 3 4 0 0 0 0 0 0
1 2 3 4 0 0 0 0 0 0
1 2 3 4 0 0 0 0 0 0
1 2 3 4 0 0 0 0 0 0
1 2 3 4 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0
2 0 0 0 0 3 0 1 4 1
0 0 0 0 0 0 1 0 0 0
1 4 0 0 0 0 0 0 0 1
0 0 0 0 2 0 0 0 2 0
0 0 4 0 0 0 0 0 0 0
1 0 0 4 0 4 0 0 3 0
0 0 0 0 0 0 0 0 0 0
0 1 2 1 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0
1 0 0 4 0 0 0 0 0 0
1 0 0 4 0 0 0 0 0 0
1 2 0 4 0 0 0 0 0 0
1 2 0 4 0 0 0 0 0 0
1 2 3 4 0 0 0 0 0 0
1 2 3 4 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 3 0
0 1 0 0 2 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 3 0 0 2 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 2 3 4 0 0 0 0 0 0
1 2 3 4 0 0 0 0 0 0
1 2 3 4 0 0 0 0 0 0
```

Okay, let's analyze the provided examples.

**Perception**

The input is a grid containing scattered pixels of various colors (blue=1, red=2, green=3, yellow=4) against a white background (0). The output grid has the same dimensions as the input but is mostly white. The key feature of the output grid is a set of vertical bars located in the first four columns (columns 0, 1, 2, and 3). Each bar consists of a single color: column 0 is blue, column 1 is red, column 2 is green, and column 3 is yellow. The height of each colored bar seems to correspond to the total count of pixels of that specific color in the input grid. These bars are aligned to the bottom edge of the output grid.

**Facts**


```yaml
- task_type: transformation
- input_domain:
    - grid: 2D array of integers (0-9)
    - colors_present: white (0), blue (1), red (2), green (3), yellow (4)
    - grid_size: consistent within pairs (e.g., 10x10)
- output_domain:
    - grid: 2D array of integers (0-9), same dimensions as input
    - structure: vertical bars of color in the leftmost columns against a white background
- elements:
    - pixels: individual cells with color values
    - colors_of_interest: blue (1), red (2), green (3), yellow (4)
    - output_bars: contiguous vertical segments of a single color
- relationships:
    - input_output_dimensions: same height and width
    - color_to_column_mapping:
        - blue (1) maps to column 0
        - red (2) maps to column 1
        - green (3) maps to column 2
        - yellow (4) maps to column 3
    - count_to_height_relationship: The count of each color (1, 2, 3, 4) in the input grid determines the height (number of pixels) of the corresponding colored bar in the output grid.
    - alignment: The colored bars in the output grid are bottom-aligned.
- actions:
    - count: Count the occurrences of each color (1, 2, 3, 4) in the input grid.
    - generate: Create a new grid of the same dimensions as the input, initialized to white (0).
    - draw_bars: For each color (1, 2, 3, 4), draw a vertical bar of that color in its designated column (0, 1, 2, 3) in the output grid. The height of the bar equals the count of that color, and the bar starts from the bottom row and extends upwards.
```


**Natural Language Program**

1.  Initialize an output grid with the same dimensions as the input grid, filling it entirely with white pixels (0).
2.  Count the total number of blue (1) pixels in the input grid. Let this count be `count_blue`.
3.  Count the total number of red (2) pixels in the input grid. Let this count be `count_red`.
4.  Count the total number of green (3) pixels in the input grid. Let this count be `count_green`.
5.  Count the total number of yellow (4) pixels in the input grid. Let this count be `count_yellow`.
6.  Determine the height of the grid, let this be `grid_height`.
7.  In the output grid, fill the cells in column 0 with blue (1) starting from row `grid_height - count_blue` down to row `grid_height - 1`.
8.  In the output grid, fill the cells in column 1 with red (2) starting from row `grid_height - count_red` down to row `grid_height - 1`.
9.  In the output grid, fill the cells in column 2 with green (3) starting from row `grid_height - count_green` down to row `grid_height - 1`.
10. In the output grid, fill the cells in column 3 with yellow (4) starting from row `grid_height - count_yellow` down to row `grid_height - 1`.
11. Leave all other cells in the output grid as white (0).
12. The resulting grid is the final output.
