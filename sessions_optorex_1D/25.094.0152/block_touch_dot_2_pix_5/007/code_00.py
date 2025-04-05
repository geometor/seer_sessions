import math
import collections

"""
Transformation Rule:
Identifies contiguous blocks of one or more zeros within an input sequence of integers, where each block is immediately preceded by a non-zero digit (Left neighbor, L) and immediately followed by a non-zero digit (Right neighbor, R). 
Based on the comparison of L and R, these identified 'mobile' zero blocks are relocated:
- If L < R, the zeros from the block are moved to the end of the sequence.
- If L > R, the zeros from the block are moved to the beginning of the sequence.
Zeros that are not part of such a L-0...0-R pattern (e.g., at the ends, adjacent to only one non-zero digit, or only next to other zeros) remain in place relative to the other non-moving elements.
The final sequence is constructed by concatenating the zeros designated for the beginning, the remaining non-zero digits and static zeros in their original relative order, and finally the zeros designated for the end.
"""

def transform(input_sequence: list[int]) -> list[int]:
    """
    Applies the transformation rule to the input sequence of integers.

    Args:
        input_sequence: A list of integers representing the input sequence.

    Returns:
        A new list of integers representing the transformed sequence.
    """
    # Input is already a list of integers, no parsing needed here.
    nums = input_sequence 
    n = len(nums)

    # Handle sequences too short for the L-0...0-R pattern
    if n < 3:
        return nums[:] # Return a copy to avoid modifying potential external references

    # Initialize collections for relocated zeros and indices to remove
    zeros_to_prepend = []
    zeros_to_append = []
    indices_to_remove = set() # Use a set for efficient lookup

    # Scan the sequence to find mobile zero blocks
    i = 0 
    while i < n:
        # Check if the current element could be the start of a mobile zero block
        # Condition: Must have a left neighbor (i>0), left neighbor non-zero, current element is zero
        if i > 0 and nums[i] == 0 and nums[i-1] != 0:
            left_neighbor = nums[i-1]
            
            # Find the end index 'k' of the contiguous block of zeros starting at 'i'
            k = i
            while k + 1 < n and nums[k+1] == 0:
                k += 1
            # 'k' now holds the index of the last zero in this block

            # Check if there is a non-zero element immediately after the block
            # Condition: Must have a right neighbor (k+1 < n), right neighbor non-zero
            if k + 1 < n and nums[k+1] != 0:
                # Found a valid L-0...0-R pattern
                right_neighbor = nums[k+1]
                num_zeros = k - i + 1 # Calculate the count of zeros in the block

                # Mark indices of this mobile zero block for removal from the core sequence
                for idx in range(i, k + 1):
                    indices_to_remove.add(idx)

                # Determine relocation based on comparison of neighbors
                if left_neighbor < right_neighbor:
                    zeros_to_append.extend([0] * num_zeros) # Add zeros to the end list
                elif left_neighbor > right_neighbor:
                    zeros_to_prepend.extend([0] * num_zeros) # Add zeros to the start list
                # If left_neighbor == right_neighbor, zeros are removed but not relocated

                # Advance the main loop index past the entire processed pattern (L, zeros, R)
                # Start checking from the element *after* the right neighbor
                i = k + 2 
                continue # Continue to the next iteration of the while loop
            else:
                # The zero block starting at 'i' does not have a valid non-zero right neighbor.
                # Therefore, this block is not mobile according to the rule.
                # Advance the index past this non-mobile block to avoid re-checking its internal zeros.
                i = k + 1
                continue # Continue to the next iteration
        
        # If the current element nums[i] did not start a mobile block, 
        # simply move to check the next index in the sequence.
        i += 1

    # Build the core sequence by filtering out the elements at the removed indices
    result_core = [nums[idx] for idx in range(n) if idx not in indices_to_remove]

    # Assemble the final sequence by concatenating the parts
    final_list = zeros_to_prepend + result_core + zeros_to_append

    return final_list

# Example of how this function might be called if input/output are strings
def solve_task(input_str: str) -> str:
    """ Parses input string, transforms the sequence, and formats the output string. """
    input_list = [int(x) for x in input_str.split()]
    output_list = transform(input_list)
    output_str = " ".join(map(str, output_list))
    return output_str