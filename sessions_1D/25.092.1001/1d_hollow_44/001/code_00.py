import numpy as np

"""
For each row in the input grid, identify contiguous horizontal segments of non-white pixels. 
If a segment's length is 3 or greater, keep the first and last pixels of the segment and change all pixels between them to white (0). 
Pixels not part of any segment (original white pixels) and pixels in segments shorter than 3 remain unchanged.
"""

def find_segments(row):
    """
    Identifies contiguous horizontal segments of non-white pixels in a row.

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        list: A list of tuples, where each tuple represents a segment
              and contains (start_index, end_index, color, length).
              Returns an empty list if no segments are found.
    """
    segments = []
    start_index = -1
    current_color = 0
    width = len(row)

    for i, pixel in enumerate(row):
        if pixel != 0: # Start or continuation of a segment
            if start_index == -1: # Start of a new segment
                start_index = i
                current_color = pixel
            # Ensure consistency if needed (though examples show uniform color segments)
            # elif pixel != current_color:
                # Handle potential segments of different colors touching - not in examples
                # For now, assume segments have uniform color as per examples
                # pass
        elif start_index != -1: # End of the current segment
            end_index = i - 1
            length = end_index - start_index + 1
            segments.append((start_index, end_index, current_color, length))
            start_index = -1 # Reset for the next segment

    # Handle segment that goes to the end of the row
    if start_index != -1:
        end_index = width - 1
        length = end_index - start_index + 1
        segments.append((start_index, end_index, current_color, length))

    return segments


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists or np.array): The input grid.

    Returns:
        np.array: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    # Iterate through each row
    for r in range(height):
        row = input_np[r, :]
        # Find all non-white segments in the current row
        segments = find_segments(row)

        # Process each found segment
        for start, end, color, length in segments:
            # Apply the hollowing rule only if length is 3 or more
            if length >= 3:
                # Iterate through the pixels *between* the start and end
                for c in range(start + 1, end):
                    # Change the intermediate pixels to white (0) in the output grid
                    output_grid[r, c] = 0

    return output_grid.tolist() # Convert back to list of lists if required by the environment
