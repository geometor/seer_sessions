import numpy as np

def analyze_examples(task_data):
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        rows, cols = input_grid.shape

        # Analyze row 2 colors
        row2_colors = np.unique(input_grid[2]).tolist()

        # Analyze last row changes
        last_row_changes = []
        for c in range(cols):
            if input_grid[rows-1, c] != output_grid[rows-1, c]:
                last_row_changes.append((c, output_grid[rows-1, c]))

        results.append({
            'row2_colors': row2_colors,
            'last_row_changes': last_row_changes
        })
    return results
task_data = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 8, 0, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 8, 0, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 4, 0, 4, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 6, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 6, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 4, 4, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 4, 0, 0]],
        },
                {
            "input": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [1, 6, 8, 0, 0, 3, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [1, 6, 8, 0, 0, 3, 0], [0, 0, 0, 0, 0, 0, 0], [0, 4, 4, 0, 0, 0, 0]],
        }

    ]
}

results = analyze_examples(task_data)
print(results)