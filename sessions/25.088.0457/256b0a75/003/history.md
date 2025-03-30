
Previous Code:
```python
import numpy as np
from collections import defaultdict

"""
Transformation Rule:

1. Identify all "L-shapes" in the input grid. An L-shape consists of exactly 
   three pixels of the same non-white color arranged to occupy three cells 
   of a 2x2 square.
2. Categorize the L-shapes based on color: azure (8) and non-azure.
3. Determine the fill color from the color of the non-azure L-shape(s). 
   Assume there's only one such color across all non-azure L-shapes.
4. Collect the coordinates of all pixels belonging to *any* identified L-shape.
5. Calculate the minimum bounding box enclosing all collected L-shape pixels.
6. Initialize the output grid as a copy of the input grid.
7. Iterate through each cell within the bounding box. If a cell is *not* part 
   of any originally identified L-shape, change its color to the determined 
   fill color. Otherwise, keep the original L-shape pixel color.
8. Pixels outside the bounding box remain unchanged.
"""

def find_l_shapes(grid):
    """
    Finds all L-shaped objects in the grid.

    An L-shape is defined as 3 pixels of the same non-white color
    occupying 3 cells of a 2x2 square.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of tuples, where each tuple is (color, set_of_coordinates).
              set_of_coordinates contains (row, col) tuples for the 3 pixels
              of the L-shape. Returns an empty list if no L-shapes are found.
    """
    l_shapes = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            # Extract the 2x2 subgrid
            subgrid = grid[r:r+2, c:c+2]
            
            # Count colors in the 2x2 subgrid, excluding white (0)
            colors = defaultdict(list)
            white_count = 0
            for i in range(2):
                for j in range(2):
                    color = subgrid[i, j]
                    coord = (r + i, c + j)
                    if color == 0:
                        white_count += 1
                    else:
                        colors[color].append(coord)

            # Check for the L-shape condition: 1 white pixel and 3 pixels of the same non-white color
            if white_count == 1:
                for color, coords in colors.items():
                    if len(coords) == 3:
                        l_shapes.append((color, set(coords)))
                        # Assuming a 2x2 can only contain one L-shape, break inner loop
                        break 
                        
    return l_shapes

def transform(input_grid):
    """
    Applies the L-shape based filling transformation to the input grid.
    
    Args:
        input_grid (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed grid as a list of lists.
    """
    
    # Convert input to numpy array for easier handling
    grid_np = np.array(input_grid, dtype=int)
    output_grid = grid_np.copy()
    rows, cols = grid_np.shape

    # 1. & 2. Find and categorize L-shapes
    all_l_shapes = find_l_shapes(grid_np)

    if not all_l_shapes:
        # If no L-shapes are found, return the original grid
        return input_grid

    azure_l_shapes = []
    non_azure_l_shapes = []
    l_shape_pixels = set() # Collect coordinates of all pixels part of any L-shape

    for color, coords in all_l_shapes:
        if color == 8: # Azure
            azure_l_shapes.append((color, coords))
        else:
            non_azure_l_shapes.append((color, coords))
        l_shape_pixels.update(coords)

    # 3. Determine fill color
    fill_color = -1 # Default invalid color
    if non_azure_l_shapes:
        # Assume all non-azure L-shapes have the same color as per examples
        fill_color = non_azure_l_shapes[0][0] 
    else:
         # If only azure L-shapes exist, there's no non-azure color to fill with.
         # Based on observation, this shouldn't happen, but if it did,
         # no filling occurs, effectively returning the input.
         # However, the bounding box is still defined by the azure shapes.
         # Let's proceed assuming fill_color is needed, and if it's -1 later, we skip filling.
         # OR maybe the fill color becomes white (0) or azure (8)? 
         # The examples always have a non-azure shape. Let's stick to the pattern.
         # If only azure shapes exist, maybe no fill happens.
         # Revisit if a test case demands different behavior.
         # For now, if fill_color remains -1, the fill step won't execute.
         pass # fill_color remains -1

    # 4. Coordinates already collected in l_shape_pixels

    # 5. Calculate bounding box
    if not l_shape_pixels:
       # Should not happen if all_l_shapes is not empty, but safety check
       return input_grid
       
    min_r = min(r for r, c in l_shape_pixels)
    max_r = max(r for r, c in l_shape_pixels)
    min_c = min(c for r, c in l_shape_pixels)
    max_c = max(c for r, c in l_shape_pixels)

    # 6. Output grid initialized as a copy earlier

    # 7. Iterate through bounding box and fill
    if fill_color != -1: # Only fill if a non-azure color was found
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                # Check if the current pixel is NOT part of any L-shape
                if (r, c) not in l_shape_pixels:
                    output_grid[r, c] = fill_color

    # Convert back to list of lists for the required output format
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 4 0 0 0 0 0 4 0 0 0 0 6 0 0 0 0 0 0 1 0 0 5 0
0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 0 0 0 8 8 0 0 0 7 0 0 0
0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 4
```
Expected Output:
```
0 4 0 0 0 0 0 4 0 0 4 1 6 1 1 1 1 0 0 1 0 0 5 0
0 0 0 0 0 0 0 0 0 0 4 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0
0 2 0 0 9 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 8 8 8 8 8 8 8 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 8 1 1 1 1 1 8 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 8 1 1 1 1 1 8 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 8 1 1 1 1 1 8 1 1 1 1 1 1 2
1 1 1 1 1 1 1 1 1 1 8 1 1 1 1 1 8 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 8 1 1 1 1 1 8 1 1 1 1 1 1 1
2 2 2 2 2 2 2 1 1 1 8 1 1 1 1 1 8 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 8 8 8 8 8 8 8 1 1 1 7 7 7 7
0 0 0 9 0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 7 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 7 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 3 1 1 1 1 1 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 1 1 1 1 1 7 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 3 1 1 1 1 1 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 1 1 3 1 1 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 1 1 3 1 1 7 0 0 0 0 0 0 4
```
Transformed Output:
```
0 4 0 0 0 0 0 4 0 0 0 0 6 0 0 0 0 0 0 1 0 0 5 0
0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 8 1 1 1 1 1 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 1 1 1 8 8 0 0 0 7 0 0 0
0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 4
```
Match: False
Pixels Off: 240
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 90.90909090909092

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 8 8 0 0 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 8 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 7 7 0 0 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 7 6 7 7 4 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 6 7 7 4 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 6 7 7 7 7 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 7 6 7 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 0 0 0 0 0 0
2 2 2 7 7 7 7 7 7 8 8 8 8 8 8 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 8 7 7 7 7 8 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 8 7 7 7 7 8 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 8 7 7 7 7 8 7 7 7 7 7 7
4 4 4 4 4 7 7 7 7 8 7 7 7 7 8 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 8 7 7 7 7 8 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 8 7 7 7 7 8 7 7 7 9 9 9
7 7 7 7 7 7 7 7 7 8 8 8 8 8 8 7 7 7 7 7 7
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 1 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 1 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 1 7 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 7 7 7 7 1 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 1 7 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 1 7 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 8 8 7 7 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 7 7 7 7 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 7 7 7 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 8 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 218
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 90.26915113871637

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 7 0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0 8 8 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 8 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 8 8 0 0 0 0 3 3 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
0 5 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 1 3 3 7 9 5 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 3 3 3 9 6 3 3 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 1 3 3 3 9 6 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 3 3 3 9 6 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 6 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 6 3 3 0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 8 8 8 8 8 8 8 8 3 3 3 3 3 6 6 6 6
3 3 3 3 3 3 8 3 3 3 3 3 3 8 3 3 3 3 3 3 3 3 3
5 5 5 5 3 3 8 3 3 3 3 3 3 8 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 8 3 3 3 3 3 3 8 3 3 3 3 3 3 3 3 3
6 6 3 3 3 3 8 3 3 3 3 3 3 8 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 8 3 3 3 3 3 3 8 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 8 3 3 3 3 3 3 8 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 8 3 3 3 3 3 3 8 3 3 3 3 3 3 3 3 3
1 1 1 3 3 3 8 3 3 3 3 3 3 8 3 3 3 3 3 3 3 3 3
6 6 3 3 3 3 8 8 8 8 8 8 8 8 3 3 3 3 1 1 1 1 1
0 0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 1 3 0 0 0 0 0 0 0 0 0
0 5 2 0 0 0 3 3 3 3 3 3 1 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 9 1 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 9 1 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 1 3 3 9 1 3 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 7 0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 3 3 3 3 8 8 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 8 3 3 3 3 3 3 8 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 8 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 8 8 3 3 3 3 3 3 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
0 5 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 263
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 99.4328922495274
Okay, let's analyze the discrepancies and refine the transformation rule.

