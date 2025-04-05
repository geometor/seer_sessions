"""
Transforms an input sequence of 12 integers based on the following rule:
1. Identify the most frequent number (background) and the least frequent non-zero count number (foreground).
2. Create an output sequence of the same length, filled initially with the background number.
3. For each occurrence of the foreground number at index 'i' in the input sequence, place it at index '(i + 4) mod 12' in the output sequence.
"""

from collections import Counter
import numpy as np # Although not strictly needed for this logic, it's often available in these environments.

def find_foreground_background(sequence):
    """Identifies the background (most frequent) and foreground (least frequent > 0) numbers."""
    if not sequence:
        return None, None
    
    counts = Counter(sequence)
    
    # Handle cases with only one unique number
    if len(counts) == 1:
        num = list(counts.keys())[0]
        return num, num # Background and foreground are the same

    # Find background (most frequent)
    background_num = counts.most_common(1)[0][0]

    # Find foreground (least frequent with count > 0)
    # Filter out counts of 0, sort by count ascending, take the first
    foreground_num = sorted([(num, count) for num, count in counts.items() if count > 0], key=lambda item: item[1])[0][0]
    
    # Check if foreground and background ended up being the same (e.g., if only two numbers exist with equal frequency)
    # In the provided examples, foreground is always different and less frequent.
    # If counts were equal, the logic might need refinement based on tie-breaking rules.
    # However, based on examples, we assume a distinct least frequent element exists.
    
    # A specific refinement for the provided examples: If 0 is present and not the most frequent, it's often the foreground.
    # Let's stick to the general min/max frequency rule derived.
    
    # Alternative approach: Find the minimum count > 0
    min_count = float('inf')
    foreground_num = None
    for num, count in counts.items():
        if 0 < count < min_count:
            min_count = count
            foreground_num = num
        # Handle tie-breaking if necessary (e.g., prefer 0 if counts are equal)
        # Based on examples, no complex tie-breaking seems needed.

    # Re-find background using max count
    max_count = 0
    background_num = None
    for num, count in counts.items():
        if count > max_count:
            max_count = count
            background_num = num
            
    # Handle edge case again if all counts are equal after filtering
    if foreground_num is None:
         # This happens if all elements are the same OR if multiple elements share the same minimum count.
         # If all are same, background is correct. If counts tie, need a rule. Let's default to the first found min.
         if len(counts) > 0:
              foreground_num = sorted(counts.items(), key=lambda item: item[1])[0][0]
              if background_num == foreground_num and len(counts) > 1: # If min and max are same but more than one number exists
                  # This implies equal distribution. Default foreground to something predictable?
                  # Or stick to the first minimum found.
                  pass # Let the initial sort decide

    # Ensure background and foreground aren't accidentally the same if multiple numbers exist
    if len(counts) > 1 and background_num == foreground_num:
         # This implies counts were equal or only one number type exists.
         # If counts were equal (e.g., 6 of A, 6 of B), which is foreground?
         # Examples suggest one number is clearly dominant.
         # Let's refine: Find max count first. Then find min count != max count.
         counts_list = counts.most_common()
         background_num = counts_list[0][0]
         if len(counts_list) > 1:
             # Find the least frequent among the rest
             foreground_num = min([item for item in counts_list if item[0] != background_num], key=lambda x: x[1])[0]
         else:
             foreground_num = background_num # Only one number type

    return background_num, foreground_num

def transform(input_grid):
    """
    Applies the transformation rule to the input grid (sequence).
    """
    sequence_length = len(input_grid)
    if sequence_length == 0:
        return []

    # 1. & 2. Identify background and foreground numbers
    background_num, foreground_num = find_foreground_background(input_grid)

    # Handle case where input is uniform
    if background_num == foreground_num:
        return list(input_grid) # No change needed if only one number type

    # 3. Initialize output sequence with the background number
    output_grid = [background_num] * sequence_length

    # 4. Iterate through input and relocate foreground numbers
    shift_amount = 4
    for i in range(sequence_length):
        # 5. Check if the current element is the foreground number
        if input_grid[i] == foreground_num:
            # 6a. Calculate the new index with wrap-around (modulo)
            new_index = (i + shift_amount) % sequence_length
            # 6b. Place the foreground number at the new index in the output
            output_grid[new_index] = foreground_num

    # 7. Return the transformed sequence
    return output_grid
