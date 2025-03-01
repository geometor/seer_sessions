def get_bounding_box(grid):
    # input is list of lists
    # Find min and max row/col for non-zero pixels
    rows = []
    cols = []
    for r_idx, row in enumerate(grid):
        for c_idx, pixel in enumerate(row):
            if pixel != 0:  # we only consider non-background cells
                rows.append(r_idx)
                cols.append(c_idx)
    if not rows:  # empty
        return (0,0,0,0)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return (min_row, min_col, max_row, max_col)

task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 7, 7, 0, 0, 0], [0, 0, 0, 0, 7, 2, 7, 0, 0, 0], [0, 0, 0, 0, 7, 7, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[7, 7, 7], [7, 2, 7], [7, 7, 7]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 2, 2, 7, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[7, 7, 7, 7], [7, 2, 2, 7], [7, 7, 7, 7]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 2, 7, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[7, 7, 7], [7, 2, 7], [7, 7, 7]]
        },

    ],
    "test": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 7, 7, 7, 7, 0, 0], [0, 0, 0, 0, 7, 7, 2, 7, 7, 0, 0], [0, 0, 0, 0, 7, 7, 7, 7, 7, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[7, 7, 7, 7, 7], [7, 7, 2, 7, 7], [7, 7, 7, 7, 7]]
        }
    ]
}

def analyze_examples(task):
    results = []
    for example in task['train']:
        input_grid = example['input']
        output_grid = example['output']

        # Find target object in input
        target_object = find_target_object(np.array(input_grid))
        target_coords = np.array(target_object)

        if target_coords.size > 0:
          in_min_row, in_min_col = np.min(target_coords, axis=0)
          in_max_row, in_max_col = np.max(target_coords, axis=0)
          in_height = in_max_row - in_min_row + 1
          in_width = in_max_col - in_min_col + 1
        else:
          # handle no target object
          in_min_row, in_min_col, in_max_row, in_max_col, in_height, in_width = (0,0,0,0,0,0)

        # output grid metrics
        out_height = len(output_grid)
        out_width = len(output_grid[0])
        
        results.append({
            'input_bounds': (in_min_row, in_min_col, in_max_row, in_max_col),
            'input_dims': (in_height, in_width),
            'output_dims': (out_height, out_width),
        })
    return results
        

results = analyze_examples(task)
for i, r in enumerate(results):
    print (f"Example {i+1}:")
    print (f"  Target Object Bounding Box (min_row, min_col, max_row, max_col): {r['input_bounds']}")
    print (f"  Target Object Dimensions (height, width): {r['input_dims']}")
    print (f"  Output Dimensions (height, width): {r['output_dims']}")