**General Assessment**

The previous code correctly identified the concept of L-shapes and the idea of using a non-azure L-shape color for filling. However, the results show that the filled area in the expected outputs is significantly larger and differently defined than the bounding box of just the L-shapes. The code failed because it incorrectly determined the region to be filled.

The expected outputs suggest a rectangular fill bounded not by the L-shapes alone, but by the extent of *all* non-white pixels in the input grid. The fill color is determined by the non-azure L-shape, and the L-shapes themselves (both azure and non-azure) are preserved (i.e., not overwritten by the fill color) within this larger bounding box. All other pixels *within* this bounding box, whether originally white or a different color, are changed to the fill color. Pixels *outside* this bounding box remain unchanged.

**Strategy:**

1.  **Verify L-shape detection:** Ensure the `find_l_shapes` function correctly identifies all L-shapes (3 pixels of the same non-white color in a 2x2 square).
2.  **Identify Fill Color:** Find the color of the non-azure L-shape(s). Assume there is only one such color across the examples.
3.  **Determine Global Bounding Box:** Find the minimum bounding box that encloses *all* non-white pixels in the input grid.
4.  **Apply Fill:** Create the output grid by copying the input. Iterate through every cell within the global bounding box. If the cell's coordinates do not belong to any identified L-shape (azure or non-azure), set its color to the fill color. Otherwise, keep the L-shape's original color. Cells outside the bounding box remain untouched.

