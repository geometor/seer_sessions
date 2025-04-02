import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing sequences of white pixels (0) 
    located horizontally between two non-white pixels to blue pixels (1).

    The transformation rule is applied row by row. For each row:
    1. Identify the column indices of all non-white pixels (pixels with value != 0). 
       These act as potential horizontal boundaries.
    2. Consider consecutive pairs of these boundary indices (left_c, right_c).
    3. If there is at least one pixel between these boundaries (i.e., right_c > left_c + 1) 
       and all pixels strictly between these boundaries (columns > left_c and < right_c) 
       in the input grid are white (0), change all these white pixels to blue (1)
       in the output grid.
    4. Pixels that are not part of such identified white segments between non-white
       boundaries remain unchanged from the input grid.
    """
    
    # Convert input list of lists to numpy array for easier slicing and manipulation
    # Using int dtype explicitly
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original input
    output_np = np.copy(input_np)
    
    height, width = input_np.shape
    
    # Iterate through each row
    for r in range(height):
        # Get the current row from the original input grid
        row = input_np[r, :]
        
        # Find indices of all non-white (non-zero) pixels in the row
        # These indices serve as the boundaries for potential white segments
        boundary_cols = np.where(row != 0)[0]
        
        # We need at least two non-white pixels in a row to potentially enclose a segment of white pixels
        if len(boundary_cols) >= 2:
            # Iterate through consecutive pairs of boundary indices
            # boundary_cols[i] is the left boundary index, boundary_cols[i+1] is the right boundary index
            for i in range(len(boundary_cols) - 1):
                left_c = boundary_cols[i]
                right_c = boundary_cols[i+1]
                
                # Check if there's actual space between the boundaries 
                # (i.e., they are not adjacent non-white pixels)
                if right_c > left_c + 1:
                    # Extract the segment of pixels strictly between the boundaries from the input row
                    segment_to_check = row[left_c + 1 : right_c]
                    
                    # Check if all pixels within this segment are white (value 0)
                    if np.all(segment_to_check == 0):
                        # If the entire segment between boundaries is white,
                        # change those pixels to blue (value 1) in the output grid
                        output_np[r, left_c + 1 : right_c] = 1
                        
    # Convert the result back to a standard Python list of lists format
    return output_np.tolist()