**Perception of Task Elements:**

1.  **Input:** The input is a 3x3 grid containing single-digit non-negative integers.
2.  **Output:** The output is a 9x9 grid containing single-digit non-negative integers.
3.  **Transformation:** The transformation involves identifying a connected group (component) of non-zero numbers in the input grid. The properties of this component (its bounding box, size, and maximum value) determine the structure and content of the output grid.
4.  **Core Logic:** The process seems to be:
    *   Find the single connected component of non-zero cells in the input (using orthogonal adjacency).
    *   Determine the component's bounding box (`min_row`, `min_col`, `max_row`, `max_col`), height (`h`), and width (`w`).
    *   Calculate a size parameter `s = h * w`.
    *   Find the maximum numerical value (`max_val`) within the component.
    *   Create an empty 9x9 output grid.
    *   Draw two squares in the output grid, both filled with `max_val`.
        *   The first square has its top-left corner at `(min_row, min_col)` and size `s x s`.
        *   The second square has its top-left corner at `(min_row + s, min_col + s)` and size `s x s`.
    *   Ensure drawing stays within the 9x9 output grid boundaries.

**Fact Specification:**


```yaml
task_elements:
  - element: input_grid
    properties:
      - type: grid
      - dimensions: 3x3
      - cell_type: integer
      - cell_range: non-negative
  - element: output_grid
    properties:
      - type: grid
      - dimensions: 9x9
      - cell_type: integer
      - cell_range: non-negative
  - element: non_zero_component
    properties:
      - source: input_grid
      - definition: A group of connected non-zero cells (orthogonal adjacency). Assumed to be a single component per input.
      - attributes:
          - bounding_box: [min_row, min_col, max_row, max_col]
          - height: number of rows in bounding box
          - width: number of columns in bounding box
          - max_value: the maximum integer value within the component cells
          - derived_size: height * width
objects:
  - object: input_grid
    description: The source 3x3 numerical grid.
  - object: non_zero_component
    description: The identified connected block of non-zero values in the input grid.
  - object: output_grid
    description: The target 9x9 numerical grid.
  - object: generated_square
    description: A square shape drawn onto the output grid. Two such squares are generated.
    properties:
      - fill_value: max_value from the non_zero_component
      - size: derived_size x derived_size (from non_zero_component)
      - position: determined by the non_zero_component's bounding_box top-left corner and derived_size.
relationships:
  - type: determination
    from: non_zero_component
    to: generated_square properties (fill_value, size, position)
  - type: composition
    from: generated_square (two instances)
    to: output_grid (squares are drawn onto the initially zero grid)
actions:
  - action: find_connected_component
    actor: system
    input: input_grid
    output: non_zero_component (including its attributes)
  - action: calculate_attributes
    actor: system
    input: non_zero_component geometry
    output: height, width, derived_size
  - action: find_maximum_value
    actor: system
    input: non_zero_component cells
    output: max_value
  - action: initialize_grid
    actor: system
    output: 9x9 zero grid (initial state of output_grid)
  - action: draw_square
    actor: system
    input: output_grid, square_parameters (top-left coords, size, fill_value)
    output: modified output_grid
```


**Natural Language Program:**

1.  Receive the 3x3 input grid.
2.  Identify all cells containing a non-zero value. If there are no non-zero cells, output a 9x9 grid filled with zeros and stop.
3.  Select one non-zero cell and find the connected component it belongs to, considering only non-zero cells and orthogonal connections (up, down, left, right).
4.  Determine the minimum row (`min_r`), maximum row (`max_r`), minimum column (`min_c`), and maximum column (`max_c`) coordinates occupied by the cells in this component (this defines the bounding box).
5.  Calculate the height (`h`) of the bounding box as `max_r - min_r + 1`.
6.  Calculate the width (`w`) of the bounding box as `max_c - min_c + 1`.
7.  Calculate a size factor `s = h * w`.
8.  Find the maximum integer value (`max_val`) present in any cell belonging to the identified component.
9.  Create a 9x9 output grid and initialize all its cells to zero.
10. Draw the first square: For each cell `(r, c)` in the output grid where `min_r <= r < min_r + s` and `min_c <= c < min_c + s`, set the cell's value to `max_val`. (Ensure `r` and `c` remain within the 0-8 range).
11. Draw the second square: For each cell `(r, c)` in the output grid where `min_r + s <= r < min_r + s + s` and `min_c + s <= c < min_c + s + s`, set the cell's value to `max_val`. (Ensure `r` and `c` remain within the 0-8 range).
12. Output the final 9x9 grid.