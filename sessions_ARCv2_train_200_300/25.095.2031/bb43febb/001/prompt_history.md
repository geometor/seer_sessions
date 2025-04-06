
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 0 0
0 5 5 5 5 5 5 0 0 0
0 5 5 5 5 5 5 0 0 0
0 5 5 5 5 5 5 0 0 0
0 5 5 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0
0 0 0 0 5 5 5 5 5 0
0 0 0 0 5 5 5 5 5 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 0 0
0 5 2 2 2 2 5 0 0 0
0 5 2 2 2 2 5 0 0 0
0 5 2 2 2 2 5 0 0 0
0 5 5 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0
0 0 0 0 5 2 2 2 5 0
0 0 0 0 5 5 5 5 5 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0
5 5 5 5 5 0 5 5 5 0
5 5 5 5 5 0 5 5 5 0
5 5 5 5 5 0 5 5 5 0
5 5 5 5 5 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0
5 2 2 2 5 0 5 5 5 0
5 2 2 2 5 0 5 2 5 0
5 2 2 2 5 0 5 2 5 0
5 5 5 5 5 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

*   **Perception of Elements:**
    *   The input and output are 2D grids of numbers.
    *   The relevant numbers appear to be 0, 5, and 2. 0 acts as a background color.
    *   The number 5 forms contiguous shapes or regions within the grid.
    *   The transformation modifies some of the cells containing '5' to '2'. The cells containing '0' remain unchanged.
    *   The change from '5' to '2' seems dependent on the local neighborhood of the cell. Specifically, '5's that are "interior" to a shape change, while those on the "boundary" do not.
    *   Comparing the two examples reveals that the definition of "interior" isn't simply being surrounded orthogonally by other '5's (as seen in the 'U' shape in train\_2).
    *   Considering the 8 neighbors (orthogonal and diagonal) provides a consistent rule: A cell changes from 5 to 2 if it has more than 5 non-zero neighbors. Otherwise, it remains 5. Cells with 0 remain 0.

*   **YAML Facts:**
    
```yaml
    objects:
      - name: grid
        properties:
          - type: 2D array
          - cells: list of cell objects
      - name: cell
        properties:
          - value: integer (0, 5 initially; 0, 2, 5 in output)
          - position: (row, column)
          - neighbors: list of 8 surrounding cells (including diagonals)

    actions:
      - name: process_grid
         LTM_description: "Iterate through each cell of the input grid and determine its corresponding value in the output grid."
        steps:
          - "For each cell in the input grid:"
          - "  Check the value of the current cell."
          - "  If the value is 0, keep it as 0 in the output."
          - "  If the value is 5:"
          - "    Identify its 8 neighbors (orthogonal and diagonal), handling boundary conditions."
          - "    Count how many of these neighbors have a non-zero value (i.e., are 5 in the input)."
          - "    If the count of non-zero neighbors is greater than 5, set the output cell value to 2."
          - "    Otherwise (if the count is 5 or less), set the output cell value to 5."

    relationships:
      - type: neighborhood
        description: "Each cell (except those on the absolute border of the grid) has 8 neighboring cells (up, down, left, right, and the four diagonals)."
      - type: transformation_condition
        description: "The transformation of a cell's value from 5 to 2 depends on the number of its non-zero neighbors."
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid with the same dimensions as the input grid.
    2.  Iterate through each cell `(r, c)` of the input grid.
    3.  Get the value `v` of the input cell at `(r, c)`.
    4.  If `v` is 0, set the corresponding cell `(r, c)` in the output grid to 0.
    5.  If `v` is 5:
        a.  Count the number of non-zero neighbors (value is not 0) among the 8 cells surrounding `(r, c)` (up, down, left, right, and diagonals), making sure to stay within the grid boundaries. Let this count be `neighbor_count`.
        b.  If `neighbor_count` is greater than 5, set the output cell `(r, c)` to 2.
        c.  Otherwise (if `neighbor_count` is 5 or less), set the output cell `(r, c)` to 5.
    6.  Return the completed output grid.
