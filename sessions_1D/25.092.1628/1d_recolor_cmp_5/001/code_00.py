import copy

"""
Iterate through the input sequence (represented as a list). Identify contiguous 
horizontal runs of green pixels (value 3). If a run of green pixels has a length 
of exactly 5, change the color of those pixels to red (value 2) in the output 
sequence. Otherwise, keep the pixels unchanged (green runs of other lengths 
remain green, white pixels remain white).
"""

def find_contiguous_runs(sequence, target_value):
    """
    Finds contiguous runs of a specific value in a 1D sequence.

    Args:
        sequence (list): The input 1D list.
        target_value: The value to find runs of.

    Returns:
        list: A list of tuples, where each tuple contains the start index, 
              end index (exclusive), and length of a run. 
              e.g., [(start1, end1, length1), (start2, end2, length2), ...]
    """
    runs = []
    i = 0
    n = len(sequence)
    while i < n:
        if sequence[i] == target_value:
            start_index = i
            while i < n and sequence[i] == target_value:
                i += 1
            end_index = i
            length = end_index - start_index
            runs.append((start_index, end_index, length))
        else:
            i += 1
    return runs

def transform(input_grid):
    """
    Transforms the input grid by changing contiguous runs of 5 green pixels (3) 
    to red pixels (2).

    Args:
        input_grid (list): A 1D list representing the input sequence.

    Returns:
        list: A 1D list representing the transformed output sequence.
    """
    # Initialize output_grid as a copy of the input
    # Input is expected to be a flat list for this task based on examples
    output_grid = copy.deepcopy(input_grid) 
    
    # Define the target color (green) and the replacement color (red)
    target_color = 3 
    replacement_color = 2
    required_length = 5

    # Find all contiguous runs of the target color (green)
    green_runs = find_contiguous_runs(input_grid, target_color)

    # Iterate through the found runs
    for start, end, length in green_runs:
        # Check if the run has the required length
        if length == required_length:
            # Change the pixels in the output grid for this run
            for i in range(start, end):
                output_grid[i] = replacement_color
                
    # Return the modified output grid
    return output_grid