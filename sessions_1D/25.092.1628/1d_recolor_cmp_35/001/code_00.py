import copy

"""
Identifies all contiguous segments of blue pixels (value 1) in the input sequence.
Finds the longest blue segment. If multiple segments share the maximum length, selects the one that starts earliest (smallest index).
Changes the color of the pixels within this selected segment from blue (1) to yellow (4) in the output sequence.
Other pixels remain unchanged.
"""

def find_segments(sequence, target_color):
    """
    Finds all contiguous segments of a target color in a sequence.

    Args:
        sequence (list): The input sequence of colors (integers).
        target_color (int): The color value to find segments of.

    Returns:
        list: A list of dictionaries, where each dictionary represents a segment
              and contains 'start' (index), 'end' (index), and 'length'.
              Returns an empty list if no segments are found.
    """
    segments = []
    start_index = -1
    for i, color in enumerate(sequence):
        if color == target_color:
            if start_index == -1:
                # Start of a new segment
                start_index = i
        elif start_index != -1:
            # End of the current segment
            segments.append({
                'start': start_index,
                'end': i - 1,
                'length': i - start_index
            })
            start_index = -1 # Reset for the next potential segment

    # Check if the sequence ends with a target segment
    if start_index != -1:
        segments.append({
            'start': start_index,
            'end': len(sequence) - 1,
            'length': len(sequence) - start_index
        })

    return segments

def transform(input_grid):
    """
    Transforms the input sequence by changing the longest contiguous block
    of blue (1) pixels to yellow (4). If there's a tie in length,
    the earliest block is chosen.

    Args:
        input_grid (list): A 1D list representing the input sequence of colors.
                           Although named 'grid', this specific task uses a 1D list.

    Returns:
        list: The transformed 1D list.
    """
    # Ensure input is treated as a 1D sequence for this task
    input_sequence = input_grid[0] if isinstance(input_grid[0], list) else input_grid

    # Initialize output_sequence as a copy of the input
    output_sequence = list(input_sequence) # Use list() for shallow copy if input is already a list

    # 1. & 2. Find all blue segments and record their properties
    blue_segments = find_segments(input_sequence, target_color=1)

    # 3. & 4. & 5. & 6. Find the longest segment (earliest in case of tie)
    longest_segment = None
    max_length = 0

    if not blue_segments:
        # No blue segments found, return the original sequence
        return output_sequence

    for segment in blue_segments:
        if segment['length'] > max_length:
            max_length = segment['length']
            longest_segment = segment
        # Tie-breaking is implicitly handled because we iterate from left to right;
        # the first segment encountered with max_length will be stored and
        # subsequent segments of the same max_length won't overwrite it.

    # 7. & 8. Modify the output sequence
    if longest_segment:
        start = longest_segment['start']
        end = longest_segment['end']
        for i in range(start, end + 1):
            # Change blue (1) to yellow (4)
            if output_sequence[i] == 1: # Double check it's blue before changing
                 output_sequence[i] = 4

    return output_sequence
