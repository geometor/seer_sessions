import numpy as np

"""
Processes an input grid based on pixel adjacency rules. 
A pixel P's color is changed to white (0) in the output grid if it meets specific criteria involving its own color and the colors of its 8 neighboring pixels (including diagonals) in the input grid. Otherwise, the pixel retains its original color.

The specific rules for changing a pixel P with color C_P to white (0) are:
- If P is Orange (7) and has at least one Blue (1) neighbor.
- If P is Gray (5) and has at least one Red (2) neighbor.
- If P is Magenta (6) and has at least one Green (3) neighbor.
- If P is Azure (8) and has at least one Magenta (6) neighbor.
- If P is Azure (8) and has at least one Orange (7) neighbor.

All other pixels, including initially white pixels, remain unchanged.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    rows, cols = input_np.shape

    # Define the relative coordinates for the 8 neighbors (Moore neighborhood)
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Define the trigger pairs (Neighbor Color, Pixel Color)
    # Note: An Azure (8) pixel is removed by *either* Magenta (6) or Orange (7) neighbors.
    trigger_rules = {
        7: {1},  # Orange (7) removed by Blue (1)
        5: {2},  # Gray (5) removed by Red (2)
        6: {3},  # Magenta (6) removed by Green (3)
        8: {6, 7} # Azure (8) removed by Magenta (6) OR Orange (7)
    }


    # Iterate through each pixel in the input grid
    for r in range(rows):
        for c in range(cols):
            current_pixel_color = input_np[r, c]

            # If the current pixel is already white, skip it
            if current_pixel_color == 0:
                continue

            # Check if the current pixel color is one that can be potentially removed
            if current_pixel_color in trigger_rules:
                trigger_neighbor_colors = trigger_rules[current_pixel_color]
                remove_pixel = False

                # Check all 8 neighbors
                for dr, dc in neighbor_offsets:
                    nr, nc = r + dr, c + dc

                    # Check if the neighbor is within the grid boundaries
                    if 0 <= nr < rows and 0 <= nc < cols:
                        neighbor_color = input_np[nr, nc]

                        # Check if the neighbor color is a trigger for the current pixel's color
                        if neighbor_color in trigger_neighbor_colors:
                            remove_pixel = True
                            break # Found a trigger neighbor, no need to check others

                # If a trigger neighbor was found, change the pixel in the output grid to white
                if remove_pixel:
                    output_grid[r, c] = 0

    # Convert the numpy array back to a list of lists for the final output
    return output_grid.tolist()