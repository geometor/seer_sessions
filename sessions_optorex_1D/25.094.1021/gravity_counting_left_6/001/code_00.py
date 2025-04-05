import collections # Although not strictly necessary here, importing common libraries is good practice.

"""
Transforms an input sequence of 12 space-separated integers.
Counts the total number of zeros (N) in the input sequence.
Generates an output sequence of 12 integers consisting of N zeros
followed by (12-N) ones, formatted as a space-separated string.
"""

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A string containing 12 space-separated integers (0-9).

    Returns:
        A string containing 12 space-separated integers (0 or 1),
        representing the transformed sequence.
    """

    # Parse the input string into a list of integers
    # Example: "5 8 2 0 6 0 2 6 0 1 4 0" -> [5, 8, 2, 0, 6, 0, 2, 6, 0, 1, 4, 0]
    input_sequence = [int(x) for x in input_str.split()]

    # Ensure input has the expected length (optional but good practice)
    if len(input_sequence) != 12:
        # Handle error appropriately, e.g., raise ValueError or return an error indicator
        # For this task, we assume valid input based on examples.
        pass 

    # Count the occurrences of the integer 0 in the input list
    zero_count = input_sequence.count(0)

    # Calculate the number of ones required for the output
    # The total length is fixed at 12
    num_ones = 12 - zero_count

    # Construct the output sequence
    # Create a list containing 'zero_count' zeros
    output_zeros = [0] * zero_count
    # Create a list containing 'num_ones' ones
    output_ones = [1] * num_ones
    # Combine the two lists to form the final output sequence
    output_sequence = output_zeros + output_ones

    # Convert the output sequence (list of integers) back to a space-separated string
    # Example: [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1] -> "0 0 0 0 1 1 1 1 1 1 1 1"
    output_str = " ".join(map(str, output_sequence))

    return output_str
