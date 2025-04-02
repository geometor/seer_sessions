import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the position of a single non-white pixel in each row.

    1.  Reshapes the flat input list into a 6x7 grid.
    2.  Initializes a 6x7 output grid filled with white (0).
    3.  Iterates through each row of the input grid.
    4.  Finds the single non-white pixel (marker) in the row, noting its column 'c' and color.
    5.  If the marker is in the last column (c=6), fills the corresponding output row from column 1 to 6 with the marker's color.
    6.  If the marker is not in the last column (c<6), fills the corresponding output row from column 'c' to 6 with the marker's color.
    """

    # Define grid dimensions based on analysis
    rows = 6
    cols = 7
    
    # Ensure input is a list or can be treated as one
    if not isinstance(input_grid, list):
        raise TypeError("Input grid must be a flat list of integers.")
        
    if len(input_grid) != rows * cols:
         raise ValueError(f"Input list length ({len(input_grid)}) does not match expected grid size {rows}x{cols}.")

    # Reshape the flat input list into a 2D NumPy array
    try:
        input_array = np.array(input_grid).reshape((rows, cols))
    except Exception as e:
        raise ValueError(f"Could not reshape input list into a {rows}x{cols} grid. Error: {e}")

    # Initialize the output grid with the background color (white=0)
    output_array = np.zeros((rows, cols), dtype=int)

    # Iterate through each row of the input grid
    for r in range(rows):
        # Get the current row
        row_data = input_array[r, :]
        
        # Find the indices of non-white pixels in the current row
        non_white_indices = np.where(row_data != 0)[0]
        
        # Check if there is exactly one non-white pixel
        if len(non_white_indices) == 1:
            # Get the column index 'c' of the marker pixel
            c = non_white_indices[0]
            # Get the color of the marker pixel
            fill_color = row_data[c]
            
            # Apply the fill logic based on the column index 'c'
            if c == cols - 1:  # Marker is in the last column
                # Fill from column 1 up to and including the last column
                output_array[r, 1:cols] = fill_color 
            else:  # Marker is not in the last column
                # Fill from column 'c' up to and including the last column
                output_array[r, c:cols] = fill_color
        # Optional: Handle cases where the assumption of exactly one non-white pixel is violated
        # else:
        #    print(f"Warning: Row {r} does not contain exactly one non-white pixel. Skipping row.")
        #    # Or copy the original row if that's the desired behavior
        #    # output_array[r, :] = input_array[r, :] 

    # Convert the NumPy array back to a list of lists for the standard ARC format
    output_grid = output_array.tolist()

    return output_grid