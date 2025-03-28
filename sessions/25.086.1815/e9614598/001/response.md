```python
import numpy as np

def find_pixels_by_color(grid, color):
    """
    Finds the coordinates of all pixels with a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to search for.

    Returns:
        list: A list of tuples, where each tuple is the (row, col) coordinate
              of a pixel with the specified color.
    """
    coords = np.argwhere(grid == color)
    # Convert numpy array coordinates to list of tuples
    return [tuple(coord) for coord in coords]

def transform(input_grid):
    """
    Transforms the input grid by finding the midpoint between two blue (1) pixels
    and drawing a green (3) cross '+' shape centered at that midpoint.

    1. Copies the input grid to create the output grid.
    2. Locates the coordinates of the two blue (1) pixels.
    3. Calculates the integer midpoint coordinates between the blue pixels.
    4. Defines the coordinates for a 3x3 cross shape (center and 4 orthogonal neighbors).
    5. Draws the green (3) cross onto the output grid at the calculated midpoint,
       overwriting existing pixels and respecting grid boundaries.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    height, width = grid.shape

    # Find the coordinates of the two blue pixels
    blue_pixel_coords = find_pixels_by_color(grid, 1)

    # Ensure exactly two blue pixels are found
    if len(blue_pixel_coords) != 2:
        # Handle error or unexpected input: returning original grid for now
        print(f"Warning: Expected 2 blue pixels, found {len(blue_pixel_coords)}. Returning original grid.")
        return input_grid # Or raise an error, depending on desired behavior

    (r1, c1), (r2, c2) = blue_pixel_coords

    # Calculate the midpoint using integer division
    mid_row = (r1 + r2) // 2
    mid_col = (c1 + c2) // 2

    # Define the relative coordinates for the cross shape (center, up, down, left, right)
    cross_offsets = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]

    # Draw the green cross on the output grid
    green_color = 3
    for dr, dc in cross_offsets:
        cross_r, cross_c = mid_row + dr, mid_col + dc

        # Check if the coordinate is within the grid boundaries
        if 0 <= cross_r < height and 0 <= cross_c < width:
            output_grid[cross_r, cross_c] = green_color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```