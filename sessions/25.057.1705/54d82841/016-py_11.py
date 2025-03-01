import numpy as np

def get_column_colors(grid, col_index):
    """Returns a sorted list of unique colors in a given column."""
    return sorted(list(np.unique(grid[:, col_index])))

def transform(grid):
    """
    Current working transformation - duplicates colors from each input column to the
    corresponding output column and appends a row of 'yellow' (4) pixels
    """
    output_grid = np.copy(grid).tolist()
    output_grid.append([4] * grid.shape[1])  # Append a row of 4s
    return np.array(output_grid)

def analyze_examples(task_data):
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid)
        correct = np.array_equal(predicted_output, output_grid)

        print(f"Example: {example.get('id', 'N/A')}")
        print(f"Input shape: {input_grid.shape}")
        print(f"Output shape: {output_grid.shape}")
        print(f"Predicted output correct?: {correct}")

        for col_index in range(input_grid.shape[1]):
            column_colors = get_column_colors(input_grid, col_index)
            output_pixel = output_grid[-1, col_index] if output_grid.shape[0] > input_grid.shape[0] else "N/A"
            print(f"  Column {col_index}: Colors = {column_colors}, Output Pixel = {output_pixel}")
        print("-" * 20)
    # analyze the test example separately
    for example in task_data['test']:
       input_grid = np.array(example['input'])
       output_grid = np.array(example['output'])
       predicted_output = transform(input_grid)
       correct = np.array_equal(predicted_output, output_grid)

       print(f"Example: test")
       print(f"Input shape: {input_grid.shape}")
       print(f"Output shape: {output_grid.shape}")
       print(f"Predicted output correct?: {correct}")
task_data = {
    "train": [
        {
            "input": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            "output": [[0, 0, 0], [0, 0, 0], [0, 0, 0], [4, 4, 4]],
            "id": "train_0",
        },
        {
            "input": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            "output": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [4, 4, 4, 4]],
            "id": "train_1",
        },
        {
            "input": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 8, 0, 0]],
            "output": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 8, 0, 0], [0, 4, 4, 4]],
            "id": "train_2",
        },
    ],
    "test": [{"input": [[0, 0, 0], [0, 0, 0], [0, 0, 0]], "output": [[0, 0, 0], [0, 0, 0], [0, 0, 0], [4, 4, 4]]}],
}

analyze_examples(task_data)