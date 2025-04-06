
## train_1

**input:**
```
0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 0 0 0
0 5 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 2 2 0 0 0
0 0 0 0 5 2 2 0 0 0
0 0 0 0 0 5 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 5 0
0 0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0
0 0 0 2 2 5 0 0 0 0
0 0 0 2 2 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

*   **Perception of Elements:**
    *   The task operates on a 2D grid containing numerical values.
    *   The primary elements are the background (value 0), a static 2x2 block (value 2), and moving objects (value 5).
    *   The transformation involves relocating the '5' objects based on their proximity to the '2' block.

*   **YAML Facts:**
    
```yaml
    task_description: Relocate objects towards a central block in a grid.
    elements:
      - object: grid
        properties:
          - type: 2D array
          - size: 10x10 (based on examples)
          - cell_values: [0, 2, 5]
      - object: target_block
        value: 2
        properties:
          - shape: 2x2
          - static: true
          - role: attractor/destination boundary
      - object: mover
        value: 5
        properties:
          - dynamic: true
          - role: entity to be moved
          - movement: directed towards target_block
          - stopping_condition: adjacent to target_block (just before collision)
    relationships:
      - type: proximity
        between: mover (5)
        and: target_block (2)
        influences: movement direction and stopping point
    actions:
      - name: identify_elements
        inputs: input_grid
        outputs: coordinates of target_block, coordinates of movers
      - name: calculate_movement
        inputs: mover_position, target_block_coordinates
        process: Determine shortest path step towards the closest cell in target_block.
        outputs: next_position
      - name: update_grid
        inputs: input_grid, final_mover_positions, target_block_coordinates
        process: Create output grid with target_block and final mover positions, filling rest with 0.
        outputs: output_grid
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid of the same dimensions as the input grid, filled with zeros.
    2.  Locate the 2x2 block of cells with value 2 in the input grid. Copy these four '2' values to their corresponding positions in the output grid.
    3.  Identify the coordinates (row, column) of all cells with value 5 in the input grid.
    4.  For each cell containing a '5' at `(start_row, start_col)`:
        a.  Initialize its current position `(curr_row, curr_col)` to `(start_row, start_col)`.
        b.  Start a movement loop:
            i.  Find the cell `(target_row, target_col)` within the 2x2 block of '2's that has the minimum Manhattan distance (`|target_row - curr_row| + |target_col - curr_col|`) from the current position `(curr_row, curr_col)`. If there are multiple such cells, any one can be chosen.
            ii. Calculate the step direction towards the chosen target cell: `step_row = sign(target_row - curr_row)` and `step_col = sign(target_col - curr_col)`, where `sign(x)` is -1 if x < 0, 1 if x > 0, and 0 if x = 0.
            iii. Determine the next potential position: `next_row = curr_row + step_row`, `next_col = curr_col + step_col`.
            iv. Check if the cell at `(next_row, next_col)` in the *input* grid contains the value 2.
            v.  If `(next_row, next_col)` contains a 2, the movement for this '5' stops. The final position is the *current* position `(curr_row, curr_col)`. Exit the movement loop for this '5'.
            vi. If `(next_row, next_col)` does not contain a 2, update the current position: `curr_row = next_row`, `curr_col = next_col`. Continue the movement loop from step 4.b.i.
        c.  Once the loop terminates, place the value 5 at the determined final position `(curr_row, curr_col)` in the output grid.
    5.  Return the completed output grid.
