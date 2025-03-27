
## train_1

**input:**
```
0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 4 4 4
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0
0 0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 2 2 1 1 1 4 4 4
0 2 2 2 1 1 1 4 4 4
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 2 2 0 0 0 0 0 0 0
0 2 2 0 0 0 0 1 1 0
0 0 0 0 4 4 0 1 1 0
0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 0 4 4 0 1 1 0
0 2 2 0 4 4 0 1 1 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 1 0 2 0 0 0 0 0 0
0 1 0 0 0 0 4 0 0 0
0 0 0 0 0 0 4 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 2 0 0 4 0 0 0
0 1 0 2 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Perception of Task Elements:**

1.  **Input/Output Grids:** The task operates on 2D grids of pixels with different colors. The output grid always has the same dimensions as the input grid.
2.  **Objects:** The input grids contain multiple distinct objects. These objects are rectangular blocks composed of a single non-white color (red, blue, yellow in the examples).
3.  **Background:** The background color is white (0).
4.  **Transformation:** The core transformation involves identifying these colored objects, determining their properties (color, shape, position), removing them from their original positions (leaving white pixels), and rearranging them into a specific configuration in the output grid.
5.  **Output Configuration:** In the output grid, the objects are placed horizontally adjacent to each other, starting from the left edge (column 0). They form a single composite rectangular shape.
6.  **Object Ordering:** The horizontal order of the objects in the output assembly corresponds to their relative horizontal position in the input grid, sorted from left to right based on their leftmost column index.
7.  **Vertical Placement:** The vertical position of the assembled object strip in the output grid depends on the vertical extent of the objects in the input grid and the overall height of the grid. Specifically, the top row of the output strip seems determined by the maximum row index occupied by any object in the input (`max_obj_row`), the common height of the objects (`obj_h`), and potentially the total grid height (`H_grid`). The rule appears to be: calculate a base `start_row = max_obj_row - obj_h + 1`; if `H_grid <= 5`, decrement `start_row` by 1.
8.  **Preservation:** The color and shape (height and width) of each individual object are preserved during the transformation.

**Facts (YAML):**


```yaml
task_type: object_manipulation
elements:
  - type: grid
    properties:
      - background_color: white (0)
      - contains: objects
  - type: object
    properties:
      - shape: rectangle
      - color: non-white (1-9)
      - contiguous: true
      - static: true (in input)
      - consistent_height: all objects within a single example share the same height
actions:
  - action: identify_objects
    inputs: input_grid
    outputs: list_of_objects (with color, shape, position)
    criteria: non-white, contiguous pixels
  - action: sort_objects
    inputs: list_of_objects
    outputs: sorted_list_of_objects
    criteria: minimum_column_index (leftmost position) ascending
  - action: determine_vertical_placement
    inputs:
      - input_grid_height (H_grid)
      - list_of_objects
    outputs: output_start_row
    logic:
      - Find max_obj_row (maximum row index occupied by any object pixel)
      - Find obj_h (common height of objects)
      - Calculate base_start_row = max_obj_row - obj_h + 1
      - If H_grid <= 5, output_start_row = base_start_row - 1
      - Else, output_start_row = base_start_row
  - action: assemble_output
    inputs:
      - output_grid_dimensions (same as input)
      - sorted_list_of_objects
      - output_start_row
    outputs: output_grid
    logic:
      - Create an empty (white) grid.
      - Place objects from sorted_list horizontally adjacent, starting at (output_start_row, 0).
relationships:
  - type: spatial_input
    description: Objects are located at various positions in the input grid.
  - type: spatial_output
    description: Objects are horizontally adjacent, forming a single row block, starting at column 0.
  - type: order_mapping
    description: The horizontal order of objects in the output matches the left-to-right order of objects in the input (based on min column index).
  - type: vertical_position_dependency
    description: The vertical placement of the output block depends on the maximum row index of input objects, object height, and potentially grid height.
```


**Natural Language Program:**

1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
2.  Identify all distinct, contiguous, non-white objects within the input grid. Record their color, shape (height `obj_h` and width), and bounding box coordinates (specifically the minimum column index `min_col`). Assume all identified objects have the same height `obj_h`.
3.  Find the maximum row index (`max_obj_row`) occupied by any pixel belonging to any identified object in the input grid.
4.  Determine the height of the input grid (`H_grid`).
5.  Calculate the target top row index (`output_start_row`) for placing the objects in the output grid using the formula: `start_row = max_obj_row - obj_h + 1`.
6.  Apply an adjustment based on grid height: If `H_grid` is less than or equal to 5, decrement `start_row` by 1. Let the final value be `output_start_row`.
7.  Sort the identified objects based on their minimum column index (`min_col`) in ascending order.
8.  Iterate through the sorted objects:
    *   Keep track of the current horizontal position (`current_col`), initialized to 0.
    *   For each object, place its pixels into the output grid, starting at row `output_start_row` and column `current_col`.
    *   Update `current_col` by adding the width of the object just placed.
9.  Return the final output grid.