**Metrics Gathering**


*code_execution:*
```python
import numpy as np
from collections import defaultdict

# Re-use the L-shape finding function from the previous attempt
def find_l_shapes(grid):
    l_shapes = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            subgrid = grid[r:r+2, c:c+2]
            colors = defaultdict(list)
            white_count = 0
            for i in range(2):
                for j in range(2):
                    color = subgrid[i, j]
                    coord = (r + i, c + j)
                    if color == 0:
                        white_count += 1
                    else:
                        colors[color].append(coord)
            if white_count == 1:
                for color, coords in colors.items():
                    if len(coords) == 3:
                        l_shapes.append((color, set(coords)))
                        break
    return l_shapes

# Function to find bounding box of non-white pixels
def find_non_white_bounding_box(grid):
    non_white_coords = np.argwhere(grid != 0)
    if non_white_coords.size == 0:
        return None # No non-white pixels
    min_r = np.min(non_white_coords[:, 0])
    max_r = np.max(non_white_coords[:, 0])
    min_c = np.min(non_white_coords[:, 1])
    max_c = np.max(non_white_coords[:, 1])
    return min_r, max_r, min_c, max_c

# --- Data for Examples ---
# Note: Input grids are copied from the prompt for clarity, converted to numpy arrays.

# Example 1 Input
grid1_in_list = [
    [0,4,0,0,0,0,0,4,0,0,0,0,6,0,0,0,0,0,0,1,0,0,5,0],
    [0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,2,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,8,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,2,0,0,0,8,0,0,0,0,0,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,8,8,0,0,0,8,8,0,0,0,7,0,0,0],
    [0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,5,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,4]
]
grid1 = np.array(grid1_in_list)

# Example 2 Input
grid2_in_list = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,3,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,2,0,0,0,0,0,0,8,8,0,0,8,8,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,8,0,0,0,0,8,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,7,0,0,0,0,8,0,0,0,9,0,0],
    [0,0,0,0,0,0,0,0,0,7,7,0,0,8,8,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
grid2 = np.array(grid2_in_list)

# Example 3 Input
grid3_in_list = [
    [0,0,0,0,0,0,0,0,0,7,0,5,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,8,8,0,0,0,0,8,8,0,0,0,0,0,6,0,0,0],
    [0,0,0,0,0,0,8,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0],
    [0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,8,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0],
    [0,6,0,0,0,0,8,8,0,0,0,0,3,3,0,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    [0,5,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
grid3 = np.array(grid3_in_list)

grids = {'ex1': grid1, 'ex2': grid2, 'ex3': grid3}
results = {}

for name, grid in grids.items():
    l_shapes = find_l_shapes(grid)
    bbox = find_non_white_bounding_box(grid)

    all_l_shape_pixels = set()
    non_azure_l_shapes = []
    azure_l_shapes = []
    fill_color = -1 # Default invalid

    for color, coords in l_shapes:
        all_l_shape_pixels.update(coords)
        if color == 8:
            azure_l_shapes.append((color, coords))
        else:
            non_azure_l_shapes.append((color, coords))

    if non_azure_l_shapes:
        # Assumption: only one non-azure color exists if present
        fill_color = non_azure_l_shapes[0][0]

    results[name] = {
        'grid_shape': grid.shape,
        'non_white_bbox': bbox,
        'num_l_shapes': len(l_shapes),
        'num_azure_l_shapes': len(azure_l_shapes),
        'num_non_azure_l_shapes': len(non_azure_l_shapes),
        'fill_color_candidate': fill_color,
        'l_shapes_details': l_shapes # Storing details might be too verbose, let's just store counts for now
    }

# Re-running L-shape detection specifically for Ex1 because I wasn't sure above
l_shapes_ex1 = find_l_shapes(grid1)
# Format coords for printing
formatted_l_shapes_ex1 = [(color, sorted(list(coords))) for color, coords in l_shapes_ex1]
results['ex1']['l_shapes_details_formatted'] = formatted_l_shapes_ex1

# Re-running L-shape detection specifically for Ex2
l_shapes_ex2 = find_l_shapes(grid2)
formatted_l_shapes_ex2 = [(color, sorted(list(coords))) for color, coords in l_shapes_ex2]
results['ex2']['l_shapes_details_formatted'] = formatted_l_shapes_ex2

# Re-running L-shape detection specifically for Ex3
l_shapes_ex3 = find_l_shapes(grid3)
formatted_l_shapes_ex3 = [(color, sorted(list(coords))) for color, coords in l_shapes_ex3]
results['ex3']['l_shapes_details_formatted'] = formatted_l_shapes_ex3


import json
print(json.dumps(results, indent=2))
```

