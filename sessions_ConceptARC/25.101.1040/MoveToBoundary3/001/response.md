```python
import numpy as np

"""
Transformation Rule:
Identify the single non-background object (red) in the input grid.
Determine the horizontal distance between the object's rightmost edge and the right edge of the grid.
Translate the object horizontally to the right by this distance, so its rightmost edge aligns with the grid's right edge.
The object's shape, color, and vertical position remain unchanged. The output grid has the same dimensions as the input grid.
"""

def find_object_pixels(grid: np.ndarray, background_color: int = 0) -> tuple[list[tuple[int, int]], int]:
    """
    Finds all pixels belonging to the first non-background object encountered.

    Args:
        grid: The input grid as a NumPy array.
        background_color: The integer value representing the background color.

    Returns:
        A tuple containing:
        - A list of (row, col) coordinates for the object's pixels.
        - The color of the object.
        Returns ([], -1) if no object is found.
    """
    object_pixels = []
    object_color = -1
    height, width = grid.shape
    
    # Find the first non-background pixel to determine object color
    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color:
                object_color = grid[r, c]
                break
        if object_color != -1:
            break

    if object_color == -1:
        return [], -1 # No object found

    # Find all pixels of that color
    for r in range(height):
        for c in range(width):
            if grid[r, c] == object_color:
                object_pixels.append((r, c))
                
    # Basic check for contiguity might be needed for more complex cases,
    # but for this task, assuming a single contiguous object of one color is sufficient.
                
    return object_pixels, object_color

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule: moves the single object horizontally
    so its right edge aligns with the grid's right edge.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    background_color = 0

    # Find the pixels and color of the object
    object_pixels, object_color = find_object_pixels(input_np, background_color)

    # If no object is found, return the input grid as is (or an empty grid of same size)
    if not object_pixels:
        return input_grid # Or return [[0]*width for _ in range(height)] if required

    # Find the rightmost column occupied by the object
    rightmost_col = -1
    for r, c in object_pixels:
        if c > rightmost_col:
            rightmost_col = c

    # Calculate the horizontal shift needed
    # Shift = (target rightmost column) - (current rightmost column)
    # Target rightmost column is width - 1
    shift = (width - 1) - rightmost_col

    # Initialize the output grid with the background color
    output_np = np.full((height, width), background_color, dtype=int)

    # Place the object in the new position on the output grid
    for r, c in object_pixels:
        new_col = c + shift
        # Ensure the new column is within grid bounds (should be by calculation)
        if 0 <= new_col < width:
            output_np[r, new_col] = object_color

    # Convert the NumPy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
```