def apply_revised_logic(sequence):
    n = len(sequence)
    target_i = -1
    # 1. Find the first index i where seq[i] == 0 and seq[i+1] != 0
    for i in range(n - 1):
        if sequence[i] == 0 and sequence[i+1] != 0:
            target_i = i
            break

    # If no such pattern found, return original sequence
    if target_i == -1:
        return list(sequence) # Return a copy

    # 2. Identify preceding non-zero block (if any)
    if target_i == 0 or sequence[target_i - 1] == 0:
        # No non-zero block immediately preceding, or already at start
        return list(sequence) # Return a copy

    # Find start index 'j' of the non-zero block ending at target_i - 1
    j = target_i - 1
    while j > 0 and sequence[j - 1] != 0:
        j -= 1

    # 3. Perform the move/shift
    output_sequence = list(sequence)
    zero_to_move = output_sequence.pop(target_i) # Remove the 0 at target_i
    output_sequence.insert(j, zero_to_move)    # Insert it at index j

    return output_sequence

def format_seq(seq):
    return " ".join(map(str, seq))

# Test cases
train_inputs = [
    [0, 3, 3, 3, 3, 3, 3, 3, 3, 2, 0, 0], # train_1
    [0, 0, 0, 0, 0, 6, 6, 2, 0, 0, 0, 0], # train_2
    [2, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0], # train_3
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 0], # train_4
    [0, 0, 0, 2, 4, 4, 4, 4, 4, 0, 0, 0], # train_5
    [0, 0, 0, 0, 0, 0, 9, 9, 9, 0, 0, 2], # train_6
    [4, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # train_7
]

expected_outputs = [
    "0 3 3 3 3 3 3 3 3 2 0 0", # train_1
    "0 0 0 0 0 6 6 2 0 0 0 0", # train_2
    "2 3 3 3 3 3 3 0 0 0 0 0", # train_3
    "5 5 5 5 5 5 5 5 5 5 2 0", # train_4
    "0 0 0 2 4 4 4 4 4 0 0 0", # train_5
    "0 0 0 0 0 0 0 9 9 9 0 2", # train_6 Corrected expected
    "0 4 2 0 0 0 0 0 0 0 0 0"  # train_7
]

results = []
for i, seq in enumerate(train_inputs):
    output_seq = apply_revised_logic(seq)
    output_str = format_seq(output_seq)
    results.append({
        "example": f"train_{i+1}",
        "input": format_seq(seq),
        "expected": expected_outputs[i],
        "actual_logic_output": output_str,
        "match": output_str == expected_outputs[i]
    })

print(results)
