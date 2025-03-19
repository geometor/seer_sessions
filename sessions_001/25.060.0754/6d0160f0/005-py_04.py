def calculate_accuracy(predicted, expected):
    """Calculates the accuracy of the prediction."""
    predicted_arr = np.array(predicted)
    expected_arr = np.array(expected)
    correct_pixels = np.sum(predicted_arr == expected_arr)
    total_pixels = predicted_arr.size  # or expected_arr.size (they should be the same)
    accuracy = correct_pixels / total_pixels if total_pixels > 0 else 0.0
    return correct_pixels, total_pixels, accuracy

# this will be populated with results
results = []

for idx, (train_input, train_output) in enumerate(zip(task.train_inputs, task.train_outputs)):
  predicted_output = transform(train_input)
  correct_pixels, total_pixels, accuracy = calculate_accuracy(predicted_output, train_output)
  results.append( {
      'example': idx,
      'correct': correct_pixels,
      'total': total_pixels,
      'accuracy': accuracy
  })

print(results)