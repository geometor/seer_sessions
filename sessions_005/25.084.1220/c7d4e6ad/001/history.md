
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
9 0 0 0 0 5 0 0 0 0
9 0 0 0 0 5 0 0 0 0
6 0 0 0 5 5 0 0 0 0
6 0 0 5 5 5 0 0 0 0
6 0 0 5 0 5 0 0 0 0
4 0 0 0 0 5 0 0 0 0
4 0 0 0 0 5 0 0 0 0
4 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
9 0 0 0 0 9 0 0 0 0
9 0 0 0 0 9 0 0 0 0
6 0 0 0 6 6 0 0 0 0
6 0 0 6 6 6 0 0 0 0
6 0 0 6 0 6 0 0 0 0
4 0 0 0 0 4 0 0 0 0
4 0 0 0 0 4 0 0 0 0
4 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 5 0 0 0 0
8 0 0 0 0 5 0 0 0 0
8 0 0 5 5 5 0 0 0 0
2 0 0 5 0 0 0 0 0 0
2 0 0 5 0 0 0 0 0 0
2 0 0 5 5 5 5 0 0 0
2 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 8 0 0 0 0
8 0 0 0 0 8 0 0 0 0
8 0 0 8 8 8 0 0 0 0
2 0 0 2 0 0 0 0 0 0
2 0 0 2 0 0 0 0 0 0
2 0 0 2 2 2 2 0 0 0
2 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples.

**Perception**

1.  **Grid Structure:** Both input and output grids are 10x10. The primary background color is white (0).
2.  **Input Objects:**
    *   There are distinct colored objects located exclusively in the first column (column 0). These objects have different colors (maroon, magenta, yellow in the first example; azure, red in the second).
    *   There is another object composed entirely of gray (5) pixels, located elsewhere in the grid, separate from the objects in the first column.
3.  **Output Objects:**
    *   The colored objects in the first column remain unchanged in the output grid.
    *   The gray object from the input grid is no longer present in the output grid.
    *   The locations previously occupied by the gray pixels are now filled with colors. These colors match the colors found in the first column *on the corresponding row*.
4.  **Transformation:** The core transformation involves replacing gray pixels. The replacement color for a gray pixel is determined by the color present in the first column (column 0) of the same row where the gray pixel was located. All other pixels (white background and the objects in the first column) are preserved.

**Facts**


```yaml
- task: Color Replacement based on Row Template
  examples:
    - input:
        grid_size: [10, 10]
        background_color: 0 # white
        objects:
          - type: template_column
            location: column 0
            colors: [9, 6, 4] # maroon, magenta, yellow
            pixels:
              - { row: 1, col: 0, color: 9 }
              - { row: 2, col: 0, color: 9 }
              - { row: 3, col: 0, color: 6 }
              - { row: 4, col: 0, color: 6 }
              - { row: 5, col: 0, color: 6 }
              - { row: 6, col: 0, color: 4 }
              - { row: 7, col: 0, color: 4 }
              - { row: 8, col: 0, color: 4 }
          - type: target_object
            color: 5 # gray
            pixels: # List of some gray pixel locations
              - { row: 1, col: 5 }
              - { row: 2, col: 5 }
              - { row: 3, col: 4 }
              - { row: 3, col: 5 }
              # ... other gray pixels
      output:
        grid_size: [10, 10]
        background_color: 0 # white
        objects:
          - type: template_column # Unchanged from input
            location: column 0
            colors: [9, 6, 4]
            pixels: # Same as input
              - { row: 1, col: 0, color: 9 }
              # ...
          - type: replaced_object # Derived from target_object
            pixels: # Corresponding output locations for input gray pixels
              - { row: 1, col: 5, color: 9 } # Replaced with color from row 1, col 0
              - { row: 2, col: 5, color: 9 } # Replaced with color from row 2, col 0
              - { row: 3, col: 4, color: 6 } # Replaced with color from row 3, col 0
              - { row: 3, col: 5, color: 6 } # Replaced with color from row 3, col 0
              # ... other replaced pixels
      relationship: The color of a gray (5) pixel in the input grid is replaced by the color found in column 0 of the same row in the input grid. All other pixels retain their original color.
    - input: # Second example similar structure
        grid_size: [10, 10]
        background_color: 0
        objects:
          - type: template_column
            location: column 0
            colors: [8, 2] # azure, red
          - type: target_object
            color: 5 # gray
      output:
        grid_size: [10, 10]
        background_color: 0
        objects:
          - type: template_column # Unchanged
            location: column 0
            colors: [8, 2]
          - type: replaced_object # Derived from target_object, colors based on template_column and row index
      relationship: Same relationship applies.
  general_rule:
    action: Replace color
    source_pixels: Pixels with color 5 (gray).
    target_pixels: Same locations as source_pixels.
    replacement_logic: For each gray pixel at (row, col), find the color of the pixel at (row, 0) in the input grid. Use this color as the replacement color for the output pixel at (row, col).
    unchanged_pixels: All non-gray pixels maintain their original color and position.
```


**Natural Language Program**

1.  Create a copy of the input grid to serve as the basis for the output grid.
2.  Iterate through each cell (pixel) of the input grid, identified by its row index `r` and column index `c`.
3.  For the current cell at `(r, c)`:
    *   Check if the color of the pixel is gray (5).
    *   If it is gray:
        *   Identify the color of the pixel located in the first column (column 0) of the same row `r` in the *input* grid. Let this color be `template_color`.
        *   Update the cell at `(r, c)` in the *output* grid with this `template_color`.
    *   If the pixel is not gray, leave the corresponding cell in the output grid unchanged (it retains the copied value from step 1).
4.  Return the modified grid as the output.
