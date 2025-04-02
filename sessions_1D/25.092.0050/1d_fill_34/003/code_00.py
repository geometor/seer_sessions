import numpy as np

"""
Transforms a 1xN input grid by finding the two non-white pixels, 
identifying their color (C), and filling the segment between 
(and including) their positions in the output grid with color C. 
The output grid has the same dimensions as the input.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms a 1xN input grid by filling the segment between two non-white pixels.

    Args:
        input_grid: A 2D NumPy array representing the input grid (expected shape 1xN).

    Returns:
        A 2D NumPy array representing the transformed output grid.
    """
    
    # Ensure input is a NumPy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Check if the input has exactly one row
    if input_grid.shape[0] != 1:
        # Handle unexpected input shape, maybe return input or raise error
        # For ARC, we usually assume valid input format based on examples.
        print(f"Warning: Expected input grid with 1 row, got shape {input_grid.shape}")
        # Let's proceed assuming the first row is the relevant one if more exist,
        # or handle potential errors if zero rows exist.
        if input_grid.shape[0] == 0:
             return np.array([[]]) # Return empty if input is empty

    # Extract the first (and only) row
    input_row = input_grid[0]
    height, width = input_grid.shape # Get original shape for output

    # Initialize variables to store the non-white color and its indices
    non_white_color = -1 # Use -1 or None as placeholder
    indices = []

    # Find the non-white color and its column indices in the row
    for i, pixel_color in enumerate(input_row):
        if pixel_color != 0:
            # If this is the first non-white pixel found, store its color
            if non_white_color == -1:
                non_white_color = pixel_color
            # Store the index (column) of the non-white pixel
            indices.append(i)
            
    # Expecting exactly two indices based on the task description
    if len(indices) != 2 or non_white_color == -1:
        # If the input doesn't match the expected pattern, return it unchanged or handle error
        # print("Warning: Did not find exactly two non-white pixels of the same color.")
        # Returning the original grid might be a safe default for unexpected cases in ARC
        return input_grid.copy() 

    # Determine the start and end column indices of the segment to fill
    start_index = min(indices)
    end_index = max(indices)

    # Create the output grid, initialized with white (0), matching input shape
    output_grid = np.zeros_like(input_grid)

    # Fill the segment in the first row of the output grid with the non-white color
    # Using array slicing for efficiency
    output_grid[0, start_index : end_index + 1] = non_white_color

    return output_grid