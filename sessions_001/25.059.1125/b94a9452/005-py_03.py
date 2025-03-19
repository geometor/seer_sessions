import numpy as np

def get_bounding_box(grid):
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:  # Handle empty grid case
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # 1. Identify the Region of Interest (ROI)
    bounding_box = get_bounding_box(input_grid)
    if bounding_box is None:  # If no non-zero pixels
        return []

    min_row, max_row, min_col, max_col = bounding_box

    # 2. Extract the ROI
    roi = input_grid[min_row:max_row+1, min_col:max_col+1]

    # 3. Invert (Transpose in this case since the shapes are square)
    output_grid = roi.T

    return output_grid.tolist()

def analyze_example(example):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    predicted_output = np.array(transform(example['input']))

    bounding_box = get_bounding_box(input_grid)
    if bounding_box:
        min_row, max_row, min_col, max_col = bounding_box
        extracted_region_shape = (max_row - min_row + 1, max_col - min_col + 1)
    else:
        extracted_region_shape = (0, 0)

    is_correct = np.array_equal(predicted_output, output_grid)

    print(f"  - Bounding Box: {bounding_box}")
    print(f"  - Extracted Region Shape: {extracted_region_shape}")
    print(f"  - Predicted Output Correct: {is_correct}")
    print(f"  - Output shape: {output_grid.shape}")
    if not is_correct:
        print(f"  - predicted != output: {not np.array_equal(output_grid, predicted_output)}")

    return bounding_box, extracted_region_shape, is_correct

task_examples = [
    {'input': [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]], 'output': [[1]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[1, 1, 1], [1, 1, 1]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[1], [1], [1], [1]]}
]
print("Example Analysis:")
for i, example in enumerate(task_examples):
    print(f"Example {i}:")
    analyze_example(example)
