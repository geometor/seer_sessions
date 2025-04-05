import math
from collections import Counter

"""
1. Parse the input string into a list of integers.
2. Determine the number of parameter digits, 'k', by iterating downwards from a maximum possible value (e.g., half the sequence length). For a given k, the last k digits are parameters, and the rest is the main sequence.
3. Identify the target digit within the potential main sequence: it's the most frequent non-zero digit (smallest in case of a tie).
4. Count the number of blocks (consecutive sequences separated by zeros) of the target digit in the potential main sequence.
5. If the block count matches k, then this k is correct. Finalize the main sequence and parameter digits.
6. Create a transformed main sequence: Iterate through the finalized main sequence. Replace digits within the i-th block of the target digit with the i-th parameter digit. Leave zeros and other non-target digits unchanged. Keep track of the current block index.
7. Concatenate the transformed main sequence and the original parameter digits.
8. Format the resulting list back into a space-separated string.
"""

def parse_input(input_str: str) -> list[int]:
    """Converts a space-separated string of digits into a list of integers."""
    return [int(d) for d in input_str.split()]

def format_output(output_list: list[int]) -> str:
    """Converts a list of integers back into a space-separated string."""
    return " ".join(map(str, output_list))

def find_target_digit(sequence: list[int]) -> int | None:
    """
    Finds the most frequent non-zero digit in the sequence.
    Returns the smallest digit in case of a tie.
    Returns None if there are no non-zero digits.
    """
    non_zero_digits = [d for d in sequence if d != 0]
    if not non_zero_digits:
        return None
    
    counts = Counter(non_zero_digits)
    max_freq = 0
    candidates = []
    
    # Find the maximum frequency
    for digit, freq in counts.items():
        if freq > max_freq:
            max_freq = freq
            
    # Find all digits with the maximum frequency
    for digit, freq in counts.items():
         if freq == max_freq:
             candidates.append(digit)

    # Return the smallest candidate if there are any
    return min(candidates) if candidates else None


def count_target_blocks(sequence: list[int], target_digit: int | None) -> int:
    """Counts blocks of the target_digit separated by zeros."""
    if target_digit is None:
        return 0

    block_count = 0
    in_block = False
    for digit in sequence:
        if digit == target_digit:
            if not in_block:
                block_count += 1
                in_block = True
        elif digit == 0:
             in_block = False
        else: # non-zero, non-target
             in_block = False # Reset block state if interrupted by other numbers too
    return block_count

def replace_target_blocks(main_sequence: list[int], target_digit: int | None, parameter_digits: list[int]) -> list[int]:
    """Replaces digits in target blocks with corresponding parameter digits."""
    if target_digit is None or not parameter_digits:
        return main_sequence[:] # Return a copy if no target or no params

    transformed_sequence = []
    block_index = -1 # 0-based index for parameter_digits
    in_block = False

    for digit in main_sequence:
        if digit == target_digit:
            if not in_block:
                block_index += 1
                in_block = True
            # Ensure we don't go out of bounds if block count calculation was off somehow
            if block_index < len(parameter_digits):
                 transformed_sequence.append(parameter_digits[block_index])
            else:
                 # Fallback: append original target digit if params run out
                 # This shouldn't happen if k determination is correct
                 transformed_sequence.append(digit)
        else:
            transformed_sequence.append(digit)
            if digit == 0:
                in_block = False
            else: # Non-zero, non-target digit also breaks the block sequence
                in_block = False
                
    return transformed_sequence


def transform(input_str: str) -> str:
    """
    Applies the transformation rule: identify target digit, count its blocks (k),
    use last k digits as parameters to replace target blocks, keep parameters at the end.
    """
    input_digits = parse_input(input_str)
    n = len(input_digits)
    
    # --- Determine k, main_sequence, parameter_digits, and target_digit ---
    determined_k = -1
    final_main_sequence = []
    final_parameter_digits = []
    final_target_digit = None

    # Iterate potential k values downwards. Max k can be n//2 or less. Let's try n-1 down to 1.
    # A reasonable max might be 5 based on examples, or more generally n // 2.
    max_k_guess = min(n // 2 + 1, 6) # Heuristic based on examples and logic
    for k in range(max_k_guess, 0, -1):
        if k >= n : continue # k must be smaller than total length

        potential_main_sequence = input_digits[:-k]
        potential_parameter_digits = input_digits[-k:]
        
        if not potential_main_sequence: continue # Need a main sequence to analyze

        potential_target_digit = find_target_digit(potential_main_sequence)
        
        # We need a target digit to count blocks for
        if potential_target_digit is not None:
            num_blocks = count_target_blocks(potential_main_sequence, potential_target_digit)

            # Check if the number of blocks matches the current guess for k
            if num_blocks == k:
                determined_k = k
                final_main_sequence = potential_main_sequence
                final_parameter_digits = potential_parameter_digits
                final_target_digit = potential_target_digit
                break # Found the correct k

    # If no k was found (e.g., all zeros input, or mismatch), return original?
    # Based on examples, seems a valid k is always found.
    # If determined_k remains -1, it implies an edge case or pattern mismatch.
    # For now, assume k is found. Handle errors later if needed.
    if determined_k == -1:
         # Fallback or error handling: maybe return input as is, or raise error
         # Let's try finding target in the whole sequence except last 2 as a guess
         # This part needs refinement based on failed cases.
         # For now, stick to the strict logic derived. If it fails, return input.
         # A simple fallback: If only zeros, return input. If non-zeros exist but no k found, return input.
         if all(d == 0 for d in input_digits):
              return input_str
         # If still no k found after loop, assume no transformation? Or maybe k=0?
         # Let's assume the described logic must find a k for valid inputs.
         # If the loop finishes without break, something is unexpected.
         # Maybe the logic needs adjusting for cases like single non-zero item etc.
         # For now, let's proceed assuming k was found if input isn't all zeros.
         # A safe fallback if k remains -1 and input isn't all zero might be needed.
         # Let's try to calculate target/blocks on full list minus maybe 2 elements if loop fails.
         # But the primary logic seems robust based on examples. Let's assume it finds k.
         # If determined_k is still -1, and there are non-zeros, this indicates a pattern break.
         # Let's return input string in this unexpected scenario for now.
         if find_target_digit(input_digits) is not None: # Check if there's anything to transform at all
             print(f"Warning: Could not determine consistent k for input: {input_str}")
             # Returning original input might be safest if logic fails
             # return input_str # Option 1: return original
             # Option 2: Assume k=0 -> no parameters, no replacement
             final_main_sequence = input_digits 
             final_parameter_digits = []
             final_target_digit = None 
         else: # All zeros case
             return input_str


    # --- Perform Replacement ---
    transformed_main_sequence = replace_target_blocks(
        final_main_sequence,
        final_target_digit,
        final_parameter_digits
    )

    # --- Construct Output ---
    output_digits = transformed_main_sequence + final_parameter_digits

    return format_output(output_digits)
