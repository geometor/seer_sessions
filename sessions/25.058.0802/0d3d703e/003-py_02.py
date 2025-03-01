def compare_grids(grid1, grid2):
    """
    Compares two grids and returns a dictionary with differences.
    """
    if len(grid1) != len(grid2) or (len(grid1) > 0 and len(grid1[0]) != len(grid2[0])):
        return {"error": "Grids have different dimensions."}

    differences = []
    for i in range(len(grid1)):
        for j in range(len(grid1[0])):
            if grid1[i][j] != grid2[i][j]:
                differences.append(
                    {
                        "row": i,
                        "col": j,
                        "grid1_value": grid1[i][j],
                        "grid2_value": grid2[i][j],
                    }
                )

    return {"differences": differences}

task_data = {
    "train": [
        {
            "input": [[5, 8, 0], [5, 5, 7]],
            "output": [[6, 9, 1], [6, 6, 8]],
        },
        {
            "input": [[7, 7, 7], [0, 1, 2]],
            "output": [[8, 8, 8], [1, 2, 3]],
        },
		{
            "input": [[4, 4, 4], [4, 4, 9]],
            "output": [[5, 5, 5], [5, 5, 0]],
        },
        {
            "input": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            "output": [[2, 3, 4], [5, 6, 7], [8, 9, 0]],
        },
    ]
}

results = []
for example in task_data["train"]:
    input_grid = example["input"]
    expected_output = example["output"]
    actual_output = transform(input_grid)
    comparison = compare_grids(expected_output, actual_output)
    results.append(
        {
            "input": input_grid,
            "expected_output": expected_output,
            "actual_output": actual_output,
            "comparison": comparison,
        }
    )

print(results)