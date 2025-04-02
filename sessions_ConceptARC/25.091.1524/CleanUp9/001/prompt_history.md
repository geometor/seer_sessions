
## train_1

**input:**
```
0 4 0 0 2 3
4 1 1 2 1 0
0 1 0 0 2 3
0 2 0 0 1 0
0 2 1 1 1 0
0 2 0 0 4 0
```


**output:**
```
0 0 0 0 0 0
0 1 1 1 1 0
0 1 0 0 1 0
0 1 0 0 1 0
0 1 1 1 1 0
0 0 0 0 0 0
```


## train_2

**input:**
```
0 5 5 6 5 6
0 5 0 0 0 6
0 3 0 0 0 5
0 3 0 3 0 5
0 5 5 5 5 5
6 6 0 5 0 3
```


**output:**
```
0 5 5 5 5 5
0 5 0 0 0 5
0 5 0 0 0 5
0 5 0 0 0 5
0 5 5 5 5 5
0 0 0 0 0 0
```

*   **Perception:** The task involves identifying a dominant color pattern within the input grid and using its spatial extent to create a solid rectangular shape in the output grid. The background color is preserved, while all other non-dominant colors are removed. Isolated single pixels of the dominant color are ignored when determining the bounds of the final rectangle.

*   **Facts:**
    
```yaml
    elements:
      - object: grid
        role: input
        attributes:
          - colors: multiple distinct colors present, including a background color (white/0).
          - patterns: scattered pixels of various colors.
      - object: grid
        role: output
        attributes:
          - colors: primarily the background color and one other 'target' color.
          - patterns: a single solid rectangle filled with the 'target' color against the background.
    transformations:
      - action: identify_background_color
        input: input grid
        output: most frequent color in the input grid
        description: Counts the occurrences of each color and selects the most frequent one as the background.
      - action: identify_target_color
        input: input grid, background_color
        output: most frequent non-background color
        description: Counts the occurrences of each non-background color and selects the most frequent one as the target color.
      - action: find_target_pixels
        input: input grid, target_color
        output: list of coordinates for target color pixels
      - action: find_connected_components
        input: list of target pixel coordinates
        output: list of components (each component is a list of coordinates)
        attributes:
          - connectivity: 8-way adjacency (horizontal, vertical, diagonal)
      - action: filter_components
        input: list of components
        output: list of components with size > 1
        description: Removes components that contain only a single pixel.
      - action: calculate_bounding_box
        input: list of filtered components
        output: coordinates of the bounding box (min_row, max_row, min_col, max_col)
        description: Finds the minimum bounding rectangle that encloses all pixels in the filtered components. If no components remain, this step might be skipped or return null.
      - action: create_output_grid
        input: input grid dimensions, background_color, target_color, bounding_box
        output: output grid
        description: Creates a new grid of the same size as the input, filled with the background color. If a bounding box exists, fills the area defined by the bounding box with the target color.
    relationships:
      - The target color in the output is determined by the most frequent non-background color in the input.
      - The position and size of the rectangle in the output are determined by the spatial extent (bounding box) of the significant connected components (size > 1) of the target color pixels in the input.
      - All other colors from the input (except the background and target colors) are replaced by the background color.
      - Single, isolated pixels of the target color in the input do not contribute to defining the bounding box for the output rectangle.
    ```


*   **Natural Language Program:**
    1.  Determine the background color by finding the most frequent color in the input grid.
    2.  Identify the 'target' color by finding the most frequent color *excluding* the background color.
    3.  Locate all pixels in the input grid that match the target color.
    4.  Group these target pixels into connected components using 8-way adjacency (pixels are connected if they touch horizontally, vertically, or diagonally).
    5.  Discard any components that consist of only a single pixel.
    6.  If no components remain after discarding single-pixel ones, create an output grid of the same dimensions as the input, filled entirely with the background color.
    7.  If components remain, calculate the overall bounding box (minimum row, maximum row, minimum column, maximum column) that encloses all pixels belonging to these remaining components.
    8.  Create an output grid of the same dimensions as the input, initially filled with the background color.
    9.  Fill the rectangular area defined by the calculated bounding box (from minimum row to maximum row, and minimum column to maximum column, inclusive) with the target color.
