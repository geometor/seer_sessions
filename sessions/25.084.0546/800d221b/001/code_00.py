"""
1.  **Iterate** through each pixel in the input grid.
2.  **Identify Key Triples:**
    *   Find all instances of key triples, being one of the colors from a list of triples `[(7,8,6),(9,8,4),(5,2,1)]` that appear in that exact horizontal or vertical order, next to eachother, in either direction.
3. **Color Replacement**:
    * Replace the middle number of the triple, with the number on the right, for example `7` in `(7,8,6)` or `9` in `(9,8,4)`.
4. **Output** is result of all replacements on input.
"""

import numpy as np

def find_triples(grid, triples):
    rows, cols = grid.shape
    triple_locations = []

    for r in range(rows):
        for c in range(cols):
            for triple in triples:
                # Check horizontal
                if c + 2 < cols:
                    if grid[r, c] == triple[0] and grid[r, c+1] == triple[1] and grid[r, c+2] == triple[2]:
                        triple_locations.append(((r, c+1), triple[2]))
                    if grid[r, c] == triple[2] and grid[r, c+1] == triple[1] and grid[r, c+2] == triple[0]:
                        triple_locations.append(((r, c+1), triple[0]))
                # Check vertical
                if r + 2 < rows:
                    if grid[r, c] == triple[0] and grid[r+1, c] == triple[1] and grid[r+2, c] == triple[2]:
                        triple_locations.append(((r+1, c), triple[2]))
                    if grid[r, c] == triple[2] and grid[r+1, c] == triple[1] and grid[r+2, c] == triple[0]:
                        triple_locations.append(((r+1, c), triple[0]))
    return triple_locations

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Define key triples
    key_triples = [(7, 8, 6), (9, 8, 4), (5, 2, 1)]

    # Find triple locations
    triple_locations = find_triples(output_grid, key_triples)

    # Replace middle element of triple
    for (r, c), replacement_value in triple_locations:
        output_grid[r, c] = replacement_value

    return output_grid