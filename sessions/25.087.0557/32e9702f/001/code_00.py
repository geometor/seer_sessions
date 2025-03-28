import numpy as np

"""
1. Create an output grid by copying the input grid.
2. Change all white (0) pixels in the output grid to gray (5).
3. Iterate through each row of the *input* grid.
4. For each row, find contiguous horizontal segments of pixels whose color is *not* white (0) and *not* green (3).
5. For each such segment found in the input grid, locate its rightmost pixel (the one with the highest column index within the segment).
6. Change the color of the corresponding pixel in the *output* grid (at the same row and column as the rightmost pixel of the input segment) to gray (5).
7. Return the modified output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the rules:
    - Changes background white (0) to gray (5).
    - Changes the rightmost pixel of horizontal segments of non-white, non-green colors to gray (5).
    
    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.
        
    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_np = input_np.copy()
    height, width = input_np.shape

    # Step 1 & 2: Copy non-white pixels and change white (0) pixels to gray (5)
    # This is done efficiently by first copying, then replacing 0s.
    output_np[output_np == 0] = 5

    # Step 3-6: Identify non-white, non-green segments in the *input* 
    #           and modify the rightmost pixel in the *output*
    for r in range(height):
        c = 0
        while c < width:
            current_color = input_np[r, c]
            
            # Check if the current pixel is the start of a segment to potentially modify
            # It must be non-white (0) and non-green (3)
            if current_color != 0 and current_color != 3:
                
                # Find the end of the contiguous segment of the same color in the input grid
                c_start = c
                while c + 1 < width and input_np[r, c + 1] == current_color:
                    c += 1
                
                # c now holds the index of the rightmost pixel of this segment
                # Modify the corresponding pixel in the output grid to gray (5)
                output_np[r, c] = 5
                
                # Move the column index past the processed segment
                c += 1
            else:
                # If the pixel is white, green, or we just finished processing a segment, 
                # simply move to the next column
                c += 1

    # Step 7: Return the modified output grid, converted back to list of lists
    return output_np.tolist()
