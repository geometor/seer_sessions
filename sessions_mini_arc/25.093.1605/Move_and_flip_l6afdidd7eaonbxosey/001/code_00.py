import numpy as np

"""
Identify the bounding box of the non-zero cluster in the input grid.
Extract this cluster.
Transpose the extracted cluster (swap rows and columns).
Place the transposed cluster into a new grid (initially all zeros) of the same dimensions as the input grid, shifting its top-left corner one position down and one position to the right relative to its original top-left corner.
If the input grid contains no non-zero elements, return a grid of zeros.
"""

def find_bounding_box(grid):
    """Finds the bounding box of non-zero elements."""
    non_zero_rows, non_zero_cols = np.nonzero(grid)
    if non_zero_rows.size == 0:
        return None  # No non-zero elements found
    min_r = np.min(non_zero_rows)
    max_r = np.max(non_zero_rows)
    min_c = np.min(non_zero_cols)
    max_c = np.max(non_zero_cols)
    return min_r, min_c, max_r, max_c

def transform(input_grid):
    """
    Transforms the input grid by finding the non-zero cluster,
    transposing it, and shifting it down and right by one position.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # Initialize the output grid with zeros, having the same dimensions as the input
    output_array = np.zeros_like(input_array)

    # Find the bounding box of the non-zero cluster in the input
    bbox = find_bounding_box(input_array)

    # If no non-zero elements are found (bbox is None), return the zero grid
    if bbox is None:
        return output_array.tolist() # Return as list of lists

    min_r, min_c, max_r, max_c = bbox

    # Extract the non-zero cluster using the bounding box coordinates
    cluster = input_array[min_r : max_r + 1, min_c : max_c + 1]

    # Transpose the extracted cluster
    transposed_cluster = cluster.T

    # Calculate the new top-left corner coordinates for the transposed cluster
    # Shift down by 1 row and right by 1 column
    new_min_r = min_r + 1
    new_min_c = min_c + 1

    # Get the dimensions of the transposed cluster
    t_rows, t_cols = transposed_cluster.shape

    # Calculate the bottom-right coordinates in the output grid
    new_max_r = new_min_r + t_rows
    new_max_c = new_min_c + t_cols

    # Place the transposed cluster into the output grid at the new location
    # Check if the new location is within the bounds of the output grid
    if new_max_r <= rows and new_max_c <= cols:
         output_array[new_min_r:new_max_r, new_min_c:new_max_c] = transposed_cluster
    # else: # Optional: handle cases where the shifted cluster goes out of bounds
         # print("Warning: Shifted cluster partially or fully outside grid bounds.")
         # Decide how to handle this - e.g., clip the cluster or raise an error.
         # For this problem based on examples, we assume it always fits.
         # If clipping is desired:
         # clip_rows = min(t_rows, rows - new_min_r)
         # clip_cols = min(t_cols, cols - new_min_c)
         # if clip_rows > 0 and clip_cols > 0:
         #    output_array[new_min_r : new_min_r + clip_rows, new_min_c : new_min_c + clip_cols] = transposed_cluster[:clip_rows, :clip_cols]
         pass # Assuming based on examples it always fits

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid