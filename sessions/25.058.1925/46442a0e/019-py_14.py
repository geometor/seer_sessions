import numpy as np

def analyze_example(input_grid, output_grid, predicted_output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_output_grid = np.array(predicted_output_grid)

    input_shape = input_grid.shape
    output_shape = output_grid.shape
    predicted_output_shape = predicted_output_grid.shape
    
    input_core = find_core(input_grid)
    if input_core is None:
      input_core_size = (0,0)
    else:
      input_core_size = (2,2)
    
    output_core = find_core(output_grid)
    if output_core is None:
      output_core_size = (0,0)
    else:
      output_core_size = (2,2)
    
    predicted_output_core = find_core(predicted_output_grid)
    if predicted_output_core is None:
      predicted_output_core_size = (0,0)
    else:
      predicted_output_core_size = (2,2)

    correct = np.array_equal(output_grid, predicted_output_grid)

    report = {
        "input_shape": input_shape,
        "output_shape": output_shape,
        "predicted_output_shape": predicted_output_shape,
        "input_core_location": input_core,
        "input_core_size": input_core_size,
        "output_core_location": output_core,
        "output_core_size": output_core_size,
        "predicted_output_core_location": predicted_output_core,
        "predicted_output_core_size": predicted_output_core_size,        
        "correct": correct,
    }
    return report
def find_core(grid):
    # Find the 2x2 yellow (4) core in the input grid.  Assumes it exists and is unique.
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if grid[r, c] == 4 and grid[r + 1, c] == 4 and grid[r, c + 1] == 4 and grid[r + 1, c + 1] == 4:
                return (r, c)
    return None

# Example data (replace with actual data from the task)
task_examples = [
    ([[4, 4, 5, 4, 4], [4, 4, 5, 4, 4], [6, 6, 5, 6, 6], [4, 4, 5, 4, 4], [4, 4, 5, 4, 4]],
     [[4, 4, 4, 4, 5, 5], [4, 4, 4, 4, 5, 5], [4, 4, 4, 4, 5, 5], [4, 4, 4, 4, 5, 5], [6, 6, 6, 6, 5, 5], [6, 6, 6, 6, 5, 5]]),
   ([[4, 4, 8, 4, 4, 3], [4, 4, 8, 4, 4, 3], [4, 4, 8, 4, 4, 3], [2, 2, 8, 2, 2, 3]],
    [[4, 4, 4, 4, 8, 8, 3], [4, 4, 4, 4, 8, 8, 3], [4, 4, 4, 4, 8, 8, 3], [4, 4, 4, 4, 8, 8, 3], [2, 2, 2, 2, 8, 8, 3]]),
   ([[4, 4, 1], [4, 4, 1], [4, 4, 1], [7, 7, 1]], 
    [[4, 4, 4, 4, 1], [4, 4, 4, 4, 1], [4, 4, 4, 4, 1], [4, 4, 4, 4, 1], [7, 7, 7, 7, 1]])
]

previous_code_predictions = [
   [[4, 4, 4, 4, 5, 0], [4, 4, 4, 4, 5, 0], [4, 4, 4, 4, 5, 0], [4, 4, 4, 4, 5, 0], [6, 6, 6, 6, 5, 0], [6, 6, 6, 6, 5, 0]],
   [[4, 4, 4, 4, 8, 8, 3], [4, 4, 4, 4, 8, 8, 3], [4, 4, 4, 4, 8, 8, 3], [4, 4, 4, 4, 8, 8, 3], [2, 2, 2, 2, 8, 8, 3], [0, 0, 0, 0, 8, 8, 3]],
   [[4, 4, 4, 4, 1], [4, 4, 4, 4, 1], [4, 4, 4, 4, 1], [4, 4, 4, 4, 1], [7, 7, 7, 7, 1], [0, 0, 0, 0, 0]]
]

reports = []
for (input_grid, output_grid), predicted_output_grid in zip(task_examples, previous_code_predictions):
    report = analyze_example(input_grid, output_grid, predicted_output_grid)
    reports.append(report)

for i, report in enumerate(reports):
    print(f"Example {i + 1}:")
    for key, value in report.items():
        print(f"  {key}: {value}")
    print("-" * 20)