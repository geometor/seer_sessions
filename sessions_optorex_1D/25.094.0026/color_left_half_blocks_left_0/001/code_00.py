import math

"""
Transforms a sequence of 0s and 2s based on contiguous runs of 2s.
Specifically, identifies runs of '2's that end either at the sequence boundary
or immediately before a '0'. For such runs, the last floor(L/2) elements
(where L is the length of the run) are changed from '2' to '8'.
Zeros remain unchanged.
"""

def find_runs_of_twos(sequence):
    """
    Identifies contiguous runs of the number 2 in the sequence.

    Args:
        sequence: A list of integers.

    Returns:
        A list of tuples, where each tuple represents a run
        (start_index, end_index, length).
    """
    runs = []
    n = len(sequence)
    i = 0
    while i < n:
        if sequence[i] == 2:
            start_index = i
            while i < n and sequence[i] == 2:
                i += 1
            end_index = i - 1
            length = end_index - start_index + 1
            runs.append((start_index, end_index, length))
        else:
            i += 1
    return runs

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: The input list of integers (0s and 2s).

    Returns:
        The transformed list of integers (0s, 2s, and 8s).
    """
    # 1. Initialize the output sequence as a copy of the input sequence.
    output_sequence = list(input_sequence)
    n = len(input_sequence)

    # 2. Identify all contiguous runs of the number '2'.
    runs = find_runs_of_twos(input_sequence)

    # 3. For each identified run of '2's:
    for start, end, length in runs:
        # a. Check the element immediately following the run.
        # b. Determine if the run terminates correctly.
        terminates_correctly = False
        if end == n - 1:  # Run ends at the last index
            terminates_correctly = True
        elif end + 1 < n and input_sequence[end + 1] == 0: # Element after run is 0
            terminates_correctly = True

        # c. If the run terminates correctly:
        if terminates_correctly:
            # i. Calculate the number of elements to change.
            num_changes = length // 2 # Equivalent to floor(length / 2)

            # ii. If num_changes > 0, change the specified '2's to '8's.
            if num_changes > 0:
                for i in range(end - num_changes + 1, end + 1):
                    output_sequence[i] = 8

    # 4. Return the modified output sequence.
    return output_sequence