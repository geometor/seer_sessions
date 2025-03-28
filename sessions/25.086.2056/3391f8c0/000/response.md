*   **Perception of Task Elements**:
    *   The input grids contain multiple distinct objects composed of contiguous pixels of the same non-white color.
    *   Each input grid features exactly two different non-white colors.
    *   The background color is consistently white (0).
    *   In the output grids, the shapes and positions of all objects are preserved exactly as they were in the input.
    *   The key transformation is a color swap: all pixels of the first non-white color in the input become the second non-white color in the output, and vice-versa.
    *   The white background pixels remain unchanged.

*   **YAML Facts**:
    
```yaml
    observations:
      - element: grid
        description: A 2D array of pixels with integer values representing colors.
        properties:
          - background_color: white (0)
          - contains: objects
      - element: object
        description: A contiguous block of pixels of the same non-white color.
        properties:
          - color: A specific non-white color (1-9).
          - shape: The geometric form defined by the arrangement of pixels.
          - position: The coordinates of the pixels within the grid.
      - element: task_rule
        description: The transformation involves swapping the colors of the objects.
        details:
          - Identify the two distinct non-white colors present in the input grid (Color A and Color B).
          - All pixels initially having Color A are changed to Color B in the output.
          - All pixels initially having Color B are changed to Color A in the output.
          - All white pixels remain unchanged.
          - The shape and position of all objects are preserved.
    examples:
      - train_1:
          - input_colors: [green (3), azure (8)]
          - output_colors: [azure (8), green (3)]
          - action: Swap green and azure.
      - train_2:
          - input_colors: [red (2), green (3)]
          - output_colors: [green (3), red (2)]
          - action: Swap red and green.
      - train_3:
          - input_colors: [blue (1), orange (7)]
          - output_colors: [orange (7), blue (1)]
          - action: Swap blue and orange.
      - train_4:
          - input_colors: [azure (8), blue (1)]
          - output_colors: [blue (1), azure (8)]
          - action: Swap azure and blue.
    ```


*   **Natural Language Program**:
    1.  Scan the input grid to identify all unique non-white pixel values (colors). There will be exactly two such colors; let them be `color1` and `color2`.
    2.  Create a new grid of the same dimensions as the input grid, initially filled with the background color (white, 0).
    3.  Iterate through each pixel (cell) of the input grid at position (row, column).
    4.  If the input pixel's color is `color1`, set the corresponding pixel in the new grid at (row, column) to `color2`.
    5.  If the input pixel's color is `color2`, set the corresponding pixel in the new grid at (row, column) to `color1`.
    6.  If the input pixel's color is white (0), set the corresponding pixel in the new grid at (row, column) to white (0).
    7.  The completed new grid is the output.