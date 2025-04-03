"""
Homogenizes the colors within the central non-white segment of a single-row 
grid (represented as a flat list) by replacing all non-white, non-dominant 
pixels in that segment with the segment's most frequent non-white color. 
White (0) padding pixels outside the segment and any white pixels inside the 
segment remain unchanged.
"""

from collections import Counter

def find_active_segment(row):
    """
    Finds the start and end indices (exclusive) of the contiguous block 
    encompassing the first to the last non-white pixel in the input row list.

    Args:
        row (list): A list of integers representing the pixel colors in the row.

    Returns:
        tuple: A tuple (start_index, end_index). Returns (None, None) if 
               no non-white pixels are found. end_index is exclusive.
    """
    start_index = -1
    end_index = -1
    # Iterate through the row to find the first and last non-zero elements
    for i, pixel in enumerate(row):
        if pixel != 0:  # Found a non-white pixel
            if start_index == -1:
                start_index = i  # Mark the start index only the first time
            end_index = i      # Continuously update the end index to the last found non-white
            
    # If no non-white pixels were found, start_index remains -1
    if start_index == -1: 
        return None, None
        
    # The end index for slicing should be one past the last non-white pixel
    return start_index, end_index + 1 

def find_dominant_color_in_segment(row, start_index, end_index):
    """
    Determines the most frequent non-zero color within a specified segment of a row.

    Args:
        row (list): The list of integers representing the full row.
        start_index (int): The starting index of the segment (inclusive).
        end_index (int): The ending index of the segment (exclusive).

    Returns:
        int or None: The most frequent non-zero color value within the segment, 
                     or None if the segment is empty, contains only zeros, 
                     or if indices are invalid.
    """
    # Validate indices and segment existence
    if start_index is None or end_index is None or start_index >= end_index or start_index < 0:
        return None 

    # Extract the segment
    segment = row[start_index:end_index]
    
    if not segment: # Should not happen if indices are valid, but good check
        return None 

    # Filter out zeros (white) and count remaining colors
    # Using a generator expression for efficiency
    color_counts = Counter(p for p in segment if p != 0)

    # If no non-zero colors were found after filtering
    if not color_counts:
        return None 
        
    # Find the most frequent color. most_common(1) returns a list [(color, count)]
    dominant_color, _ = color_counts.most_common(1)[0]
    return dominant_color

def transform(input_grid):
    """
    Applies the color normalization transformation to the input grid (row).

    Args:
        input_grid (list): A flat list of integers representing a single row. 
                          (Note: Although named input_grid for consistency 
                           with ARC terminology, it's treated as a single row/list).

    Returns:
        list: The transformed flat list (row).
    """
    # Handle potential list-of-lists input by assuming the first element is the row
    # This handles both flat list and [[list]] inputs gracefully for this specific task
    if isinstance(input_grid, list) and len(input_grid) > 0 and isinstance(input_grid[0], list):
      input_row = input_grid[0]
    elif isinstance(input_grid, list):
      input_row = input_grid # Assume it's already a flat list
    else:
      # Handle invalid input type if necessary, e.g., raise TypeError or return empty
      print(f"Warning: Unexpected input type: {type(input_grid)}. Assuming empty.")
      return []

    # Handle empty row case
    if not input_row:
        return [] 

    # Initialize the output row as a copy of the input row
    output_row = list(input_row)
    
    # 1. Identify the active segment (indices of first to last non-white pixels)
    start_index, end_index = find_active_segment(input_row)

    # 2. If no non-white segment exists (row is all white or empty), return the original copy
    if start_index is None:
        return output_row 

    # 3. Determine the dominant color within the identified active segment
    dominant_color = find_dominant_color_in_segment(input_row, start_index, end_index)
    
    # 4. If a dominant color is found, normalize the segment in the output row
    if dominant_color is not None:
        # Iterate *only* through the indices corresponding to the active segment
        for i in range(start_index, end_index):
            # Check if the current pixel in the segment is not white (0) 
            # AND is not the dominant color.
            if output_row[i] != 0 and output_row[i] != dominant_color:
                 # Replace this 'impurity' pixel with the dominant color
                output_row[i] = dominant_color
                # Pixels that are 0 or already the dominant color within the segment are unchanged.
                
    # 5. Return the modified row. Pixels outside the segment (padding) were never touched.
    return output_row