import numpy as np

def analyze_example(name, input_grid, output_grid):
    input_row = np.array(input_grid, dtype=int).flatten() # Ensure 1D
    output_row = np.array(output_grid, dtype=int).flatten() # Ensure 1D

    input_len = len(input_row)
    output_len = len(output_row)

    # Find input block
    non_white_in = np.where(input_row != 0)[0]
    if len(non_white_in) == 0:
        in_color, in_start, in_block_len = None, -1, 0
    else:
        in_start = non_white_in[0]
        in_color = input_row[in_start]
        in_block_len = 0
        for i in range(in_start, input_len):
            if input_row[i] == in_color:
                in_block_len += 1
            else:
                break

    # Find output block
    non_white_out = np.where(output_row != 0)[0]
    if len(non_white_out) == 0:
        out_color, out_start, out_block_len = None, -1, 0
    else:
        out_start = non_white_out[0]
        out_color = output_row[out_start]
        out_block_len = 0
        for i in range(out_start, output_len):
            if output_row[i] == out_color:
                out_block_len += 1
            else:
                break

    shift = -1
    if in_start != -1 and out_start != -1:
        shift = out_start - in_start

    in_end_index = in_start + in_block_len -1 if in_start != -1 else -1
    # Calculate hypothetical new end index based on refined rules
    hyp_out_start = in_start + 3
    hyp_out_block_len = in_block_len - 1 if in_start == 0 else in_block_len
    hyp_out_end_index = hyp_out_start + hyp_out_block_len - 1

    # Check condition for output length reduction
    len_reduction_cond = hyp_out_end_index < (input_len - 2) if in_start != -1 else False

    return {
        "Example": name,
        "Input Len": input_len,
        "Output Len": output_len,
        "Grid Len Diff": output_len - input_len,
        "Input Block Start": int(in_start) if in_start != -1 else -1,
        "Input Block Len": int(in_block_len) if in_block_len > 0 else 0,
        "Output Block Start": int(out_start) if out_start != -1 else -1,
        "Output Block Len": int(out_block_len) if out_block_len > 0 else 0,
        "Block Len Diff": out_block_len - in_block_len if in_block_len > 0 else 0,
        "Shift": int(shift),
        "Block Start@0": in_start == 0,
        "Hypothetical Output End Index": hyp_out_end_index if in_start != -1 else -1,
        "Output Len Reduced? (Hypothesis: End < InLen-2)": len_reduction_cond
    }

# Example 1 Data
input1 = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]
output1 = [0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0]

# Example 2 Data
input2 = [0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
output2 = [0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Example 3 Data
input3 = [0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0]
output3 = [0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0]


analysis1 = analyze_example("Train 1", input1, output1)
analysis2 = analyze_example("Train 2", input2, output2)
analysis3 = analyze_example("Train 3", input3, output3)

print(analysis1)
print(analysis2)
print(analysis3)