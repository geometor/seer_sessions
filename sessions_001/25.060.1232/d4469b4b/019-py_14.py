import numpy as np

def analyze_example(input_grid, output_grid):
    green_count = np.sum(input_grid == 3)
    output_height = output_grid.shape[0]
    output_width = output_grid.shape[1]
    gray_count = np.sum(output_grid == 5)
    input_height = input_grid.shape[0]
    input_width = input_grid.shape[1]

    print(f"  Green Count: {green_count}")
    print(f"  Output Dimensions: {output_height}x{output_width}")
    print(f"  Gray Count: {gray_count}")
    print(f"  Input Dimensions: {input_height}x{input_width}")
    print(f"  Input Grid:\n{input_grid}")
    print(f"  Output Grid:\n{output_grid}")

# assuming task is defined globally e.g. task = get_arc_task("...")
# I am in a restricted environment so can not define this here
# here is an example of what would be done, the actual code will be executed below this.
"""
for i, example in enumerate(task["train"]):
  print("Example",i)
  analyze_example(np.array(example['input']), np.array(example['output']))
"""

examples = [
    {
        'input': [[0, 0, 3, 0, 0, 0, 0],
                  [0, 0, 3, 0, 0, 0, 0],
                  [0, 0, 3, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0]],
        'output': [[0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [5, 5, 5, 0, 0]]
    },
    {
        'input': [[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 3, 0, 0, 0, 0],
                  [0, 0, 3, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0]],
        'output': [[0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [5, 5, 0, 0, 0]]
    },
    {
        'input': [[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 3, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]],
        'output': [[0, 0, 0, 0, 0, 0]]
    },
     {
        'input': [[3, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 3, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]],
        'output': [[0, 0, 0, 0, 0, 0]]
    }

]
for i, example in enumerate(examples):
  print("Example",i)
  analyze_example(np.array(example['input']), np.array(example['output']))