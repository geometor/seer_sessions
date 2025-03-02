import numpy as np

def analyze_results(examples, transform_function):
    results = []
    for i, (input_grid, output_grid) in enumerate(examples):
        transformed_grid = transform_function(input_grid.copy())
        expected_azure = np.sum(output_grid == 8)
        actual_azure = np.sum(transformed_grid == 8)
        expected_green = np.sum(output_grid == 3)
        actual_green = np.sum(transformed_grid == 3)

        results.append({
            "example": i + 1,
            "expected_azure": expected_azure,
            "actual_azure": actual_azure,
            "expected_green": expected_green,
            "actual_green": actual_green,
            "azure_correct": expected_azure == actual_azure,
            "green_correct": expected_green == actual_green
        })
    return results

# dummy transform and examples for demonstration, will use in subsequent turn
def dummy_transform(input_grid):
    return input_grid

dummy_examples = [
  (np.array([[8,0,0],[0,0,0],[0,0,0]]), np.array([[8,0,0],[0,0,0],[0,0,0]])),
  (np.array([[8,0,0],[0,8,0],[0,0,0]]), np.array([[8,0,0],[0,8,0],[0,0,0]]))
  ]

analysis = analyze_results(dummy_examples, dummy_transform)
print(analysis)