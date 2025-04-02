import numpy as np

"""
Transforms an input grid by recoloring two specific shapes (yellow=4, orange=7) based on a comparison of their pixel counts.

1. Count the number of yellow (4) pixels in the input grid.
2. Count the number of orange (7) pixels in the input grid.
3. Compare the counts:
   - If the count of yellow pixels equals the count of orange pixels, the target replacement color is azure (8).
   - Otherwise, the target replacement color is gray (5).
4. Create an output grid by replacing all yellow (4) and orange (7) pixels in the input grid with the determined target replacement color.
5. Keep all other pixels (background white=0) unchanged.
"""

def transform(input_grid):
    """
    Applies the recoloring transformation based on pixel counts.

    Args:
        input_grid (list[list[int]]): The input 2D grid.

    Returns:
        list[list[int]]: The transformed 2D grid.
    """
    # Convert the input list of lists to a NumPy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)

    # Count the occurrences of yellow (4) pixels
    yellow_count = np.sum(grid_np == 4)

    # Count the occurrences of orange (7) pixels
    orange_count = np.sum(grid_np == 7)

    # Determine the target replacement color based on the counts
    if yellow_count == orange_count:
        target_color = 8  # Azure
    else:
        target_color = 5  # Gray

    # Initialize the output grid as a copy of the input grid
    output_grid_np = grid_np.copy()

    # Identify the locations of yellow (4) and orange (7) pixels
    mask = (output_grid_np == 4) | (output_grid_np == 7)

    # Change the color of the identified pixels to the target color
    output_grid_np[mask] = target_color

    # Convert the NumPy array back to a list of lists for the final output
    output_grid = output_grid_np.tolist()

    return output_grid
