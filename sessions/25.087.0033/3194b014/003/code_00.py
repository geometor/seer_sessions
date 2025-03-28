import numpy as np
from collections import Counter

"""
Identifies all 3x3 monochromatic subgrids within the input grid. 
Counts the occurrences of each color forming these subgrids.
Determines the color that appears most frequently in these 3x3 solid squares.
Creates a 3x3 output grid filled entirely with this most frequent color.
"""

def find_most_frequent_3x3_color(grid):
    """
    Finds the color that forms the most numerous 3x3 monochromatic subgrids.

    Args:
        grid (np.array): The input grid as a numpy array.

    Returns:
        int: The color value that forms the most 3x3 solid squares.
        Returns -1 if no solid 3x3 squares are found.
    """
    height, width = grid.shape
    # Use a Counter to store the counts of colors forming solid 3x3 squares
    color_counts = Counter()

    # Iterate through all possible top-left corners of a 3x3 square
    for r in range(height - 2):
        for c in range(width - 2):
            # Extract the 3x3 subgrid
            subgrid = grid[r:r+3, c:c+3]
            
            # Get the color of the top-left pixel of the subgrid
            potential_color = subgrid[0, 0]
            
            # Check if all elements in the subgrid are the same color
            if np.all(subgrid == potential_color):
                # Increment the count for this color
                color_counts[potential_color] += 1

    # Find the color with the highest count
    if not color_counts:
        # Handle the case where no solid 3x3 squares are found
        print("Warning: No solid 3x3 square found in the input grid.")
        return -1 # Or perhaps 0 (white) as a default? Returning -1 signals an issue.
        
    # Find the color(s) with the maximum frequency
    max_freq = 0
    most_frequent_colors = []
    for color, count in color_counts.items():
        if count > max_freq:
            max_freq = count
            most_frequent_colors = [color]
        elif count == max_freq:
            most_frequent_colors.append(color)

    # If there's a tie in frequency, the problem description doesn't specify
    # a tie-breaking rule. Based on re-evaluating the examples, the simple
    # max frequency seemed sufficient. We'll pick the first one found in case of a tie,
    # which depends on dictionary iteration order (or use min/max color value if needed).
    # Let's just return the first one encountered for now.
    # Alternatively, sorting and picking lowest/highest color value could be a tie-breaker.
    if len(most_frequent_colors) > 1:
         print(f"Warning: Tie detected for most frequent 3x3 color between {most_frequent_colors}. Selecting {most_frequent_colors[0]}.")

    return most_frequent_colors[0]


def transform(input_grid):
    """
    Transforms the input grid based on finding the most frequent solid 3x3 color.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed 3x3 output grid.
    """
    # Convert input_grid to a numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)

    # Find the color that forms the most 3x3 solid squares
    target_color = find_most_frequent_3x3_color(grid_np)

    # Handle the case where no solid 3x3 was found
    if target_color == -1:
        # Return a default 3x3 grid (e.g., white)
        output_grid_np = np.zeros((3, 3), dtype=int)
    else:
        # Create the 3x3 output grid filled with the target color
        output_grid_np = np.full((3, 3), target_color, dtype=int)

    # Convert the numpy array back to a list of lists for the required format
    output_grid = output_grid_np.tolist()

    return output_grid