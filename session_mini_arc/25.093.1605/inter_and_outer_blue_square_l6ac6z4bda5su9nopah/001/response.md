```python
import numpy as np

"""
Transforms an input grid based on the values of orthogonal neighbors for cells containing '0'.

The transformation rules are applied to each cell (r, c) in the input grid:
1. If the cell value `input_grid[r][c]` is not 0, it remains unchanged in the output grid.
2. If the cell value `input_grid[r][c]` is 0, check its orthogonal neighbors:
    a) If the cell is directly between two '5's vertically (neighbor above and neighbor below are both 5), the output cell becomes 1.
    b) If the cell is directly between two '5's horizontally (neighbor left and neighbor right are both 5), the output cell becomes 1.
    c) If the cell has exactly one orthogonal neighbor with value 2 AND exactly one orthogonal neighbor with value 5, the output cell becomes 1.
    d) If the cell has exactly one orthogonal neighbor with value 2 AND zero orthogonal neighbors with value 5, the output cell becomes 1.
3. If none of the above conditions (a, b, c, d) are met for a cell containing 0, it remains 0 in the output grid.
"""

def transform(input_grid):
    """
    Applies transformation rules to a 2D grid.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed grid.
    """
    # Convert input to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Only apply rules if the current cell is 0
            if input_np[r, c] == 0:
                
                # --- Check Rule a: Vertical 5s ---
                rule_a = False
                # Check if neighbors above and below exist and are both 5
                if r > 0 and r < rows - 1:
                    if input_np[r-1, c] == 5 and input_np[r+1, c] == 5:
                        rule_a = True

                # --- Check Rule b: Horizontal 5s ---
                rule_b = False
                # Check if neighbors left and right exist and are both 5
                if c > 0 and c < cols - 1:
                    if input_np[r, c-1] == 5 and input_np[r, c+1] == 5:
                        rule_b = True

                # --- Count orthogonal neighbors for rules c and d ---
                count2 = 0
                count5 = 0
                
                # Check Up neighbor
                if r > 0:
                    neighbor_val = input_np[r-1, c]
                    if neighbor_val == 2: count2 += 1
                    if neighbor_val == 5: count5 += 1
                # Check Down neighbor
                if r < rows - 1:
                    neighbor_val = input_np[r+1, c]
                    if neighbor_val == 2: count2 += 1
                    if neighbor_val == 5: count5 += 1
                # Check Left neighbor
                if c > 0:
                    neighbor_val = input_np[r, c-1]
                    if neighbor_val == 2: count2 += 1
                    if neighbor_val == 5: count5 += 1
                # Check Right neighbor
                if c < cols - 1:
                    neighbor_val = input_np[r, c+1]
                    if neighbor_val == 2: count2 += 1
                    if neighbor_val == 5: count5 += 1

                # --- Check Rule c: One 2 and one 5 ---
                rule_c = (count2 == 1 and count5 == 1)

                # --- Check Rule d: One 2 and zero 5s ---
                rule_d = (count2 == 1 and count5 == 0)

                # --- Apply transformation if any rule matches ---
                if rule_a or rule_b or rule_c or rule_d:
                    output_grid[r, c] = 1
                    
    # Return the modified grid
    return output_grid.tolist() # Convert back to list of lists if required by caller context, or return output_grid directly

```