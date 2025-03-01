import numpy as np

def analyze_results(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        expected_output_grid = np.array(example['output'])
        predicted_output_grid = transform(input_grid)

        # Basic metrics
        input_shape = input_grid.shape
        output_shape = expected_output_grid.shape
        predicted_output_shape = predicted_output_grid.shape

        red_pixels_input = np.argwhere(input_grid == 2).tolist()
        red_pixels_expected = np.argwhere(expected_output_grid == 2).tolist()
        red_pixels_predicted = np.argwhere(predicted_output_grid == 2).tolist()

        azure_pixels_expected = np.argwhere(expected_output_grid == 8).tolist()
        azure_pixels_predicted = np.argwhere(predicted_output_grid == 8).tolist()

        correct_pixels = np.sum(predicted_output_grid == expected_output_grid)
        total_pixels = expected_output_grid.size
        accuracy = correct_pixels / total_pixels if total_pixels > 0 else 0.0


        result = {
            'input_shape': input_shape,
            'output_shape': output_shape,
            'predicted_output_shape': predicted_output_shape,
            'red_pixels_input': red_pixels_input,
            'red_pixels_expected': red_pixels_expected,
            'red_pixels_predicted': red_pixels_predicted,
            'azure_pixels_expected': azure_pixels_expected,
            'azure_pixels_predicted': azure_pixels_predicted,
            'accuracy': accuracy
        }
        results.append(result)
    return results

# Assuming 'task' variable holds the ARC task data
# Replace this with the actual task data loading
task_data = {
    "train": [
  {
    "input": [
      [0, 0, 0, 0, 0],
      [0, 0, 2, 0, 0],
      [0, 0, 0, 0, 0]
    ],
    "output": [
      [8, 0, 8, 0, 8, 2, 8, 0, 8, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [8, 0, 8, 0, 8, 0, 8, 0, 8, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [8, 0, 8, 0, 8, 2, 8, 0, 8, 0]
    ]
  },
  {
    "input": [
      [0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 2, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0]
    ],
    "output": [
      [8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [8, 0, 8, 0, 8, 0, 8, 2, 8, 0, 8, 0, 8, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 2, 8, 0]
    ]
  },
  {
    "input": [
      [0, 0, 0, 0],
      [0, 2, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0]
    ],
    "output": [
      [8, 0, 8, 2, 8, 0, 8, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [8, 0, 8, 0, 8, 0, 8, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [8, 0, 8, 2, 8, 0, 8, 0]
    ]
  }
]
}

analysis = analyze_results(task_data)
for i, result in enumerate(analysis):
    print(f"Example {i+1}:")
    print(f"  Input Shape: {result['input_shape']}")
    print(f"  Output Shape: {result['output_shape']}")
    print(f"  Predicted Output Shape: {result['predicted_output_shape']}")
    print(f"  Red Pixels (Input): {result['red_pixels_input']}")
    print(f"  Red Pixels (Expected): {result['red_pixels_expected']}")
    print(f"  Red Pixels (Predicted): {result['red_pixels_predicted']}")
    print(f"  Azure Pixels (Expected): {result['azure_pixels_expected']}")
    print(f"  Azure Pixels (Predicted): {result['azure_pixels_predicted']}")
    print(f"  Accuracy: {result['accuracy']:.4f}")
    print("-" * 20)