*code_execution_result:*
outcome: OUTCOME_FAILED
```
Traceback (most recent call last):
  File "<string>", line 176, in <module>
  File "__init__.py", line 238, in dumps
    **kw).encode(obj)
          ^^^^^^^^^^^
  File "encoder.py", line 202, in encode
    chunks = list(chunks)
             ^^^^^^^^^^^^
  File "encoder.py", line 432, in _iterencode
    yield from _iterencode_dict(o, _current_indent_level)
  File "encoder.py", line 406, in _iterencode_dict
    yield from chunks
  File "encoder.py", line 406, in _iterencode_dict
    yield from chunks
  File "encoder.py", line 326, in _iterencode_list
    yield from chunks
  File "encoder.py", line 439, in _iterencode
    o = _default(o)
        ^^^^^^^^^^^
  File "encoder.py", line 180, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
TypeError: Object of type int64 is not JSON serializable

```
It seems there was an issue serializing numpy data types to JSON. Let's correct that and gather the metrics.


*code_execution:*
```python
import numpy as np
from collections import defaultdict
import json

# Helper function to convert numpy types for JSON serialization
def make_serializable(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, set):
        # Convert sets to sorted lists for consistent output
        return sorted(list(obj), key=lambda x: (x[0], x[1]))
    elif isinstance(obj, tuple):
        return tuple(make_serializable(item) for item in obj)
    elif isinstance(obj, list):
        return [make_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    else:
        return obj

# Re-use the L-shape finding function
def find_l_shapes(grid):
    l_shapes = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            subgrid = grid[r:r+2, c:c+2]
            colors = defaultdict(list)
            white_count = 0
            for i in range(2):
                for j in range(2):
                    color = subgrid[i, j]
                    coord = (r + i, c + j)
                    if color == 0:
                        white_count += 1
                    else:
                        colors[color].append(coord)
            if white_count == 1:
                for color, coords in colors.items():
                    if len(coords) == 3:
                        # Store coords as a set initially for easy update later
                        l_shapes.append((color, set(coords)))
                        break
    # Convert color (potentially numpy int) to Python int and coords set to sorted list for final output
    return [(int(color), sorted(list(coords), key=lambda x: (x[0], x[1]))) for color, coords in l_shapes]


# Function to find bounding box of non-white pixels
def find_non_white_bounding_box(grid):
    non_white_coords = np.argwhere(grid != 0)
    if non_white_coords.size == 0:
        return None
    min_r = np.min(non_white_coords[:, 0])
    max_r = np.max(non_white_coords[:, 0])
    min_c = np.min(non_white_coords[:, 1])
    max_c = np.max(non_white_coords[:, 1])
    # Return as python ints
    return int(min_r), int(max_r), int(min_c), int(max_c)

# --- Data for Examples ---
# Example 1 Input
grid1_in_list = [
    [0,4,0,0,0,0,0,4,0,0,0,0,6,0,0,0,0,0,0,1,0,0,5,0],
    [0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,2,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,8,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,2,0,0,0,8,0,0,0,0,0,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,8,8,0,0,0,8,8,0,0,0,7,0,0,0],
    [0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,5,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,4]
]
grid1 = np.array(grid1_in_list)

# Example 2 Input
grid2_in_list = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,3,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,2,0,0,0,0,0,0,8,8,0,0,8,8,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,8,0,0,0,0,8,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,7,0,0,0,0,8,0,0,0,9,0,0],
    [0,0,0,0,0,0,0,0,0,7,7,0,0,8,8,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
grid2 = np.array(grid2_in_list)

# Example 3 Input
grid3_in_list = [
    [0,0,0,0,0,0,0,0,0,7,0,5,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,8,8,0,0,0,0,8,8,0,0,0,0,0,6,0,0,0],
    [0,0,0,0,0,0,8,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0],
    [0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,8,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0],
    [0,6,0,0,0,0,8,8,0,0,0,0,3,3,0,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    [0,5,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
grid3 = np.array(grid3_in_list)

grids = {'ex1': grid1, 'ex2': grid2, 'ex3': grid3}
results = {}
all_l_shape_pixel_coords = {} # Store all pixels belonging to any L-shape per example

for name, grid in grids.items():
    l_shapes = find_l_shapes(grid) # Gets list of (color, sorted_list_of_coords)
    bbox = find_non_white_bounding_box(grid)

    current_all_l_shape_pixels = set()
    non_azure_l_shapes = []
    azure_l_shapes = []
    fill_color = -1 # Default invalid

    for color, coords in l_shapes:
        # Coords is already a list of tuples here
        current_all_l_shape_pixels.update(coords) # Add tuple coords to set
        if color == 8:
            azure_l_shapes.append((color, coords))
        else:
            non_azure_l_shapes.append((color, coords))

    if non_azure_l_shapes:
        # Assumption: only one non-azure color exists if present
        fill_color = non_azure_l_shapes[0][0] # Get color from first non-azure L-shape

    # Store the set of L-shape pixel coordinates for this example
    all_l_shape_pixel_coords[name] = current_all_l_shape_pixels

    results[name] = {
        'grid_shape': grid.shape,
        'non_white_bbox': bbox, # (min_r, max_r, min_c, max_c)
        'num_l_shapes': len(l_shapes),
        'num_azure_l_shapes': len(azure_l_shapes),
        'num_non_azure_l_shapes': len(non_azure_l_shapes),
        'fill_color_candidate': fill_color,
        'l_shapes_details': l_shapes # List of (color, sorted_list_of_coords)
    }

# Make the entire results structure serializable before printing
serializable_results = make_serializable(results)
print(json.dumps(serializable_results, indent=2))
```

