
## train_1

**input:**
```
2 2 2 2 8 8 8 8 8 8 8 8 8 8 8
2 2 2 2 8 8 8 8 8 8 8 8 8 8 8
2 2 2 2 8 8 8 8 8 8 8 8 8 8 8
2 2 2 2 8 8 8 8 8 8 8 8 8 8 8
2 2 2 2 8 8 8 8 8 8 8 8 8 8 8
2 2 2 2 8 8 8 8 8 8 8 8 8 8 8
2 2 2 2 8 8 8 8 8 8 8 8 8 8 8
2 2 2 2 8 8 8 8 8 8 8 8 8 8 8
2 2 2 2 8 8 8 8 8 8 8 8 8 8 8
3 3 3 3 5 5 5 5 5 5 5 5 5 5 5
3 3 3 3 5 5 5 5 5 5 5 5 5 5 5
3 3 3 3 5 5 5 5 5 5 5 5 5 5 5
3 3 3 3 5 5 5 5 5 5 5 5 5 5 5
```


**output:**
```
2 8
3 5
```


## train_2

**input:**
```
4 4 4 4 4 5 5 5 2 2 2 2 2 2
4 4 4 4 4 5 5 5 2 2 2 2 2 2
4 4 4 4 4 5 5 5 2 2 2 2 2 2
4 4 4 4 4 5 5 5 2 2 2 2 2 2
1 1 1 1 1 3 3 3 2 2 2 2 2 2
1 1 1 1 1 3 3 3 2 2 2 2 2 2
1 1 1 1 1 3 3 3 2 2 2 2 2 2
1 1 1 1 1 3 3 3 2 2 2 2 2 2
1 1 1 1 1 3 3 3 2 2 2 2 2 2
1 1 1 1 1 3 3 3 2 2 2 2 2 2
1 1 1 1 1 3 3 3 2 2 2 2 2 2
1 1 1 1 1 3 3 3 2 2 2 2 2 2
```


**output:**
```
4 5 2
1 3 2
```


## train_3

**input:**
```
1 1 1 2 2 2 2 2 8 8 8 8 8 8
1 1 1 2 2 2 2 2 8 8 8 8 8 8
1 1 1 2 2 2 2 2 8 8 8 8 8 8
1 1 1 2 2 2 2 2 8 8 8 8 8 8
1 1 1 2 2 2 2 2 8 8 8 8 8 8
5 5 5 6 6 6 6 6 3 3 3 3 3 3
5 5 5 6 6 6 6 6 3 3 3 3 3 3
5 5 5 6 6 6 6 6 3 3 3 3 3 3
5 5 5 6 6 6 6 6 3 3 3 3 3 3
5 5 5 6 6 6 6 6 3 3 3 3 3 3
5 5 5 6 6 6 6 6 3 3 3 3 3 3
5 5 5 6 6 6 6 6 3 3 3 3 3 3
5 5 5 6 6 6 6 6 3 3 3 3 3 3
5 5 5 6 6 6 6 6 3 3 3 3 3 3
5 5 5 6 6 6 6 6 3 3 3 3 3 3
```


**output:**
```
1 2 8
5 6 3
```


## train_4

**input:**
```
8 8 8 7 7 7 7 7 9 9 9 9 8 8 8
8 8 8 7 7 7 7 7 9 9 9 9 8 8 8
8 8 8 7 7 7 7 7 9 9 9 9 8 8 8
8 8 8 7 7 7 7 7 9 9 9 9 8 8 8
3 3 3 1 1 1 1 1 6 6 6 6 4 4 4
3 3 3 1 1 1 1 1 6 6 6 6 4 4 4
3 3 3 1 1 1 1 1 6 6 6 6 4 4 4
3 3 3 1 1 1 1 1 6 6 6 6 4 4 4
3 3 3 1 1 1 1 1 6 6 6 6 4 4 4
2 2 2 4 4 4 4 4 1 1 1 1 5 5 5
2 2 2 4 4 4 4 4 1 1 1 1 5 5 5
2 2 2 4 4 4 4 4 1 1 1 1 5 5 5
2 2 2 4 4 4 4 4 1 1 1 1 5 5 5
2 2 2 4 4 4 4 4 1 1 1 1 5 5 5
2 2 2 4 4 4 4 4 1 1 1 1 5 5 5
```


**output:**
```
8 7 9 8
3 1 6 4
2 4 1 5
```

*   **Perception:** The input grids are composed of large, rectangular blocks of solid colors. These blocks are arranged adjacent to each other, forming a larger grid structure within the input. The output grid is a significantly smaller grid where each cell corresponds to one of the color blocks in the input. The color of each cell in the output matches the color of the corresponding block in the input, and the relative spatial arrangement of the blocks is preserved.

*   **YAML Facts:**
    
```yaml
    task_description: Downsample a grid composed of solid color blocks into a smaller grid representing the blocks.
    
    elements:
      - element: input_grid
        description: A 2D grid composed of adjacent, solid-colored rectangular blocks.
        properties:
          - shape: variable (height x width)
          - content: integers 0-9 representing colors
          - structure: divided into distinct rectangular regions of uniform color
    
      - element: output_grid
        description: A smaller 2D grid representing the blocks found in the input grid.
        properties:
          - shape: determined by the number of unique block rows and columns in the input
          - content: integers 0-9 representing the colors of the corresponding blocks
          - structure: each cell corresponds to a unique block in the input grid
    
    relationships:
      - type: correspondence
        description: Each cell in the output grid corresponds to a distinct, contiguous block of color in the input grid.
      - type: spatial_preservation
        description: The relative position (top-left, top-right, bottom-left, etc.) of the color blocks in the input grid is maintained in the output grid.
      - type: color_mapping
        description: The color of a cell in the output grid is the same as the color of the corresponding block in the input grid.
    
    actions:
      - action: identify_blocks
        description: Segment the input grid into its constituent contiguous blocks of uniform color.
      - action: determine_representative_points
        description: Find a unique point (e.g., the top-left corner) for each identified block.
      - action: determine_output_dimensions
        description: Calculate the number of rows and columns for the output grid based on the unique row and column indices of the representative points.
      - action: construct_output
        description: Create the output grid by placing the color of each input block into the corresponding cell based on the relative positions of their representative points.
    ```


*   **Natural Language Program:**
    1.  Identify all distinct, contiguous blocks (regions) of uniform color within the input grid.
    2.  For each identified block, determine its color and find its top-leftmost pixel coordinate.
    3.  Collect all unique top-leftmost row indices and sort them.
    4.  Collect all unique top-leftmost column indices and sort them.
    5.  Create a new output grid with dimensions equal to (number of unique row indices) x (number of unique column indices).
    6.  Iterate through the identified blocks. For each block with top-left coordinate (r, c) and color V:
        a.  Find the index `out_r` corresponding to `r` in the sorted unique row indices.
        b.  Find the index `out_c` corresponding to `c` in the sorted unique column indices.
        c.  Set the pixel at `output_grid[out_r][out_c]` to the block's color V.
    7.  Return the constructed output grid.
