import numpy as np

# Provided input and output grids from the examples
examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 1, 0, 0, 0],
                           [0, 0, 0, 0, 4, 0, 0, 0],
                           [0, 0, 0, 0, 2, 0, 0, 0]]),
        "output": np.array([[1],
                            [4],
                            [2]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 5, 0, 0, 0],
                           [0, 0, 0, 0, 6, 0, 0, 0],
                           [0, 0, 0, 0, 8, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[5],
                            [6],
                            [8]])
    },
     {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 7, 0, 0, 0, 0],
                           [0, 0, 0, 0, 7, 0, 0, 0, 0],
                           [0, 0, 0, 0, 7, 0, 0, 0, 0],
                           [0, 0, 0, 0, 7, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[7]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 3, 0, 0, 0, 0],
                           [0, 0, 0, 0, 3, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[3]])
    }
]

def analyze_results(examples, transform_function):
  results = []
  for i, example in enumerate(examples):
      input_grid = example['input']
      expected_output = example['output']
      actual_output = transform_function(input_grid)
      
      results.append({
          "example_index": i,
          "input_shape": input_grid.shape,
          "output_shape": expected_output.shape,
          "actual_output_shape": actual_output.shape,
          "correct": np.array_equal(expected_output, actual_output)
      })

  return results

from previous_response import transform  #import our transform function
results = analyze_results(examples, transform)

for result in results:
    print(f"Example {result['example_index']}:")
    print(f"  Input Shape: {result['input_shape']}")
    print(f"  Output Shape: {result['output_shape']}")
    print(f"  Actual Output Shape: {result['actual_output_shape']}")
    print(f"  Correct: {result['correct']}")
    print("-" * 20)
