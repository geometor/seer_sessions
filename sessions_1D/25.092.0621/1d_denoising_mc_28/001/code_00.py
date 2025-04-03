import collections
import copy

"""
Identifies contiguous segments of non-white (non-zero) pixels in a 1D input sequence. 
For each segment, determines the most frequent color (dominant color). 
Replaces all other non-white pixels within that segment with the dominant color. 
White (zero) pixels remain unchanged.
"""

def find_segments(sequence):
    """
    Finds the start and end indices of contiguous non-zero segments.

    Args:
        sequence (list): The input sequence of color values.

    Returns:
        list: A list of tuples, where each tuple is (start_index, end_index).
              end_index is inclusive.
    """
    segments = []
    start_index = -1
    in_segment = False
    for i, pixel in enumerate(sequence):
        if pixel != 0 and not in_segment:
            # Start of a new segment
            start_index = i
            in_segment = True
        elif pixel == 0 and in_segment:
            # End of the current segment
            segments.append((start_index, i - 1))
            in_segment = False
            start_index = -1
    # Handle segment extending to the end of the sequence
    if in_segment:
        segments.append((start_index, len(sequence) - 1))
    return segments

def find_dominant_color(segment_values):
    """
    Finds the most frequent color in a list of pixel values.
    If there's a tie, the numerically smallest color value wins.

    Args:
        segment_values (list): A list of non-zero color values from a segment.

    Returns:
        int: The dominant color value.
    """
    if not segment_values:
        return 0 # Should not happen for valid segments, but safe default

    counts = collections.Counter(segment_values)
    max_count = 0
    dominant_color = -1

    # Find the max count
    for color, count in counts.items():
        if count > max_count:
            max_count = count

    # Find colors with the max count
    candidates = []
    for color, count in counts.items():
        if count == max_count:
            candidates.append(color)
    
    # Return the smallest color value among candidates
    return min(candidates)


def transform(input_grid):
    """
    Transforms the input grid (1D sequence) according to the rules:
    1. Find contiguous segments of non-zero pixels.
    2. For each segment, find the dominant (most frequent) color.
    3. Replace all non-dominant, non-zero pixels in the segment with the dominant color.
    4. Zero pixels remain unchanged.

    Args:
        input_grid (list): A 1D list of integers representing pixel colors.

    Returns:
        list: The transformed 1D list of integers.
    """
    # Initialize output_grid as a copy of the input
    output_grid = copy.deepcopy(input_grid)
    
    # Find all non-zero segments
    segments = find_segments(input_grid)

    # Process each segment
    for start, end in segments:
        # Extract the values of the pixels within the current segment
        segment_values = [input_grid[i] for i in range(start, end + 1)]
        
        # Determine the dominant color for this segment
        dominant_color = find_dominant_color(segment_values)

        # Iterate through the segment indices in the output grid
        for i in range(start, end + 1):
            # If a pixel is part of the segment (non-zero) and not the dominant color
            if output_grid[i] != 0 and output_grid[i] != dominant_color:
                # Change its color to the dominant color
                output_grid[i] = dominant_color

    # Return the modified grid
    return output_grid