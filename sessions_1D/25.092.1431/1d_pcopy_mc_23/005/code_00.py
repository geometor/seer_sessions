import copy

"""
Transforms a 1D sequence by finding isolated non-white pixels flanked by white pixels 
and expanding the non-white color to replace the flanking white pixels.

Specifically, the transformation rule identifies patterns of `[white, non-white, white]` 
(represented numerically as `[0, C, 0]` where C is any color from 1 to 9) in the 
input sequence. For each occurrence of this pattern found in the original input sequence, 
it replaces the corresponding triplet of elements in a copy of the sequence with 
`[C, C, C]`. Pixels not part of such a pattern remain unchanged. The process ensures 
that modifications are based solely on the original input state, preventing cascading 
effects within a single transformation step.
"""

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence (list): A list of integers (0-9) representing the input 1D sequence.

    Returns:
        list: A new list representing the transformed sequence.
    """
    # Create a deep copy of the input sequence to store the output.
    # Modifications will be made to this copy, ensuring that the pattern matching
    # logic always refers to the original, unmodified input sequence.
    output_sequence = copy.deepcopy(input_sequence)
    
    # Get the length of the input sequence.
    n = len(input_sequence)

    # Iterate through the sequence, focusing on potential central elements of the [0, C, 0] pattern.
    # The loop must start at index 1 and end at index n-2 (exclusive of n-1) to allow
    # safe access to the element before (i-1) and the element after (i+1).
    # If the sequence length is less than 3, this range will be empty, and the loop won't run,
    # correctly handling short sequences.
    for i in range(1, n - 1):
        
        # Check if the triplet centered at index 'i' in the *original* input sequence
        # matches the pattern [0, C, 0], where C is any non-white color (1-9).
        if input_sequence[i-1] == 0 and input_sequence[i] != 0 and input_sequence[i+1] == 0:
            
            # If the pattern is found, identify the non-white color 'C' to be expanded.
            color_to_expand = input_sequence[i]
            
            # Modify the corresponding elements in the *output* sequence.
            # Replace the [0, C, 0] pattern at indices [i-1, i, i+1] with [C, C, C].
            output_sequence[i-1] = color_to_expand
            output_sequence[i]   = color_to_expand
            output_sequence[i+1] = color_to_expand

    # Return the modified sequence.
    return output_sequence