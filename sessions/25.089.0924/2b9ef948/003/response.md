```python
import numpy as np

"""
Transformation Rule:
1. Locate a 3x3 pattern in the input grid consisting of 8 yellow (4) pixels forming a border around a single, non-yellow, non-white central pixel.
2. Determine the color of this central pixel. This color becomes the background fill color for the output grid.
3. Identify the coordinates of *all* yellow (4) pixels present anywhere in the input grid.
4. Initialize the output grid with the same dimensions as the input grid, completely filled with the determined background color.
5. Iterate through the coordinates of all identified yellow pixels from the input. Set the pixels at these specific coordinates in the output grid back to yellow (4), overlaying the background fill.
6. All other non-yellow elements from the input grid are ignored.
"""

def find_yellow_square_center_color(grid):
    """
    Scans the grid to find the 3x3 yellow square pattern and return its center color.

    Args:
        grid (np.array): The input grid.

    Returns:
        int: The color of the center pixel if the pattern is found,
             otherwise None.
    """
    rows, cols = grid.shape
    for r in range(rows - 2):
        for c in range(cols - 2):
            # Extract the 3x3 subgrid
            subgrid = grid[r:r+3, c:c+3]

            # Check center pixel color (must not be yellow or white)
            center_color = subgrid[1, 1]
            if center_color == 4 or center_color == 0:
                continue

            # Check if border pixels are yellow (4)
            is_yellow_border = True
            for i in range(3):
                for j in range(3):
                    if i == 1 and j == 1: # Skip center
                        continue
                    if subgrid[i, j] != 4:
                        is_yellow_border = False
                        break
                if not is_yellow_border:
                    break

            if is_yellow_border:
                # Pattern found
                return center_color
    return None # Pattern not found

def find_all_pixels_of_color(grid, color):
    """
    Finds all coordinates of pixels with a specific color.

    Args:
        grid (np.array): The input grid.
        color (int): The color to find.

    Returns:
        list: A list of (row, col) tuples for pixels matching the color.
    """
    coords = np.where(grid == color)
    return list(zip(coords[0], coords[1]))


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # 1 & 2: Find the 3x3 square and determine the background color
    background_color = find_yellow_square_center_color(input_grid)

    if background_color is None:
        # Handle cases where the pattern isn't found (shouldn't occur based on examples)
        print("Warning: Characteristic 3x3 yellow square pattern not found.")
        # Return a default or copy? Let's return a copy.
        return np.copy(input_grid)

    # 3: Identify the coordinates of all yellow pixels in the input
    yellow_coords = find_all_pixels_of_color(input_grid, 4) # 4 is yellow

    # 4: Initialize the output grid with the background color
    output_grid = np.full_like(input_grid, background_color)

    # 5: Overlay all original yellow pixels onto the output grid
    for r, c in yellow_coords:
        output_grid[r, c] = 4 # Set to yellow

    # 6: Implicitly done by initializing with background and only overlaying yellow.
    return output_grid
```