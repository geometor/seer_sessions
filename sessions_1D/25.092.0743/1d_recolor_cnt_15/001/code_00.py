import numpy as np

"""
Recolors contiguous horizontal blocks of orange (7) pixels based on their length.
- Blocks of length 1 become azure (8).
- Blocks of length 2 become gray (5).
- Blocks of length 3 become maroon (9).
- White (0) pixels remain unchanged.
The input is assumed to be a 1D grid (represented as a 2D array with height 1).
"""

def find_contiguous_segments(row, target_color):
    """
    Finds contiguous segments of a specific color in a 1D list (row).

    Args:
        row (list): The input row (list of pixel values).
        target_color (int): The color value to find segments of.

    Returns:
        list: A list of tuples, where each tuple is (start_index, end_index, length).
              end_index is exclusive (like Python slices).
    """
    segments = []
    i = 0
    n = len(row)
    while i < n:
        if row[i] == target_color:
            start_index = i
            # Find the end of the segment
            j = i + 1
            while j < n and row[j] == target_color:
                j += 1
            end_index = j
            length = end_index - start_index
            segments.append((start_index, end_index, length))
            i = end_index # Move past the found segment
        else:
            i += 1
    return segments

def transform(input_grid):
    """
    Transforms the input grid by recoloring orange segments based on their length.

    Args:
        input_grid (list of lists): A 2D list representing the input grid (height 1).

    Returns:
        list of lists: The transformed grid.
    """
    # Ensure input is treated as a NumPy array for easier handling, though list ops work too
    input_array = np.array(input_grid, dtype=int)
    
    # We expect a 1xN grid
    if input_array.shape[0] != 1:
        # Handle potential errors or unexpected input dimensions if necessary
        # For this specific task based on examples, we assume height is 1.
        pass 
        
    input_row = input_array[0] # Get the single row
    output_row = np.copy(input_row) # Initialize output as a copy

    # Define the color mapping based on segment length
    length_to_color_map = {
        1: 8,  # azure
        2: 5,  # gray
        3: 9   # maroon
    }
    
    # Find all segments of orange (7)
    orange_segments = find_contiguous_segments(input_row.tolist(), 7) # Use list version for find_segments

    # Apply the transformation for each found orange segment
    for start, end, length in orange_segments:
        # Determine the replacement color based on length
        if length in length_to_color_map:
            replacement_color = length_to_color_map[length]
            # Fill the corresponding segment in the output row with the new color
            output_row[start:end] = replacement_color
        # Else: if length is not in map, the segment remains orange (or handle as error/default)
        # Based on examples, only lengths 1, 2, 3 occur and need mapping.

    # Return the transformed row wrapped in a list to match the 2D grid format
    return output_row.reshape(1, -1).tolist()
