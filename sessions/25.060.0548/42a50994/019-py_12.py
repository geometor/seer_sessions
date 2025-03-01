def analyze_results(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid)
        
        #check equality
        grids_equal = np.array_equal(output_grid, predicted_output)
        
        # diff grids
        diff_grid = None
        if not grids_equal:
            diff_grid = np.where(output_grid != predicted_output, output_grid, -1)
            # -1 means they're the same in that location, otherwise it is the value from the true output
        
        results.append({
            'input': input_grid.tolist(),
            'output': output_grid.tolist(),
            'predicted_output': predicted_output.tolist(),
            'grids_equal': grids_equal,
            'diff_grid': diff_grid.tolist() if diff_grid is not None else None
        })
    return results


task = {
    "train": [
        {
            "input": [[5, 5, 5, 5, 5, 0, 5, 5, 5]],
            "output": [[5, 0, 0, 0, 0, 0, 5, 0, 0]]
        },
        {
            "input": [[0, 5, 5, 5, 5, 5, 5, 5, 0]],
            "output": [[0, 5, 0, 0, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[5, 5, 5, 0, 5, 5, 5, 0, 5, 5]],
            "output": [[5, 0, 0, 0, 5, 0, 0, 0, 5, 0]]
        },
        {
          "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 5, 5, 0, 5, 5, 5, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 5, 5, 0, 5, 5, 5, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
          ],
          "output": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 0, 0, 0, 5, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 5, 0, 0, 5, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
          ]
        }
    ]
}

analysis = analyze_results(task)

for i, result in enumerate(analysis):
    print(f"Example {i+1}:")
    print(f"  Grids Equal: {result['grids_equal']}")
    if not result['grids_equal']:
        print(f"  Diff Grid:\n{result['diff_grid']}")