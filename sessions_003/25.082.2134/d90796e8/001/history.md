
## train_1

**input:**
```
3 2 0
0 0 0
0 5 0
```


**output:**
```
8 0 0
0 0 0
0 5 0
```


## train_2

**input:**
```
5 0 0 0 0 0
0 0 3 2 0 0
0 0 0 0 0 0
0 3 0 0 0 2
0 2 0 0 0 0
5 0 0 3 0 0
0 0 0 0 0 0
```


**output:**
```
5 0 0 0 0 0
0 0 8 0 0 0
0 0 0 0 0 0
0 8 0 0 0 2
0 0 0 0 0 0
5 0 0 3 0 0
0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 2 0
3 0 0 0 0 0 3
5 0 2 3 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 2 0
3 2 0 0 0 3 0
0 0 0 5 0 0 0
```


**output:**
```
0 0 0 0 0 2 0
3 0 0 0 0 0 3
5 0 0 8 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
8 0 0 0 0 8 0
0 0 0 5 0 0 0
```

Okay, I'm ready to analyze the provided input-output examples and try to discern the underlying transformation rule. Here's my breakdown of the task:

**Perception of Elements:**

*   The task involves 2D grids of varying sizes.
*   Each cell in the grid contains a single digit integer (0-9), representing a color.
*   The transformation involves changing some of the digits/colors while keeping others the same.
*   The dimensions of the grid (height and width) remain constant between input and output.
*   It seems like colors "red" and "green" are somehow related
*   It seems like specific locations with non-zero colors may drive color changes
*   The transformation appears localized. It does not change all values of a specific
    color

**YAML Block - Facts:**


```yaml
objects:
  - type: grid
    properties:
      - dimensions: variable (but consistent between input and output)
      - cells: contain single-digit integers (0-9) representing colors
  - type: cell
    properties:
      - value: integer (0-9)
      - color: mapped from value (using COLOR_MAP)
      - position: (row, column) coordinates within the grid

actions:
  - type: value_change
    description: The value (and therefore color) of some cells changes.
    conditions:
      - The change seems related by adjaceny of "green" and "red"

relationships:
  - input_grid: transformed_to -> output_grid
  - cell: part_of -> grid
  - cell_value: corresponds_to -> color
  - red_cell: adjacent_or_diagonal_to -> green_cell_in_input_changes_to: blue_cell
```


**Natural Language Program:**

1.  **Iterate** through each cell of the input grid.
2.  **Identify** locations with color "red" and "green".
3.  **Check Adjacency**: For each "red" cell, determine whether it is
    adjacent (horizontally, vertically, or diagonally) to a cell of color
    "green"
4. **Replace** with "azure": When both conditions are met ("red" adjacent to "green"), change the value of the "red" in the output to "azure" (8).
5.  **Preserve Other Cells**: All other cells in the input grid retain their original values in the output grid.

In summary: Red pixels that are next to green pixels become azure pixels. All other pixels remain unchanged.

