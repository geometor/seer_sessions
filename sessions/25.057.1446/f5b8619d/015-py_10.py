import numpy as np

def compare_grids(predicted_output, expected_output):
    """Compares two grids and returns a dictionary of differences."""
    if predicted_output.shape != expected_output.shape:
        return {"shape_mismatch": True, "details": f"Predicted shape: {predicted_output.shape}, Expected shape: {expected_output.shape}"}

    differences = {}
    mismatched_pixels = np.where(predicted_output != expected_output)
    if mismatched_pixels[0].size > 0:  # Check if there are any mismatches
      differences["pixel_mismatches"] = []
      for i in range(len(mismatched_pixels[0])):
          row = mismatched_pixels[0][i]
          col = mismatched_pixels[1][i]
          differences["pixel_mismatches"].append({
              "row": int(row),
              "col": int(col),
              "predicted_value": int(predicted_output[row, col]),
              "expected_value": int(expected_output[row, col])
          })

    return differences

# Example Task Data (replace with the actual data from the task)
task_data = {
  "train": [
    {
      "input": np.array([[4, 0], [0, 4]]),
      "output": np.array([[4, 8, 0, 0], [8, 4, 0, 0], [0, 0, 4, 8], [0, 0, 8, 4]])
    },
    {
      "input": np.array([[0, 5], [5, 0]]),
      "output": np.array([[0, 0, 6, 5], [0, 0, 5, 6], [6, 5, 0, 0], [5, 6, 0, 0]])
    },
    {
      "input": np.array([[6, 6], [6, 0]]),
      "output": np.array([[6, 1, 6, 1], [1, 6, 1, 6], [6, 1, 0, 0], [1, 6, 0, 0]])
    }
  ]
}

results = {}

# Assuming 'transform' function is defined as in the provided code
for i, example in enumerate(task_data["train"]):
  input_grid = example['input']
  expected_output = example['output']
  predicted_output = transform(input_grid)
  results[f"example_{i+1}"] = compare_grids(predicted_output, expected_output)

print(results)
