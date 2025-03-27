"""
Transforms the input grid by identifying a 'target color' (excluding white 0 and gray 5)
and replacing all its occurrences with gray (5).

The selection process for the target color is as follows:
1. Calculate pixel counts for all relevant colors (not 0 or 5).
2. If no relevant colors exist, return the original grid.
3. Check if all relevant colors have the same pixel count.
   a. If YES: Select the relevant color with the LOWEST index.
   b. If NO:
      i. Find the minimum count among relevant colors.
      ii. Identify colors tied for this minimum count.
      iii. If only one color has the minimum count, select it.
      iv. If multiple colors tie for the minimum count:
          - Sort the tied colors by index.
          - If 3 colors tie, select the MIDDLE index color.
          - If 4 colors tie, select the HIGHEST index color.
          - (Other tie numbers currently default to the highest index as per the previous attempt, though this might need refinement if new examples arise).
4. Replace all pixels of the selected target color with gray (5).
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Applies the described transformation rule to the input grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)

    # Flatten the array to easily count pixel occurrences
    flat_array = input_array.flatten()

    # Count occurrences of each color
    color_counts = Counter(flat_array)

    # Filter out white (0) and gray (5) and store counts for relevant colors
    relevant_color_counts = {}
    for color, count in color_counts.items():
        if color != 0 and color != 5:
            # Ensure keys are standard integers, not numpy types
            relevant_color_counts[int(color)] = count

    # Handle the case where there are no relevant colors to change
    if not relevant_color_counts:
        return output_array.tolist() # Return the original grid

    target_color = -1 # Initialize target_color to an invalid value

    # Check if all relevant colors have the same count
    counts_list = list(relevant_color_counts.values())
    all_counts_same = len(set(counts_list)) == 1

    if all_counts_same:
        # If all counts are the same, select the color with the lowest index
        target_color = min(relevant_color_counts.keys())
    else:
        # If counts differ, find the minimum count and handle ties
        min_count = min(counts_list)

        # Identify all colors that have this minimum count
        min_count_colors = sorted([color for color, count in relevant_color_counts.items() if count == min_count])

        num_tied = len(min_count_colors)

        if num_tied == 1:
            # If only one color has the minimum count, select it
            target_color = min_count_colors[0]
        elif num_tied == 3:
            # If three colors tie, select the middle index one
            target_color = min_count_colors[1]
        elif num_tied == 4:
             # If four colors tie (and not all counts were the same initially), select the highest index one
             target_color = min_count_colors[3] # Index 3 for a list of 4 elements
        else:
            # Default fallback for other tie numbers (e.g., 2) - using highest index based on initial code
            # This might need adjustment if examples with other tie numbers appear.
            if min_count_colors: # Ensure list is not empty
                 target_color = max(min_count_colors)


    # If a valid target color was selected, replace it with gray (5)
    if target_color != -1:
        output_array[input_array == target_color] = 5

    # Convert the output NumPy array back to a list of lists
    return output_array.tolist()