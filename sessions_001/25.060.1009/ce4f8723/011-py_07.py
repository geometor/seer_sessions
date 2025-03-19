import numpy as np

def analyze_example(example):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid.shape
    
    print(f"  Input: {input_height}x{input_width}")
    print(f"  Output: {output_height}x{output_width}")

    for color in range(10):
      input_count = np.sum(input_grid == color)
      output_count = np.sum(output_grid == color)
      if input_count + output_count > 0:
          print(f"  Color {color}: Input={input_count}, Output={output_count}")

examples = [
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0], [0, 3, 3, 0], [0, 3, 3, 0], [0, 0, 0, 0]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 0], [0, 0, 1, 1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0], [0, 3, 3, 3, 0], [0, 3, 3, 3, 0], [0, 0, 0, 0, 0]]
    },
        {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 8, 8, 8, 8, 8, 8, 0], [0, 0, 8, 8, 8, 8, 8, 8, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0], [0, 3, 3, 3, 0], [0, 3, 3, 3, 0], [0, 0, 0, 0, 0]]
    },
    {
        "input" : [[0, 0, 0, 0, 0, 0],
                   [0, 2, 2, 2, 2, 0],
                   [0, 2, 2, 2, 2, 0],
                   [0, 2, 2, 2, 2, 0],
                   [0, 2, 2, 2, 2, 0],
                   [0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0],
                   [0, 3, 0],
                   [0, 3, 0],
                   [0, 0, 0]]

    }
]

for i, example in enumerate(examples):
    print(f"Example {i+1}:")
    analyze_example(example)
    print("-" * 20)