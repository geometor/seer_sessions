def describe_grid(grid):
    """Provides a basic description of a grid."""
    grid = np.array(grid)
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    return {
        'shape': (rows, cols),
        'unique_colors': unique_colors.tolist()
    }


task_data = {
    "train": [
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 5, 5, 5, 0, 0, 0, 0, 0, 0],
                [0, 5, 5, 5, 0, 0, 0, 0, 0, 0],
                [0, 5, 5, 5, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 0, 0, 0],
                [0, 5, 5, 5],
                [0, 5, 5, 5],
                [0, 5, 5, 5],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ]
        },
       {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 8, 8, 8, 0, 0],
                [0, 0, 0, 0, 0, 8, 8, 8, 0, 0],
                [0, 0, 0, 0, 0, 8, 8, 8, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ]
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 7, 0, 0, 0, 0, 0, 0, 0],
                [0, 7, 7, 7, 0, 0, 0, 0, 0, 0],
                [0, 0, 7, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 0, 0, 0],
                [0, 0, 7, 0],
                [0, 7, 7, 7],
                [0, 0, 7, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ]
        }

    ]
}

for i, example in enumerate(task_data['train']):
    input_grid = example['input']
    output_grid = example['output']
    predicted_output = transform(input_grid)
    print(f"Example {i+1}:")
    print(f"  Input Description: {describe_grid(input_grid)}")
    print(f"  Output Description: {describe_grid(output_grid)}")
    print(f"  Predicted Output Description: {describe_grid(predicted_output)}")
    print(f"  Correct: {np.array_equal(output_grid, predicted_output)}")
    print("-" * 20)
