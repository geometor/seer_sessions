import numpy as np

# Example grids (replace with actual data from the task)
train_examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 4, 4, 4, 4, 0],
                           [0, 4, 4, 4, 4, 0],
                           [0, 0, 0, 0, 0, 0]]),
        "output": np.array([[1]])
    },
      {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 8, 8, 8, 0, 0],
                          [0, 0, 0, 0, 8, 8, 8, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[8, 8, 8],
                           [8, 8, 8],
                           [8, 8, 8]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output" : np.array([[1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1]])
    },
     {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 6, 0, 0, 0],
                           [0, 0, 0, 0, 6, 6, 0, 0, 0],
                           [0, 0, 0, 6, 6, 6, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[5]])

    }

]

def assess_examples(examples, transform_function):
    results = []
    for i, example in enumerate(examples):
        input_grid = example['input']
        expected_output = example['output']
        predicted_output = transform_function(input_grid)
        is_correct = np.array_equal(predicted_output, expected_output)
        results.append({
            'example_index': i,
            'input_shape': input_grid.shape,
            'output_shape': expected_output.shape,
            'predicted_output_shape': predicted_output.shape,
            'is_correct': is_correct
        })
    return results

def simple_transform(input_grid):
  """
  A placeholder transform - replace with the generated transform function
  """
  return np.array([[1]])

results = assess_examples(train_examples, simple_transform)

for result in results:
  print (result)