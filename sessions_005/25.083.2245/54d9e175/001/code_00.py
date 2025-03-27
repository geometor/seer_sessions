"""
1.  **Identify Horizontal Lines:** Divide the input grid into horizontal lines. A horizontal line is a sequence of digits that are:
    *   Bounded by the digit '5' on both sides, *or*
    *   Bounded by the digit '5' on one side and the edge of the grid on the other, *or*
    *   Bounded by the edges of the grid on both sides.

2.  **Digit Mapping:** For each horizontal line in input, replace all digits (excluding the bounding '5's) according to these rules:
    *   If the non-five digits between the 5 separators, in order, are `0`, `1`, `0`, replace all of those digits with `6`.
    *   If the non-five digits between the 5 separators, in order, are `0`, `2`, `0`, replace all of those digits with `7`.
    *   If the non-five digits between the 5 separators, in order, are `0`, `3`, `0`, replace all of those digits with `8`.
    *   If the non-five digits between the 5 separators, in order, are `0`, `4`, `0`, replace all of those digits with `9`.

3.  **Preserve Separators:** The digit '5' and its position remains unchanged.

4. **Output.** The output grid dimensions will match those of the input grid.
"""

import numpy as np

def find_horizontal_lines(grid):
    lines = []
    for i, row in enumerate(grid):
        current_line = []
        for j, cell in enumerate(row):
            if cell == 5:
                if current_line:
                    lines.append((i, current_line))
                    current_line = []
            else:
                current_line.append((j, cell))
        if current_line:
            lines.append((i, current_line))
    return lines

def transform(input_grid):
    # initialize output_grid
    output_grid = np.full(input_grid.shape, 0, dtype=int)
    
    # Identify Horizontal lines
    lines = find_horizontal_lines(input_grid)
      
    # Digit Mapping and preserve separators.
    for row_index, line in lines:
        
        #Extract the digits from the line data
        digits = [digit for _, digit in line]
        
        # Perform the digit mapping based on observed rules
        if digits == [0, 1, 0]:
            replacement = 6
        elif digits == [0, 2, 0]:
            replacement = 7
        elif digits == [0, 3, 0]:
            replacement = 8
        elif digits == [0, 4, 0]:
            replacement = 9
        else: # handles lines of all 0.
             replacement = 0      
        
        # Place the replacement digits in the output grid, and handle 5's.
        for col_index, original_digit in line:
            output_grid[row_index, col_index] = replacement
    
    # Fill in the 5's.
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i,j] == 5:
                output_grid[i,j] = 5


    return output_grid