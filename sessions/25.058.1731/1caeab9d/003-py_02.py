def grid_to_str(grid):
    return '\n'.join(''.join(str(cell) for cell in row) for row in grid)

def analyze_example(example_pair, example_number):
    input_grid = example_pair['input']
    expected_output_grid = example_pair['output']
    predicted_output_grid = transform(input_grid)

    print(f"Example {example_number}:")
    print("Input Grid:")
    print(grid_to_str(input_grid))
    print("\nExpected Output Grid:")
    print(grid_to_str(expected_output_grid))
    print("\nPredicted Output Grid:")
    print(grid_to_str(predicted_output_grid))

    input_objects = find_objects(np.array(input_grid))
    expected_objects = find_objects(np.array(expected_output_grid))
    print("\nInput Objects:", len(input_objects))
    print("Expected Output Objects:", len(expected_objects))



    print("\nCorrect Prediction:", predicted_output_grid == expected_output_grid)
    print("-" * 30)

task = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 8, 8, 0, 0, 6, 0],
        [0, 8, 8, 8, 0, 0, 6, 0],
        [0, 8, 8, 8, 0, 0, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 8, 8, 8, 0, 6, 0],
        [0, 8, 8, 8, 0, 6, 0],
        [0, 8, 8, 8, 0, 6, 0],
        [0, 0, 0, 0, 0, 0, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 3, 0, 4, 4, 0, 0, 0],
        [0, 3, 3, 0, 4, 4, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 3, 0, 4, 4, 0, 1, 1, 0, 0],
        [0, 3, 3, 0, 4, 4, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
        {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 7, 7, 7, 7, 0],
        [0, 0, 0, 0, 0, 7, 7, 7, 7, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 5, 5, 5, 0, 0, 0],
        [0, 0, 0, 0, 5, 5, 5, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 5, 5, 5, 0, 7, 7, 7, 7, 0, 0, 0],
        [0, 2, 0, 5, 5, 5, 0, 7, 7, 7, 7, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    }

  ],
  "test": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 9, 0, 0],
        [0, 0, 0, 0, 9, 9, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 4, 4, 4, 4, 0, 0, 0],
        [0, 4, 4, 4, 4, 0, 0, 0],
        [0, 4, 4, 4, 4, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 4, 4, 4, 4, 0, 9, 9, 0, 0],
        [0, 4, 4, 4, 4, 0, 9, 9, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    }
  ]
}

for i, example in enumerate(task["train"]):
    analyze_example(example, i + 1)