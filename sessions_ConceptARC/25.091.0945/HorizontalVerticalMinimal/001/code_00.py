import numpy as np

"""
Identify all maximal horizontal line segments in the input grid that meet the following criteria:
1. Composed of contiguous pixels of the same non-white color.
2. Have a length of at least 2 pixels.
3. Have a thickness of exactly 1 pixel (pixels directly above/below are not the same color).
Create an output grid of the same dimensions as the input, initialized with the background color (white, 0).
Copy only the identified qualifying horizontal segments to the output grid, preserving their color and position.
"""

def transform(input_grid):
    """
    Transforms the input grid by retaining only horizontal line segments
    of length 2 or more and thickness 1.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    # Initialize output_grid with the background color (0)
    output_grid = np.zeros_like(input_np)

    # Iterate through each row to find horizontal segments
    for r in range(height):
        c = 0
        while c < width:
            color = input_np[r, c]
            # Skip background color or if it's part of a segment already processed
            if color == 0:
                c += 1
                continue

            # Find the end of the contiguous segment of the same color
            start_c = c
            while c < width and input_np[r, c] == color:
                c += 1
            end_c = c - 1  # Inclusive index of the last pixel in the segment

            # Calculate segment length
            length = end_c - start_c + 1

            # Check if the segment meets the minimum length requirement (>= 2)
            if length >= 2:
                # Check if the segment has a thickness of exactly 1
                is_thin = True
                for current_c in range(start_c, end_c + 1):
                    # Check pixel above (if not in the first row)
                    if r > 0 and input_np[r - 1, current_c] == color:
                        is_thin = False
                        break
                    # Check pixel below (if not in the last row)
                    if r < height - 1 and input_np[r + 1, current_c] == color:
                        is_thin = False
                        break
                
                # If the segment is long enough and thin enough, copy it to the output grid
                if is_thin:
                    output_grid[r, start_c : end_c + 1] = color
            
            # Continue scanning from the next column after the segment
            # No need to increment c here as the inner while loop already moved it past the segment

    return output_grid.tolist()