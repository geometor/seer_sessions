import numpy as np

"""
Transforms a 9x9 input grid into a 3x3 output grid.
The input grid is divided into nine 3x3 subgrids. 
For each 3x3 subgrid:
1. Find all unique colors present.
2. Filter out white (0) and gray (5).
3. If exactly one distinct color remains after filtering, the corresponding pixel in the output grid takes this color.
4. If zero distinct colors remain (i.e., the subgrid contains only white and/or gray), the corresponding output pixel is white (0).
"""

def find_dominant_color(subgrid):
    """
    Finds the dominant non-background, non-noise color in a subgrid.
    Args:
        subgrid (np.array): A 3x3 numpy array representing the subgrid.
    Returns:
        int: The dominant color, or 0 (white) if none found (only white/gray present).
    """
    # Find unique colors in the subgrid
    unique_colors = np.unique(subgrid)

    # Filter out background (0) and noise (5) colors
    filtered_colors = [color for color in unique_colors if color != 0 and color != 5]

    # Determine the output color
    if len(filtered_colors) == 1:
        # If exactly one non-background, non-noise color is found, use it
        return filtered_colors[0]
    else:
        # Otherwise (including cases with multiple colors or only 0s and 5s), default to white
        return 0

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Args:
        input_grid (list of lists): The input 9x9 grid.
    Returns:
        list of lists: The transformed 3x3 output grid.
    """
    # Convert input list of lists to a numpy array for easier slicing
    input_array = np.array(input_grid, dtype=int)
    input_height, input_width = input_array.shape
    output_height = input_height // 3
    output_width = input_width // 3

    # Initialize the output grid with white (0)
    output_array = np.zeros((output_height, output_width), dtype=int)

    # Iterate through the input grid in 3x3 steps
    for r in range(0, input_height, 3):
        for c in range(0, input_width, 3):
            # Extract the 3x3 subgrid
            subgrid = input_array[r:r+3, c:c+3]

            # Find the dominant color in the subgrid (excluding 0 and 5)
            dominant_color = find_dominant_color(subgrid)

            # Assign the dominant color to the corresponding pixel in the output grid
            output_array[r // 3, c // 3] = dominant_color

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()
    return output_grid
