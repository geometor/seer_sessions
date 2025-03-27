```python
import numpy as np
from typing import List, Set, Tuple

"""
Transformation Rule:

1. Initialize the output grid as a copy of the input grid.
2. Iterate through each cell (pixel) of the input grid.
3. If the current cell's color is magenta (6):
    a. Identify its orthogonal neighbors (up, down, left, right) that are within the grid boundaries.
    b. Collect the colors of these neighbors, excluding any magenta (6) neighbors.
    c. Determine the unique non-magenta neighbor colors found.
    d. If there is exactly one unique non-magenta neighbor color, change the corresponding cell in the output grid to that color.
    e. If there are zero or more than one unique non-magenta neighbor colors, the cell in the output grid retains its original color (magenta, 6).
4. If the current cell's color is not magenta (6), its color in the output grid remains unchanged from the input.
5. Return the modified output grid.

Color mapping reference:
    magenta: 6
"""

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    A magenta (6) pixel changes color if it has exactly one unique non-magenta orthogonal neighbor color, 
    adopting that neighbor's color. Otherwise, it remains magenta. Non-magenta pixels remain unchanged.
    
    Args:
        input_grid (List[List[int]]): A 2D list representing the input grid.

    Returns:
        List[List[int]]: A 2D list representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    height, width = input_array.shape
    
    magenta_color = 6

    # Iterate through each cell of the grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell is magenta
            if input_array[r, c] == magenta_color:
                
                neighbor_colors: Set[int] = set()
                
                # Define potential orthogonal neighbors' relative coordinates
                neighbors_coords: List[Tuple[int, int]] = [
                    (r - 1, c),  # Up
                    (r + 1, c),  # Down
                    (r, c - 1),  # Left
                    (r, c + 1)   # Right
                ]
                
                # Check each neighbor
                for nr, nc in neighbors_coords:
                    # Ensure the neighbor is within the grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        neighbor_color = input_array[nr, nc]
                        # If the neighbor is not magenta, add its color to the set
                        if neighbor_color != magenta_color:
                            neighbor_colors.add(neighbor_color)
                            
                # If there is exactly one unique non-magenta neighbor color
                if len(neighbor_colors) == 1:
                    # Change the output cell's color to the unique neighbor color
                    output_array[r, c] = neighbor_colors.pop()
                    
            # If the cell is not magenta, it remains unchanged (already copied)

    return output_array.tolist()

```