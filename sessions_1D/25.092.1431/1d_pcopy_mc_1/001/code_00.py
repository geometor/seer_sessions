import copy

"""
Transform a 1D sequence of pixels based on a local pattern.
Identify triplets of pixels in the input sequence matching the pattern [0, C, 0], 
where C is any non-zero color (1-9) and 0 is the background color.
For each matched pattern, replace the triplet [0, C, 0] in the output sequence 
with [C, C, C], using the color C found in the middle of the input pattern.
Pixels not part of such a matched pattern remain unchanged in the output.
The transformation is applied based on the original input sequence.
"""

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of integers representing the 1D pixel sequence.

    Returns:
        A list of integers representing the transformed 1D pixel sequence.
    """

    # Initialize output_sequence as a copy of the input_sequence
    # This ensures pixels not involved in the transformation are preserved
    output_sequence = copy.deepcopy(input_sequence)
    n = len(input_sequence)

    # Scan for the pattern [0, C, 0]
    # Iterate through the input_sequence, focusing on the middle element of potential triplets
    # The loop range ensures we can safely access i-1 and i+1
    for i in range(1, n - 1):
        # Check if the current triplet in the *input* sequence matches the pattern
        # input_sequence[i-1] should be the background color (0)
        # input_sequence[i] should be a non-background color (C != 0)
        # input_sequence[i+1] should be the background color (0)
        if input_sequence[i-1] == 0 and input_sequence[i] != 0 and input_sequence[i+1] == 0:
            # Get the color C from the middle of the matched pattern
            color_c = input_sequence[i]
            
            # Apply the transformation: change the corresponding triplet in the output_sequence
            # Set the pixel at index i-1 to color C
            output_sequence[i-1] = color_c
            # Set the pixel at index i to color C
            output_sequence[i] = color_c
            # Set the pixel at index i+1 to color C
            output_sequence[i+1] = color_c

    # Return the modified sequence
    return output_sequence