def describe_grid(grid):
    """Provides a description of the grid, focusing on azure regions and other relevant colors."""
    grid = np.array(grid)
    azure_regions = find_regions(grid, 8)
    description = {
        "azure_regions": [],
        "rows_with_orange": [],
        "rows_with_magenta": []
    }
    for i, region in enumerate(azure_regions):
        rows = sorted(list(set([r for r, _ in region])))
        description["azure_regions"].append({
            "region_index": i,
            "rows": rows,
            "start_row": rows[0]
        })

    for row_index in range(grid.shape[0]):
      if 7 in grid[row_index,:]:
        description["rows_with_orange"].append(row_index)
      if 6 in grid[row_index,:]:
        description["rows_with_magenta"].append(row_index)

    return description

def analyze_results(task):
    results_summary = []
    for example in task['train']:

        input_grid = example['input']
        output_grid = example['output']
        predicted_output = transform(input_grid)

        input_description = describe_grid(input_grid)
        output_description = describe_grid(output_grid) #Might not be useful
        
        correct = np.array_equal(np.array(output_grid), predicted_output)

        results_summary.append(
            {
                'correct' : correct,
                'input' : input_description,
                'output' : output_description
            }
        )
    return results_summary

task = {
    "train": [
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 7, 7, 7, 7, 7, 7, 0, 0, 0],
                [0, 7, 7, 7, 7, 7, 7, 0, 0, 0],
                [0, 7, 7, 7, 7, 7, 7, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 8, 8, 8, 0, 0, 0, 0],
                [0, 0, 0, 8, 8, 8, 0, 0, 0, 0],
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 7, 7, 7, 7, 7, 7, 0, 0, 0],
                [0, 7, 7, 7, 7, 7, 7, 0, 0, 0],
                [0, 7, 7, 7, 7, 7, 7, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 6, 6, 6, 0, 0, 0, 0],
                [0, 0, 0, 6, 6, 6, 0, 0, 0, 0],
            ],
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                [0, 0, 0, 0, 0, 6, 0, 0, 0, 0],
                [0, 0, 0, 0, 8, 8, 8, 0, 0, 0],
                [0, 0, 0, 8, 8, 8, 0, 0, 0, 0],
                [0, 0, 0, 8, 8, 8, 0, 0, 0, 0],
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 7, 7, 7, 7, 7, 7, 0, 0, 0],
                [0, 7, 7, 7, 7, 7, 7, 0, 0, 0],
                [0, 7, 7, 7, 7, 7, 7, 0, 0, 0],
                [0, 0, 0, 0, 0, 6, 0, 0, 0, 0],
                [0, 0, 0, 0, 6, 6, 6, 0, 0, 0],
                [0, 0, 0, 6, 6, 6, 0, 0, 0, 0],
                [0, 0, 0, 6, 6, 6, 0, 0, 0, 0],
            ],
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 8, 8, 8, 0, 0, 0],
                [0, 0, 0, 8, 8, 8, 0, 0, 0, 0],
                [7, 0, 0, 8, 8, 8, 0, 0, 0, 0],
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 7, 7, 7, 7, 7, 7, 0, 0, 0],
                [0, 7, 7, 7, 7, 7, 7, 0, 0, 0],
                [0, 7, 7, 7, 7, 7, 7, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 6, 6, 6, 0, 0, 0],
                [0, 0, 0, 6, 6, 6, 0, 0, 0, 0],
                [7, 0, 0, 6, 6, 6, 0, 0, 0, 0],
            ],
        },
    ]
}

results = analyze_results(task)
print(results)