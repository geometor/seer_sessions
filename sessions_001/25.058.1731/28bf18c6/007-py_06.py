import numpy as np

def analyze_example(input_grid, output_grid, example_id):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    # find azure region
    azure_rows, azure_cols = np.where(input_grid == 8)
    
    report = {
        "example_id": example_id,
        "input_dimensions": input_grid.shape,
        "output_dimensions": output_grid.shape,
        "azure_present_input": 8 in input_grid,        
        "input_region_copied": "n/a",
        "output_region_check": "n/a"
    }
    if report["azure_present_input"]:
      min_row, max_row = np.min(azure_rows), np.max(azure_rows)
      min_col, max_col = np.min(azure_cols), np.max(azure_cols)

      rows_with_azure = np.unique(azure_rows)
      cols_with_azure = np.unique(azure_cols)
      input_region_copied = input_grid[min_row:max_row+1, min_col:max_col+1]
      selection_region_copied = input_grid[np.ix_(rows_with_azure, cols_with_azure)]

      # compare
      report["input_region_copied"] = input_region_copied.tolist()
      report["output_region_check"] = np.array_equal(selection_region_copied, output_grid)
      report["selection_region_copied"] = selection_region_copied.tolist()
    return report

def analyze_task(task):
    reports = []
    for i, example in enumerate(task['train']):
        reports.append(analyze_example(example['input'], example['output'], i + 1))
    return reports

task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 8, 8, 0, 0, 0, 0, 0, 0], [0, 8, 8, 8, 0, 0, 0, 0, 0, 0], [0, 8, 8, 8, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[8, 8, 8], [8, 8, 8], [8, 8, 8]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": []
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 8, 8, 0, 0, 0, 1, 0, 0], [0, 8, 8, 8, 0, 0, 0, 1, 0, 0], [0, 8, 8, 8, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 7, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[1], [1], [1]]
        }
    ]
}
reports = analyze_task(task)
for report in reports:
    print(report)