*code_execution_result:*
outcome: OUTCOME_OK
```
{
  "ex1": {
    "grid_shape": [
      22,
      24
    ],
    "non_white_bbox": [
      0,
      21,
      1,
      23
    ],
    "num_l_shapes": 4,
    "num_azure_l_shapes": 3,
    "num_non_azure_l_shapes": 1,
    "fill_color_candidate": 1,
    "l_shapes_details": [
      [
        1,
        [
          [
            4,
            10
          ],
          [
            4,
            11
          ],
          [
            5,
            10
          ]
        ]
      ],
      [
        8,
        [
          [
            4,
            15
          ],
          [
            4,
            16
          ],
          [
            5,
            16
          ]
        ]
      ],
      [
        8,
        [
          [
            10,
            10
          ],
          [
            11,
            10
          ],
          [
            11,
            11
          ]
        ]
      ],
      [
        8,
        [
          [
            10,
            16
          ],
          [
            11,
            15
          ],
          [
            11,
            16
          ]
        ]
      ]
    ]
  },
  "ex2": {
    "grid_shape": [
      23,
      21
    ],
    "non_white_bbox": [
      1,
      21,
      2,
      18
    ],
    "num_l_shapes": 4,
    "num_azure_l_shapes": 3,
    "num_non_azure_l_shapes": 1,
    "fill_color_candidate": 7,
    "l_shapes_details": [
      [
        8,
        [
          [
            7,
            9
          ],
          [
            7,
            10
          ],
          [
            8,
            9
          ]
        ]
      ],
      [
        8,
        [
          [
            7,
            13
          ],
          [
            7,
            14
          ],
          [
            8,
            14
          ]
        ]
      ],
      [
        7,
        [
          [
            13,
            9
          ],
          [
            14,
            9
          ],
          [
            14,
            10
          ]
        ]
      ],
      [
        8,
        [
          [
            13,
            14
          ],
          [
            14,
            13
          ],
          [
            14,
            14
          ]
        ]
      ]
    ]
  },
  "ex3": {
    "grid_shape": [
      23,
      23
    ],
    "non_white_bbox": [
      0,
      22,
      1,
      19
    ],
    "num_l_shapes": 4,
    "num_azure_l_shapes": 3,
    "num_non_azure_l_shapes": 1,
    "fill_color_candidate": 3,
    "l_shapes_details": [
      [
        8,
        [
          [
            6,
            6
          ],
          [
            6,
            7
          ],
          [
            7,
            6
          ]
        ]
      ],
      [
        8,
        [
          [
            6,
            12
          ],
          [
            6,
            13
          ],
          [
            7,
            13
          ]
        ]
      ],
      [
        8,
        [
          [
            14,
            6
          ],
          [
            15,
            6
          ],
          [
            15,
            7
          ]
        ]
      ],
      [
        3,
        [
          [
            14,
            13
          ],
          [
            15,
            12
          ],
          [
            15,
            13
          ]
        ]
      ]
    ]
  }
}

```
**Facts (YAML)**


