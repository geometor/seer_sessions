import numpy as np

"""
Transforms an input grid based on the following rules:
1. Create an output grid by copying the input grid.
2. Iterate through each row of the input grid to find contiguous horizontal segments of non-white (0) pixels.
3. For each segment found:
    a. If the segment's color is *not* green (3), change the rightmost pixel of that segment in the *output grid* to gray (5).
    b. If the segment's color *is* green (3), leave the segment unchanged in the output grid.
4. After processing all segments, iterate through the grid positions. If a pixel was originally white (0) in the *input grid*, change the corresponding pixel in the *output grid* to gray (5).
5. Return the modified output grid.
"""

# Note: No external library imports needed beyond numpy

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    
    # Step 1: Initialize output_grid as a copy of the input
    output_np = input_np.copy()
    height, width = input_np.shape

    # Step 2 & 3: Iterate through rows to find horizontal segments of non-white pixels
    for r in range(height):
        c = 0
        while c < width:
            # Get the color of the current pixel from the original input
            current_input_color = input_np[r, c]

            # Check if the pixel is non-white (start of a potential segment)
            if current_input_color != 0:
                # Found the start of a segment
                segment_color = current_input_color
                c_start = c

                # Find the end of the contiguous segment of the *same* color in the *input* grid
                # We iterate `c` forward as long as we're within bounds and the next pixel matches the segment color
                while c + 1 < width and input_np[r, c + 1] == segment_color:
                    c += 1
                # Now, 'c' holds the index of the rightmost pixel of this segment
                c_end = c 

                # Step 3a: If the segment color is not green (3), update the output grid
                if segment_color != 3:
                    # Change the rightmost pixel of this segment in the *output* grid to gray (5)
                    output_np[r, c_end] = 5
                # Step 3b: If the color is green (3), do nothing (it's already copied correctly)

                # Move the column index past the processed segment to continue searching
                c += 1
            else:
                # If the pixel is white (0), simply move to the next column
                c += 1

    # Step 4: Change all pixels that were originally white (0) in the input to gray (5) in the output
    # This uses boolean indexing for efficiency: 
    # It finds all indices where input_np is 0 and sets the corresponding indices in output_np to 5.
    output_np[input_np == 0] = 5

    # Step 5: Return the modified output grid, converted back to list of lists format
    return output_np.tolist()