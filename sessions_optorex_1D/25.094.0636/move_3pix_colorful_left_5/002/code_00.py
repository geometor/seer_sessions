import numpy as np

def analyze_example(input_str, output_str):
    # Ensure input_str and output_str are treated as strings
    input_str = str(input_str)
    output_str = str(output_str)
    
    input_arr = np.array([int(x) for x in input_str.split()])
    output_arr = np.array([int(x) for x in output_str.split()])
    n = len(input_arr)
    
    non_zero_indices = np.nonzero(input_arr)[0]
    
    if len(non_zero_indices) == 0:
        start_index = -1
        end_index = -1
        segment = np.array([])
        segment_len = 0
        original_segment_str = "N/A (all zeros)"
    else:
        start_index = non_zero_indices[0]
        end_index = non_zero_indices[-1]
        segment = input_arr[start_index : end_index + 1]
        segment_len = len(segment)
        original_segment_str = " ".join(map(str, segment))

    target_start_index = max(0, start_index - 3) if start_index != -1 else 0
    
    # Reconstruct the expected output based on the rule
    reconstructed_output = np.zeros(n, dtype=int)
    if start_index != -1:
         # Calculate the actual end placement index, respecting array bounds
        place_len = min(segment_len, n - target_start_index)
        # Ensure segment slicing matches place_len
        reconstructed_output[target_start_index : target_start_index + place_len] = segment[:place_len]


    match = np.array_equal(reconstructed_output, output_arr)

    return {
        "input": input_str,
        "output": output_str,
        "length": n,
        "first_nz_idx": start_index,
        "last_nz_idx": end_index,
        "segment": original_segment_str,
        "segment_len": segment_len,
        "target_start_idx": target_start_index,
        "reconstructed_output": " ".join(map(str, reconstructed_output.tolist())), # Convert to list then string
        "output_matches_reconstruction": match
    }

examples = [
    ("0 0 0 0 0 0 0 1 2 3 7 0", "0 0 0 0 1 2 3 7 0 0 0 0"),
    ("0 0 0 1 3 9 4 6 6 9 0 0", "1 3 9 4 6 6 9 0 0 0 0 0"),
    ("0 0 0 1 3 3 2 7 8 3 4 0", "1 3 3 2 7 8 3 4 0 0 0 0"),
    ("0 0 0 4 3 2 2 6 3 0 0 0", "4 3 2 2 6 3 0 0 0 0 0 0"),
    ("0 0 0 0 0 3 5 5 0 0 0 0", "0 0 3 5 5 0 0 0 0 0 0 0"),
    ("0 0 0 0 0 0 4 9 9 0 0 0", "0 0 0 4 9 9 0 0 0 0 0 0"),
    ("0 0 0 0 0 9 5 2 7 8 2 0", "0 0 9 5 2 7 8 2 0 0 0 0"),
    # Add a hypothetical all-zero case
    ("0 0 0 0 0 0 0 0 0 0 0 0", "0 0 0 0 0 0 0 0 0 0 0 0"),
    # Add a hypothetical case where shift goes past index 0
    ("1 2 3 0 0 0 0 0 0 0 0 0", "1 2 3 0 0 0 0 0 0 0 0 0"),
]

analysis_results = [analyze_example(inp, outp) for inp, outp in examples]

# Pretty print the results
import json
print(json.dumps(analysis_results, indent=2))