```yaml
task_description: Fill a rectangular region based on L-shapes and global pixel bounds.

definitions:
  - object: L-shape
    description: A group of exactly 3 pixels of the same non-white color occupying 3 cells of a 2x2 square.
    properties:
      - color: (Integer 1-9, excluding 8 for 'fill_color' determination)
      - coordinates: (Set of 3 (row, col) tuples)
      - type: (azure (8) or non-azure)
  - object: Azure L-shape
    description: An L-shape with color 8 (azure).
  - object: Non-Azure L-shape
    description: An L-shape with a color other than 0 (white) or 8 (azure).
    notes: Assumed to be only one color type present per grid among these.
  - object: Fill Color
    description: The color used to fill the target region.
    derivation: Determined by the color of the Non-Azure L-shape(s).
  - object: Global Bounding Box
    description: The smallest rectangle enclosing all non-white pixels in the input grid.
    properties:
      - min_row: (Integer)
      - max_row: (Integer)
      - min_col: (Integer)
      - max_col: (Integer)
  - object: Target Fill Region
    description: All cells within the Global Bounding Box.
  - object: Preserved Pixels
    description: Pixels within the Target Fill Region that retain their original color.
    derivation: These are the pixels belonging to *any* L-shape (azure or non-azure).

actions:
  - action: Identify L-shapes
    inputs: [Input Grid]
    outputs: [List of L-shapes (color, coordinates)]
  - action: Determine Fill Color
    inputs: [List of L-shapes]
    outputs: [Fill Color]
    logic: Find the color of the first Non-Azure L-shape.
  - action: Calculate Global Bounding Box
    inputs: [Input Grid]
    outputs: [Global Bounding Box (min_r, max_r, min_c, max_c)]
    logic: Find min/max row/col of all non-white pixels.
  - action: Generate Output Grid
    inputs: [Input Grid, List of L-shapes, Fill Color, Global Bounding Box]
    outputs: [Output Grid]
    logic:
      1. Copy Input Grid to Output Grid.
      2. Identify all pixel coordinates belonging to any L-shape (Preserved Pixels).
      3. Iterate through each cell (r, c) within the Global Bounding Box.
      4. If (r, c) is NOT in the set of Preserved Pixels, set Output Grid[r, c] = Fill Color.
      5. Cells outside the Global Bounding Box remain unchanged from the input.

examples_summary:
  - example: 1
    grid_shape: [22, 24]
    l_shapes: 4 (1 non-azure Blue(1), 3 azure)
    fill_color: 1 (Blue)
    global_bbox: [0, 21, 1, 23]
  - example: 2
    grid_shape: [23, 21]
    l_shapes: 4 (1 non-azure Orange(7), 3 azure)
    fill_color: 7 (Orange)
    global_bbox: [1, 21, 2, 18]
  - example: 3
    grid_shape: [23, 23]
    l_shapes: 4 (1 non-azure Green(3), 3 azure)
    fill_color: 3 (Green)
    global_bbox: [0, 22, 1, 19]

```


