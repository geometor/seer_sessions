
Previous Code:
```python
import numpy as np

"""
Transforms an input grid based on pixel adjacency rules.

Rule: If a green pixel (3) is directly adjacent (horizontally or vertically) 
to at least one red pixel (2) in the input grid, it changes to blue (1) 
in the output grid. All other pixels (white (0), red (2), and green (3) pixels 
not adjacent to red) retain their original colors.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed output grid.
    """
    # Convert input to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize the output grid as a copy of the input
    output_grid = np.copy(input_np)

    # Iterate through each pixel in the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is green (3)
            if input_np[r, c] == 3:
                # Check neighbors for red (2) pixels
                has_red_neighbor = False
                # Define potential neighbor coordinates (up, down, left, right)
                neighbors = [
                    (r - 1, c),  # Up
                    (r + 1, c),  # Down
                    (r, c - 1),  # Left
                    (r, c + 1)   # Right
                ]

                for nr, nc in neighbors:
                    # Check if the neighbor is within grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor is red (2) in the input grid
                        if input_np[nr, nc] == 2:
                            has_red_neighbor = True
                            break  # Found a red neighbor, no need to check further

                # If a red neighbor was found, change the current pixel to blue (1) in the output grid
                if has_red_neighbor:
                    output_grid[r, c] = 1
            
            # If the current pixel is not green, or if it's green but has no red neighbors,
            # its value in the output_grid remains as copied from the input_grid.

    return output_grid.tolist() # Return as list of lists per ARC standard
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 3 3
0 0 3 3 3 3 3 3 3 3 3 0 0 0 0 3 3 3 3 3
0 0 3 3 3 3 3 2 3 3 3 0 0 0 0 3 3 3 3 3
0 0 2 3 3 3 3 3 3 2 3 0 0 0 2 3 3 2 3 3
0 0 3 3 3 3 3 3 3 3 3 0 0 0 0 3 3 3 3 3
0 0 3 3 3 3 3 2 3 3 3 0 2 0 0 3 3 3 3 3
0 0 3 3 3 3 3 3 3 3 3 0 0 0 0 3 3 3 3 3
0 0 3 3 3 3 3 3 3 3 3 0 0 0 0 3 3 3 3 2
0 0 3 2 3 3 3 3 3 3 3 0 0 0 0 3 3 3 3 3
0 0 3 3 3 3 3 2 3 3 3 0 0 2 0 2 3 3 3 3
0 0 2 3 3 3 3 3 3 3 3 0 2 0 0 3 3 3 3 3
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3
0 0 0 3 3 3 3 3 3 3 3 3 3 0 0 3 3 3 3 3
0 0 0 3 3 3 3 3 3 3 3 3 3 0 0 3 3 3 3 3
0 2 0 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 2 3 3 3 0 2 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 2 3 0 0 0 0 0 0 0
0 0 0 3 3 3 3 2 3 3 3 3 3 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 2 3 3 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 3 3
0 0 3 3 3 3 1 1 1 3 3 0 0 0 0 3 3 3 3 3
0 1 1 1 3 3 1 2 1 1 1 0 0 0 0 3 1 1 1 3
0 1 2 1 3 3 1 1 1 2 1 0 0 0 2 3 1 2 1 3
0 1 1 1 3 3 1 1 1 1 1 0 0 0 0 3 1 1 1 3
0 0 3 3 3 3 1 2 1 3 3 0 2 0 0 3 3 3 3 3
0 0 3 3 3 3 1 1 1 3 3 0 0 0 0 3 3 3 1 1
0 0 1 1 1 3 3 3 3 3 3 0 0 0 0 3 3 3 1 2
0 0 1 2 1 3 1 1 1 3 3 0 0 0 1 1 1 3 1 1
0 1 1 1 1 3 1 2 1 3 3 0 0 2 1 2 1 3 3 3
0 1 2 1 3 3 1 1 1 3 3 0 2 0 1 1 1 3 3 3
0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3
0 0 0 3 3 3 3 3 3 3 3 3 3 0 0 3 3 3 3 3
0 0 0 3 3 3 3 3 3 3 3 3 3 0 0 3 3 3 3 3
0 2 0 3 3 3 3 3 1 1 1 3 3 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 1 2 1 1 1 0 2 0 0 0 0 0
0 0 0 3 3 3 1 1 1 1 1 2 1 0 0 0 0 0 0 0
0 0 0 3 3 3 1 2 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 3 3 3 1 1 1 1 2 1 3 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 1 3 3 3 3
0 0 3 3 3 3 3 1 3 3 3 0 0 0 0 3 3 3 3 3
0 0 1 3 3 3 1 2 1 1 3 0 0 0 0 3 3 1 3 3
0 0 2 1 3 3 3 1 1 2 1 0 0 0 2 1 1 2 1 3
0 0 1 3 3 3 3 1 3 1 3 0 0 0 0 3 3 1 3 3
0 0 3 3 3 3 1 2 1 3 3 0 2 0 0 3 3 3 3 3
0 0 3 3 3 3 3 1 3 3 3 0 0 0 0 3 3 3 3 1
0 0 3 1 3 3 3 3 3 3 3 0 0 0 0 3 3 3 1 2
0 0 1 2 1 3 3 1 3 3 3 0 0 0 0 1 3 3 3 1
0 0 1 1 3 3 1 2 1 3 3 0 0 2 0 2 1 3 3 3
0 0 2 1 3 3 3 1 3 3 3 0 2 0 0 1 3 3 3 3
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3
0 0 0 3 3 3 3 3 3 3 3 3 3 0 0 3 3 3 3 3
0 0 0 3 3 3 3 3 3 3 3 3 3 0 0 3 3 3 3 3
0 2 0 3 3 3 3 3 3 1 3 3 3 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 1 2 1 1 3 0 2 0 0 0 0 0
0 0 0 3 3 3 3 1 3 1 1 2 1 0 0 0 0 0 0 0
0 0 0 3 3 3 1 2 1 3 1 1 3 0 0 0 0 0 0 0
0 0 0 3 3 3 3 1 3 1 2 1 3 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 48
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 24.0

## Example 2:
Input:
```
0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 3 3 2 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 2 3 3 3 3 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 2 0 0 0 0 0
2 0 2 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 3 2 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 2 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 2 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 2 0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 2 0 3 3 3 3 3 3 3 3 2 0 0 0
0 0 0 0 0 0 0 0 3 3 2 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 3 3 3 2 3 3 3 3 3 0 0 0
0 0 0 0 0 2 0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 2 0 3 2 3 3 3 3 3 3 3 2 0 0
```
Expected Output:
```
0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 1 1 1 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 3 1 2 1 3 3 1 1 1 3 3 3 0 0 0 0 0
0 0 0 3 1 1 1 3 3 1 2 1 3 1 1 1 0 0 0 0
0 0 0 3 3 3 3 3 3 1 1 1 3 1 2 1 0 0 0 0
2 0 2 1 1 1 3 3 3 3 3 3 3 1 1 1 0 0 0 0
0 0 0 1 2 1 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 1 1 1 3 3 3 3 3 3 3 3 3 0 2 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 1 2 1 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 2 0 1 1 1 3 3 3 3 3 1 1 1 0 0
0 0 0 0 0 0 2 0 3 1 1 1 3 3 3 1 2 1 0 0
0 0 0 0 0 0 0 0 3 1 2 1 1 3 3 1 1 1 0 0
0 0 0 0 0 0 0 0 3 1 1 2 1 3 3 3 3 0 0 0
0 0 0 0 0 2 0 0 1 1 1 1 1 3 3 3 3 0 0 0
0 0 0 0 0 0 2 0 1 2 1 3 3 3 3 3 3 2 0 0
```
Transformed Output:
```
0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 1 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 3 1 2 1 3 3 3 1 3 3 3 3 0 0 0 0 0
0 0 0 3 3 1 3 3 3 1 2 1 3 3 1 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 1 3 3 1 2 0 0 0 0 0
2 0 2 1 1 3 3 3 3 3 3 3 3 3 1 0 0 0 0 0
0 0 0 1 2 1 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 3 1 3 3 3 3 3 3 3 3 3 3 0 2 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 2 1 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 2 0 0 1 3 3 3 3 3 3 3 1 0 0 0
0 0 0 0 0 0 2 0 3 3 1 3 3 3 3 1 2 0 0 0
0 0 0 0 0 0 0 0 3 1 2 1 3 3 3 3 1 0 0 0
0 0 0 0 0 0 0 0 3 3 1 2 1 3 3 3 3 0 0 0
0 0 0 0 0 2 0 0 3 1 3 1 3 3 3 3 3 0 0 0
0 0 0 0 0 0 2 0 1 2 1 3 3 3 3 3 1 2 0 0
```
Match: False
Pixels Off: 35
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 17.5

## Example 3:
Input:
```
0 0 0 0 0 2 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 2 0 0 0 0 3 3 3 3 3 2 0 0
0 3 3 3 3 0 0 0 0 3 3 3 3 3 3 0 0
0 3 3 3 3 0 0 0 0 3 2 2 3 3 3 0 0
0 2 0 0 0 0 0 0 0 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 2 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0
0 3 3 1 1 1 0 0 0 0 0 0 0 1 1 1 0
0 3 3 1 2 1 0 0 0 3 3 3 3 1 2 1 0
0 3 3 1 1 1 0 0 0 1 1 1 1 1 1 1 0
0 3 3 3 3 0 0 0 0 1 2 2 1 3 3 0 0
0 2 0 0 0 0 0 0 0 1 1 1 1 3 3 0 0
0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 2 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0
0 3 3 3 1 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 1 2 0 0 0 0 3 3 3 3 1 2 0 0
0 3 3 3 1 0 0 0 0 3 1 1 3 3 1 0 0
0 1 3 3 3 0 0 0 0 1 2 2 1 3 3 0 0
0 2 0 0 0 0 0 0 0 3 1 1 3 3 3 0 0
0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0
```
Match: False
Pixels Off: 16
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 18.823529411764696
