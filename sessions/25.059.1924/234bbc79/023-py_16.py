def show_grid(grid, title="Grid"):
    """Displays a grid in a human-readable format."""
    print(f"\n--- {title} ---")
    for row in grid:
        print(row)
    print("-" * 20)

def analyze_example(example, transform_function):
    """Analyzes a single example, prints input, expected, and actual outputs."""
    
    input_grid = example['input']
    expected_output = example['output']
    actual_output = transform_function(input_grid)

    show_grid(input_grid, "Input Grid")
    show_grid(expected_output, "Expected Output")
    show_grid(actual_output, "Actual Output")

    correct = (np.array(expected_output) == np.array(actual_output)).all()
    print(f"Correct: {correct}")
    return correct


task = {
  "train": [
    {
      "input": [
        [5, 5, 1, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 1, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 2, 5]
      ],
      "output": [
        [1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 2]
      ]
    },
    {
      "input": [
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [2, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1]
      ]
    },
    {
      "input": [
        [5, 5, 1, 5, 5, 5, 5, 5, 5, 5, 5, 2, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
      ],
      "output": [
        [1, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
      {
      "input": [
        [5, 1, 5, 2, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5]
      ],
      "output": [
        [1,2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
      ]
    }

  ],
  "test": [
    {
      "input": [
        [5, 5, 5, 5, 5, 2, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [1, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5]
      ],
      "output": [
        [0,0,0,0,0,2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
      ]
    }
  ]
}

results = []
for example in task["train"]:
    results.append(analyze_example(example, transform))