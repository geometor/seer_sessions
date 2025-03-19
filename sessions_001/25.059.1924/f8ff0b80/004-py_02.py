"""
1.  **Identify Shapes:** Examine the input grid and identify all distinct, contiguous shapes. A shape is defined as a group of one or more adjacent pixels of the same color. Diagonal adjacency is included in the definition of adjacency.
2.  **Extract Colors:** For each identified shape, extract the numerical color value of the pixels within that shape.
3. **Order colors:** Create an ordered sequence of the extracted colors. The ordering does not seem to follow any apparent rule besides that it should contain the color values, exactly once.
4.  **Output Sequence:** Output the sequence as a column vector.
"""

import numpy as np

def find_shapes(grid):
    """Finds contiguous shapes in a grid."""
    shapes = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, current_shape):
        """Depth-first search to find contiguous pixels of the same color."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_shape.append((row, col))
        # Check all 8 neighbors (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(row + dr, col + dc, color, current_shape)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                current_shape = []
                dfs(row, col, grid[row, col], current_shape)
                if current_shape:
                    shapes.append((grid[row,col], current_shape))  # Store color and shape
    return shapes

def transform(input_grid):
    # Find shapes in the input grid
    shapes = find_shapes(np.array(input_grid))

    # Extract the color of each shape
    colors = []
    
    for color, _ in shapes:
        colors.append(color)
    
    colors = sorted(list(set(colors)))

    return colors