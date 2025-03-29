"""
Transformation Rule:
Iterate through each pixel of the input grid. If a pixel is azure (8), check if there are blue pixels (1) located exactly two steps away in all four cardinal directions (up, down, left, right) relative to the azure pixel's position. If all four such blue pixels exist within the grid boundaries, change the color of the central azure pixel to yellow (4) in the output grid. Otherwise, the pixel retains its original color.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a NumPy array for easier indexing and boundary checks
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # Define the target color (azure) and the marker color (blue)
    target_color = 8
    marker_color = 1
    replacement_color = 4

    # Define the relative positions of the required markers (2 steps away cardinally)
    relative_positions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is the target color (azure)
            if input_array[r, c] == target_color:
                
                all_markers_found = True
                # Check for the required marker pixels at relative positions
                for dr, dc in relative_positions:
                    nr, nc = r + dr, c + dc # Calculate neighbor coordinates

                    # Check if the neighbor coordinates are within grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor pixel has the marker color (blue)
                        if input_array[nr, nc] != marker_color:
                            all_markers_found = False
                            break # No need to check further if one marker is missing or wrong color
                    else:
                        # If any required marker position is outside the grid, the condition is not met
                        all_markers_found = False
                        break 
                
                # If all four markers were found in the correct positions and color
                if all_markers_found:
                    # Change the color of the pixel in the output grid to yellow
                    output_array[r, c] = replacement_color

    # Convert the NumPy array back to a list of lists for the final output
    return output_array.tolist()
