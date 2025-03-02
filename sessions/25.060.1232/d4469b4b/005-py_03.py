examples = task["train"]
results = []

for i, example in enumerate(examples):
    input_grid = example["input"]
    expected_output_grid = example["output"]
    predicted_output_grid = transform(input_grid)

    results.append(
      {
        "example":i,
        "input_shape": np.array(input_grid).shape,
        "output_shape": np.array(expected_output_grid).shape,
        "predicted_shape": np.array(predicted_output_grid).shape,
        "match": np.array_equal(predicted_output_grid,expected_output_grid)
      }
    )

for result in results:
    print(result)