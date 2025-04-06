
## train_1

**input:**
```
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
7 8 7 8 7 8 7 0
7 8 7 8 7 8 0 0
7 8 7 8 7 0 0 0
0 8 7 8 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
8 7 8 7 8 7 8
0 7 8 7 8 7 0
0 0 8 7 8 0 0
0 0 0 7 0 0 0
0 0 0 0 0 0 0
```

Okay, let's break down the transformation logic for this task.

**Perception of Elements:**

1.    **Input/Output Format:** Both input and output are 2D grids (matrices) of integers. The dimensions seem to remain consistent between input and output for each example.
2.  **Key Input Feature:** The input grids contain mostly zeros but have a distinct vertical line composed of the number 7.
3.  **Output Pattern:** The output grids also contain zeros, 7s, and a new number, 8. The 7s and 8s form a pattern that seems to originate from the location of the input line of 7s but expands outwards. The original line of 7s in the input is not directly preserved, except potentially the topmost '7'.
4.  **Propagation:** The pattern in the output looks like a wave or propagation spreading from a starting point. The values alternate between 7 and 8 as the pattern spreads.
5.  **Starting Point:** Comparing the two examples, the pattern seems to consistently start from the *topmost* '7' found in the input grid.
6.  **Alternating Values:** Cells adjacent (orthogonally) to a '7' in the output pattern become '8', and cells adjacent to an '8' become '7', provided they haven't been filled yet. This suggests a Breadth-First Search (BFS) or similar layer-by-layer expansion where the value depends on the value of the cell from which it's expanding.

**YAML Facts:**


```yaml
Task: Grid value propagation based on seed location

Objects:
  - Input_Grid:
      Type: 2D integer array
      Contains: Background value (0), Seed value (7)
      Structure: Primarily background values with one or more occurrences of the seed value, often forming a vertical line.
  - Output_Grid:
      Type: 2D integer array
      Dimensions: Same as Input_Grid
      Contains: Background value (0), Propagation values (7, 8)
      Structure: A pattern of alternating propagation values expanding from a specific point, replacing original values.
  - Seed_Cell:
      Identification: The topmost cell in the Input_Grid containing the Seed value (7).
      Properties: Row index, Column index, Value (7).
  - Propagation_Pattern:
      Values: Alternating sequence (7, 8, 7, 8, ...)
      Mechanism: Spreads outwards orthogonally (up, down, left, right) from the Seed_Cell.

Relationships:
  - Origin: The Propagation_Pattern in the Output_Grid originates from the Seed_Cell identified in the Input_Grid.
  - Overwrite: The Propagation_Pattern overwrites the initial content (0s or other 7s from the input) of the Output_Grid cells it covers.
  - Adjacency_Rule: Orthogonally adjacent cells in the Propagation_Pattern have alternating values (if one is 7, its newly filled neighbors are 8, and vice-versa).

Action:
  - Find_Seed: Locate the row and column of the topmost Seed value (7) in the Input_Grid.
  - Initialize_Output: Create an Output_Grid of the same size as the Input_Grid, filled with the background value (0).
  - Propagate:
      Starting_Condition: Place the Seed value (7) at the Seed_Cell location in the Output_Grid.
      Process: Perform a Breadth-First Search (BFS) starting from the Seed_Cell.
      Rule: For each cell visited, assign the alternating value (8 if current is 7, 7 if current is 8) to its unvisited orthogonal neighbors within the grid boundaries. Mark neighbors as visited and add them to the BFS queue.
      Termination: Continue until the BFS queue is empty.
```


**Natural Language Program:**

1.  Create a new grid, `output_grid`, with the same dimensions as the `input_grid`, and initialize all its cells to 0.
2.  Scan the `input_grid` row by row, then column by column, to find the coordinates `(seed_row, seed_col)` of the first cell encountered that contains the value 7.
3.  If no cell with the value 7 is found in the `input_grid`, return the initialized `output_grid`.
4.  If a seed cell `(seed_row, seed_col)` is found:
    a.  Initialize a queue data structure for Breadth-First Search (BFS).
    b.  Initialize a data structure (e.g., a set of coordinate tuples or a boolean grid) called `visited` to keep track of cells that have been assigned a value and added to the queue.
    c.  Set the value of `output_grid[seed_row][seed_col]` to 7.
    d.  Add the tuple `(seed_row, seed_col, 7)` representing (row, column, value) to the queue.
    e.  Add the coordinates `(seed_row, seed_col)` to `visited`.
    f.  While the queue is not empty:
        i.   Dequeue the next element `(current_row, current_col, current_value)`.
        ii.  Determine the `next_value` for neighbors: if `current_value` is 7, `next_value` is 8; otherwise, `next_value` is 7.
        iii. Consider the four orthogonal neighbors: `(current_row - 1, current_col)`, `(current_row + 1, current_col)`, `(current_row, current_col - 1)`, `(current_row, current_col + 1)`.
        iv.  For each neighbor `(neighbor_row, neighbor_col)`:
             1. Check if `(neighbor_row, neighbor_col)` is within the valid bounds of the grid.
             2. Check if `(neighbor_row, neighbor_col)` has *not* been marked as `visited`.
             3. If both checks pass:
                 *   Set `output_grid[neighbor_row][neighbor_col]` to `next_value`.
                 *   Mark `(neighbor_row, neighbor_col)` as `visited`.
                 *   Enqueue the tuple `(neighbor_row, neighbor_col, next_value)`.
5.  Return the completed `output_grid`.
