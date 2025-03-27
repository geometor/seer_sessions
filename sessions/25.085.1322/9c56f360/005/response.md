```python
import numpy as np

"""
Processes each row of the input grid independently.
For the current row:
    a. Create a reference copy of the original row.
    b. Find all green pixels and calculate their target columns based on the first azure pixel to their left (target = azure_col + 1, or 0 if no azure pixel).
    c. Identify the columns occupied by stationary green pixels (those whose target column is their original column). Store these in a set `stationary_green_columns`.
    d. Create an empty set `occupied_moved_destinations` to track columns filled by green pixels that have successfully moved during this row's processing.
    e. Iterate through the green pixels of the original row from right to left based on their column index `c`.
    f. For each green pixel at original column `c` with target `target_c`:
        i. If the pixel is stationary (`c == target_c`), do nothing.
        ii. If the pixel wants to move (`c != target_c`):
            1. Check for stationary conflict: If `target_c` is in `stationary_green_columns`, the pixel cannot move. Do nothing.
            2. If no stationary conflict: Calculate the final destination `dest_c`, starting at `target_c`.
            3. Check for dynamic conflict: While `dest_c` is in `occupied_moved_destinations`, increment `dest_c` by 1.
            4. Check bounds and place: If `dest_c` is within the grid width:
                A. Add `dest_c` to `occupied_moved_destinations`.
                B. Update the output grid: Set pixel at (row, `c`) to white (0).
                C. Update the output grid: Set pixel at (row, `dest_c`) to green (3).
            5. If `dest_c` is out of bounds (due to dynamic conflict pushing), the pixel cannot move. Do nothing (it stays at `c`).
Return the final output grid.
"""

def find_target_column(row_array, start_col):
    """
    Determines the target column for a green pixel based on azure pixels to its left.

    Args:
        row_array (np.array): The 1D numpy array representing the original row.
        start_col (int): The column index of the green pixel.

    Returns:
        int: The target column index.
    """
    target_c = 0  # Default target is column 0
    # Scan leftwards from start_col - 1 down to 0
    for c in range(start_col - 1, -1, -1):
        if row_array[c] == 8:  # Found an azure pixel
            target_c = c + 1  # Target is the column immediately to its right
            break  # Stop searching once the leftmost azure is found
    return target_c

def transform(input_grid):
    """
    Transforms the input grid by moving green pixels leftward based on azure pixel
    positions within each row, resolving conflicts with stationary and other moved pixels.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_np)
    height, width = output_grid.shape

    # Iterate through each row independently
    for r in range(height):
        # Get the original state of the current row for reference
        original_row = input_np[r, :]
        
        # Find column indices of all green pixels in the original row
        green_cols_indices = np.where(original_row == 3)[0]
        
        # --- Pre-calculation Step ---
        # Store targets and identify stationary green pixels
        green_pixel_info = {} # Dict: {col: target_col}
        stationary_green_columns = set()
        for c in green_cols_indices:
            target_c = find_target_column(original_row, c)
            green_pixel_info[c] = target_c
            if c == target_c:
                stationary_green_columns.add(c)

        # Keep track of destination columns occupied by *moved* green pixels in this row's pass
        occupied_moved_destinations = set()

        # --- Main Processing Loop (Right-to-Left) ---
        # Process green pixels from right to left within the row based on original positions
        for c in sorted(green_cols_indices, reverse=True):
            
            target_c = green_pixel_info[c]

            # If the pixel is stationary, do nothing.
            if c == target_c:
                continue 
                
            # --- Attempt to Move ---
            # Check for stationary conflict: If target is a stationary green pixel's location
            if target_c in stationary_green_columns:
                # Cannot move, pixel stays at original position 'c'.
                # No change needed in output_grid.
                continue

            # Calculate the final destination column, resolving dynamic collisions
            dest_c = target_c
            while dest_c in occupied_moved_destinations:
                 dest_c += 1
            
            # Check if the final destination is within bounds
            if dest_c < width:
                # Mark the final destination column as occupied *by a moved pixel*
                occupied_moved_destinations.add(dest_c)

                # Update the output grid: 
                # Erase original position 
                output_grid[r, c] = 0  
                # Place green at destination
                output_grid[r, dest_c] = 3 
            else:
                 # Pixel could not find a valid spot within the grid width due to collisions.
                 # It remains in its original position 'c'.
                 # No change needed in output_grid.
                 pass # Explicitly show no action needed

    # Convert the final numpy array back to list of lists for the expected output format
    return output_grid.tolist()
```