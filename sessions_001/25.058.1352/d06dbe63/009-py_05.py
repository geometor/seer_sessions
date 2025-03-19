import numpy as np

def analyze_examples(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        seed_row, seed_col = -1, -1
        for r in range(input_grid.shape[0]):
            for c in range(input_grid.shape[1]):
                if input_grid[r, c] == 8:
                    seed_row, seed_col = r, c
                    break
            if seed_row != -1:
                break

        results.append({
            'input_shape': input_grid.shape,
            'output_shape': output_grid.shape,
            'seed_location': (seed_row, seed_col),
            'seed_present_in_output': output_grid[seed_row,seed_col] == 8 if seed_row !=-1 else False
        })
    return results
task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 0, 8, 0, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 5, 0, 0], [0, 0, 0, 8, 0, 0], [0, 0, 0, 5, 0, 0], [0, 0, 0, 5, 0, 0]]
        }
    ]
}

results = analyze_examples(task)
for i, res in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input Shape: {res['input_shape']}")
    print(f"  Output Shape: {res['output_shape']}")
    print(f"  Seed Location: {res['seed_location']}")
    print(f"  Seed Present in Output: {res['seed_present_in_output']}")