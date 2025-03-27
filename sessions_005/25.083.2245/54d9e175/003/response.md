```python
"""
1.  **Replicate Grid:** Create an exact copy of the input grid. This copy will become the output grid.

2.  **Identify Horizontal Lines:** Within each row of the *input* grid, identify horizontal lines. A horizontal line is a sequence of digits that is:
    *   Delimited by the digit '5' on both sides, *or*
    *   Delimited by the digit '5' on one side and the edge of the grid on the other, *or*
    *   Delimited by the edges of the grid on both sides (if no '5's are present in the row).

3.  **Digit Mapping:** For each horizontal line identified in the *input* grid, extract the sequence of digits *excluding* any bounding '5's. Apply the following mapping rules to these digits, and make the replacements in the corresponding positions of the *output* grid:
    *   If the sequence is `0`, `1`, `0`, replace all digits in that line segment in the output grid with `6`.
    *   If the sequence is `0`, `2`, `0`, replace all digits in that line segment in the output grid with `7`.
    *   If the sequence is `0`, `3`, `0`, replace all digits in that line segment in the output grid with `8`.
    *   If the sequence is `0`, `4`, `0`, replace all digits in that line segment in the output grid with `9`.

4.  **Preserve Separators and Other Digits:** The digit '5', and all other digits that do not belong to a transformed line, maintain their original values and positions from the input grid to the output grid. Ensure these are correctly copied during the initial replication.

5. **Output.** Return the modified copy of the grid (the output grid).
"""

import numpy as np

def find_horizontal_lines(grid):
    lines = []
    for i, row in enumerate(grid):
        current_line = []
        start = 0
        for j, cell in enumerate(row):
            if cell == 5:
                if j > start:
                    lines.append((i, list(range(start, j))))
                start = j + 1
        if start < len(row):
            lines.append((i, list(range(start, len(row)))))
    return lines

def transform(input_grid):
    # Replicate Grid
    output_grid = np.copy(input_grid)

    # Identify Horizontal Lines
    lines = find_horizontal_lines(input_grid)

    # Digit Mapping
    for row_index, col_indices in lines:
        # Extract digits from the input grid
        digits = [input_grid[row_index, col] for col in col_indices]

        # Check if the line needs transformation based on mapping rules.
        if all(d in [0, 1, 2, 3, 4] for d in digits):  # Important: Only consider lines with 0-4 for transformation.
           if digits == [0, 1, 0]:
              replacement = 6
           elif digits == [0, 2, 0]:
              replacement = 7
           elif digits == [0, 3, 0]:
              replacement = 8
           elif digits == [0, 4, 0]:
              replacement = 9
           else:
              replacement = None # no replacement

           # Apply replacement in the output grid
           if replacement is not None:
              for col_index in col_indices:
                 output_grid[row_index, col_index] = replacement

    return output_grid
```