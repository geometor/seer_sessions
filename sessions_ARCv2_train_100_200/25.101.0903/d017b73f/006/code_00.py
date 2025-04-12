import numpy as np
import json

def get_detailed_metrics(input_grid_list, expected_output_list):
    input_grid = np.array(input_grid_list)
    # Handle potentially empty expected output correctly
    if isinstance(expected_output_list, list) and len(expected_output_list) > 0 and isinstance(expected_output_list[0], list):
         out_h = len(expected_output_list)
         out_w = len(expected_output_list[0]) if out_h > 0 else 0
         expected_output_grid = np.array(expected_output_list) # Only create if valid
    else:
         out_h, out_w = 0, 0 # Assuming empty if not list of lists
         expected_output_grid = np.array([]) # Empty numpy array

    in_h, in_w = input_grid.shape if input_grid.ndim == 2 and input_grid.size > 0 else (0, 0)

    if in_h == 0 or in_w == 0:
        non_empty_cols_in = []
        empty_cols_in = list(range(in_w)) if in_w > 0 else []
    else:
        all_indices = set(range(in_w))
        non_empty_cols_in = [c for c in range(in_w) if not np.all(input_grid[:, c] == 0)]
        empty_cols_in = sorted(list(all_indices - set(non_empty_cols_in)))

    num_non_empty_in = len(non_empty_cols_in)

    # Map original non-empty indices to new indices
    col_mapping = {orig_idx: new_idx for new_idx, orig_idx in enumerate(non_empty_cols_in)}

    # Calculate required shifts (if possible)
    required_shifts = {}
    proposed_shifts = {}
    shift_comparison = {}

    H = in_h # Grid Height

    if H == out_h and num_non_empty_in == out_w and H > 0 and out_w > 0:
        for c_orig in non_empty_cols_in:
            c_new = col_mapping[c_orig]
            input_col = input_grid[:, c_orig]
            output_col = expected_output_grid[:, c_new]
            col_id = f"c={c_orig}->c_new={c_new}"

            # Find actual required shift
            found_shift = -1 # Indicate not found
            for s_test in range(H):
                 if np.array_equal(np.roll(input_col, s_test), output_col):
                     found_shift = s_test
                     break
            required_shifts[col_id] = found_shift if found_shift != -1 else "Mismatch"

            # Calculate proposed shift (rule S = c_new // H)
            proposed_s = c_new // H
            proposed_shifts[col_id] = proposed_s

            # Compare
            if found_shift != -1:
                 shift_comparison[col_id] = {
                     "required": found_shift,
                     "proposed_c_new_div_H": proposed_s,
                     "match": found_shift == proposed_s
                 }
            else:
                 shift_comparison[col_id] = {
                     "required": "Mismatch",
                     "proposed_c_new_div_H": proposed_s,
                     "match": False
                 }

    metrics = {
        "input_dims": f"{in_h}x{in_w}",
        "output_dims": f"{out_h}x{out_w}",
        "dims_match_expected": (in_h == out_h) and (num_non_empty_in == out_w),
        "non_empty_cols_count": num_non_empty_in,
        "original_non_empty_indices": non_empty_cols_in,
        "original_empty_indices": empty_cols_in,
        "col_mapping_c_to_c_new": col_mapping,
        "shift_analysis": shift_comparison
    }
    return metrics

# Example 1
input1 = [[0,0,0,0,0,0,8,0,0,0,0],[2,2,2,0,8,8,8,0,0,0,0],[0,0,2,0,0,0,0,0,6,6,6]]
output1 = [[0,0,0,0,0,0,0,0,0],[2,2,2,0,0,8,6,6,6],[0,0,2,8,8,8,0,0,0]]
# Example 2
input2 = [[0,0,0,3,3,0,0,1,0,2,2],[2,2,0,0,0,0,1,1,0,0,2],[0,2,0,0,0,0,0,0,0,0,0]]
output2 = [[0,0,0,0,0,0,0,0],[2,2,0,0,0,1,2,2],[0,2,3,3,1,1,0,2]]
# Example 3
input3 = [[0,1,1,0,0,0,0,0,2,2,0],[1,1,0,0,2,2,0,2,2,0,0],[0,0,0,0,0,2,0,0,0,0,0]]
output3 = [[0,1,1,2,2,0,2,2],[1,1,0,0,2,2,2,0],[0,0,0,0,0,0,0,0]]
# Example 4
input4 = [[0,2,0,0,0,0,0,0,0],[2,2,0,1,1,0,2,2,2],[0,0,0,0,1,0,0,0,0]]
output4 = [[0,2,1,1,0,0,0],[2,2,0,1,2,2,2],[0,0,0,0,0,0,0]]

metrics1 = get_detailed_metrics(input1, output1)
metrics2 = get_detailed_metrics(input2, output2)
metrics3 = get_detailed_metrics(input3, output3)
metrics4 = get_detailed_metrics(input4, output4)

print("Example 1 Metrics:\n", json.dumps(metrics1, indent=2))
print("\nExample 2 Metrics:\n", json.dumps(metrics2, indent=2))
print("\nExample 3 Metrics:\n", json.dumps(metrics3, indent=2))
print("\nExample 4 Metrics:\n", json.dumps(metrics4, indent=2))