# Example usage (Conceptual - will be implemented later)

def analyze_results(task_examples, transform_function):
  results = []
  for example in task_examples:
    input_grid = example['input']
    expected_output = example['output']
    predicted_output = transform_function(input_grid)
    comparison = np.array_equal(predicted_output, expected_output)

    # determine if the prediction matches
    results.append({
      'input': input_grid,
      'expected': expected_output,
      'predicted': predicted_output,
      'correct': comparison
    })

  return results

# assuming ARC data structured for each problem
# results = analyze_results(task.train, transform)
# for item in results:
#   print(item['correct'])

# the code above is a rough outline - to be implemented, it will
# 1. execute on the training dataset
# 2. compare the output
# 3. show failures

# then, the following code will show exact differences in the grids
# for result in results:
#   if not result['correct']:
#         diff = result['predicted'] != result['expected']
#         diff_indices = np.where(diff)
#         print("Differences found at indices:", diff_indices)
#         print("Predicted values at differences", result['predicted'][diff_indices])
#         print("Expected values at differences", result['expected'][diff_indices])
