import math  # Although not used in the final version, good practice to import if math ops might be needed.
import collections # Although not used in the final version, good practice to import if counting ops might be needed.

"""
Transforms an input sequence of 12 space-separated integers.
The transformation involves dividing the input sequence into three equal segments of 4 integers each.
Let the segments be A (indices 0-3), B (indices 4-7), and C (indices 8-11).
The output sequence is formed by concatenating these segments in the order: B, then C, then A.
The resulting sequence is formatted back into a space-separated string.
"""

def transform(input_str: str) -> str:
    """
    Applies the segment rearrangement transformation to the input string.

    Args:
        input_str: A string containing 12 space-separated integers.

    Returns:
        A string containing the transformed sequence of 12 space-separated integers.
    """

    # 1. Parse the input string into a list of integers.
    input_list = [int(x) for x in input_str.split()]

    # Check if input has the expected length (optional but good practice)
    if len(input_list) != 12:
        # Handle error appropriately, e.g., raise ValueError or return specific error string
        # For this context, we assume valid input based on examples.
        pass 

    # 2. Divide the input list into three consecutive segments of length 4.
    # Segment A: Elements from index 0 to 3.
    segment_a = input_list[0:4]
    # Segment B: Elements from index 4 to 7.
    segment_b = input_list[4:8]
    # Segment C: Elements from index 8 to 11.
    segment_c = input_list[8:12]

    # 3. Construct the output list by concatenating the segments in the order B, C, A.
    output_list = segment_b + segment_c + segment_a

    # 4. Format the resulting list back into a space-separated string.
    output_str = " ".join(map(str, output_list))

    return output_str
