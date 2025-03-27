*   **Perception of the task elements:**
    *   The input is a grid containing several distinct geometric shapes (objects) made of different colors (blue, red, green, yellow, orange, azure) on a white background.
    *   The output is a small, single-column grid listing specific colors found in the input.
    *   The task requires identifying the colors present in the input grid (excluding the white background) and ordering them based on certain properties of the corresponding objects.
    *   In each example, there are exactly three different non-background colors, and the output is always a 3x1 grid containing these three colors.
    *   The order of colors in the output depends on the properties of the objects in the input grid. Specifically, the size (number of pixels) of the objects associated with each color seems primary, with positional information (minimum row index) used as a secondary sorting criterion.

*   **Facts:**
    
```yaml
    elements:
      - type: grid
        role: input
        description: A 2D grid containing pixels of different colors, forming distinct objects against a white (0) background.
      - type: grid
        role: output
        description: A 3x1 (column) grid containing single pixels representing colors found in the input grid.
      - type: object
        description: Contiguous blocks of non-white pixels in the input grid. Each color present forms one or more such objects. For this task, we consider all pixels of a given color together.
      - type: color
        description: An integer value from 1 to 9 representing a specific color. The background color is white (0).
      - type: property
        name: size
        description: The total count of pixels for a given non-white color in the input grid.
      - type: property
        name: min_row
        description: The smallest row index (0-based, top-to-bottom) where a given non-white color appears in the input grid.
      - type: action
        name: identify_colors
        description: Find all unique non-white colors present in the input grid.
      - type: action
        name: calculate_properties
        description: For each identified color, calculate its size (pixel count) and its minimum row index.
      - type: action
        name: sort_colors
        description: Arrange the identified colors based on a specific order.
          - Primary criterion: Sort by size in descending order.
          - Secondary criterion (tiebreaker): If sizes are equal, sort by minimum row index in ascending order.
      - type: relationship
        description: The output grid contains the colors identified from the input, sorted according to the `sort_colors` action. The output format is a column vector (3x1 grid).

    ```


*   **Natural Language Program:**
    1.  Identify all unique colors present in the input grid, ignoring the background color (white, 0).
    2.  For each unique non-white color found:
        a.  Count the total number of pixels of that color in the grid (this is the color's 'size').
        b.  Find the minimum row index (topmost row) where this color appears (this is the color's 'min_row').
    3.  Create a list of the identified colors.
    4.  Sort this list of colors based on the following criteria:
        a.  Primarily, sort in descending order of their 'size'.
        b.  Secondarily, if two colors have the same 'size', sort them in ascending order of their 'min_row'.
    5.  Construct the output grid as a single column (3x1) containing the sorted colors in the determined order.