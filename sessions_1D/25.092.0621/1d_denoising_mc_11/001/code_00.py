import collections

def find_non_white_segment(row):
    """
    Finds the start and end indices of the contiguous non-white segment.
    
    Args:
        row (list): The input row (list of integers).
        
    Returns:
        tuple: (start_index, end_index) or (None, None) if no non-white segment exists.
    """
    start_index = None
    end_index = None
    
    # Find the first non-white pixel index
    for i, pixel in enumerate(row):
        if pixel != 0:
            start_index = i
            break
            
    # If no non-white pixel found, return None
    if start_index is None:
        return None, None
        
    # Find the last non-white pixel index by searching backwards
    for i in range(len(row) - 1, start_index - 1, -1):
        if row[i] != 0:
            end_index = i
            break
            
    return start_index, end_index

def determine_dominant_color(segment):
    """
    Determines the most frequent non-white color in a segment.
    
    Args:
        segment (list): The segment of the row (list of integers).
        
    Returns:
        int: The dominant color, or None if the segment is empty or all white.
    """
    # Filter out white pixels (0)
    non_white_pixels = [pixel for pixel in segment if pixel != 0]
    
    if not non_white_pixels:
        return None
        
    # Count frequencies of non-white pixels
    counts = collections.Counter(non_white_pixels)
    
    # Find the color with the highest frequency
    # If there's a tie, most_common(1) returns one of them
    dominant_color = counts.most_common(1)[0][0]
    
    return dominant_color

def transform(input_grid):
    """
    Identifies a central segment of non-white pixels in a 1D input grid (row).
    Determines the most frequent non-white color (dominant color) within that segment.
    Replaces all other non-white pixels (noise) within the segment with the dominant color.
    Leading/trailing white pixels remain unchanged.
    """
    # The input is expected to be a single row, represented as a list
    input_row = input_grid[0] # Assuming input_grid is a list containing one row list
    
    # Initialize output_row as a copy of the input_row
    output_row = list(input_row)
    
    # 1. Identify the contiguous central segment of non-white pixels
    start_index, end_index = find_non_white_segment(input_row)
    
    # If no non-white segment exists, return the original row
    if start_index is None:
        return [output_row] # Return as a grid (list of lists)

    # Extract the segment
    segment = input_row[start_index : end_index + 1]
    
    # 2. Determine the dominant color within this central segment
    dominant_color = determine_dominant_color(segment)
    
    # If no dominant color could be determined (e.g., segment was all white, though 
    # find_non_white_segment should prevent this), return original
    if dominant_color is None:
         return [output_row]

    # 3. Iterate through the pixels of the identified central segment in the output row
    # 4. For each pixel, if it's not white and not the dominant color, change it.
    for i in range(start_index, end_index + 1):
        if output_row[i] != 0 and output_row[i] != dominant_color:
            output_row[i] = dominant_color
            
    # Return the modified row wrapped in a list to match grid format
    return [output_row]