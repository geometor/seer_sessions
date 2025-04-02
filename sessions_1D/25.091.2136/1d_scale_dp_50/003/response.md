```python
import numpy as np

def transform(input_grid):
    """
    Transforms a 1xN input grid by finding a contiguous block of a non-background,
    non-boundary color (the 'source block'), finding an orange (7) boundary
    pixel to its right, and filling the space between the source block and the
    boundary pixel with the source block's color.

    The input grid is expected to be a 2D NumPy array with shape (1, N).
    The output grid will have the same shape.
    """

    # Ensure input is a NumPy array
    input_grid_np = np.array(input_grid, dtype=int)

    # Check if the input grid has exactly one row
    if input_grid_np.shape[0] != 1:
        # Handle unexpected input shape, perhaps return input or raise error
        # For this task, based on examples, we assume shape is (1, N)
        # If input is empty or has wrong shape, returning it might be safest
        # return input_grid_np
        # Let's assume valid input based on ARC task structure
        pass # Continue assuming input_grid_np.shape[0] == 1

    # Extract the first (and only) row
    # Using [0] directly as we assume the shape is valid
    input_row = input_grid_np[0]
    # Create a copy to modify for the output
    output_row = input_row.copy()

    source_color = -1
    source_start_index = -1
    source_end_index = -1
    boundary_index = -1
    width = len(input_row)

    # 1. Find the start and color of the source block
    # Iterate through the row to find the first pixel that isn't white (0) or orange (7)
    for i in range(width):
        pixel = input_row[i]
        if pixel != 0 and pixel != 7:
            source_color = pixel
            source_start_index = i
            source_end_index = i # Initialize end index to the start index
            break # Exit loop once the start of the source block is found

    # If no source block was found (e.g., row is all 0s and 7s), return original grid
    if source_start_index == -1:
        return input_grid_np

    # 2. Find the end of the source block (contiguous run of source_color)
    # Continue scanning from the pixel *after* the start index
    for i in range(source_start_index + 1, width):
        if input_row[i] == source_color:
            source_end_index = i # Update the end index if pixel matches source color
        else:
            break # Stop when a different color is encountered

    # 3. Find the boundary pixel (orange '7') located *after* the source block ends
    # Scan starting from the index immediately after the source block's end
    for i in range(source_end_index + 1, width):
        if input_row[i] == 7:
            boundary_index = i
            break # Exit loop once the boundary pixel is found

    # If no boundary pixel (7) was found after the source block, return the original grid
    # (This case might not occur based on provided examples, but ensures robustness)
    if boundary_index == -1:
        return input_grid_np

    # 4. Fill the gap between the source block end and the boundary pixel
    # Iterate through indices from *after* the source block's end up to *before* the boundary index
    for i in range(source_end_index + 1, boundary_index):
        # Change the pixel in the output row to the source color
        output_row[i] = source_color

    # 5. Construct the final 2D output grid
    # Reshape the modified 1D row back into a 2D array with one row
    output_grid = np.array([output_row])

    return output_grid

```