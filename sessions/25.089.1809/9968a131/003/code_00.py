import numpy as np
from typing import List, Tuple, Optional

"""
Transformation Rule Description:

1.  **Rule Identification:** Analyze the first provided training input/output pair to identify a specific 3-pixel horizontal sequence (A, B, C) in the input that transforms into its right cyclic shift (C, A, B) in the output. Find the first such occurrence. This (ABC -> CAB) pair defines the transformation rule for the task.
2.  **Rule Application:** For a given test input grid:
    a. Create a copy of the test input grid.
    b. Iterate through each row of the original test input grid.
    c. Scan each row from left to right, checking for non-overlapping occurrences of the identified input sequence (ABC).
    d. When an occurrence of ABC is found starting at a certain position, replace the corresponding three pixels in the copied grid with the identified output sequence (CAB).
    e. Advance the scan position by 3 after a replacement, or by 1 if no match was found at the current position.
    f. Pixels not part of a replaced sequence remain unchanged in the copied grid.
3.  **Output:** Return the modified copied grid.
"""

def find_transformation_rule(train_input: np.ndarray, train_output: np.ndarray) -> Optional[Tuple[Tuple[int, ...], Tuple[int, ...]]]:
    """
    Finds the first differing 3-element horizontal sequence and its transformed version.
    Assumes the transformation is a right cyclic shift (ABC -> CAB).

    Args:
        train_input: The input grid from the training example (numpy array).
        train_output: The output grid from the training example (numpy array).

    Returns:
        A tuple containing (input_sequence_ABC, output_sequence_CAB), or None if no such rule is found.
    """
    height, width = train_input.shape
    if width < 3:
        # Cannot find a 3-element sequence if width is less than 3
        return None

    for r in range(height):
        for c in range(width - 2):
            input_seq = tuple(train_input[r, c:c+3])
            output_seq = tuple(train_output[r, c:c+3])

            # Check if sequences differ
            if input_seq != output_seq:
                # Verify if it's the specific cyclic shift ABC -> CAB
                # expected_output_seq = (input_seq[-1],) + input_seq[:-1] # Left shift
                expected_output_seq = (input_seq[2], input_seq[0], input_seq[1]) # Right shift CAB

                if output_seq == expected_output_seq:
                    # Found the rule
                    return input_seq, output_seq
                else:
                    # Found a difference, but it doesn't match the expected cyclic shift pattern.
                    # This might indicate a different rule or noise.
                    # Continue searching for the *first* match that fits the pattern.
                    pass

    # No matching transformation rule found in the examples
    return None

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the learned transformation rule (replace ABC with CAB) to the input grid.
    The rule (ABC -> CAB) is determined by analyzing the first training example.
    """
    input_arr = np.array(input_grid, dtype=int)
    output_arr = np.copy(input_arr) # Initialize output_grid as a copy
    height, width = input_arr.shape

    # --- Determine the Rule using the First Training Example ---
    # In a real ARC scenario, the training examples are provided alongside the test input.
    # We simulate this by defining the first training pair here.
    train1_in_data = [[7, 3, 8, 7], [7, 8, 3, 7], [7, 3, 8, 7], [7, 8, 3, 7]]
    train1_out_data = [[7, 3, 8, 7], [7, 7, 8, 3], [7, 3, 8, 7], [7, 7, 8, 3]]
    train1_in_arr = np.array(train1_in_data, dtype=int)
    train1_out_arr = np.array(train1_out_data, dtype=int)

    transformation_rule = find_transformation_rule(train1_in_arr, train1_out_arr)

    # If no rule was found, return the original grid
    if transformation_rule is None:
        # print("Warning: No suitable transformation rule (ABC -> CAB) found in the reference training example. Returning input grid unchanged.")
        return input_grid
        
    sequence_to_find, replacement_sequence = transformation_rule
    # print(f"Applying rule: {sequence_to_find} -> {replacement_sequence}") # Optional debug print

    # --- Apply the Transformation to the input_grid ---
    # Iterate through each row
    for r in range(height):
        c = 0  # Start scanning from the beginning of the row
        while c <= width - 3:  # Ensure there's space for a 3-pixel sequence
            # Check if the current 3-pixel sequence in the *original* input matches the one to find
            current_sequence = tuple(input_arr[r, c:c+3])

            if current_sequence == sequence_to_find:
                # If it matches, replace the corresponding sequence in the output array
                output_arr[r, c:c+3] = replacement_sequence
                # Advance the column index by 3 to avoid overlapping matches
                c += 3
            else:
                # If it doesn't match, advance the column index by 1
                c += 1

    # Convert the result back to a list of lists
    return output_arr.tolist()