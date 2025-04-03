import copy

"""
Transforms a 1xN input grid by identifying contiguous horizontal segments of orange (7) pixels. 
Segments with odd length are replaced with green (3) pixels.
Segments with even length are replaced with maroon (9) pixels.
Background white (0) pixels remain unchanged.
"""

def find_segments(row, target_color):
    """
    Identifies contiguous horizontal segments of a specific color in a 1D list (row).

    Args:
        row (list): A list of pixel values representing a row in the grid.
        target_color (int): The color value to find segments of.

    Returns:
        list: A list of tuples, where each tuple represents a segment
              and contains the start and end index (inclusive) of the segment.
              e.g., [(start1, end1), (start2, end2), ...]
    """
    segments = []
    start_index = -1
    # Iterate through the row with index
    for i, pixel in enumerate(row):
        # Ensure pixel is compared as an integer
        is_target = int(pixel) == target_color

        # Start of a new segment
        if is_target and start_index == -1:
            start_index = i

        # End of the current segment (pixel is not target OR it's the end of the row)
        # We check if start_index is not -1 to ensure we are currently inside a segment
        if not is_target and start_index != -1:
            segments.append((start_index, i - 1))
            start_index = -1 # Reset for the next potential segment

    # Handle segment that extends to the very end of the row
    if start_index != -1:
        segments.append((start_index, len(row) - 1))

    return segments

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list): A list of lists representing the input grid. 
                           Expected to be 1xN for this specific task.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    # Validate input format - expect a list containing one list (the row)
    if not isinstance(input_grid, list) or len(input_grid) == 0 or not isinstance(input_grid[0], list):
        # Handle invalid input, perhaps return empty or raise error
        # For ARC, returning the input might be a fallback, but here we aim for correctness.
        return [] # Or raise ValueError("Invalid input grid format")

    # Extract the single row from the input grid
    # Ensure it's treated as a standard Python list to avoid potential NumPy issues
    input_row = list(input_grid[0]) 
    
    # Create a copy of the input row to modify for the output.
    # This ensures background pixels are preserved unless overwritten.
    output_row = list(input_row) 

    # Define the colors involved
    input_color = 7  # orange
    odd_length_color = 3  # green
    even_length_color = 9 # maroon

    # Find all contiguous segments of the input color (orange) in the input row
    orange_segments = find_segments(input_row, input_color)

    # Process each identified orange segment
    for start, end in orange_segments:
        # Calculate the length of the segment
        length = end - start + 1
        
        # Determine the new color based on the segment length's parity
        if length % 2 != 0:  # Odd length
            new_color = odd_length_color
        else:  # Even length
            new_color = even_length_color
            
        # Update the pixels in the output row for the current segment's range
        for i in range(start, end + 1):
            output_row[i] = new_color
            
    # Return the transformed row, wrapped in a list to match the required grid format (list of lists)
    return [output_row]
