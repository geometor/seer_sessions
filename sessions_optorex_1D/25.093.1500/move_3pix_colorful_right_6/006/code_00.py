# Code used for analysis (results shown in the 'code_output' block previously)
import numpy as np

def analyze_example(input_str, output_str):
    input_list = [int(x) for x in input_str.split()]
    output_list = [int(x) for x in output_str.split()]
    input_length = len(input_list)
    output_length = len(output_list)

    first_nz_index = None
    last_nz_index = None
    for i, val in enumerate(input_list):
        if val != 0:
            if first_nz_index is None: first_nz_index = i
            last_nz_index = i

    non_zero_block = []
    expected_output_start_index = None
    block_matches = False

    if first_nz_index is not None:
        non_zero_block = input_list[first_nz_index : last_nz_index + 1]
        expected_output_start_index = first_nz_index + 3
        if expected_output_start_index < output_length:
             len_to_check = min(len(non_zero_block), output_length - expected_output_start_index)
             if len_to_check > 0 and output_list[expected_output_start_index : expected_output_start_index + len_to_check] == non_zero_block[:len_to_check]:
                 is_zero_before = all(v == 0 for v in output_list[:expected_output_start_index])
                 is_zero_after = all(v == 0 for v in output_list[expected_output_start_index + len_to_check:])
                 block_matches = is_zero_before and is_zero_after
    else: # Handle all zeros input
        block_matches = all(v == 0 for v in output_list)

    return {
        "input_length": input_length, "output_length": output_length,
        "first_nz_index": first_nz_index, "last_nz_index": last_nz_index,
        "non_zero_block": non_zero_block, "expected_output_start_index": expected_output_start_index,
        "shift_rule_applies": block_matches
    }

examples = [
    {"input": "0 0 1 0 0 0 0 0 0 0 0 0", "output": "0 0 0 0 0 1 0 0 0 0 0 0"},
    {"input": "7 4 0 0 0 0 0 0 0 0 0 0", "output": "0 0 0 7 4 0 0 0 0 0 0 0"},
    {"input": "0 2 2 0 0 0 0 0 0 0 0 0", "output": "0 0 0 0 2 2 0 0 0 0 0 0"},
    {"input": "0 0 4 5 0 0 0 0 0 0 0 0", "output": "0 0 0 0 0 4 5 0 0 0 0 0"},
    {"input": "0 1 5 9 9 3 4 8 9 0 0 0", "output": "0 0 0 0 1 5 9 9 3 4 8 9"},
    {"input": "0 7 7 3 4 4 1 2 0 0 0 0", "output": "0 0 0 0 7 7 3 4 4 1 2 0"},
    {"input": "0 0 0 0 0 0 8 6 6 0 0 0", "output": "0 0 0 0 0 0 0 0 0 8 6 6"},
    {"input": "0 0 8 3 2 5 5 2 3 0 0 0", "output": "0 0 0 0 0 8 3 2 5 5 2 3"}, # Test example
]
analysis_results = [analyze_example(ex["input"], ex["output"]) for ex in examples]
# print(analysis_results) # Output shown previously