
## train_1

**input:**
```
0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 0 0 1 0
0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0
0 6 0 0 6 6 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 6 6 6 6 6 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 6 6 6 6 6 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 6 6 6 6 6 0
0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0
3 3 3 3 3 0 3 3
3 3 3 3 3 3 0 3
3 3 0 3 3 3 3 3
3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

Okay, let's analyze the task examples.

## Perception

1.  **Input/Output Grids:** Each example consists of an input grid and a corresponding output grid of the same dimensions (8x8 in all provided examples).
2.  **Colors:** The grids primarily use white (0) as the background color. Each input grid features a prominent shape or pattern made of a single non-white color (blue=1, magenta=6, green=3).
3.  **Transformation:** The core transformation involves changing some white pixels (0) within the input grid to the non-white color present in that grid. The surrounding non-white shape and the white pixels outside this shape remain unchanged.
4.  **Pattern:** The white pixels that are changed appear to be "holes" or "gaps" within the main colored shape.
    *   In `train_1`, a 1x2 horizontal gap `(0 0)` within a blue rectangle is filled with blue.
    *   In `train_2`, a 1x2 horizontal gap `(0 0)` in the *topmost row* of a hollow magenta structure is filled with magenta. Other internal white pixels remain unchanged.
    *   In `train_3`, two separate single-pixel gaps `(0)` within a green shape are filled with green.
5.  **Key Insight:** The transformation doesn't fill *all* internal white pixels. Comparing
```python
"""
Identifies small connected components of white pixels (color 0) that do not 
touch the grid border and fills them with the surrounding non-white color. 
A component is considered 'small' if it contains 1 or 2 pixels.
The surrounding non-white color is assumed to be the single dominant 
non-white color present in the input grid's shape.
Connectivity is determined by 4-way adjacency (up, down, left, right).
"""

import collections
import numpy as np

def find_fill_color(grid):
    """
    Finds the first non-background (non-zero) color in the grid.
    Assumes there is one dominant non-white color forming the shape.
    
    Args:
        grid (np.array): The input grid.
    
    Returns:
        int: The first non-zero color value found, or 0 if the grid is all zeros.
    """
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                return grid[r, c]
    # Return background color if no non-zero color is found
    return 0 

def transform(input_grid):
    """
    Transforms the input grid by filling small (size <= 2), non-border-touching
    white components with the dominant non-white color.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    # Create a copy to modify, preserving the original input grid state for checks
    output_grid = grid.copy()
    # Keep track of visited pixels during component search
    visited = np.zeros_like(grid, dtype=bool)
    
    # Determine the color to use for filling the holes
    fill_color = find_fill_color(grid)
    
    # If the grid is entirely background or no fill color found, return the original
    if fill_color == 0: 
        return output_grid.tolist() 

    # Queue for Breadth-First Search (BFS)
    q = collections.deque()

    # Iterate through each pixel to find starting points for white components
    for r in range(height):
        for c in range(width):
            # Start a new component search if we find an unvisited white pixel
            if grid[r, c] == 0 and not visited[r, c]:
                # Initialize properties for the current component
                component_pixels = []
                touches_border = False
                is_valid_component = True # Assume valid until found otherwise
                
                # Start BFS from this pixel
                q.append((r, c))
                visited[r, c] = True
                
                # Process the queue until the component is fully explored
                while q:
                    curr_r, curr_c = q.popleft()
                    component_pixels.append((curr_r, curr_c))
                    
                    # Check if this pixel is on the border
                    if curr_r == 0 or curr_r == height - 1 or curr_c == 0 or curr_c == width - 1:
                        touches_border = True
                        
                    # Explore neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Check if neighbor is within grid boundaries
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if neighbor is part of the same white component
                            if grid[nr, nc] == 0 and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))

                # Component search finished, check conditions for filling
                component_size = len(component_pixels)
                
                # Fill the component in the output grid if it's small and not touching the border
                if not touches_border and component_size <= 2:
                    for pr, pc in component_pixels:
                        output_grid[pr, pc] = fill_color

    # Convert the result back to a list of lists
    return output_grid.tolist()
```
```python
"""
Transforms the input grid by finding the dominant non-white color (C) and 
filling any white pixel (0) that has 3 or 4 neighbors of color C with that color C.
Neighbors are checked using 4-way adjacency (up, down, left, right).
"""

import numpy as np

def find_dominant_color(grid):
    """
    Finds the first non-background (non-zero) color in the grid.
    Assumes there is one dominant non-white color forming the shape.
    
    Args:
        grid (np.array): The input grid.
    
    Returns:
        int: The first non-zero color value found, or None if the grid is all zeros.
    """
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0:
            return color
    return None # Return None if only background color (0) is found

def count_neighbors(grid, r, c, color):
    """
    Counts the number of 4-directionally adjacent neighbors of a pixel (r, c) 
    that have the specified color. Handles boundary conditions.

    Args:
        grid (np.array): The grid.
        r (int): Row index of the pixel.
        c (int): Column index of the pixel.
        color (int): The color to count neighbors for.

    Returns:
        int: The number of neighbors with the specified color.
    """
    height, width = grid.shape
    count = 0
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        # Check if neighbor is within grid boundaries
        if 0 <= nr < height and 0 <= nc < width:
            # Check if neighbor has the target color
            if grid[nr, nc] == color:
                count += 1
    return count

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    
    # Create a copy to modify
    output_grid = grid.copy()

    # Find the dominant non-white color
    dominant_color = find_dominant_color(grid)

    # If no dominant color found (e.g., all white grid), return the original grid
    if dominant_color is None:
        return output_grid.tolist()

    # Iterate through each pixel of the original grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is white (0)
            if grid[r, c] == 0:
                # Count how many neighbors have the dominant color
                neighbor_count = count_neighbors(grid, r, c, dominant_color)
                
                # If the count is 3 or more, fill the pixel in the output grid
                if neighbor_count >= 3:
                    output_grid[r, c] = dominant_color

    # Convert the result back to a list of lists
    return output_grid.tolist()
```
