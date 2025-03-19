import numpy as np

def analyze_results(examples, transform_function):
  """
    Analyzes the results of applying the transform function to a list of input/output examples.

    Args:
      examples: list of dictionaries where "input" is the matrix, and "output" is the expected output.
      transform_function: the function to run.

    Returns:
      A dictionary of results:
        example_index: metrics
  """
  results_summary = {}

  for ex_idx, example in enumerate(examples):
      input_grid = np.array(example['input'])
      expected_output = np.array(example['output'])
      actual_output = transform_function(input_grid)
      comparison = np.array_equal(actual_output, expected_output)
      
      results_summary[ex_idx] = {
          'correct': comparison,
          'input_shape': input_grid.shape,
          'output_shape': expected_output.shape,
          'actual_output_shape': actual_output.shape
      }

  return results_summary

# Mock examples
examples = [
    {'input': [[0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 2, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 8, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0]],
     'output': [[0, 0, 0, 2, 0, 0, 0],
                [0, 0, 0, 2, 0, 0, 0],
                [0, 0, 0, 2, 0, 0, 0],
                [0, 0, 0, 8, 0, 0, 0],
                [0, 0, 0, 8, 0, 0, 0],
                [0, 0, 0, 8, 0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 6, 0, 0, 0, 0, 3, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 5, 0, 0, 0]],
     'output': [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 6, 6, 0, 0, 0, 3, 3, 3],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 5, 0, 0, 0],
                [0, 0, 0, 0, 5, 0, 0, 0]]},
     {'input' : [[0, 0, 0, 0, 0, 0],
                [0, 0, 5, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]],
     'output': [[0, 0, 0, 0, 0, 0],
                [0, 0, 5, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]]},
     {'input': [[0,5,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0]],
     'output': [[0,5,0,0,0,0,0,0,0],
                 [0,5,0,0,0,0,0,0,0],
                 [0,5,0,0,0,0,0,0,0],
                 [0,5,0,0,0,0,0,0,0],
                 [0,5,0,0,0,0,0,0,0]]}
]

results = analyze_results(examples, transform)
print(results)
