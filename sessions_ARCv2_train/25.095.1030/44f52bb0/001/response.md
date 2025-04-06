```python
import numpy as np

"""
Analyzes the symmetry of a 3x3 input grid containing 0s and 2s.
Outputs 1 if the grid exhibits horizontal, vertical, main diagonal,
anti-diagonal, or 180-degree rotational symmetry.
Outputs 7 otherwise.
"""

# Helper function to check horizontal symmetry
def is_horizontally_symmetric(grid):
    """Checks if the grid is symmetric across the horizontal midline."""
    return np.array_equal(grid[0,:], grid[2,:])

# Helper function to check vertical symmetry
def is_vertically_symmetric(grid):
    """Checks if the grid is symmetric across the vertical midline."""
    return np.array_equal(grid[:,0], grid[:,2])

# Helper function to check main diagonal symmetry
def is_diagonally_symmetric(grid):
    """Checks if the grid is symmetric across the main diagonal (top-left to bottom-right)."""
    return np.array_equal(grid, grid.T) # Check if the grid is equal to its transpose

# Helper function to check anti-diagonal symmetry
def is_anti_diagonally_symmetric(grid):
    """Checks if the grid is symmetric across the anti-diagonal (top-right to bottom-left)."""
    # Compare elements across the anti-diagonal
    # grid[0,0] == grid[2,2]
    # grid[0,1] == grid[1,2]
    # grid[1,0] == grid[2,1]
    # grid[0,2] == grid[0,2] (trivial)
    # grid[1,1] == grid[1,1] (trivial)
    # grid[2,0] == grid[2,0] (trivial)
    if grid[0,0] != grid[2,2]: return False
    if grid[0,1] != grid[1,2]: return False
    if grid[1,0] != grid[2,1]: return False
    return True

# Helper function to check 180-degree rotational symmetry
def is_rotationally_symmetric_180(grid):
    """Checks if the grid is symmetric after a 180-degree rotation."""
    # Compare elements opposite through the center
    # grid[i,j] == grid[2-i, 2-j]
    # grid[0,0] == grid[2,2]
    # grid[0,1] == grid[2,1]
    # grid[0,2] == grid[2,0]
    # grid[1,0] == grid[1,2]
    # grid[1,1] == grid[1,1] (trivial)
    rotated_grid = np.rot90(grid, 2) # Rotate 180 degrees
    return np.array_equal(grid, rotated_grid)

def transform(input_grid):
    """
    Receives a 3x3 input grid.
    Checks for horizontal, vertical, diagonal, anti-diagonal, and 180-degree rotational symmetry.
    Returns 1 if any symmetry is found, otherwise returns 7.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    grid = np.array(input_grid)

    # Check for horizontal symmetry
    if is_horizontally_symmetric(grid):
        return 1

    # Check for vertical symmetry
    if is_vertically_symmetric(grid):
        return 1

    # Check for main diagonal symmetry
    if is_diagonally_symmetric(grid):
        return 1

    # Check for anti-diagonal symmetry
    if is_anti_diagonally_symmetric(grid):
        return 1

    # Check for 180-degree rotational symmetry
    if is_rotationally_symmetric_180(grid):
        return 1

    # If none of the symmetries are found, return 7
    return 7
```