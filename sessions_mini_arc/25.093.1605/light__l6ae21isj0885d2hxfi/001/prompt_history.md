
## train_1

**input:**
```
0 0 2 0 0
0 0 2 0 0
2 2 4 2 2
0 0 2 0 0
0 0 2 0 0
```


**output:**
```
4 0 0 0 4
0 4 0 4 0
0 0 4 0 0
0 4 0 4 0
4 0 0 0 4
```


## train_2

**input:**
```
0 3 3 0 0
0 3 3 0 0
0 5 3 0 0
0 3 3 0 0
0 3 3 0 0
```


**output:**
```
0 0 0 5 0
5 0 5 0 0
0 5 0 0 0
5 0 5 0 0
0 0 0 5 0
```


## train_3

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 1 1
0 0 0 1 6
```


**output:**
```
6 0 0 0 0
0 6 0 0 0
0 0 6 0 0
0 0 0 6 0
0 0 0 0 6
```


## train_4

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 7 7 7 0
0 7 2 7 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
2 0 0 0 2
0 2 0 2 0
0 0 2 0 0
```

Okay, I will analyze the provided examples to understand the transformation task.

### Perception

1.  **Input/Output Format:** Both input and output are represented as 5x5 grids containing single digits (0-9). The digit '0' appears to function as a background color/value.
2.  **Core Transformation Element:** The transformation seems to hinge on identifying a specific, unique cell within the input grid. I'll call this the "kernel" cell.
3.  **Kernel Identification:** The kernel cell seems to be characterized by its value (color). In grids containing distinct groups of non-zero colors, the kernel is the cell whose color forms a group of size one, distinct from larger adjacent groups of other colors.
    *   In `train_1`, the '4' is unique compared to the connected '2's.
    *   In `train_2`, the '5' is unique compared to the connected '3's.
    *   In `train_3`, the '6' is unique compared to the connected '1's.
    *   In `train_4`, the '2' is unique compared to the connected '7's.
    The kernel has both a value (`kernel_value`) and a position (`kernel_r`, `kernel_c`).
4.  **Output Construction:** The output grid is generated based on the identified kernel.
    *   It has the same dimensions as the input (5x5).
    *   It is initially filled with the background color '0'.
    *   The `kernel_value` is then "painted" onto the output grid.
    *   The *pattern* of the painted cells corresponds to all cells lying on the four diagonal lines extending outwards from the kernel's position (`kernel_r`, `kernel_c`) until they hit the grid boundaries. The kernel cell itself is included. All other cells remain '0'.

### Facts


```yaml
objects:
  - name: input_grid
    type: grid
    properties:
      - dimensions: [5, 5]
      - cells: list of cell objects
  - name: output_grid
    type: grid
    properties:
      - dimensions: [5, 5]
      - cells: list of cell objects
  - name: cell
    type: grid_element
    properties:
      - value: integer (0-9)
      - position: [row, column]
  - name: kernel_cell
    type: cell
    properties:
      - identified_by: being the single instance of its non-zero value, distinct from any adjacent connected groups of other non-zero values.
      - value: kernel_value (integer)
      - position: kernel_position ([kernel_r, kernel_c])

relationships:
  - type: determination
    subject: kernel_cell
    object: input_grid
    details: The kernel_cell (value and position) is determined by analyzing the spatial arrangement and values of non-zero cells in the input_grid.
  - type: creation
    subject: output_grid
    object: kernel_cell
    details: The output_grid's non-zero pattern and value are derived from the kernel_cell's value and position.
  - type: pattern_formation
    subject: output_grid non-zero cells
    object: kernel_position
    details: The positions of non-zero cells in the output grid form diagonal lines radiating from the kernel_position within the grid boundaries.
  - type: value_propagation
    subject: output_grid non-zero cells
    object: kernel_value
    details: The value of all non-zero cells in the output grid is equal to the kernel_value.

actions:
  - name: identify_kernel
    inputs: [input_grid]
    outputs: [kernel_value, kernel_position]
    description: Scan the input grid to find the cell that represents the singular instance of its value, differentiated from surrounding connected non-zero structures. Extract its value and position.
  - name: generate_diagonal_pattern
    inputs: [kernel_position, grid_dimensions]
    outputs: [set_of_coordinates]
    description: Calculate the coordinates of all cells lying on the four diagonal paths starting from kernel_position and extending to the grid boundaries. Include the kernel_position itself.
  - name: create_output
    inputs: [grid_dimensions, kernel_value, set_of_coordinates]
    outputs: [output_grid]
    description: Create a new grid of the specified dimensions, initialize with '0', and place the kernel_value at each coordinate in the set_of_coordinates.

```


### Natural Language Program

1.  **Analyze Input:** Examine the input 5x5 grid. Identify the "kernel" cell: find the cell containing a non-zero value (`kernel_value`) that exists as a single instance, distinct from any surrounding connected components formed by other non-zero values. Record its value (`kernel_value`) and its position (`kernel_r`, `kernel_c`).
2.  **Initialize Output:** Create a new 5x5 grid and fill it entirely with the value 0.
3.  **Trace Diagonals:** Determine the set of all grid coordinates `(r, c)` that satisfy the following conditions, staying within the 0-indexed 5x5 grid boundaries (0 <= r < 5, 0 <= c < 5):
    *   The coordinate `(kernel_r, kernel_c)` itself.
    *   Coordinates `(kernel_r - k, kernel_c - k)` for k = 1, 2, ... while coordinates are valid. (Up-Left)
    *   Coordinates `(kernel_r - k, kernel_c + k)` for k = 1, 2, ... while coordinates are valid. (Up-Right)
    *   Coordinates `(kernel_r + k, kernel_c - k)` for k = 1, 2, ... while coordinates are valid. (Down-Left)
    *   Coordinates `(kernel_r + k, kernel_c + k)` for k = 1, 2, ... while coordinates are valid. (Down-Right)
4.  **Populate Output:** For each coordinate `(r, c)` identified in step 3, set the value of the cell at `(r, c)` in the output grid to `kernel_value`.
5.  **Finalize:** The resulting grid is the final output.
