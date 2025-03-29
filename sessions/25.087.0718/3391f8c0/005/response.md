```python
import numpy as np

"""
The transformation identifies the two distinct non-white colors present in the input grid.
It then creates an output grid by swapping these two colors wherever they appear.
Specifically, every pixel that had the first non-white color in the input grid will have the second non-white color in the output grid, and vice versa.
Background pixels (white, color 0) remain unchanged.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Swaps the two non-white colors found in the input grid pixel by pixel.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the output grid with the two non-white colors swapped.
        Background pixels remain unchanged.
    """
    # Create a copy of the input grid to modify
    output_grid = input_grid.copy()
    
    # Find the unique non-white color values
    unique_colors = np.unique(input_grid)
    non_white_colors = unique_colors[unique_colors != 0]

    # Check if there are exactly two non-white colors
    if len(non_white_colors) != 2:
        # If not exactly two, return the original grid unchanged 
        # (based on problem constraints implicitly suggesting this scenario)
        return output_grid

    color1 = non_white_colors[0]
    color2 = non_white_colors[1]

    # Iterate through each pixel of the grid
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            # Get the color of the current pixel in the original input
            current_color = input_grid[r, c]

            # If the pixel has color1, change it to color2 in the output grid
            if current_color == color1:
                output_grid[r, c] = color2
            # If the pixel has color2, change it to color1 in the output grid
            elif current_color == color2:
                output_grid[r, c] = color1
            # Otherwise (it's the background color 0), leave it unchanged 
            # (already handled by copying initially)

    return output_grid
```