**Natural Language Program**

1.  **Identify all L-shapes:** Scan the input grid for any L-shapes. An L-shape consists of exactly three pixels of the same non-white color (colors 1 through 9) that occupy three out of four cells in any 2x2 square. Record the color and the set of coordinates for each L-shape found.
2.  **Determine the Fill Color:** Examine the identified L-shapes. Find the L-shape(s) whose color is *not* azure (color 8). The color of this non-azure L-shape is the "Fill Color". (Based on the examples, there appears to be only one such non-azure color present per grid). If no non-azure L-shapes are found, this rule may not apply (though this case is not present in the examples).
3.  **Collect all L-shape Pixel Coordinates:** Create a single set containing the coordinates of all pixels that are part of *any* identified L-shape (both azure and non-azure). These pixels will be preserved.
4.  **Calculate the Global Bounding Box:** Find the minimum and maximum row and column indices occupied by *any* non-white pixel (colors 1 through 9) in the input grid. This defines the rectangular region for the filling operation.
5.  **Generate the Output Grid:**
    a.  Start with a copy of the input grid.
    b.  Iterate through every cell (row `r`, column `c`) within the Global Bounding Box (from `min_row` to `max_row`, and `min_col` to `max_col`, inclusive).
    c.  For each cell `(r, c)`, check if its coordinates are present in the set of collected L-shape pixel coordinates.
    d.  If the coordinates `(r, c)` are *not* in the L-shape coordinates set, change the color of this cell in the output grid to the determined Fill Color.
    e.  If the coordinates `(r, c)` *are* in the L-shape coordinates set, leave the cell's color unchanged (it keeps its original L-shape color).
    f.  All cells outside the Global Bounding Box remain unchanged from the input grid.
6.  Return the modified grid.
