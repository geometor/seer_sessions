import numpy as np

def transform(input_grid):
    """
    Iterates through each row of the input grid. If an Orange pixel (7) is found,
    it identifies the contiguous block of White pixels (0) immediately to its left within the same row. 
    It then finds the color of the pixel immediately to the left of this White block (the source pixel).
    Finally, it replaces the color of all pixels within the White block with the source pixel's color.
    """
    
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each row
    for r in range(rows):
        # Find the column index of the first Orange marker (7) in the current row
        marker_c = -1
        for c in range(cols):
            if output_grid[r, c] == 7:
                marker_c = c
                break # Process the first marker found in the row

        # If an Orange marker was found in this row
        if marker_c != -1:
            # Find the contiguous block of White pixels (0) immediately to the left
            white_cols = []
            current_c = marker_c - 1
            while current_c >= 0 and output_grid[r, current_c] == 0:
                # Insert at the beginning to maintain left-to-right order later
                white_cols.insert(0, current_c) 
                current_c -= 1

            # If a block of White pixels was found adjacent to the marker
            if white_cols:
                # Determine the column index of the source pixel (left of the white block)
                source_c = white_cols[0] - 1

                # Ensure the source pixel index is valid (within the grid bounds)
                if source_c >= 0:
                    # Get the fill color from the source pixel in the *original* grid
                    fill_color = input_grid[r, source_c] 
                    
                    # Change the color of the identified White pixels in the output grid
                    for c_fill in white_cols:
                        output_grid[r, c_fill] = fill_color
                        
            # Optimization: Once a marker is processed in a row, move to the next row
            # (Based on the examples showing only one relevant marker per row)
            # If multiple markers per row were possible and needed independent processing,
            # this break would be removed or logic adjusted.
            # In this case, finding the *first* marker and processing it fits the examples.
            # The outer loop `for c in range(cols)` already broke, so this comment is explanatory.


    return output_grid