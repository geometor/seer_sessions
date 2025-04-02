```python
"""
Pixel-wise color transformation based on input color:
- If the input pixel color is Green (3) or Red (2), change it to Yellow (4).
- If the input pixel color is Blue (1), Magenta (6), Orange (7), or Azure (8), change it to Gray (5).
- White (0) pixels remain White (0).
"""

import numpy as np

def transform(input_grid):
    """
    Applies a pixel-wise color transformation to the input grid based on specific color rules.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert the input list of lists to a numpy array for efficient operations
    input_array = np.array(input_grid, dtype=int)
    
    # Create a copy of the input array to modify, preserving the original dimensions and background
    output_array = np.copy(input_array)

    # Define the color mappings
    # Map Green (3) or Red (2) to Yellow (4)
    mask_yellow = (input_array == 3) | (input_array == 2)
    output_array[mask_yellow] = 4

    # Map Blue (1), Magenta (6), Orange (7), or Azure (8) to Gray (5)
    mask_gray = (input_array == 1) | (input_array == 6) | (input_array == 7) | (input_array == 8)
    output_array[mask_gray] = 5
    
    # White (0) pixels remain unchanged as they were copied initially

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid

```