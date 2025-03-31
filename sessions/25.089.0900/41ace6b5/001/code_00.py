import numpy as np

"""
Transforms the input grid based on row position relative to two marker rows (identified by red '2' and gray '5' pixels) and column parity (even/odd).

1.  Find the row index of the 'red marker row' (contains red '2' in even columns).
2.  Find the row index of the 'gray marker row' (contains gray '5' in even columns, directly below the red marker row).
3.  Iterate through each cell (r, c) of the input grid.
4.  If the column 'c' is odd:
    - If row 'r' is at or above the red marker row, set the output cell to azure '8'.
    - If row 'r' is the gray marker row, set the output cell to blue '1'.
    - If row 'r' is below the gray marker row, set the output cell to maroon '9'.
5.  If the column 'c' is even:
    - If row 'r' is the gray marker row and the input cell is azure '8', set the output cell to blue '1'.
    - If row 'r' is below the gray marker row and the input cell is azure '8' or blue '1', set the output cell to maroon '9'.
    - Otherwise, keep the original input cell value.
"""

def find_marker_rows(grid):
    """
    Finds the row indices of the red (2) and gray (5) marker rows.
    Assumes marker colors appear in even columns of their respective rows.
    """
    red_marker_row_index = -1
    gray_marker_row_index = -1
    height, width = grid.shape

    for r in range(height):
        found_red = False
        found_gray = False
        for c in range(0, width, 2): # Check only even columns
            if grid[r, c] == 2:
                found_red = True
            if grid[r, c] == 5:
                found_gray = True
        
        if found_red:
            red_marker_row_index = r
        if found_gray:
            gray_marker_row_index = r
            
        # Optimization: if both are found, we can potentially stop early 
        # if we assume they are consecutive and unique.
        # Given the examples, gray is always directly below red.
        if red_marker_row_index != -1 and gray_marker_row_index != -1:
            # Verify gray is directly below red
            if gray_marker_row_index == red_marker_row_index + 1:
                 break 
            else: # Reset if assumption is broken (though unlikely based on examples)
                 red_marker_row_index = -1 
                 gray_marker_row_index = -1
                 
    # If only red was found, assume gray is below it
    if red_marker_row_index != -1 and gray_marker_row_index == -1 and red_marker_row_index + 1 < height:
        # Check if the row below red actually contains gray markers
        is_actual_gray_row = False
        for c in range(0, width, 2):
            if grid[red_marker_row_index + 1, c] == 5:
                is_actual_gray_row = True
                break
        if is_actual_gray_row:
            gray_marker_row_index = red_marker_row_index + 1


    if red_marker_row_index == -1 or gray_marker_row_index == -1:
        # Handle cases where markers might not be found as expected, 
        # although the examples guarantee their presence.
        # For robustness, one might raise an error or return default indices.
        print("Warning: Marker rows not found or not structured as expected.")
        # Fallback or error handling could go here. Let's assume they are always found per task structure.
        # Re-scan specifically for gray if red was found but gray wasn't below it
        if red_marker_row_index != -1 and gray_marker_row_index == -1:
             for r in range(height):
                 for c in range(0, width, 2):
                     if grid[r, c] == 5:
                         gray_marker_row_index = r
                         break
                 if gray_marker_row_index != -1:
                     break


    return red_marker_row_index, gray_marker_row_index


def transform(input_grid):
    """
    Applies the transformation rule based on marker rows and column parity.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)

    # Find the marker row indices
    red_marker_row_index, gray_marker_row_index = find_marker_rows(input_grid_np)

    # Check if marker rows were found successfully
    if red_marker_row_index == -1 or gray_marker_row_index == -1:
        print("Error: Could not find marker rows. Returning input grid.")
        return input_grid # Or raise an exception

    # Iterate through each cell of the grid
    for r in range(height):
        for c in range(width):
            original_color = input_grid_np[r, c]

            # Check if the column index 'c' is odd
            if c % 2 != 0:
                # Apply rules for odd columns based on row position relative to markers
                if r <= red_marker_row_index:
                    output_grid[r, c] = 8  # azure
                elif r == gray_marker_row_index:
                    output_grid[r, c] = 1  # blue
                elif r > gray_marker_row_index:
                    output_grid[r, c] = 9  # maroon
            
            # Check if the column index 'c' is even
            else: # c % 2 == 0
                # Apply rules for even columns based on row position and original color
                if r == gray_marker_row_index and original_color == 8: # Azure in gray marker row
                    output_grid[r, c] = 1 # blue
                elif r > gray_marker_row_index and (original_color == 8 or original_color == 1): # Azure or Blue below gray marker row
                    output_grid[r, c] = 9 # maroon
                # Otherwise (all other cases in even columns), the color remains unchanged (already copied)

    # Convert numpy array back to list of lists for the expected output format
    return output_grid.tolist()