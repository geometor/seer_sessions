```python
"""
Transformation Rule:
1. Identify connected components of non-orange (7) pixels using 8-way adjacency.
2. For each component, determine its bounding box.
3. If a component's bounding box is exactly 3x3 pixels in size:
    a. Identify the 8 pixels forming the perimeter of this 3x3 box in the input grid.
    b. Rotate the values of these 8 perimeter pixels one step counter-clockwise.
    c. Place these rotated values into the corresponding perimeter positions in the output grid.
    d. The central pixel of the 3x3 box remains unchanged.
4. All pixels outside of these identified 3x3 bounding boxes remain unchanged from the input grid.
The output grid is initially a copy of the input grid, and modifications are applied based on the identified 3x3 components.
"""

import numpy as np
from typing import List, Tuple, Set

def find_connected_components(grid: np.ndarray, background_color: int) -> List[List[Tuple[int, int]]]:
    """
    Finds all connected components of non-background pixels using 8-way adjacency.

    Args:
        grid: The input numpy array representing the grid.
        background_color: The integer value representing the background color.

    Returns:
        A list of components, where each component is a list of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and not visited[r, c]:
                # Start BFS for a new component
                component = []
                q = [(r, c)]
                visited[r, c] = True
                while q:
                    row, col = q.pop(0)
                    component.append((row, col))

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue  # Skip self
                            nr, nc = row + dr, col + dc

                            # Check bounds and if it's a non-background pixel and not visited
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] != background_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                components.append(component)
    return components

def get_bounding_box(component: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """
    Calculates the bounding box of a component.

    Args:
        component: A list of (row, col) tuples representing the pixels of the component.

    Returns:
        A tuple (min_row, min_col, max_row, max_col).
    """
    if not component:
        return -1, -1, -1, -1 # Or raise an error

    rows = [p[0] for p in component]
    cols = [p[1] for p in component]
    return min(rows), min(cols), max(rows), max(cols)

def rotate_perimeter(input_grid: np.ndarray, output_grid: np.ndarray, r: int, c: int):
    """
    Rotates the perimeter of the 3x3 subgrid starting at (r, c) counter-clockwise.
    Reads from input_grid and writes to output_grid.

    Args:
        input_grid: The original input grid.
        output_grid: The grid to be modified.
        r: The top row index of the 3x3 box.
        c: The left column index of the 3x3 box.
    """
    # Store the original perimeter values from the input_grid
    p = [
        input_grid[r, c],     input_grid[r, c+1],   input_grid[r, c+2],
        input_grid[r+1, c+2], input_grid[r+2, c+2], input_grid[r+2, c+1],
        input_grid[r+2, c],   input_grid[r+1, c]
    ]

    # Apply rotated values to the output_grid perimeter
    output_grid[r, c]   = p[2]  # Top-Right   -> Top-Left
    output_grid[r, c+1] = p[7]  # Middle-Left -> Top-Center
    output_grid[r, c+2] = p[4]  # Bottom-Right-> Top-Right
    output_grid[r+1, c] = p[6]  # Bottom-Left -> Middle-Left
    # Center output_grid[r+1, c+1] remains unchanged (already copied)
    output_grid[r+1, c+2]= p[1]  # Top-Center  -> Middle-Right
    output_grid[r+2, c] = p[0]  # Top-Left    -> Bottom-Left
    output_grid[r+2, c+1]= p[3]  # Middle-Right-> Bottom-Center
    output_grid[r+2, c+2]= p[5]  # Bottom-Center->Bottom-Right

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by finding 3x3 components of non-orange pixels
    and rotating their perimeters counter-clockwise.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Define background color
    background_color = 7

    # Find all connected components of non-background pixels
    components = find_connected_components(input_grid, background_color)

    # Process each component
    for component in components:
        if not component:
            continue
            
        # Calculate the bounding box
        min_r, min_c, max_r, max_c = get_bounding_box(component)

        # Check if the bounding box is exactly 3x3
        height = max_r - min_r + 1
        width = max_c - min_c + 1

        if height == 3 and width == 3:
            # If it's a 3x3 box, rotate its perimeter
            # The rotation uses values from the original input_grid
            # and writes the results to the output_grid.
            rotate_perimeter(input_grid, output_grid, min_r, min_c)
            # Note: The center pixel output_grid[min_r+1, min_c+1] is already
            # correct because output_grid started as a copy of input_grid.

    # Return the modified output grid
    return output_grid
```