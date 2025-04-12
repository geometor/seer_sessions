import numpy as np

def analyze_example_pure_block(input_grid):
    grid_np = np.array(input_grid)
    metrics = {}
    input_width = grid_np.shape[1]
    metrics['input_width'] = input_width

    # Dominant Color
    unique_colors = np.unique(grid_np)
    non_white_colors = unique_colors[unique_colors != 0]
    if len(non_white_colors) == 0:
         metrics['dominant_color'] = None
         metrics['relevant_row_indices'] = []
         metrics['pure_column_indices'] = []
         metrics['pure_column_count'] = 0
         metrics['largest_pure_block_size'] = 0
         return metrics

    dominant_color = int(non_white_colors[0])
    metrics['dominant_color'] = dominant_color

    # Relevant Rows (contain dominant color)
    rows_with_color = np.any(grid_np == dominant_color, axis=1)
    relevant_row_indices = np.where(rows_with_color)[0]
    metrics['relevant_row_indices'] = relevant_row_indices.tolist()

    # Pure Columns (contain ONLY dominant color within RELEVANT rows)
    pure_column_indices = []
    if relevant_row_indices.size > 0: # Check if list is not empty
        num_cols = grid_np.shape[1]
        for j in range(num_cols):
            column_slice = grid_np[relevant_row_indices, j]
            # Check if ALL elements in this slice are the dominant color
            if np.all(column_slice == dominant_color):
                pure_column_indices.append(j)
    metrics['pure_column_indices'] = pure_column_indices
    metrics['pure_column_count'] = len(pure_column_indices)

    # Find largest contiguous block of pure columns
    max_len = 0
    current_len = 0
    last_idx = -2 # Start with a value that ensures the first index starts a new block
    pure_column_indices.sort() # Ensure indices are sorted
    if not pure_column_indices: # Handle case with no pure columns
        max_len = 0
    else:
        for idx in pure_column_indices:
            if idx == last_idx + 1:
                # This index is contiguous with the previous one
                current_len += 1
            else:
                # Non-contiguous index, start a new block
                max_len = max(max_len, current_len) # Record the length of the previous block
                current_len = 1 # Start new block of length 1
            last_idx = idx
        max_len = max(max_len, current_len) # Record the length of the last block

    metrics['largest_pure_block_size'] = max_len

    return metrics

# Example Data
train_1_input = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[0,2,2,2,2,2,0,0,0,0,0,0,0,0,0],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[0,2,2,2,2,2,0,0,0,0,0,0,0,0,0],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
train_2_input = [[0,0,0,0,0,0],[6,6,6,6,6,6],[0,0,0,0,0,0],[6,6,6,6,6,6],[0,6,6,6,6,0],[6,6,6,6,6,6],[0,6,6,6,6,0],[6,6,6,6,6,6],[0,0,0,0,0,0],[6,6,6,6,6,6],[0,0,0,0,0,0],[6,6,6,6,6,6],[0,0,0,0,0,0],[6,6,6,6,6,6]]
train_3_input = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],[0,0,0,0,0,0,0,0,0,0,0,4,4,4,0,0],[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]]

metrics_1 = analyze_example_pure_block(train_1_input)
metrics_2 = analyze_example_pure_block(train_2_input)
metrics_3 = analyze_example_pure_block(train_3_input)

metrics_1['expected_size'] = 5
metrics_2['expected_size'] = 5
metrics_3['expected_size'] = 3

print("--- Metrics Example 1 ---")
print(metrics_1)
print("--- Metrics Example 2 ---")
print(metrics_2)
print("--- Metrics Example 3 ---")
print(metrics_3)