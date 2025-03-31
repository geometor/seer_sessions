import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Finds the second most frequent non-white color in the input grid and outputs a 1x1 grid of that color.

    Steps:
    1. Convert the input grid (list of lists) to a NumPy array.
    2. Flatten the array to easily count all pixel values.
    3. Filter out the white pixels (value 0).
    4. Count the occurrences of each remaining color.
    5. Sort the colors by frequency in descending order.
    6. If there are at least two non-white colors, select the color corresponding to the second highest frequency.
    7. Create a 1x1 NumPy array filled with the selected color.
    8. If there are fewer than two non-white colors, the behavior based on just train_1 is undefined, but we might need to adjust based on other examples (returning an empty grid or the most frequent if only one exists, etc.). For now, let's assume train_1 is representative and there will always be at least two non-white colors if the transformation is possible. If only one non-white color exists, perhaps return that? Let's stick to the second-most frequent rule for now and see if other examples break it. If there are no non-white colors, return an empty or default grid (e.g., 1x1 white).
    """

    # Convert the input list of lists to a NumPy array
    grid = np.array(input_grid, dtype=int)

    # Flatten the grid to a 1D array to easily count pixels
    pixels = grid.flatten()

    # Filter out white pixels (value 0)
    non_white_pixels = [p for p in pixels if p != 0]

    # Count the frequency of each non-white color
    color_counts = Counter(non_white_pixels)

    # If there are no non-white colors, return a default (e.g., 1x1 white)
    if not color_counts:
        return np.array([[0]], dtype=int) # Default to 1x1 white grid

    # Sort the colors by frequency in descending order
    # .most_common() returns a list of (color, count) tuples sorted by count
    sorted_colors = color_counts.most_common()

    # Check if there are at least two distinct non-white colors
    if len(sorted_colors) >= 2:
        # Select the second most frequent color (index 1)
        second_most_frequent_color = sorted_colors[1][0]
        # Create the 1x1 output grid
        output_grid = np.array([[second_most_frequent_color]], dtype=int)
    elif len(sorted_colors) == 1:
         # Handle the case where there is only one non-white color.
         # Based *only* on train_1, the rule is "second most frequent".
         # If only one exists, there is no second.
         # What should happen? Let's return the *most* frequent one for now.
         # This might need revision based on other examples.
        most_frequent_color = sorted_colors[0][0]
        output_grid = np.array([[most_frequent_color]], dtype=int)
    else: # This case should be covered by the initial check, but included for completeness
        output_grid = np.array([[0]], dtype=int) # Default to 1x1 white grid if something unexpected happens


    return output_grid.tolist() # Convert back to list of lists for consistency