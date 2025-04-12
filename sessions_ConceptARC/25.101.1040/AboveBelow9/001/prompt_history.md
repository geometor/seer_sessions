
## train_1

**input:**
```
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 3 0 0 3 3 0 0 0 0 0
0 0 3 0 0 3 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 7 7 7 7 7 7 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 7 7 7 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 7 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 0 0 0 0 0
```


**output:**
```
0 0 0 0 7 7 7 7 7 7 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input grids contain a prominent horizontal line of yellow pixels (color 4).
    *   There are other colored objects (green in the first example, orange in the second) distributed in the grid, both above and below the yellow line.
    *   The background color is white (color 0).
    *   In the output grids, the yellow line remains unchanged.
    *   All pixels and objects *above* the yellow line remain unchanged.
    *   All pixels *below* the yellow line are changed to the background color (white/0), effectively removing any objects that were previously below the yellow line.
    *   The yellow line acts as a separator or boundary. The transformation selectively removes content based on its position relative to this boundary.

*   **Facts:**
    
```yaml
    elements:
      - object: grid
        description: A 2D array of pixels with colors 0-9.
      - object: separator_line
        properties:
          - color: yellow (4)
          - shape: horizontal line spanning the width of the grid
          - role: boundary defining regions (above, below)
      - object: content_pixels
        properties:
          - color: non-white (colors 1-9, excluding the separator color in its row)
          - position: relative to the separator_line (above or below)
      - object: background_pixels
        properties:
          - color: white (0)

    relationships:
      - type: spatial
        description: Content pixels are either located in rows above the separator_line or in rows below the separator_line.

    actions:
      - name: identify_separator
        inputs: grid
        outputs: row_index_of_separator_line
        description: Find the row index containing the horizontal yellow line.
      - name: preserve_above
        inputs: grid, row_index_of_separator_line
        outputs: portion_of_output_grid
        description: Copy all rows from the input grid up to and including the separator_line row to the output grid.
      - name: remove_below
        inputs: grid_dimensions, row_index_of_separator_line
        outputs: portion_of_output_grid
        description: Fill all rows below the separator_line row in the output grid with the background color (white/0).
    ```


*   **Natural Language Program:**
    1.  Identify the row containing the horizontal yellow (4) line which acts as a separator.
    2.  Create an output grid of the same dimensions as the input grid.
    3.  Copy all rows from the input grid, up to and including the separator row, directly to the corresponding rows in the output grid.
    4.  Fill all rows in the output grid *below* the separator row with the background color (white/0).
