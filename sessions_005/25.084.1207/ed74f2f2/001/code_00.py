import numpy as np

"""
Identifies two 3x3 patterns (Left Pattern - LP, Right Pattern - RP) within the input grid.
Determines an output color based on comparing the number of gray pixels in LP and RP.
If the counts are equal, the color is Green(3) for a count of 5, and Red(2) for a count of 4.
If the counts are unequal, the color is determined by the count of pixels that are gray in either LP OR RP. Blue(1) for an OR count of 8, Red(2) for an OR count of 9.
Constructs a 3x3 output grid where the shape matches the gray pixels of the RP, using the determined output color.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the comparison of two 3x3 subgrids.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed 3x3 output grid.
    """
    # Convert input to numpy array for easier slicing and operations
    grid = np.array(input_grid, dtype=int)

    # 1. Identify the Left Pattern (LP) subgrid
    left_pattern = grid[1:4, 1:4]

    # 2. Identify the Right Pattern (RP) subgrid
    right_pattern = grid[1:4, 5:8]

    # 3. Count gray pixels in Left Pattern
    left_count = np.count_nonzero(left_pattern == 5)

    # 4. Count gray pixels in Right Pattern
    right_count = np.count_nonzero(right_pattern == 5)

    # 5. Initialize Output Color variable
    output_color = 0 # Default or error color, although not expected based on examples

    # 6. Determine Output Color based on counts
    if left_count == right_count:
        if left_count == 5:
            output_color = 3 # Green
        elif left_count == 4:
            output_color = 2 # Red
        # Add handling for other counts if necessary, although not seen in examples
        else:
             # Placeholder if other equal counts appear
             # For now, use a default or raise an error? Let's use 0.
             output_color = 0

    else: # left_count != right_count
        # Calculate the logical OR pattern
        # Treat gray (5) as True, white (0) as False
        or_pattern = (left_pattern == 5) | (right_pattern == 5)
        # Count the number of True pixels in the OR grid
        or_count = np.count_nonzero(or_pattern)

        if or_count == 8:
            output_color = 1 # Blue
        elif or_count == 9: # Based on example 5
             output_color = 2 # Red
        # Add handling for other OR counts if necessary
        else:
            # Placeholder if other unequal counts/OR counts appear
            # For now, use a default or raise an error? Let's use 0.
             output_color = 0


    # 7. Create the 3x3 output grid
    # Initialize with zeros (white)
    output_grid = np.zeros_like(right_pattern, dtype=int)

    # 8. Populate the output grid based on the Right Pattern and Output Color
    # Where right_pattern has a gray pixel (5), set output_grid to output_color
    # Otherwise, it remains white (0)
    output_grid = np.where(right_pattern == 5, output_color, 0)

    # 9. Return the final output grid as a list of lists
    return output_grid.tolist()
