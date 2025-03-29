import numpy as np
from typing import List, Tuple

"""
Transformation Rule:
1. Identify all pixels with the color azure (8) in the input grid.
2. If no azure pixels are found, return the input grid unchanged.
3. Determine the minimum bounding box that encloses all azure pixels. The bounding box is defined by the minimum and maximum row and column indices of the azure pixels.
4. Create a copy of the input grid to serve as the output grid.
5. Iterate through each pixel (r, c) of the input grid.
6. If the pixel at (r, c) is blue (1):
   a. Check if the pixel's coordinates (r, c) fall within the row and column range of the calculated bounding box (inclusive).
   b. Check if any of the pixel's 8 neighbors (orthogonal and diagonal) in the input grid have the color azure (8).
   c. If both conditions (a and b) are true, change the color of the pixel at (r, c) in the output grid to green (3).
7. Return the modified output grid.
"""

def find_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates of pixels with a specific color."""
    coords = np.argwhere(grid == color)
    return [tuple(coord) for coord in coords]

def get_bounding_box(coords: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """Calculates the bounding box (min_r, min_c, max_r, max_c) for a list of coordinates."""
    if not coords:
        # This case should be handled before calling, but added for safety.
        raise ValueError("Cannot calculate bounding box for empty coordinates list.")
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    return (min(rows), min(cols), max(rows), max(cols))

def has_neighbor_color(grid: np.ndarray, r: int, c: int, color: int) -> bool:
    """Checks if any of the 8 neighbors of pixel (r, c) has the specified color."""
    height, width = grid.shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the center pixel itself
            if dr == 0 and dc == 0:
                continue
            
            nr, nc = r + dr, c + dc
            
            # Check if the neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor has the target color
                if grid[nr, nc] == color:
                    return True
    return False

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule: Changes blue pixels within the bounding box
    of azure pixels to green if they are adjacent to an azure pixel.
    """
    # Convert input list of lists to a numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, ensuring the original input is unchanged
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Define the relevant colors
    BLUE = 1
    GREEN = 3
    AZURE = 8

    # Step 1: Find all azure pixels
    azure_coords = find_pixels(input_np, AZURE)

    # Step 2: If no azure pixels, return the original grid
    if not azure_coords:
        return input_grid

    # Step 3: Determine the bounding box of azure pixels
    min_r, min_c, max_r, max_c = get_bounding_box(azure_coords)

    # Step 4 & 5: Iterate through each pixel of the grid
    for r in range(height):
        for c in range(width):
            # Step 6: Check if the current pixel is blue
            if input_np[r, c] == BLUE:
                
                # Step 6a: Check if the pixel is within the bounding box
                is_in_bbox = (min_r <= r <= max_r and min_c <= c <= max_c)

                # Step 6b: Check if it has an azure neighbor
                has_azure_neighbor = has_neighbor_color(input_np, r, c, AZURE)

                # Step 6c: If both conditions are met, change the pixel to green in the output grid
                if is_in_bbox and has_azure_neighbor:
                    output_np[r, c] = GREEN

    # Step 7: Return the modified grid as a list of lists
    return output_np.tolist()