# Code used for verification (results embedded below)
import numpy as np # Not strictly needed here, but good practice if array ops were considered

def verify_example(input_str, output_str, expected_length=12, shift_amount=3, padding_value=0):
    """Verifies a single input/output example against the shift logic."""
    try:
        input_list = [int(x) for x in input_str.strip().split()]
        output_list = [int(x) for x in output_str.strip().split()]
    except ValueError:
        print(f"Error parsing example: Input='{input_str}', Output='{output_str}'")
        return False, "Parsing Error"

    if len(input_list) != expected_length or len(output_list) != expected_length:
        print(f"Length mismatch: Input={len(input_list)}, Output={len(output_list)}, Expected={expected_length}")
        return False, "Length Mismatch"

    elements_to_keep_count = expected_length - shift_amount
    if elements_to_keep_count < 0: elements_to_keep_count = 0 # Handle edge case

    kept_elements = input_list[:elements_to_keep_count]
    padding_list = [padding_value] * shift_amount
    calculated_output = padding_list + kept_elements

    # Ensure calculated output also matches expected length (important if input was shorter)
    calculated_output = calculated_output[:expected_length]
    while len(calculated_output) < expected_length:
        calculated_output.append(padding_value) # Pad if necessary

    match = (calculated_output == output_list)
    details = f"Input: {input_list}, Expected Output: {output_list}, Calculated Output: {calculated_output}"
    # print(details) # Optional: print details for each example
    return match, details

# Example Data (first few examples)
examples = [
    ("6 5 0 0 0 0 0 0 0 0 0 0", "0 0 0 6 5 0 0 0 0 0 0 0"),
    ("0 0 9 1 5 0 0 0 0 0 0 0", "0 0 0 0 0 9 1 5 0 0 0 0"),
    ("0 0 0 2 6 5 3 9 9 0 0 0", "0 0 0 0 0 0 2 6 5 3 9 9"),
    ("6 4 9 1 8 6 4 9 0 0 0 0", "0 0 0 6 4 9 1 8 6 4 9 0"),
    ("0 0 0 0 0 2 3 3 1 0 0 0", "0 0 0 0 0 0 0 0 2 3 3 1"),
    ("0 0 0 6 1 8 8 1 0 0 0 0", "0 0 0 0 0 0 6 1 8 8 1 0"),
    ("7 2 7 8 1 5 5 0 0 0 0 0", "0 0 0 7 2 7 8 1 5 5 0 0"),
]

results = []
for i, (inp, outp) in enumerate(examples):
    match, details = verify_example(inp, outp)
    results.append({"Example": i+1, "Match": match}) # Removed details for brevity

print(results)
