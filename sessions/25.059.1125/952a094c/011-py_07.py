def report(input, expected, actual):
    input_colors = np.unique(input)
    expected_colors = np.unique(expected)
    actual_colors = np.unique(actual)
    diff_expected = np.sum(input != expected)
    diff_actual = np.sum(input != actual)
    print(f"  Input colors: {input_colors}")
    print(f"  Expected colors: {expected_colors}")
    print(f"  Actual colors: {actual_colors}")
    print(f"  Differences (input vs. expected): {diff_expected}")
    print(f"  Differences (input vs. actual): {diff_actual}")
    print(f"  Correct pixels (expected vs. actual): {np.sum(expected == actual)}")
    print(f"  Total pixels: {input.size}")
    print(f"  Accuracy: {np.sum(expected == actual) / input.size:.2f}")

for i in range(len(task.train)):
  input = task.train[i].input.grid
  expected = task.train[i].output.grid
  actual = transform(input)
  print (f"Example {i}:")
  report(input, expected, actual)