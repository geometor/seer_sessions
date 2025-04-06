
## train_1

**input:**
```
7 6 6 3 7
7 7 7 4 7
7 7 7 6 7
7 7 6 6 6
7 7 7 6 7
```


**output:**
```
7 3 3 7 7
7 7 7 7 7
7 7 7 4 7
7 7 4 4 4
7 7 7 4 7
```


## train_2

**input:**
```
7 7 7 6
3 7 6 6
7 7 6 7
7 7 7 7
1 6 6 6
7 7 6 7
```


**output:**
```
7 7 7 6
7 7 6 6
7 7 6 7
7 7 7 7
7 1 1 1
7 7 1 7
```

## Perception

The input and output are 2D grids containing single-digit integers. The transformation appears to operate on connected components of identical, non-7 numbers. The number 7 seems to function as a background or neutral element, remaining unchanged. The core logic involves identifying contiguous blocks (horizontally or vertically adjacent) of the same number (other than 7) and then modifying the numbers within those blocks based on two factors: the original number in the block and the size (number of cells) of the block.

Specifically:
1.  Isolated non-6 numbers (components of size 1) are changed to 7.
2.  Components composed of the number 6 are transformed based on their size:
    *   Size 1: Remain 6.
    *   Size 2: Change to 3.
    *   Size 3: Remain 6.
    *   Size 4: Change to 1.
    *   Size 5: Change to 4.
3.  All cells originally containing 7 remain 7.

## Facts


```yaml
elements:
  - element: Grid
    properties:
      - rows: integer
      - columns: integer
      - cells: list of list of integers
  - element: Cell
    properties:
      - value: integer (0-9)
      - row_index: integer
      - column_index: integer
      - is_background: boolean (true if value is 7)
  - element: Component
    properties:
      - cells: list of Cell objects
      - value: integer (the common value of cells in the component, must not be 7)
      - size: integer (number of cells in the component)
      - connectivity: 4-directional (horizontal and vertical adjacency)

actions:
  - action: Identify Components
    description: Scan the input grid to find connected regions of cells sharing the same non-7 value. Use 4-directional adjacency.
    inputs:
      - input_grid: Grid
    outputs:
      - components: list of Component objects

  - action: Transform Component
    description: Apply a specific value transformation to all cells within a component based on its original value and size.
    inputs:
      - component: Component
    outputs:
      - new_value: integer

transformation_rules:
  - rule: Background Preservation
    condition: Cell value is 7.
    action: Keep cell value as 7 in the output.
  - rule: Isolated Non-6 Transformation
    condition: Component size is 1 AND component value is NOT 6.
    action: Change the value of the component's cell to 7.
  - rule: Size-Based Transformation for Value 6
    condition: Component value IS 6.
    sub_rules:
      - condition: Component size is 1.
        action: Keep the value 6.
      - condition: Component size is 2.
        action: Change the value of the component's cells to 3.
      - condition: Component size is 3.
        action: Keep the value 6.
      - condition: Component size is 4.
        action: Change the value of the component's cells to 1.
      - condition: Component size is 5.
        action: Change the value of the component's cells to 4.
      # Note: Assumes no other sizes for value 6 components appear or they remain unchanged.
  - rule: Default Component Preservation
    condition: Applies if no other rule matches a component (e.g., non-6 component with size > 1).
    action: Keep the original value of the component's cells. (Though not observed in examples).

relationships:
  - relationship: Adjacency
    description: Cells are adjacent if they share an edge (horizontally or vertically).
  - relationship: Component Membership
    description: A cell belongs to a component if it shares the same non-7 value as other cells in the component and is connected to them through a path of adjacent cells with that same value.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Create a `visited` grid of the same dimensions, initially all `False`, to keep track of cells already processed as part of a component.
3.  Iterate through each cell (`r`, `c`) of the input grid.
4.  If the cell `(r, c)` has already been visited or its value is 7, continue to the next cell.
5.  If the cell `(r, c)` has not been visited and its value is not 7, start a search (e.g., Breadth-First Search or Depth-First Search) from this cell to find its connected component:
    a.  Initialize a list `current_component_cells` to store the coordinates of cells in the component.
    b.  Initialize a queue or stack for the search, starting with `(r, c)`.
    c.  Mark `(r, c)` as visited.
    d.  Store the `component_value` (the value at `input_grid[r][c]`).
    e.  While the search queue/stack is not empty:
        i.  Dequeue/pop a cell `(curr_r, curr_c)`.
        ii. Add `(curr_r, curr_c)` to `current_component_cells`.
        iii. Examine its four neighbors (up, down, left, right).
        iv. For each valid neighbor `(next_r, next_c)` that is within grid bounds, has not been visited, and has the same `component_value` as the starting cell:
            *   Mark `(next_r, next_c)` as visited.
            *   Enqueue/push `(next_r, next_c)`.
6.  Once the search is complete for the current component, determine its `component_size` (the number of cells in `current_component_cells`).
7.  Determine the `new_value` for the cells in this component based on the `component_value` and `component_size`:
    a.  If `component_value` is not 6 and `component_size` is 1, set `new_value` to 7.
    b.  If `component_value` is 6:
        *   If `component_size` is 1, set `new_value` to 6.
        *   If `component_size` is 2, set `new_value` to 3.
        *   If `component_size` is 3, set `new_value` to 6.
        *   If `component_size` is 4, set `new_value` to 1.
        *   If `component_size` is 5, set `new_value` to 4.
        *   Otherwise (for other sizes, if applicable), set `new_value` to the original `component_value` (6).
    c.  Otherwise (if `component_value` is not 6 and `component_size` > 1), set `new_value` to the original `component_value`.
8.  Iterate through all cell coordinates `(cell_r, cell_c)` stored in `current_component_cells` and update the `output_grid[cell_r][cell_c]` with the calculated `new_value`.
9.  After iterating through all cells in the input grid, the `output_grid` contains the final transformed result. Return the `output_grid`.
