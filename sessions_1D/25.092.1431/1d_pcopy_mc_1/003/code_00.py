import copy
import numpy as np # Although not strictly needed for this simple list manipulation, numpy is often used in ARC tasks

"""
Transform a 1D sequence of pixels based on a local pattern.
Identify triplets of pixels in the input sequence matching the pattern [0, C, 0], 
where C is any non-zero color (1-9) and 0 is the background color (white).
For each matched pattern found in the original input sequence, replace the 
corresponding triplet [0, C, 0] in the output sequence with [C, C, C], 
using the color C found in the middle of the input pattern.
Pixels not part of such a matched pattern remain unchanged in the output.
The transformation operates on the sequence as a 1D list of integers.
"""

def transform(input_sequence):
    """
    Applies the pattern replacement transformation to the input sequence.

    Args:
        input_sequence: A list of integers representing the 1D pixel sequence. 
                          It's assumed this is a flat list, not a 2D array/grid.

    Returns:
        A list of integers representing the transformed 1D pixel sequence.
    """
    
    # Ensure input is treated as a list if it's passed as a NumPy array (common in ARC)
    if isinstance(input_sequence, np.ndarray):
        # Flatten if it's multidimensional, although examples suggest 1D
        input_sequence = input_sequence.flatten().tolist() 
    elif not isinstance(input_sequence, list):
        # Handle potential other types if necessary, or raise an error
        # For now, assume list or numpy array
        raise TypeError("Input must be a list or numpy array")

    # Initialize output_sequence as a deep copy of the input_sequence
    # This ensures pixels not involved in the transformation are preserved
    # and modifications don't affect the original input sequence check loop
    output_sequence = copy.deepcopy(input_sequence)
    n = len(input_sequence)

    # Check if the sequence is long enough to contain a triplet
    if n < 3:
        return output_sequence # Cannot form a triplet, return copy of input

    # Scan for the pattern [0, C, 0] using the original input_sequence
    # Iterate through the input_sequence, focusing on potential middle elements 'C'
    # The loop range ensures we can safely access indices i-1 and i+1
    for i in range(1, n - 1):
        # Define the potential triplet from the *original* input sequence
        prev_pixel = input_sequence[i-1]
        current_pixel = input_sequence[i]
        next_pixel = input_sequence[i+1]

        # Check if the triplet matches the pattern [white, C, white]
        # where white is 0 and C is any non-white color (1-9)
        if prev_pixel == 0 and current_pixel != 0 and next_pixel == 0:
            # Pattern matched! Get the color C
            color_c = current_pixel
            
            # Apply the transformation: change the corresponding triplet in the output_sequence
            # Replace [0, C, 0] with [C, C, C]
            output_sequence[i-1] = color_c
            output_sequence[i]   = color_c
            output_sequence[i+1] = color_c

    # Return the modified sequence
    return output_sequence
