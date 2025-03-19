import numpy as np

def compare_grids(grid1, grid2):
    """Compares two grids and returns a report of differences."""
    if grid1.shape != grid2.shape:
        return "Grids have different shapes."

    diff_indices = np.where(grid1 != grid2)
    num_differences = len(diff_indices[0])
    
    report = f"Number of differences: {num_differences}\n"
    if num_differences > 0:
        report += "Differences at (row, col) indices:\n"
        for i in range(num_differences):
            row = diff_indices[0][i]
            col = diff_indices[1][i]
            report += f"  ({row}, {col}): Expected {grid2[row, col]}, Got {grid1[row, col]}\n"

    return report

# Example grids from the prompt - I will use the actual outputs later
train_ex = []
train_ex.append(({'input': np.array([[4, 4, 4, 4, 4, 4, 4, 4, 4],
       [4, 4, 4, 4, 4, 4, 1, 4, 4],
       [4, 4, 4, 4, 4, 4, 1, 4, 4],
       [4, 4, 4, 4, 1, 1, 1, 4, 4],
       [4, 4, 4, 4, 1, 4, 4, 4, 4],
       [4, 4, 2, 2, 4, 4, 4, 4, 4],
       [4, 4, 2, 2, 4, 4, 4, 6, 6],
       [4, 4, 4, 4, 4, 4, 4, 6, 6]]), 'output': np.array([[4, 4, 4, 4, 4, 4, 4, 4, 4],
       [4, 4, 4, 4, 4, 4, 1, 4, 4],
       [4, 4, 4, 4, 4, 4, 1, 4, 4],
       [4, 4, 4, 4, 1, 1, 1, 4, 4],
       [4, 4, 4, 4, 1, 4, 4, 4, 4],
       [4, 4, 2, 2, 1, 4, 4, 4, 4],
       [4, 4, 2, 2, 1, 4, 4, 6, 6],
       [4, 4, 4, 4, 1, 4, 4, 6, 6]])}, {'input': np.array([[4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 1, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 1, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 1, 4],
       [4, 4, 4, 4, 4, 1, 1, 1, 1, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
       [4, 2, 2, 4, 4, 4, 4, 4, 4, 4],
       [4, 2, 2, 4, 4, 4, 4, 4, 4, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
       [4, 4, 4, 4, 4, 4, 4, 6, 6, 4],
       [4, 4, 4, 4, 4, 4, 4, 6, 6, 4]]), 'output': np.array([[4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 1, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 1, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 1, 4],
       [4, 4, 4, 4, 4, 1, 1, 1, 1, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
       [4, 2, 2, 4, 4, 4, 4, 1, 4, 4],
       [4, 2, 2, 4, 4, 4, 4, 1, 4, 4],
       [4, 4, 4, 4, 4, 4, 4, 1, 4, 4],
       [4, 4, 4, 4, 4, 4, 4, 6, 6, 4],
       [4, 4, 4, 4, 4, 4, 4, 6, 6, 4]])}, {'input': np.array([[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 4],
       [4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
       [4, 4, 4, 2, 2, 4, 4, 4, 4, 4, 4],
       [4, 4, 4, 2, 2, 4, 4, 4, 4, 4, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 6, 6, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 6, 6, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]]), 'output': np.array([[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 4],
       [4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
       [4, 4, 4, 2, 2, 4, 4, 4, 1, 4, 4],
       [4, 4, 4, 2, 2, 4, 4, 4, 1, 4, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 1, 4, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 6, 6, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 6, 6, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]])})

def get_predicted_output(input_grid):
    # Call transform and return output
    return transform(input_grid)

results = []    
for ex in train_ex:
    input_grid = ex['input']
    expected_output = ex['output']
    predicted_output = get_predicted_output(input_grid)
    comparison = compare_grids(expected_output, predicted_output)
    results.append({'input': input_grid.tolist(), 'expected': expected_output.tolist(), 'predicted': predicted_output.tolist(), 'comparison': comparison})

for item in results:
  print(item['comparison'])