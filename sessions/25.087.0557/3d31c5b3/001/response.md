```python
"""
Transforms a 12x6 input grid into a 3x6 output grid based on a pixel-wise priority overlay rule.

The input grid is treated as four stacked 3x6 blocks. For each pixel position (r, c) in the output grid (0 <= r < 3, 0 <= c < 6), the corresponding pixels in the four input blocks are examined:
- P1: input[r, c] (Block 1, rows 0-2)
- P2: input[r + 3, c] (Block 2, rows 3-5)
- P3: input[r + 6, c] (Block 3, rows 6-8)
- P4: input[r + 9, c] (Block 4, rows 9-11)

The output pixel value at (r, c) is determined by the first non-white pixel encountered in the following priority order:
1. If P1 is Gray (5), the output is Gray (5).
2. Else if P2 is Yellow (4), the output is Yellow (4).
3. Else if P4 is Azure (8), the output is Azure (8).
4. Else if P3 is Red (2), the output is Red (2).
5. Otherwise (if all corresponding P1, P2, P3, P4 are White or don't match the priority condition), the output is White (0).
"""

import numpy as np

def transform(input_grid):
    """
    Applies the priority overlay transformation to the input grid.

    Args:
        input_grid (np.ndarray): A 12x6 numpy array representing the input grid.

    Returns:
        np.ndarray: A 3x6 numpy array representing the transformed output grid.
    """
    # Ensure input is a numpy array
    input_grid = np.array(input_grid)
    
    # Define grid dimensions
    input_height, input_width = input_grid.shape
    output_height = 3
    output_width = 6
    
    # Check if input dimensions are correct (optional but good practice)
    if input_height != 12 or input_width != 6:
        raise ValueError("Input grid must be 12x6")

    # Initialize the output grid with White (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell of the output grid
    for r in range(output_height):
        for c in range(output_width):
            # Get the corresponding pixel values from the four input blocks
            p1 = input_grid[r, c]       # Block 1 (Gray priority)
            p2 = input_grid[r + 3, c]   # Block 2 (Yellow priority)
            p3 = input_grid[r + 6, c]   # Block 3 (Red priority)
            p4 = input_grid[r + 9, c]   # Block 4 (Azure priority)

            # Apply the priority rule
            if p1 == 5:
                output_grid[r, c] = 5  # Gray has highest priority
            elif p2 == 4:
                output_grid[r, c] = 4  # Yellow is next
            elif p4 == 8:
                output_grid[r, c] = 8  # Azure is next
            elif p3 == 2:
                output_grid[r, c] = 2  # Red is last priority before default
            else:
                output_grid[r, c] = 0  # Default to White if no priority color found

    return output_grid

```