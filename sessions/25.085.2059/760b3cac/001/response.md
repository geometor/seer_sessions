```python
import numpy as np

def find_colored_pixels(grid, color):
    """Finds all coordinates of pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def transform(input_grid):
    """
    Identifies the azure object (color 8) in the input grid.
    Calculates the reflection of each azure pixel across the vertical line 
    immediately to the left of the object's leftmost extent.
    Adds these reflected azure pixels to the grid, preserving the original 
    azure pixels and all other pixels.
    If no azure pixels are present, the grid remains unchanged.
    """
    
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid)
    output_grid = np.copy(input_array)
    height, width = input_array.shape

    # Define the color to be reflected (azure)
    reflect_color = 8

    # Find all pixels of the target color
    azure_pixels = find_colored_pixels(input_array, reflect_color)

    # If no azure pixels are found, return the original grid
    if not azure_pixels:
        return output_grid.tolist() # return as list of lists

    # Find the leftmost column index of the azure object
    min_col = min(c for r, c in azure_pixels)

    # Calculate reflections and update the output grid
    for r, c in azure_pixels:
        # Calculate the reflected column index
        # Reflection line is at x = min_col - 0.5
        # reflected_c = (min_col - 0.5) - (c - (min_col - 0.5))
        # reflected_c = min_col - 0.5 - c + min_col - 0.5
        # reflected_c = 2 * min_col - c - 1
        reflected_c = 2 * min_col - c - 1

        # Check if the reflected column is within the grid bounds
        if 0 <= reflected_c < width:
            # Add the reflected pixel to the output grid
            output_grid[r, reflected_c] = reflect_color

    # Return the modified grid as a list of lists
    return output_grid.tolist()
```