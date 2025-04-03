
## train_1

**input:**
```
0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0
0 0 2 2 2 2 4 0 0
0 0 2 2 2 2 2 0 0
0 0 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 4
```


**output:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0
0 0 2 2 2 2 2 0 0
0 0 2 2 2 2 2 0 0
0 0 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
6 0 0 6 0 0 0 0 6
0 0 0 0 3 0 0 6 0
0 0 0 3 3 3 0 0 0
0 0 3 3 6 3 3 0 0
0 3 3 3 3 6 3 6 0
6 0 3 3 3 3 3 0 0
0 0 0 3 6 3 0 0 0
0 6 0 0 3 0 6 0 0
0 0 6 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 3 3 3 0 0 0
0 0 3 3 3 3 3 0 0
0 3 3 3 3 3 3 3 0
0 0 3 3 3 3 3 0 0
0 0 0 3 3 3 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input and output are grids (matrices) of the same dimensions, filled with integers representing colors (0 being the background).
    *   The input grid contains multiple non-zero colors, often forming distinct shapes or scattered points.
    *   The output grid retains only one of the non-zero colored shapes from the input, replacing all other cells (including those with other non-zero colors) with the background color (0).
    *   The shape retained in the output appears to be the largest contiguous block of a single color present in the input grid. Contiguity is defined by horizontal and vertical adjacency.

*   **Facts:**
    
```yaml
    Objects:
      - Grid: A 2D array of cells.
        Properties:
          - dimensions (rows, columns)
          - cells
      - Cell: An element within the grid.
        Properties:
          - row_index
          - column_index
          - value (color)
      - Block: A connected component of cells sharing the same non-zero color.
        Properties:
          - color
          - size (number of cells)
          - cell_coordinates (list of (row, col) tuples)
        Relationships:
          - Cells within a block are adjacent (horizontally or vertically) to at least one other cell in the same block.

    Actions:
      - Identify Blocks: Scan the input grid to find all distinct contiguous blocks of non-zero colored cells.
      - Determine Largest Block: Compare the identified blocks based on their size (number of cells) and select the block with the maximum size. (Assume a single largest block exists based on examples).
      - Generate Output: Create a new grid of the same dimensions as the input, initialized with the background color (0). Fill the cells corresponding to the coordinates of the largest identified block with that block's color.

    Relationships:
      - Input grid is transformed into the Output grid.
      - The Output grid contains a subset of the non-zero cells from the Input grid, specifically those belonging to the largest block.
    ```


*   **Natural Language Program:**
    1.  Initialize an empty list to store identified blocks and a variable to track the largest block found so far (initially none).
    2.  Create a boolean grid of the same dimensions as the input grid, initialized to `False`, to keep track of visited cells during block identification.
    3.  Iterate through each cell (row `r`, column `c`) of the input grid.
    4.  If the cell `(r, c)` has a non-zero color and has not been visited:
        a.  Start a search (e.g., Breadth-First Search or Depth-First Search) from this cell.
        b.  Identify all reachable cells that are connected (horizontally or vertically) and have the *same* non-zero color as the starting cell `(r, c)`.
        c.  Mark all cells found in this block as visited in the boolean grid.
        d.  Record the block's color, its size (count of cells), and the coordinates of all cells belonging to it.
        e.  Compare the size of this newly found block with the size of the largest block found so far. If the current block is larger, update the largest block record.
    5.  After iterating through all cells, create a new output grid of the same dimensions as the input, filled entirely with the background color (0).
    6.  If a largest block was identified (i.e., the input grid was not entirely background), iterate through the cell coordinates stored for the largest block. For each coordinate `(r_block, c_block)`, set the corresponding cell in the output grid to the color of the largest block.
    7.  Return the generated output grid.
