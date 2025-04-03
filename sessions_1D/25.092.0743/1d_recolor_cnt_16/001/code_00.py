import numpy as np

"""
Transforms the input grid by recoloring contiguous horizontal segments of gray (5) pixels based on their length.
- Segments of length 1 become red (2).
- Segments of length 2 become magenta (6).
- Segments of length 3 become blue (1).
- White (0) pixels remain unchanged.
The transformation assumes the input grid is essentially a single row (1xN dimension).
"""

def transform(input_grid):
    """
    Applies the length-based recoloring transformation to gray segments.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid. 
                                       Expected to have only one row.

    Returns:
        list[list[int]]: The transformed 2D grid.
    """
    # Ensure input is valid and has at least one row
    if not input_grid or not input_grid[0]:
        return [] 

    # Extract the single row from the input grid
    input_row = input_grid[0]
    width = len(input_row)
    
    # Initialize the output row with the background color (white/0)
    output_row = [0] * width

    # Variables to track the current segment of gray pixels
    current_segment_start = -1
    current_segment_length = 0

    # Iterate through each pixel in the input row
    for i, pixel in enumerate(input_row):
        if pixel == 5:  # If the pixel is gray
            if current_segment_start == -1:
                # Mark the start of a new gray segment
                current_segment_start = i
            # Increment the length of the current segment
            current_segment_length += 1
        else:  # If the pixel is not gray (it's white/0)
            if current_segment_start != -1:
                # A gray segment just ended, process it
                # Determine the output color based on the segment length
                output_color = 0 # Default/fallback
                if current_segment_length == 1:
                    output_color = 2  # Red for length 1
                elif current_segment_length == 2:
                    output_color = 6  # Magenta for length 2
                elif current_segment_length == 3:
                    output_color = 1  # Blue for length 3
                # Note: If length is not 1, 2, or 3, the segment pixels remain 0 (white)
                #       as per the examples.

                # Fill the corresponding segment in the output row with the determined color
                for j in range(current_segment_start, current_segment_start + current_segment_length):
                    if 0 <= j < width: # Basic boundary check
                        output_row[j] = output_color

                # Reset segment tracking variables
                current_segment_start = -1
                current_segment_length = 0
            # The current non-gray pixel position in output_row remains 0 (initialized value)

    # After the loop, check if a gray segment extends to the very end of the row
    if current_segment_start != -1:
        # Process the final segment
        output_color = 0 
        if current_segment_length == 1:
            output_color = 2
        elif current_segment_length == 2:
            output_color = 6
        elif current_segment_length == 3:
            output_color = 1

        # Fill the final segment in the output row
        for j in range(current_segment_start, current_segment_start + current_segment_length):
            if 0 <= j < width:
                output_row[j] = output_color

    # Format the result back into a list of lists (grid structure)
    output_grid = [output_row]
    
    return output_grid