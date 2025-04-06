**Perception:**

The task involves extracting a specific rectangular subgrid from a larger input grid. The input grids contain repeating background patterns (like `0 1 2 3`, `0 1 2`, or `0 1`) and embedded rectangular structures. These structures are defined by a solid border of a single digit (e.g., `8` in train_1, `3` in train_2 and train_3), which is distinct from the immediate background pattern. The content inside the border can vary. The output grid corresponds exactly to the largest such bordered rectangle found within the input grid, including its border.

**YAML Facts:**


```yaml
task_elements:
  - object: input_grid
    properties:
      - type: 2D array of integers
      - contains: background_pattern (repeating sequence)
      - contains: bordered_rectangle (one or more)
  - object: bordered_rectangle
    properties:
      - shape: rectangle
      - border: composed of a single, uniform digit (border_digit)
      - interior: can contain various digits
      - location: embedded within the input_grid
      - size: defined by width and height
    relationships:
      - distinct_from: background_pattern (the border_digit is not part of the immediate background sequence)
  - object: output_grid
    properties:
      - type: 2D array of integers
      - content: identical to the largest bordered_rectangle from the input_grid
    relationships:
      - derived_from: input_grid
      - corresponds_to: the bordered_rectangle with the maximum area

actions:
  - action: identify_rectangles
    description: Scan the input_grid to find all rectangular regions enclosed by a solid border of a single digit.
  - action: determine_largest
    description: Calculate the area (width * height) for each identified bordered_rectangle and select the one with the maximum area.
  - action: extract_subgrid
    description: Copy the portion of the input_grid corresponding to the selected largest bordered_rectangle (including its border).
  - action: output_result
    description: Return the extracted subgrid.
```


**Natural Language Program:**

1.  Iterate through each cell of the input grid.
2.  If a cell contains a digit that could potentially form the top-left corner of a rectangular border, attempt to identify a complete rectangular frame originating from this cell, where all border cells contain the same digit.
3.  Keep track of all valid bordered rectangles found. A valid rectangle must have a border composed entirely of the same single digit.
4.  For each valid bordered rectangle found, calculate its area (width multiplied by height).
5.  Identify the bordered rectangle with the largest area among all found rectangles.
6.  Extract the subgrid from the input grid that corresponds exactly to the bounding box of this largest bordered rectangle (including the border cells).
7.  Return this extracted subgrid as the output.