```python
import numpy as np

"""
Transforms the input grid based on the relative positions of azure (8) and yellow (4) objects.

1. Identifies all azure (color 8) pixels and all yellow (color 4) pixels.
2. If no azure pixels are found, the original grid is returned.
3. Determines the horizontal span of the azure object by finding its minimum (min_col_azure) 
   and maximum (max_col_azure) column indices.
4. Calculates the center of this horizontal span: center_azure = (min_col_azure + max_col_azure) / 2.0.
5. Calculates the average column index of all yellow pixels (avg_col_yellow).
6. Compares avg_col_yellow to center_azure to determine the reflection direction:
   - If avg_col_yellow >= center_azure, reflection is to the RIGHT. 
     The reflection axis is the vertical line x = max_col_azure + 0.5.
   - If avg_col_yellow < center_azure (or if no yellow pixels are found), 
     reflection is to the LEFT. The reflection axis is the vertical line x = min_col_azure - 0.5.
7. Creates a copy of the input grid.
8. For each original azure pixel (r, c):
   - Calculates its reflected column coordinate (reflected_c) based on the determined axis.
   - Right Reflection: reflected_c = 2 * max_col_azure + 1 - c
   - Left Reflection: reflected_c = 2 * min_col_azure - 1 - c
   - If the reflected coordinate (r, reflected_c) is within the grid bounds, 
     sets the corresponding pixel in the output grid copy to azure (8).
9. Returns the modified grid.
"""

def find_colored_pixels(grid, color):
    """Finds all coordinates (row, col) of pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def calculate_average_column(pixels):
    """Calculates the average column index for a list of pixel coordinates."""
    if not pixels:
        # Return NaN if no pixels; comparison logic handles NaN later
        return np.nan 
    cols = [c for r, c in pixels]
    return np.mean(cols)

def transform(input_grid):
    # Convert input grid (list of lists) to a NumPy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original input
    output_grid = np.copy(input_array)
    height, width = input_array.shape

    # Define the colors involved in the transformation
    azure_color = 8
    yellow_color = 4

    # Locate all pixels of the specified colors
    azure_pixels = find_colored_pixels(input_array, azure_color)
    yellow_pixels = find_colored_pixels(input_array, yellow_color)

    # If there are no azure pixels, no transformation occurs, return the original grid
    if not azure_pixels:
        return output_grid.tolist() 

    # Calculate necessary properties of the azure object
    azure_cols = [c for r, c in azure_pixels]
    min_col_azure = min(azure_cols)
    max_col_azure = max(azure_cols)
    # Calculate the center of the azure object's horizontal extent
    center_azure = (min_col_azure + max_col_azure) / 2.0

    # Calculate the average column index for the yellow object
    avg_col_yellow = calculate_average_column(yellow_pixels)

    # Determine the reflection direction based on yellow object's average position 
    # relative to the azure object's center. 
    # If avg_col_yellow is NaN (no yellow pixels), treat it as less than center_azure (default to left).
    reflect_right = not np.isnan(avg_col_yellow) and avg_col_yellow >= center_azure

    # Iterate through each azure pixel to calculate and apply its reflection
    for r, c in azure_pixels:
        reflected_c = -1 # Initialize with an invalid column index

        if reflect_right:
            # Calculate reflection across axis x = max_col_azure + 0.5
            reflected_c = 2 * max_col_azure + 1 - c
        else: # Reflect left
            # Calculate reflection across axis x = min_col_azure - 0.5
            reflected_c = 2 * min_col_azure - 1 - c

        # Check if the calculated reflected column is within the grid's boundaries
        if 0 <= reflected_c < width:
            # Convert reflected_c to integer (should already be int, but ensures type safety)
            reflected_c_int = int(round(reflected_c)) 
            # Set the pixel at the reflected coordinates to the azure color in the output grid
            output_grid[r, reflected_c_int] = azure_color

    # Convert the final NumPy array back to a list of lists for the expected output format
    return output_grid.tolist()
```