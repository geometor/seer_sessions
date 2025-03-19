import numpy as np

def get_grid_dimensions(grid_str):
    rows = grid_str.strip().split('\n')
    return len(rows), len(rows[0].split())

def analyze_examples(task_data):
    results = []
    for example in task_data['train']:
        input_dims = get_grid_dimensions(example['input'])
        output_dims = get_grid_dimensions(example['output'])

        # convert to grids
        input_grid = np.array([[int(c) for c in row.split()] for row in example['input'].strip().split('\n')])
        output_grid = np.array([[int(c) for c in row.split()] for row in example['output'].strip().split('\n')])        

        #check initial rule
        initial_rule_holds = True

        # Iterate through the input grid
        for i in range(input_grid.shape[0]):
          for j in range(input_grid.shape[1]):
            pixel_value = input_grid[i,j]

            # if non-zero, check 5x5
            if pixel_value != 0:
                row_start = i * 5
                col_start = j * 5
                
                # Check bounds for 5x5 block
                if row_start + 5 <= output_grid.shape[0] and col_start + 5 <= output_grid.shape[1]:
                    block = output_grid[row_start:row_start + 5, col_start:col_start + 5]
                    if not np.all(block == pixel_value):
                        initial_rule_holds = False
                        break
                else:
                    initial_rule_holds = False
                    break

          if not initial_rule_holds:
              break

        results.append({
            'input_dims': input_dims,
            'output_dims': output_dims,
            'initial_rule_holds': initial_rule_holds
        })
    return results

# task data
task_data = {
    "train": [
        {
            "input": "0 0 0\n0 1 0\n0 0 0",
            "output": "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 1 1 1 1 1 0 0 0 0 0\n0 0 0 0 0 1 1 1 1 1 0 0 0 0 0\n0 0 0 0 0 1 1 1 1 1 0 0 0 0 0\n0 0 0 0 0 1 1 1 1 1 0 0 0 0 0\n0 0 0 0 0 1 1 1 1 1 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
        },
        {
            "input": "0 0 0\n0 2 0\n0 0 0",
            "output": "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 2 2 2 2 2 0 0 0 0 0\n0 0 0 0 0 2 2 2 2 2 0 0 0 0 0\n0 0 0 0 0 2 2 2 2 2 0 0 0 0 0\n0 0 0 0 0 2 2 2 2 2 0 0 0 0 0\n0 0 0 0 0 2 2 2 2 2 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
        },
		{
            "input": "7 0 0\n0 0 0\n0 0 0",
            "output": "7 7 7 7 7 0 0 0 0 0 0 0 0 0 0\n7 7 7 7 7 0 0 0 0 0 0 0 0 0 0\n7 7 7 7 7 0 0 0 0 0 0 0 0 0 0\n7 7 7 7 7 0 0 0 0 0 0 0 0 0 0\n7 7 7 7 7 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
        },
        {
            "input": "0 0 0\n0 0 0\n0 0 5",
            "output": "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n5 5 5 5 5 5 5 5 5 5 5 5 5 5 5"
        }
    ]
}

results = analyze_examples(task_data)
print(results)