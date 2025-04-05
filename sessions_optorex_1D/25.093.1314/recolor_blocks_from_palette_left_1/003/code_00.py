import math
from collections import Counter
import re # Not strictly needed for the final logic, but useful for block finding sometimes

"""
Transforms a sequence of digits represented as a space-separated string. 
The transformation identifies a 'target' digit within the main part of the sequence 
(excluding 'k' trailing parameter digits). This target digit is the most frequent 
non-zero digit (smallest in case of a tie). The number 'k' is determined dynamically 
by finding a value such that 'k' equals the number of blocks (consecutive sequences 
separated by non-target digits) of the target digit in the main sequence (input[:-k]). 
Once k is determined, the transformation replaces each occurrence of the target digit 
within its respective block in the main sequence with the corresponding parameter digit 
from the end of the original sequence (the i-th block is replaced using the i-th 
parameter digit). Zeros and other non-target digits remain unchanged in the main sequence. 
The final output is the transformed main sequence concatenated with the original k 
parameter digits, formatted back into a space-separated string.
"""

# === Helper Functions ===

def parse_input(input_str: str) -> list[int]:
    """Converts a space-separated string of digits into a list of integers."""
    # Added basic error handling for potentially non-string inputs during testing
    if not isinstance(input_str, str):
        # Attempt conversion if possible, otherwise raise error or handle specific types
        input_str = str(input_str) 
    
    # Handle potential empty strings or strings with only spaces
    parts = input_str.split()
    if not parts:
        return []
    return [int(d) for d in parts]

def format_output(output_list: list[int]) -> str:
    """Converts a list of integers back into a space-separated string."""
    return " ".join(map(str, output_list))

def find_target_digit(sequence: list[int]) -> int | None:
    """
    Finds the most frequent non-zero digit in the sequence.
    Returns the smallest digit in case of a tie.
    Returns None if there are no non-zero digits or the sequence is empty.
    """
    if not sequence:
        return None
    non_zero_digits = [d for d in sequence if d != 0]
    if not non_zero_digits:
        return None
    
    counts = Counter(non_zero_digits)
    if not counts: return None 
    
    # Find the maximum frequency
    max_freq = 0
    for freq in counts.values():
         if freq > max_freq:
             max_freq = freq

    # Find all digits with the maximum frequency
    candidates = [digit for digit, freq in counts.items() if freq == max_freq]

    # Return the smallest candidate
    return min(candidates)

def count_target_blocks(sequence: list[int], target_digit: int | None) -> int:
    """
    Counts blocks of the target_digit. A block is one or more consecutive
    target_digits separated from other blocks by any digit that is NOT 
    the target_digit (including 0).
    """
    if target_digit is None or not sequence:
        return 0

    block_count = 0
    in_block = False
    for digit in sequence:
        if digit == target_digit:
            if not in_block:
                block_count += 1
                in_block = True
        else: # Any other digit breaks the block sequence
             in_block = False
    return block_count

def replace_target_blocks(main_sequence: list[int], target_digit: int | None, parameter_digits: list[int]) -> list[int]:
    """
    Replaces digits in target blocks with corresponding parameter digits.
    Returns a new list representing the transformed main sequence.
    """
    # If no target or no parameters, or sequence is empty, return a copy of the original
    if target_digit is None or not parameter_digits or not main_sequence:
        return main_sequence[:] 

    transformed_sequence = []
    block_index = -1 # Use 0-based index for accessing parameter_digits
    in_block = False

    for digit in main_sequence:
        if digit == target_digit:
            if not in_block:
                block_index += 1 # Start of a new block
                in_block = True
            # Check if block_index is valid for parameter_digits
            if block_index < len(parameter_digits):
                 transformed_sequence.append(parameter_digits[block_index])
            else:
                 # Fallback: If somehow block count > len(params), append original.
                 # This indicates an issue in k determination but prevents crashing.
                 transformed_sequence.append(digit) 
        else:
            # Current digit is not the target digit
            transformed_sequence.append(digit)
            in_block = False # Any non-target digit ends the current block state
                
    return transformed_sequence

# === Main Transformation Function ===

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string sequence.
    """
    # 1. Parse Input
    input_digits = parse_input(input_str)
    n = len(input_digits)

    if n == 0:
        return "" # Handle empty input

    # Check for all zeros case early
    if all(d == 0 for d in input_digits):
        return input_str

    # 2. Determine k (Number of Parameters)
    determined_k = -1
    final_main_sequence = []
    final_parameter_digits = []
    final_target_digit = None

    # Iterate potential k values downwards. Max k can be n-1. 
    # Start from a reasonable guess like n // 2 + 1 downwards to 1.
    max_k_guess = min(n // 2 + 1, n - 1) if n > 1 else 0 
    
    for k in range(max_k_guess, 0, -1):
        # k must be < n to have a non-empty main sequence
        if k >= n: continue 

        potential_main_sequence = input_digits[:-k]
        potential_parameter_digits = input_digits[-k:]
        
        # Should not happen with k < n check, but defensive
        if not potential_main_sequence: continue 

        # Identify potential target digit in this main sequence
        potential_target_digit = find_target_digit(potential_main_sequence)
        
        # If a target digit exists, count its blocks
        if potential_target_digit is not None:
            num_blocks = count_target_blocks(potential_main_sequence, potential_target_digit)

            # Check if the number of blocks matches the current guess for k
            if num_blocks == k:
                # Found the consistent k, main sequence, parameters, and target
                determined_k = k
                final_main_sequence = potential_main_sequence
                final_parameter_digits = potential_parameter_digits
                final_target_digit = potential_target_digit
                break # Stop searching for k

    # 3. Handle No Match (Fallback)
    # If loop finishes without finding a matching k, it's an unexpected state 
    # given the problem examples. Return the original input as a safe fallback.
    # The all-zeros case is handled above. This covers non-zero inputs where
    # the k/block-count logic doesn't converge.
    if determined_k == -1:
         # This case should ideally not be reached based on training data pattern
         # print(f"Warning: Could not determine consistent k for input: {input_str}")
         return input_str

    # If k was found, but the corresponding main sequence had no non-zeros
    # (e.g. input="0 0 0 1 2", k=2 -> main="0 0 0", target=None)
    # final_target_digit would be None.

    # 4. Transform Main Sequence
    # Pass the determined components to the replacement function.
    # If final_target_digit is None, replace_target_blocks returns a copy.
    transformed_main_sequence = replace_target_blocks(
        final_main_sequence,
        final_target_digit,
        final_parameter_digits
    )

    # 5. Construct Final Sequence
    output_digits = transformed_main_sequence + final_parameter_digits

    # 6. Format Output
    return format_output(output_digits)
