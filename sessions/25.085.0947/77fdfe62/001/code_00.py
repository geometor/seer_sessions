import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. Identifies a rectangular frame of blue (1) pixels, assumed to be one pixel in from the edge based on examples.
    2. Extracts the inner area enclosed by this frame (content between rows/cols 2 and n-3).
    3. Identifies the four corner colors of the original input grid (top-left, top-right, bottom-left, bottom-right).
    4. Creates an output grid with the same dimensions as the inner area.
    5. Populates the output grid pixel by pixel:
       - If a pixel in the inner area is white (0), the corresponding output pixel is set to white (0).
       - If a pixel in the inner area is azure (8), the corresponding output pixel takes the color
         of the input grid's corner corresponding to the quadrant (Top-Left, Top-Right, Bottom-Left, Bottom-Right) 
         the pixel falls into within the inner area. The inner area is divided into four equal or near-equal quadrants.
    """

    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Handle grids too small to contain the assumed frame and inner area
    if input_array.shape[0] < 5 or input_array.shape[1] < 5:
        # Based on the examples, a minimum size is needed for the 2-away slicing.
        # Return an empty grid or handle as an error case if needed.
        return [] 

    input_height, input_width = input_array.shape

    # Step 3: Identify the four corner colors from the input grid
    top_left_color = input_array[0, 0]
    top_right_color = input_array[0, input_width - 1]
    bottom_left_color = input_array[input_height - 1, 0]
    bottom_right_color = input_array[input_height - 1, input_width - 1]

    # Step 1 & 2: Identify frame and extract the inner area
    # Based on examples, the frame is assumed at row/col 1 and row/col n-2.
    # The inner area is extracted using slicing [2:-2], which takes elements
    # from index 2 up to (but not including) the element at index -2 (second to last).
    inner_area = input_array[2:-2, 2:-2]
    
    # Check if inner_area extraction resulted in a valid grid (should be true if initial check passed)
    if inner_area.size == 0:
        return [] 

    inner_height, inner_width = inner_area.shape

    # Step 4: Create a new output grid initialized with zeros (white)
    # Dimensions match the extracted inner_area
    output_array = np.zeros((inner_height, inner_width), dtype=int)

    # Calculate midpoints for quadrant division using integer division
    # This handles both even and odd dimensions correctly for splitting purposes.
    mid_row = inner_height // 2
    mid_col = inner_width // 2

    # Step 5: Iterate through each pixel (r, c) in the inner_area
    for r in range(inner_height):
        for c in range(inner_width):
            pixel_value = inner_area[r, c]

            # a. If the inner_area pixel is white (0), the output pixel remains white (0) (already initialized)
            if pixel_value == 0:
                # output_array[r, c] = 0 # Already 0 by initialization
                pass 
            # b. If the inner_area pixel is azure (8), determine quadrant and assign corner color
            elif pixel_value == 8:
                # Determine quadrant based on row and column relative to midpoints
                if r < mid_row and c < mid_col:  # Top-Left Quadrant
                    output_array[r, c] = top_left_color
                elif r < mid_row and c >= mid_col: # Top-Right Quadrant
                    output_array[r, c] = top_right_color
                elif r >= mid_row and c < mid_col: # Bottom-Left Quadrant
                    output_array[r, c] = bottom_left_color
                else: # Bottom-Right Quadrant (r >= mid_row and c >= mid_col)
                    output_array[r, c] = bottom_right_color
            # else: # Optional: Handle unexpected pixel values in the inner area
                  # For this task, assume only 0 and 8 are present as per perception.
                  # If other colors could appear, a rule would be needed.

    # Convert the final numpy array back to a standard list of lists format
    output_grid = output_array.tolist()

    # Step 6: Return the populated output grid
    return output_grid