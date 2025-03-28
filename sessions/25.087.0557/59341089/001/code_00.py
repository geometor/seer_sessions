import numpy as np

"""
Accepts an input grid, creates a horizontally flipped version of it, and then
constructs the output grid by concatenating the flipped version, the original version,
the flipped version again, and the original version again, side-by-side horizontally.
"""

def transform(input_grid):
    """
    Transforms the input grid by creating a horizontally flipped version and
    concatenating them in the sequence: flipped, original, flipped, original.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
                          Or numpy.ndarray if numpy conversion is preferred downstream.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Create a horizontally flipped version of the input array
    # np.fliplr flips the array in the left/right direction.
    flipped_array = np.fliplr(input_array)

    # Concatenate the arrays horizontally (along axis=1) in the specified order:
    # flipped, original, flipped, original
    output_array = np.concatenate((flipped_array, input_array, flipped_array, input_array), axis=1)

    # Convert the final numpy array back to a list of lists if required,
    # although numpy arrays are often more convenient for grid operations.
    # return output_array.tolist()
    return output_array