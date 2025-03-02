import numpy as np

train_examples = [
    {
        "input": np.array([[0, 5, 0, 5, 0, 5, 0, 5, 0],
                           [5, 0, 5, 0, 5, 0, 0, 0, 0],
                           [0, 5, 0, 5, 0, 5, 0, 5, 0]]),
        "output": np.array([[0, 3, 0, 3, 0, 5, 0, 5, 0],
                            [5, 0, 3, 0, 5, 0, 0, 0, 0],
                            [0, 3, 0, 3, 0, 5, 0, 5, 0]]),
    },
        {
        "input": np.array([[0, 5, 0, 5, 0, 0, 5, 0, 5],
                           [0, 0, 5, 0, 5, 0, 5, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [5, 0, 5, 0, 5, 0, 5, 0, 5]]),
        "output": np.array([[0, 3, 0, 3, 0, 0, 3, 0, 3],
                            [0, 0, 3, 0, 3, 0, 3, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [3, 0, 3, 0, 3, 0, 3, 0, 3]]),
    },
    {
        "input": np.array([[5, 0, 5, 5, 0, 5, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [5, 0, 5, 5, 0, 5, 0, 5, 5, 0, 5, 5]]),
        "output": np.array([[3, 0, 3, 3, 0, 3, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [3, 0, 3, 3, 0, 3, 0, 3, 3, 0, 3, 3]]),
    }
]

def analyze_examples(examples):
    for i, example in enumerate(examples):
        input_grid = example["input"]
        output_grid = example["output"]

        print(f"Example {i+1}:")

        # Input analysis
        input_gray_positions = np.argwhere(input_grid == 5)
        print(f"  Input Gray Pixel Positions:\n{input_gray_positions}")

        # Output analysis
        output_green_positions = np.argwhere(output_grid == 3)
        print(f"  Output Green Pixel Positions:\n{output_green_positions}")

        # Relationship
        print(f" Gray Pixels that turn Green")
        for pos in output_green_positions:
          if input_grid[pos[0], pos[1]] == 5:
              print(pos)
        print("-" * 20)

analyze_examples(train_examples)
