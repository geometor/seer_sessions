import numpy as np

def analyze_example(input_grid_list, output_grid_list):
    input_grid = np.array(input_grid_list)
    output_grid = np.array(output_grid_list)

    if input_grid.ndim != 2 or input_grid.shape[0] != 1: return {"error": "Input is not a 1xN grid"}
    if output_grid.ndim != 2 or output_grid.shape[0] != 1: return {"error": "Output is not a 1xN grid"}

    input_row = input_grid[0]
    output_row = output_grid[0]
    width = input_row.shape[0]

    pattern_count = 0
    pattern_indices = []
    for i in range(1, width - 1):
        if input_row[i] > 0 and input_row[i-1] == 0 and input_row[i+1] == 0:
            pattern_count += 1
            pattern_indices.append(i)

    diff_count = np.sum(input_row != output_row)
    # Each pattern 0 C 0 -> C C C changes the two outer 0s.
    expected_changed_pixels = pattern_count * 2

    return {
        "input_shape": input_grid.shape,
        "output_shape": output_grid.shape,
        "isolated_pixel_pattern_count": pattern_count,
        "isolated_pixel_indices": pattern_indices,
        "changed_pixels_count": diff_count,
        "expected_changed_pixels": expected_changed_pixels,
        "match": diff_count == expected_changed_pixels
    }

# Example Data
train1_in = [[0, 4, 4, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
train1_out = [[0, 4, 4, 4, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
train2_in = [[0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
train2_out = [[0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
train3_in = [[0, 0, 8, 8, 8, 0, 0, 0, 0, 8, 0, 0, 0, 8, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
train3_out = [[0, 0, 8, 8, 8, 0, 0, 0, 8, 8, 8, 0, 8, 8, 8, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

results = {
    "train_1": analyze_example(train1_in, train1_out),
    "train_2": analyze_example(train2_in, train2_out),
    "train_3": analyze_example(train3_in, train3_out),
}

print(results)
# Output from execution:
# {'train_1': {'input_shape': (1, 33), 'output_shape': (1, 33), 'isolated_pixel_pattern_count': 1, 'isolated_pixel_indices': [6], 'changed_pixels_count': np.int64(2), 'expected_changed_pixels': 2, 'match': True}, 'train_2': {'input_shape': (1, 33), 'output_shape': (1, 33), 'isolated_pixel_pattern_count': 2, 'isolated_pixel_indices': [8, 12], 'changed_pixels_count': np.int64(4), 'expected_changed_pixels': 4, 'match': True}, 'train_3': {'input_shape': (1, 33), 'output_shape': (1, 33), 'isolated_pixel_pattern_count': 3, 'isolated_pixel_indices': [9, 13, 19], 'changed_pixels_count': np.int64(6), 'expected_changed_pixels': 6, 'match': True}}
