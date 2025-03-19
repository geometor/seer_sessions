task_examples = [
  {
    "input": np.array([[8, 8, 8, 8, 8, 8], [8, 1, 1, 1, 1, 8], [8, 1, 1, 1, 1, 8], [8, 8, 8, 8, 8, 8]]),
    "output": np.array([[8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 1, 1, 1, 1, 8, 8], [8, 8, 1, 1, 1, 1, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8]])
  },
  {
    "input": np.array([[8, 1, 8, 8, 8, 8, 8, 1, 8], [8, 1, 1, 1, 1, 1, 1, 1, 8], [8, 1, 8, 8, 8, 8, 8, 1, 8]]),
    "output": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 1, 8, 8, 8, 8, 1, 8, 8, 8], [8, 8, 1, 1, 1, 1, 1, 1, 1, 8, 8], [8, 8, 1, 8, 8, 8, 8, 1, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])
  },
  {
    "input" : np.array([[5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 0, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]]),
    "output" : np.array([[5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 0, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5]])
  },
    {
        "input" : np.array([[5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 0, 0, 5, 5],
                            [5, 5, 5, 5, 0, 0, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5],
                           ]),
        "output": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 0, 0, 5, 5, 5, 5],
                            [5, 5, 5, 5, 0, 0, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           ])
    }
]

# store the result to avoid recomputing
results = []

for i, example in enumerate(task_examples):
    input_grid = example['input']
    expected_output = example['output']
    predicted_output = transform(input_grid)
    results.append(np.array_equal(predicted_output, expected_output))
    print(f"Example {i+1}:")
    print(f"Input:\n{input_grid}")
    print(f"Expected Output:\n{expected_output}")
    print(f"Predicted Output:\n{predicted_output}")
    print(f"Prediction Correct: {np.array_equal(predicted_output, expected_output)}")
    # find the border region
    border_region = find_contiguous_region(input_grid, 0, 0)
    print(f"Border Region: {border_region}")
    print("-" * 20)

print(results)