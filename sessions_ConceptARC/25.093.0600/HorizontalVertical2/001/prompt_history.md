
## train_1

**input:**
```
2 3 2 3 2 2 0 0 0 0 0 0 0 0
2 3 2 3 2 2 0 0 0 0 0 0 0 0
2 3 2 3 2 2 0 2 2 2 2 2 2 0
2 3 2 3 2 2 0 2 2 2 2 2 2 0
2 3 2 3 2 2 0 3 3 3 3 3 3 0
2 3 2 3 2 2 0 2 2 2 2 2 2 0
0 0 0 0 0 0 0 3 3 3 3 3 3 0
0 2 3 2 3 2 0 2 2 2 2 2 2 0
0 2 3 2 3 2 0 0 0 0 0 0 0 0
0 2 3 2 3 2 0 0 0 0 0 0 0 0
0 2 3 2 3 2 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2 2 2 2 0
0 0 0 0 0 0 0 2 2 2 2 2 2 0
0 0 0 0 0 0 0 3 3 3 3 3 3 0
0 0 0 0 0 0 0 2 2 2 2 2 2 0
0 0 0 0 0 0 0 3 3 3 3 3 3 0
0 0 0 0 0 0 0 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0
0 8 8 8 8 8 0 1 6 1 6 1
0 4 4 4 4 4 0 1 6 1 6 1
0 8 8 8 8 8 0 1 6 1 6 1
0 4 4 4 4 4 0 1 6 1 6 1
0 8 8 8 8 8 0 1 6 1 6 1
0 4 4 4 4 4 0 1 6 1 6 1
0 4 4 4 4 4 0 1 6 1 6 1
0 4 4 4 4 4 0 1 6 1 6 1
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

*   **perception**: The input grids contain numerical values, predominantly zeros forming a background. Within this background, there are distinct rectangular blocks composed of non-zero digits. In each example, there appear to be two such blocks separated by at least one column of zeros. The transformation involves selecting one of these blocks and discarding the other, replacing the discarded block's area with zeros. The selection criteria seem to be based on the properties of the blocks themselves. In `train_1`, the right block is kept; in `train_2`, the left block is kept. Comparing the two examples, the block with the larger sum of its constituent digits is retained in the output, while the other block is removed.

*   **facts**:
    
```yaml
    task_type: grid_transformation
    input_elements:
      - type: grid
        description: A 2D array of single digits.
        properties:
          - dimensions: variable (e.g., 11x14, 12x12)
          - background_value: 0
          - objects:
              - type: block
                description: Rectangular or near-rectangular connected components of non-zero digits.
                properties:
                  - connectivity: Typically 4-connectivity (up, down, left, right) defines a component.
                  - separation: Blocks are separated by one or more columns/rows of the background value (0).
                  - values: Contain digits greater than 0.
                  - sum: The sum of all digits within the block.
    output_elements:
      - type: grid
        description: A 2D array of single digits, representing the transformed input.
        properties:
          - dimensions: same as input grid
          - background_value: 0
          - objects:
              - type: block
                description: Only one of the input blocks remains.
                relationship_to_input: This is the input block with the highest sum of its constituent digits.
    transformation:
      action: identify_blocks
      description: Find all distinct connected components (blocks) of non-zero numbers in the input grid.
      action: calculate_sum
      description: For each identified block, calculate the sum of all its digit values.
      action: select_block
      description: Choose the block that has the maximum sum. If there's a tie, the provided examples don't specify a tie-breaker, but the rule seems to uniquely select one block based on sum in the examples.
      action: generate_output
      description: Create a new grid of the same dimensions as the input, filled with the background value (0).
      action: copy_selected_block
      description: Copy the digits from the selected block (the one with the maximum sum) from their original positions in the input grid to the corresponding positions in the new output grid.
    relationships:
      - The output grid retains only the non-zero block from the input grid that possesses the largest sum of its elements. All other non-zero elements from the input are replaced by the background value (0).
    ```

*   **natural language program**:
    1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with zeros.
    2.  Identify all distinct connected blocks of non-zero numbers in the input grid. Consider cells connected horizontally or vertically as part of the same block.
    3.  For each identified block, calculate the sum of the numerical values of all cells within that block.
    4.  Find the block that has the maximum sum among all identified blocks.
    5.  Iterate through the cells of the input grid. If a cell belongs to the block identified in step 4 (the block with the maximum sum), copy its value to the corresponding cell in the output grid.
    6.  Return the resulting output grid.
