import numpy as np

def find_azure_line_row(grid):
    """Finds the row index containing the horizontal azure (8) line."""
    for r in range(grid.shape[0]):
        if np.all(grid[r, :] == 8) or (np.count_nonzero(grid[r, :] == 8) > 1 and np.all(grid[r, grid[r,:] != 0] == 8)):
             # Check if the row consists entirely of 8s or mostly 8s excluding 0s
             # Second condition handles cases like train_3 where the line isn't full width
             is_line = True
             for c in range(grid.shape[1]):
                 # Check if non-zero elements are 8
                 if grid[r, c] != 0 and grid[r, c] != 8:
                     is_line = False
                     break
                 # Check for vertical continuity for non-zero elements (basic check)
                 if grid[r,c] == 8:
                     if c > 0 and grid[r, c-1] == 0: # Gap before an 8
                         has_8_after = False
                         for k in range(c + 1, grid.shape[1]):
                            if grid[r, k] == 8:
                                has_8_after = True
                                break
                         if not has_8_after: # Isolated 8 segment at the end
                             pass # Allow it
                         # else: # Gap within the line - might not be the line
                         #    is_line = False
                         #    break
                     if c < grid.shape[1] - 1 and grid[r, c+1] == 0: # Gap after an 8
                          has_8_before = False
                          for k in range(c):
                             if grid[r, k] == 8:
                                 has_8_before = True
                                 break
                          if not has_8_before: # Isolated 8 segment at the beginning
                             pass # Allow it
                          # else: # Gap within the line
                          #    is_line = False
                          #    break


             # Check if there's at least one group of adjacent 8s
             has_adjacent_8 = False
             if np.count_nonzero(grid[r, :] == 8) > 0:
                 for c in range(grid.shape[1] -1):
                     if grid[r, c] == 8 and grid[r, c+1] == 8:
                         has_adjacent_8 = True
                         break
                 # Handle single column grids or single 8 in a row
                 if grid.shape[1] == 1 and grid[r, 0] == 8:
                     has_adjacent_8 = True
                 # If only one 8 exists, consider it part of the 'line' for this logic
                 if not has_adjacent_8 and np.count_nonzero(grid[r, :] == 8) == 1:
                     has_adjacent_8 = True


             if is_line and has_adjacent_8 and np.count_nonzero(grid[r,:] == 8) > 0:
                 return r
    return -1 # Indicate not found


def transform(input_grid):
    """
    Identifies a horizontal line of azure (8) pixels.
    All non-white, non-azure pixels located above this line "fall" vertically downwards
    until they land on the azure line or stack on top of another fallen pixel of the
    same color within the same column.
    Pixels below the azure line are removed (set to white 0).
    The azure line itself remains unchanged.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.zeros_like(input_grid_np) # Start with a white grid

    # Find the row index of the azure line
    azure_line_row = find_azure_line_row(input_grid_np)

    if azure_line_row == -1:
        # If no distinct azure line is found, return the input as is or handle error
        # For now, let's return the original grid, assuming the line is a key feature
        return input_grid

    # Copy the azure line to the output grid
    output_grid[azure_line_row, :] = input_grid_np[azure_line_row, :]

    # Process each column independently
    for c in range(input_grid_np.shape[1]):
        # Collect falling pixels from above the azure line in this column
        falling_pixels = []
        for r in range(azure_line_row):
            pixel = input_grid_np[r, c]
            if pixel != 0 and pixel != 8: # Ignore white and azure pixels
                falling_pixels.append(pixel)

        # Place the falling pixels in the output grid, stacking upwards from the line
        current_row = azure_line_row - 1
        for pixel in reversed(falling_pixels): # Place from bottom up
            if current_row >= 0:
                output_grid[current_row, c] = pixel
                current_row -= 1
            else:
                # Should not happen if grid height is sufficient, but handles overflow
                break

    return output_grid.tolist()