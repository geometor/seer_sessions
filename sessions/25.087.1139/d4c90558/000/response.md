**Perception**

1.  **Input Grid Structure:** The input grids contain multiple distinct objects (shapes) defined by contiguous blocks of non-white, non-gray colors. These shapes act as containers.
2.  **Contained Elements:** Within the bounding box defined by each colored shape, there are several gray pixels (color 5). These gray pixels appear to be the primary elements of interest associated with each shape.
3.  **Background:** The background color is white (color 0) and is ignored in the transformation.
4.  **Output Grid Structure:** The output grid is significantly smaller and consists of horizontal rows of pixels.
5.  **Input-Output Relationship:** Each row in the output corresponds to one of the colored shapes found in the input.
6.  **Color Mapping:** The color of each output row matches the color of its corresponding shape in the input.
7.  **Length Encoding:** The number of colored pixels in each output row is equal to the count of gray pixels found within the bounding box of the corresponding shape in the input.
8.  **Ordering:** The rows in the output grid are arranged vertically based on the top-most coordinate of their corresponding shapes in the input grid (top shape first, bottom shape last).
9.  **Padding:** The width of the output grid is determined by the maximum number of gray pixels associated with any single shape. Rows representing shapes with fewer gray pixels are padded with the background color (white) on the right to match this maximum width.

**YAML Facts**


```yaml
task_description: Transform input grid by summarizing information about colored shapes based on enclosed gray pixels.

elements:
  - type: grid
    properties:
      - background_color: white (0)
      - contains_shapes: true
      - contains_inclusions: true

  - type: shape
    properties:
      - definition: Contiguous block of the same non-white, non-gray color.
      - role: container
      - attributes:
        - color: (e.g., magenta, red, azure, blue, orange, green, yellow)
        - location: defined by pixel coordinates
        - bounding_box: minimum rectangle enclosing the shape
        - associated_inclusions: gray pixels within the bounding box

  - type: inclusion
    properties:
      - color: gray (5)
      - location: specific pixel coordinates within the input grid
      - relationship: associated with a shape if located within its bounding box

transformation:
  - action: identify_shapes
    description: Find all distinct shape objects in the input grid.
    inputs: input_grid
    outputs: list_of_shapes (each with color, bounding_box)

  - action: count_inclusions_per_shape
    description: For each identified shape, count the number of gray pixels within its bounding box.
    inputs: list_of_shapes, input_grid
    outputs: list_of_shape_summaries (each with color, gray_count, top_coordinate)

  - action: sort_shapes
    description: Sort the shape summaries based on their top-most coordinate in ascending order.
    inputs: list_of_shape_summaries
    outputs: sorted_shape_summaries

  - action: determine_output_dimensions
    description: Calculate the height (number of shapes) and width (maximum gray_count) of the output grid.
    inputs: sorted_shape_summaries
    outputs: output_height, output_width

  - action: construct_output_grid
    description: Create the output grid. For each sorted shape summary, create a row using its color repeated 'gray_count' times, padded with white to match 'output_width'.
    inputs: sorted_shape_summaries, output_height, output_width, background_color (white)
    outputs: output_grid

output_specification:
  - type: grid
    properties:
      - height: number of shapes found in input
      - width: maximum count of gray pixels associated with any single shape
      - structure: rows representing shapes, ordered top-to-bottom based on input position
      - content: each row contains the shape's color repeated N times (N = gray count), padded with white.
```


**Natural Language Program**

1.  Identify all distinct, connected shapes in the input grid that are not white (0) or gray (5). For each shape, record its color, determine its bounding box (the smallest rectangle enclosing all its pixels), and find its top-most row coordinate.
2.  For each identified shape, count how many gray (5) pixels are located strictly within its bounding box. Record this count for each shape.
3.  Determine the maximum gray pixel count found across all shapes. This will be the width of the output grid.
4.  Determine the number of shapes found. This will be the height of the output grid.
5.  Sort the shapes based on their top-most row coordinate in ascending order (top to bottom).
6.  Construct the output grid row by row based on the sorted shapes:
    *   For each shape in the sorted list:
        *   Create a row.
        *   Fill the beginning of the row with the shape's color, repeated a number of times equal to its associated gray pixel count.
        *   Fill the remainder of the row (up to the maximum width determined in step 3) with the white (0) background color.
7.  Return the constructed output grid.