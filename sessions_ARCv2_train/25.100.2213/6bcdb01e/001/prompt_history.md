
## train_1

**input:**
```
8 7 7 8 7 8 7
7 8 8 7 7 7 8
7 7 7 7 7 7 7
7 7 7 7 7 7 8
7 7 7 7 7 8 7
3 3 7 7 8 7 7
7 7 7 8 7 7 7
```


**output:**
```
8 7 7 8 7 8 7
7 8 8 3 3 3 8
7 7 7 3 7 3 7
3 3 3 3 3 3 8
7 7 7 3 7 8 7
3 3 3 3 8 7 7
7 7 7 8 7 7 7
```


## train_2

**input:**
```
7 8 7 8 7
8 7 7 7 8
7 7 7 7 7
7 3 7 7 8
7 3 7 8 7
```


**output:**
```
7 8 7 8 7
8 3 3 3 8
7 3 7 3 7
3 3 3 3 8
7 3 7 8 7
```

## Perception

The task involves transforming a 2D grid of digits based on a spreading or filling rule originating from specific cells.
- The input and output are grids of the same dimensions containing single digits.
- The digits 3, 7, and 8 appear to have distinct roles.
- The digit 3 seems to be the "active" or "source" element.
- The digit 7 seems to be the "background" or "fillable" element.
- The digit 8 seems to be a "barrier" or "boundary" element that stops the spread.
- The transformation involves the digit 3 "spreading" into adjacent cells containing the digit 7. Adjacency is considered horizontal and vertical (not diagonal).
- The spread continues iteratively until no more 7s adjacent to 3s can be converted.
- The initial positions of 3s act as the starting points for the spread.
- Cells containing 8 remain unchanged and block the spread of 3 through them.

## Facts

```yaml
objects:
  - name: grid
    properties:
      - type: 2D array of integers
      - contains cells
  - name: cell
    properties:
      - position: (row, column)
      - value: integer (digit)
  - name: digit_3
    properties:
      - role: source
      - action: spreads_to_neighbors
  - name: digit_7
    properties:
      - role: background
      - state: potentially_replaceable
  - name: digit_8
    properties:
      - role: barrier
      - state: blocks_spread
relationships:
  - type: adjacency
    between: cell
    definition: Cells sharing a horizontal or vertical edge.
  - type: transformation
    input: input_grid
    output: output_grid
    rule: fill_from_sources
actions:
  - name: fill_from_sources
    actor: digit_3
    target: adjacent digit_7 cells
    constraint: blocked_by_digit_8
    effect: changes target cell value from 7 to 3
    condition: continues until no more valid targets exist
```

## Natural Language Program

1.  **Initialize**: Create a copy of the input grid, which will become the output grid.
2.  **Identify Sources**: Find the coordinates of all cells in the input grid that initially contain the digit 3.
3.  **Prepare for Spread**: Create a queue (or similar data structure) and add the coordinates of all identified source cells to it.
4.  **Spread Loop**: While the queue is not empty:
    a.  **Get Current Cell**: Remove one cell's coordinates (row, col) from the front of the queue.
    b.  **Check Neighbors**: Examine the four adjacent cells (up, down, left, right) of the current cell.
    c.  **Process Neighbor**: For each valid neighbor (within grid boundaries):
        i.  **Check if Fillable**: If the neighbor cell in the *output* grid currently contains the digit 7:
            1.  **Fill**: Change the neighbor cell's value in the output grid to 3.
            2.  **Add to Queue**: Add the neighbor cell's coordinates to the queue to continue the spread from this new location.
5.  **Finalize**: Once the queue is empty (meaning no more spreading is possible), the process is complete. The modified grid is the final output.
