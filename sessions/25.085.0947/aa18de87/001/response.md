```python
"""
Fill horizontal segments between pairs of marker pixels in each row with red (2).
The marker color is the single non-white color present in the input grid.
A horizontal segment is filled only if all pixels within that segment (strictly between the marker pair) are white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by filling horizontal segments between marker pairs.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: The transformed grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    # Create a copy of the input array to modify, this will become the output
    output_array = input_array.copy()

    # Identify the marker color: the single non-white color in the grid
    marker_color = None
    unique_colors = np.unique(input_array)
    non_white_colors = unique_colors[unique_colors != 0] # Filter out white (0)

    # Check if exactly one non-white color exists, as expected by the task description
    if len(non_white_colors) == 1:
        marker_color = non_white_colors[0]
    elif len(non_white_colors) == 0:
        # If the grid is all white or empty, there's nothing to fill
        return output_array.tolist() # Return the unmodified grid
    else:
        # If multiple non-white colors exist, this contradicts the task description.
        # Based on the examples, we assume only one marker color.
        # For robustness, we could raise an error or pick one, but sticking to the pattern:
        # Assuming the task guarantees one marker color if any non-white pixels exist.
        # If this assumption is wrong, the behavior might be incorrect for unexpected inputs.
         marker_color = non_white_colors[0] # Defaulting to the first found, but ideally handle error.
         # print(f"Warning: Multiple non-white colors found ({non_white_colors}). Using {marker_color} as marker.")


    # Get the dimensions of the grid
    rows, cols = input_array.shape

    # Iterate through each row of the grid
    for r in range(rows):
        # Find the column indices of all pixels with the marker color in the current row
        marker_indices = np.where(input_array[r, :] == marker_color)[0]
        # np.where returns a tuple, get the array of indices

        # Sort indices just in case they aren't ordered (though np.where usually returns sorted)
        marker_indices.sort()

        # Proceed only if there are at least two marker pixels in the row to form a pair
        if len(marker_indices) >= 2:
            # Iterate through consecutive pairs of marker indices (col1, col2)
            for i in range(len(marker_indices) - 1):
                col1 = marker_indices[i]
                col2 = marker_indices[i+1]

                # Check if there is space between the markers (col2 > col1 + 1)
                if col2 > col1 + 1:
                    # Define the segment of the row strictly between the markers
                    segment_slice = slice(col1 + 1, col2)
                    segment = input_array[r, segment_slice]

                    # Check if all pixels in this segment are white (0)
                    if np.all(segment == 0):
                        # If all are white, change the color of these pixels to red (2) in the output grid
                        output_array[r, segment_slice] = 2

    # Convert the final NumPy array back to a list of lists before returning
    return output_array.tolist()
```