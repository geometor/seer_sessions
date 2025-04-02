*   **Perception of Task Elements:**
    *   The input grids consistently contain exactly two distinct, non-touching objects against a white background.
    *   One object is always blue (color 1).
    *   The other object is always green (color 3).
    *   The objects can vary in shape (lines, rectangles, single pixels) and size.
    *   The output grid contains only one of the objects from the input grid.
    *   The output object is cropped to its minimal bounding box.
    *   Comparing the input and output across examples reveals that the selection criterion is based on the vertical position of the objects. The object that appears higher up in the grid (i.e., has pixels in rows with lower indices) is the one selected for the output.

*   **YAML Facts:**
    
```yaml
    task_description: Identify the blue (1) and green (3) objects in the input grid and select the one positioned higher vertically. Output the selected object cropped to its minimal bounding box.

    elements:
      - element: grid
        description: A 2D array of pixels with colors represented by integers 0-9. Background is white (0).
      - element: object
        description: A contiguous block of non-white pixels of the same color.
        properties:
          - color: The integer value (1 for blue, 3 for green).
          - pixels: Set of coordinates (row, col) belonging to the object.
          - bounding_box: The smallest rectangle containing all object pixels.
          - min_row_index: The smallest row index among all object pixels.

    relationships:
      - type: spatial_position
        description: Comparing the vertical position of the blue and green objects.
        based_on: min_row_index property. One object is 'higher' if its min_row_index is less than the other's.

    actions:
      - action: identify_objects
        description: Locate and separate the contiguous blue object and the contiguous green object.
        inputs: input_grid
        outputs: blue_object, green_object
      - action: determine_vertical_position
        description: Find the minimum row index for both the blue and green objects.
        inputs: blue_object, green_object
        outputs: min_row_blue, min_row_green
      - action: select_higher_object
        description: Choose the object with the smaller minimum row index.
        inputs: blue_object, green_object, min_row_blue, min_row_green
        outputs: selected_object
      - action: extract_bounding_box
        description: Create a new grid containing only the pixels of the selected object, cropped to its minimal bounding box dimensions.
        inputs: selected_object
        outputs: output_grid
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous group of blue (1) pixels, representing the blue object.
    2.  Identify the contiguous group of green (3) pixels, representing the green object.
    3.  Determine the topmost row index occupied by any pixel of the blue object.
    4.  Determine the topmost row index occupied by any pixel of the green object.
    5.  Compare these topmost row indices. Select the object (either blue or green) whose topmost row index is smaller (meaning it appears higher in the grid).
    6.  Create a new output grid that contains only the pixels of the selected object, cropped to its minimal bounding box (the smallest rectangle enclosing the object).