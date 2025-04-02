```python
import numpy as np

"""
Identifies local patterns of three adjacent pixels in a line (horizontally or vertically) 
where all three pixels have distinct colors (C1, C2, C3). If the color of the outermost pixel 
in one direction (C3) is not the background color (0), then the middle pixel (C2) and the 
inner pixel (C1) are both changed to the color C3. Changes are determined based on the 
input grid and applied simultaneously to an output grid.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the grid by finding specific three-pixel patterns and applying color changes.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # List to store changes as (row, col, new_color) tuples
    changes = []

    # Iterate through each pixel as a potential 'center' or 'border' pixel
    for r in range(height):
        for c in range(width):
            c_border = input_grid[r, c]

            # Check horizontal neighbors: C_left - C_border - C_right
            if c > 0 and c < width - 1:
                c_left = input_grid[r, c - 1]
                c_right = input_grid[r, c + 1]

                # Check distinctness for left -> right leak (right is adjacent/leaking)
                if c_left != c_border and c_left != c_right and c_border != c_right:
                    # Ensure the leaking color is not background (0)
                    if c_right != 0:
                        # Mark inner (left) and border (center) pixels for change
                        changes.append((r, c - 1, c_right)) # Inner
                        changes.append((r, c, c_right))     # Border
                
                # Check distinctness for right -> left leak (left is adjacent/leaking)
                if c_right != c_border and c_right != c_left and c_border != c_left:
                     # Ensure the leaking color is not background (0)
                    if c_left != 0:
                         # Mark inner (right) and border (center) pixels for change
                        changes.append((r, c + 1, c_left)) # Inner
                        changes.append((r, c, c_left))     # Border

            # Check vertical neighbors: C_top - C_border - C_bottom
            if r > 0 and r < height - 1:
                c_top = input_grid[r - 1, c]
                c_bottom = input_grid[r + 1, c]

                # Check distinctness for top -> bottom leak (bottom is adjacent/leaking)
                if c_top != c_border and c_top != c_bottom and c_border != c_bottom:
                     # Ensure the leaking color is not background (0)
                    if c_bottom != 0:
                        # Mark inner (top) and border (center) pixels for change
                        changes.append((r - 1, c, c_bottom)) # Inner
                        changes.append((r, c, c_bottom))     # Border

                # Check distinctness for bottom -> top leak (top is adjacent/leaking)
                if c_bottom != c_border and c_bottom != c_top and c_border != c_top:
                     # Ensure the leaking color is not background (0)
                    if c_top != 0:
                        # Mark inner (bottom) and border (center) pixels for change
                        changes.append((r + 1, c, c_top)) # Inner
                        changes.append((r, c, c_top))     # Border

    # Apply all collected changes to the output grid
    # Using a dictionary ensures only the last change for a given pixel is applied,
    # although the logic should generally result in only one change per relevant pixel.
    change_dict = {}
    for r, c, color in changes:
        change_dict[(r, c)] = color

    for (r, c), color in change_dict.items():
        output_grid[r, c] = color
        
    return output_grid
```