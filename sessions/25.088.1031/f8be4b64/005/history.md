
Previous Code:
```python
import numpy as np

"""
Identifies specific patterns in the input grid: a non-white (0) and non-green (3) 
center pixel surrounded by a green (3) '+' shape (orthogonal neighbors). 
For each such pattern found, it draws horizontal and vertical lines extending 
across the grid, centered on the pattern's center pixel. The lines use the 
color of the center pixel. These lines overwrite existing pixels in the output 
grid, except for any green pixels that are part of any identified '+' shape.
"""

def transform(input_grid):
    """
    Transforms the input grid by drawing lines from centers of green '+' patterns.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    height, width = input_grid.shape
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    centers = []
    protected_coords = set()

    # 1. Find all centers and identify protected green '+' pixels
    for r in range(height):
        for c in range(width):
            pixel_color = input_grid[r, c]

            # Check if the pixel is a potential center (not white and not green)
            if pixel_color != 0 and pixel_color != 3:
                
                # Define neighbor coordinates
                neighbors_coords = [
                    (r - 1, c),  # Up
                    (r + 1, c),  # Down
                    (r, c - 1),  # Left
                    (r, c + 1)   # Right
                ]
                
                is_center_of_plus = True
                actual_neighbors = [] # Store valid neighbor coords
                
                # Check if all four neighbors are within bounds and are green
                for nr, nc in neighbors_coords:
                    if not (0 <= nr < height and 0 <= nc < width and input_grid[nr, nc] == 3):
                        is_center_of_plus = False
                        break
                    actual_neighbors.append((nr, nc)) # Add valid green neighbor coord
                
                # If it's a confirmed center of a green '+' pattern
                if is_center_of_plus:
                    # Store center info
                    centers.append({'r': r, 'c': c, 'color': pixel_color})
                    # Add the coordinates of the green '+' arms to the protected set
                    for coord in actual_neighbors:
                        protected_coords.add(coord)

    # 2. Draw lines for each found center
    for center in centers:
        r, c, center_color = center['r'], center['c'], center['color']
        
        # Draw horizontal line, avoiding protected green pixels
        for j in range(width):
            if (r, j) not in protected_coords:
                output_grid[r, j] = center_color
                
        # Draw vertical line, avoiding protected green pixels
        for i in range(height):
            if (i, c) not in protected_coords:
                output_grid[i, c] = center_color

    # Ensure the center pixel itself has the correct color (it might be overwritten
    # by another line if not protected, but drawing it last for its own lines ensures
    # it's correct unless another line overwrites it later, which seems intended).
    # Re-checking logic: The lines should overwrite everything except protected green cells.
    # The previous loops already handle overwriting, including centers. No extra step needed.

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 2 3 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 3 6 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 8 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
2 2 2 2 3 2 3 2 2 2 2 2 2 0 2 2 2 2 2 2 3 0 8 0 0 0 0 0 0 0
0 0 0 0 0 3 6 6 6 6 6 6 6 0 6 6 6 6 6 3 6 3 8 6 6 6 6 6 6 6
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 3 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 3 0 3 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 3 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 3 0 0 0 0 0 0 0
8 8 8 8 8 2 8 8 8 8 8 8 8 0 8 8 8 8 8 8 6 3 8 3 8 8 8 8 8 8
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 3 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
2 2 2 2 3 2 3 2 2 2 2 2 2 2 2 2 2 2 2 2 3 2 8 2 2 2 2 2 2 2
6 6 6 6 6 3 6 6 6 6 6 6 6 6 6 6 6 6 6 3 6 3 8 6 6 6 6 6 6 6
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 3 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 3 0 3 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 3 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 3 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3 8 3 8 8 8 8 8 8
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 3 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 18
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 4.0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 3 5 3 0 0 0 0 3 0
0 0 3 0 0 0 0 3 6 3
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 3 8 3 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 5 0 0 8 0 0 6 0
0 0 3 0 0 8 0 0 6 0
5 3 5 3 5 8 5 5 3 0
0 0 3 6 6 8 6 3 6 3
0 0 5 0 0 8 0 0 3 0
0 0 5 0 0 3 0 0 6 0
8 8 5 8 3 8 3 8 6 8
0 0 5 0 0 3 0 0 6 0
0 0 5 0 0 8 0 0 6 0
0 0 5 0 0 8 0 0 6 0
```
Transformed Output:
```
0 0 5 0 0 8 0 0 6 0
0 0 3 0 0 8 0 0 6 0
5 3 5 3 5 8 5 5 3 5
6 6 3 6 6 8 6 3 6 3
0 0 5 0 0 8 0 0 3 0
0 0 5 0 0 3 0 0 6 0
8 8 8 8 3 8 3 8 8 8
0 0 5 0 0 3 0 0 6 0
0 0 5 0 0 8 0 0 6 0
0 0 5 0 0 8 0 0 6 0
```
Match: False
Pixels Off: 5
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 10.0

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 5 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 6 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 4 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 0 3 0 0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 3 0 3 0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 0 3 0 0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 3 0 0 0 0
5 5 5 0 5 5 5 6 5 5 5 5 3 5 3 5 5 5
0 0 0 0 0 0 0 6 0 0 0 0 0 3 4 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 4 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0 5 4 0 0 0
6 6 6 0 6 6 3 6 3 6 6 6 6 5 4 6 6 6
0 0 0 0 0 0 0 3 0 0 0 0 0 5 4 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 4 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 3 0 0 0
4 4 4 0 4 4 4 6 4 4 4 4 4 3 4 3 4 4
0 0 0 0 0 0 0 6 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 0 4 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 6 0 0 0 0 0 5 4 0 0 0
0 0 0 3 0 0 0 6 0 0 0 0 0 5 4 0 0 0
0 0 3 0 3 0 0 6 0 0 0 0 0 5 4 0 0 0
0 0 0 3 0 0 0 6 0 0 0 0 0 5 4 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 4 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 4 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 3 4 0 0 0
5 5 5 5 5 5 5 6 5 5 5 5 3 5 3 5 5 5
0 0 0 0 0 0 0 6 0 0 0 0 0 3 4 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 4 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0 5 4 0 0 0
6 6 6 6 6 6 3 6 3 6 6 6 6 6 4 6 6 6
0 0 0 0 0 0 0 3 0 0 0 0 0 5 4 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 4 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 3 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 3 4 3 4 4
0 0 0 0 0 0 0 6 0 0 0 0 0 5 3 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 4 0 0 0
```
Match: False
Pixels Off: 14
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 8.641975308641975

## Example 4:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 3 2 3 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 3 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
2 2 3 2 3 2 2 2 0 2 2 2 2
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 3 0 0 0 0
0 0 0 2 0 0 0 3 0 3 0 0 0
0 0 0 2 0 0 0 0 3 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
2 2 3 2 3 2 2 2 2 2 2 2 2
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 3 0 0 0 0
0 0 0 2 0 0 0 3 0 3 0 0 0
0 0 0 2 0 0 0 0 3 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 1
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 1.1834319526627155
