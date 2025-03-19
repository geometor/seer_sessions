def show_result(input_grid, expected_output):
    predicted_output = transform(input_grid)
    print(f"  Expected: {expected_output}")
    print(f"  Predicted: {predicted_output}")
    print(f"  Match: {predicted_output == expected_output}")

task_data = [
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 7, 7, 0, 0, 0],
            [0, 0, 0, 0, 7, 7, 0, 0, 0],
            [0, 0, 0, 0, 7, 7, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [7]
    },
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 4, 4, 4, 0, 0],
            [0, 0, 0, 4, 4, 4, 4, 0, 0],
            [0, 0, 0, 4, 4, 4, 4, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [4]
    },
    {
      "input" : [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 2, 0, 0, 0],
            [0, 0, 0, 0, 2, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
      ],
      "output" : [2]
    },
        {
      "input" : [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 7, 7, 7, 7, 7, 7, 0, 0],
            [0, 0, 7, 7, 7, 7, 7, 7, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      ],
      "output" : [7]
    }
]

for i, example in enumerate(task_data):
    print(f"Example {i+1}:")
    show_result(example["input"], example["output"])
