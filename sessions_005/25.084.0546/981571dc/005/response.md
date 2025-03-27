```python
"""
Copy non-zero pixels from input to output. Fill zero-valued pixels in the
output based on the values of their nearest non-zero neighbors in the four
cardinal directions (up, down, left, right). If at least two neighbors have the
same non-zero value, set the output pixel to that value; otherwise, leave it
unchanged (which should apply only if the input was zero).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the input grid
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 0:  # Process only zero-valued pixels in input
                
                neighbors = []

                # Check up
                if r > 0:
                    neighbors.append(input_grid[r - 1, c])
                # Check down
                if r < rows - 1:
                    neighbors.append(input_grid[r + 1, c])
                # Check left
                if c > 0:
                    neighbors.append(input_grid[r, c - 1])
                # Check right
                if c < cols - 1:
                    neighbors.append(input_grid[r, c + 1])

                #remove zeros
                neighbors = [n for n in neighbors if n!=0]

                counts = {}
                for n in neighbors:
                    if n != 0: #consider only non-zero neighbors
                        counts[n] = counts.get(n, 0) + 1

                # Find neighbors with count >= 2
                for val, count in counts.items():
                    if count >= 2:
                        output_grid[r, c] = val
                        break # found a match, move to next pixel

    return output_grid.tolist()
```