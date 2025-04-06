
## train_1

**input:**
```
8 8 0 0 2 2 0
0 8 8 0 2 2 8
0 0 0 8 0 8 0
8 0 0 0 0 0 0
0 2 2 0 8 0 8
0 2 2 8 8 0 8
```


**output:**
```
0
```


## train_2

**input:**
```
8 0 0 0 0 8 0
0 0 2 2 0 8 0
8 0 2 2 0 0 0
0 0 8 0 0 8 0
0 0 8 2 2 0 8
8 0 0 2 2 8 0
```


**output:**
```
8
```


## train_3

**input:**
```
8 0 0 2 2 8
8 0 8 2 2 0
0 0 0 0 8 0
2 2 8 0 8 0
2 2 0 0 0 8
0 8 8 0 8 0
```


**output:**
```
0
```


## train_4

**input:**
```
0 8 0 0 0 0 0
2 2 0 8 8 8 0
2 2 8 8 0 2 2
0 0 8 0 0 2 2
0 8 0 0 8 0 0
```


**output:**
```
8
```


## train_5

**input:**
```
8 2 2 8 8 0 0
0 2 2 0 0 0 8
0 8 8 0 0 8 0
0 0 8 0 0 0 8
8 0 8 8 8 2 2
8 0 0 0 0 2 2
```


**output:**
```
8
```


## train_6

**input:**
```
0 0 8 0 8
2 2 8 0 0
2 2 0 0 8
0 0 0 2 2
8 8 0 2 2
```


**output:**
```
0
```

*   **Perception of Task Elements:**
    *   The input is a grid represented as a multi-line string of space-separated digits.
    *   The digits observed in the input grids are 0, 2, and 8.
    *   The size (rows and columns) of the input grid varies across examples.
    *   The output is always a single digit: either 0 or 8.
    *   The digit '2' often appears in adjacent horizontal pairs (`2 2`).
    *   In some inputs, these horizontal pairs are stacked vertically to form 2x2 squares of `2`s (`[[2, 2], [2, 2]]`).
    *   The transformation logic appears to depend on two factors: the shape of the grid (square vs. non-square) and the presence of these 2x2 squares of `2`s.

*   **Facts:**
    
```yaml
    objects:
      - name: input_grid
        properties:
          - type: 2D array of integers
          - digits: [0, 2, 8]
          - rows: integer (number of rows)
          - columns: integer (number of columns)
          - shape: derived property (square if rows == columns, non-square otherwise)
      - name: two_by_two_square_pattern
        properties:
          - structure: [[2, 2], [2, 2]]
          - exists_in_grid: boolean (whether at least one instance is found in input_grid)
      - name: output_value
        properties:
          - type: integer
          - possible_values: [0, 8]

    actions:
      - name: parse_input
        description: Convert the input string into the input_grid object.
      - name: calculate_dimensions
        description: Determine the rows and columns properties of the input_grid.
      - name: check_grid_shape
        description: Determine the shape property (square or non-square) of the input_grid.
      - name: search_for_pattern
        description: Iterate through all 2x2 subgrids of input_grid to determine if the two_by_two_square_pattern exists. Update the exists_in_grid property.
      - name: determine_output
        description: Calculate the output_value based on the grid shape and pattern existence.

    relationships:
      - The output_value depends on the input_grid's shape.
      - If the input_grid's shape is non-square, the output_value depends on whether the two_by_two_square_pattern exists_in_grid.
    ```


*   **Natural Language Program:**
    1.  Read the input string and parse it into a 2D grid of integers.
    2.  Determine the number of rows and columns in the grid.
    3.  Check if the number of rows is equal to the number of columns (i.e., if the grid is square).
    4.  If the grid is square, the output is 0.
    5.  If the grid is not square:
        a.  Search the grid for any 2x2 subgrid that consists entirely of the digit 2 (i.e., `[[2, 2], [2, 2]]`).
        b.  If at least one such 2x2 subgrid of `2`s is found, the output is 8.
        c.  If no such 2x2 subgrid of `2`s is found, the output is 0.
