import copy

"""
Identifies the two non-white pixels in the input row.
Determines the leftmost (start_index) and rightmost (end_index) positions of these pixels.
Notes the color of these pixels (marker_color).
Creates a copy of the input row.
Fills the segment in the copied row from start_index to end_index (inclusive) with the marker_color.
Returns the modified row.
"""

def find_non_white_pixels(row):
    """Finds the indices and color of non-white pixels in a row."""
    non_white_pixels = []
    marker_color = None
    for index, pixel_color in enumerate(row):
        if pixel_color != 0:
            non_white_pixels.append(index)
            # Assuming both markers have the same color, as per examples
            marker_color = pixel_color 
    return non_white_pixels, marker_color

def transform(input_grid):
    """
    Transforms the input grid by finding two marker pixels and filling the segment 
    between them (inclusive) with their color.
    
    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid. 
                                       Expected to be 1xN for this task.

    Returns:
        list[list[int]]: The transformed grid.
    """
    # Ensure input is treated as a single row
    if not input_grid or not input_grid[0]:
        return [] # Handle empty input
        
    input_row = input_grid[0]
    
    # Initialize output_grid as a copy of the input_grid
    # Using deepcopy to avoid modifying the original input structure if needed elsewhere
    output_grid = copy.deepcopy(input_grid)
    output_row = output_grid[0]

    # 1. Identify all non-white pixels and their color
    non_white_indices, marker_color = find_non_white_pixels(input_row)

    # Check if exactly two markers were found (as per observed examples)
    if len(non_white_indices) != 2 or marker_color is None:
        # If not exactly two markers, return the original grid or handle error
        # For this specific task based on examples, we expect exactly two.
        # Returning the copy unmodified if the pattern doesn't match.
        print(f"Warning: Expected 2 non-white markers, found {len(non_white_indices)}. Returning original grid.")
        return output_grid 

    # 3. & 4. Find the start and end indices
    start_index = min(non_white_indices)
    end_index = max(non_white_indices)

    # 5. Output row already initialized as a copy.
    # 6. & 7. Iterate and fill the segment
    for i in range(start_index, end_index + 1):
        output_row[i] = marker_color

    # 8. Return the modified grid
    return output_grid