"""
Transformation Rule:
1. Receive the input as a 2D NumPy grid, assumed to have a single row (shape 1xN).
2. Locate the column index of the first occurrence of the green pixel (value 3) within the row. This marker acts as a separator.
3. Partition the input grid row into three parts based on this column index:
    *   `segment_before`: The sub-grid containing columns from the beginning up to (but not including) the marker's column.
    *   `marker_pixel_value`: The single green pixel value (3) at the marker's column index.
    *   `segment_after`: The sub-grid containing columns from the one after the marker's column to the end of the row.
4. Process the `segment_before`:
    *   Extract all white pixels (value 0) into a new 1D array.
    *   Extract all non-white pixels (values 1-9) into another new 1D array, ensuring their original relative order is maintained.
5. Construct the final output grid by horizontally concatenating (along axis 1) the following components, ensuring each is a 2D array with 1 row:
    *   The 1D array of white pixels, reshaped to (1, number_of_white_pixels).
    *   The 1D array of non-white pixels, reshaped to (1, number_of_non_white_pixels).
    *   The `marker_pixel_value`, reshaped to (1, 1).
    *   The `segment_after` sub-grid (which is already 1xM).
6. Return the constructed 2D output grid (shape 1xN).
"""

import numpy as np

def find_first_marker_column(grid: np.ndarray, marker_color: int) -> int:
    """
    Finds the column index of the first occurrence of the marker color in the first row of a 2D grid.

    Args:
        grid: The 2D input NumPy array (assumed 1xN).
        marker_color: The integer value of the marker pixel to find.

    Returns:
        The column index of the first marker.

    Raises:
        ValueError: If the marker color is not found in the first row of the grid.
    """
    # Find indices where the color matches in the first row
    marker_indices = np.where(grid[0, :] == marker_color)[0]
    if marker_indices.size == 0:
        raise ValueError(f"Marker color {marker_color} not found in the input grid's first row.")
    # Return the first column index found
    return marker_indices[0]

def separate_pixels_in_row(segment: np.ndarray, target_color: int) -> (np.ndarray, np.ndarray):
    """
    Separates a 1D NumPy array (representing a row segment) into two 1D arrays:
    one with the target color and one with all other colors, preserving the
    relative order within the second array.

    Args:
        segment: The 1D NumPy array segment to process.
        target_color: The integer value of the color to separate out.

    Returns:
        A tuple containing two 1D NumPy arrays:
        (array_of_target_color_pixels, array_of_other_color_pixels)
    """
    target_pixels = segment[segment == target_color]
    other_pixels = segment[segment != target_color]
    return target_pixels, other_pixels

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input 1xN grid by rearranging pixels before the green (3) marker.
    White pixels (0) are moved to the beginning of the pre-marker segment, followed
    by the non-white pixels in their original relative order. The marker and
    the post-marker segment remain unchanged in position relative to the end.

    Args:
        input_grid: A 2D NumPy array (shape 1xN) representing the input pixel row.

    Returns:
        A 2D NumPy array (shape 1xN) representing the transformed pixel row.
    """
    # Define marker and target colors
    marker_color = 3
    white_color = 0

    # Ensure input is 2D
    if input_grid.ndim != 2 or input_grid.shape[0] != 1:
         # Handle unexpected input shapes if necessary, here we assume 1xN based on task description
         # For robustness, could raise an error or try to adapt.
         print(f"Warning: Expected input shape 1xN, got {input_grid.shape}. Proceeding assuming first row.")
         # If it's 1D, reshape it
         if input_grid.ndim == 1:
             input_grid = input_grid.reshape(1, -1)
         elif input_grid.shape[0] > 1:
             # Decide how to handle multi-row inputs if needed.
             # For now, process only the first row as per examples.
             pass # Fall through and process grid[0,:]


    # 1. Locate the column index of the green marker pixel (3) in the first row
    try:
        marker_index = find_first_marker_column(input_grid, marker_color)
    except ValueError as e:
        # Handle case where marker is not found
        print(f"Warning: {e}. Returning original grid.")
        return input_grid

    # 2. Partition the input grid row into segments based on the marker index
    # Slicing a 2D array like this keeps the 2D shape (e.g., (1, k))
    segment_before_2d = input_grid[:, :marker_index]
    marker_value_2d = input_grid[:, marker_index:marker_index+1] # Keep as 2D (1,1)
    segment_after_2d = input_grid[:, marker_index + 1:]

    # 3. Process the segment *before* the marker
    #    Extract the 1D row from the 2D segment
    if segment_before_2d.size > 0:
        segment_before_1d = segment_before_2d[0, :]
        # Separate white pixels (0) from non-white pixels, preserving non-white order
        white_pixels_1d, non_white_pixels_1d = separate_pixels_in_row(segment_before_1d, white_color)
    else:
        # Handle empty segment before marker
        white_pixels_1d = np.array([], dtype=input_grid.dtype)
        non_white_pixels_1d = np.array([], dtype=input_grid.dtype)

    # 4. Reshape the separated 1D arrays back to 2D (1 row) for concatenation
    white_pixels_2d = white_pixels_1d.reshape(1, -1)
    non_white_pixels_2d = non_white_pixels_1d.reshape(1, -1)

    # 5. Construct the final output grid by concatenating the parts horizontally (axis=1)
    output_grid = np.concatenate((
        white_pixels_2d,
        non_white_pixels_2d,
        marker_value_2d,
        segment_after_2d
    ), axis=1)

    return output_grid