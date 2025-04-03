# Using the locally tested transform_row function from the thought block
train_1_in = [[0, 0, 4, 4, 4, 0, 0, 3, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
train_1_out_expected = [[0, 0, 4, 4, 4, 0, 3, 3, 3, 0, 0, 0, 8, 8, 8, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
train_2_in = [[0, 5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
train_2_out_expected = [[0, 5, 5, 5, 0, 0, 0, 5, 5, 5, 0, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
train_3_in = [[0, 0, 2, 2, 2, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
train_3_out_expected = [[0, 0, 2, 2, 2, 0, 0, 0, 5, 5, 5, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# Note: Using the full transform function structure for metrics
import copy

def _find_isolated_pixels(input_row):
    isolated_pixels_info = []
    row_len = len(input_row)
    for i in range(1, row_len - 1):
        current_color = input_row[i]
        if current_color == 0: continue
        left_color = input_row[i - 1]
        right_color = input_row[i + 1]
        if left_color != current_color and right_color != current_color:
            isolated_pixels_info.append((i, current_color))
    return isolated_pixels_info

def transform(input_grid):
    if not input_grid or not input_grid[0]: return [[]] # Handle empty grid/row
    input_row = input_grid[0]
    row_len = len(input_row)
    if row_len == 0: return [[]]
    output_row = copy.deepcopy(input_row)
    isolated_pixels = _find_isolated_pixels(input_row)
    for index, color in isolated_pixels:
        if index - 1 >= 0: output_row[index - 1] = color
        output_row[index] = color
        if index + 1 < row_len: output_row[index + 1] = color
    return [output_row]

print("--- Example 1 ---")
isolated_1 = _find_isolated_pixels(train_1_in[0])
output_1 = transform(train_1_in)
print(f"Input Size: 1x{len(train_1_in[0])}")
print(f"Isolated Pixels Found (Index, Color): {isolated_1}")
print(f"Output Matches Expected: {output_1 == train_1_out_expected}")

print("\n--- Example 2 ---")
isolated_2 = _find_isolated_pixels(train_2_in[0])
output_2 = transform(train_2_in)
print(f"Input Size: 1x{len(train_2_in[0])}")
print(f"Isolated Pixels Found (Index, Color): {isolated_2}")
print(f"Output Matches Expected: {output_2 == train_2_out_expected}")

print("\n--- Example 3 ---")
isolated_3 = _find_isolated_pixels(train_3_in[0])
output_3 = transform(train_3_in)
print(f"Input Size: 1x{len(train_3_in[0])}")
print(f"Isolated Pixels Found (Index, Color): {isolated_3}")
print(f"Output Matches Expected: {output_3 == train_3_out_expected}")
