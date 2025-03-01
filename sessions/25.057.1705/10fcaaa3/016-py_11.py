import numpy as np

def get_yellow_positions(grid):
    return np.array(np.where(grid == 4)).T.tolist()

def analyze_examples(task):
    examples = task.get("train")
    results = []
    for i, example in enumerate(examples):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        input_height, input_width = input_grid.shape
        output_height, output_width = output_grid.shape
        input_yellow_positions = get_yellow_positions(input_grid)
        output_yellow_positions = get_yellow_positions(output_grid)

        # verify background is a checkerboard
        checkerboard = True
        for row in range(output_height):
            for col in range(output_width):
                if (row + col) % 2 == 0:
                    if output_grid[row,col] != 8:
                        checkerboard = False
                        break;
                else:
                    if output_grid[row,col] != 0 and output_grid[row,col] != 4:
                        checkerboard = False
                        break
            if checkerboard != True:
                break;

        results.append({
            "example": i + 1,
            "input_dimensions": f"{input_height}x{input_width}",
            "output_dimensions": f"{output_height}x{output_width}",
            "input_yellow_positions": input_yellow_positions,
            "output_yellow_positions": output_yellow_positions,
            "checkerboard": checkerboard
        })
    return results

# Assuming 'task' is defined elsewhere and contains the ARC task data
# Example usage with a placeholder task:

task = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0],
        [0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [8, 0, 8, 0, 8, 0],
        [0, 8, 0, 8, 4, 8],
        [8, 0, 8, 4, 8, 0],
        [0, 8, 4, 8, 0, 8],
        [8, 4, 8, 0, 8, 0],
        [4, 8, 0, 8, 0, 8]
      ]
    },
      {
      "input": [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 4, 0]
      ],
      "output": [
        [8, 0, 8, 4, 8, 0, 8],
        [0, 8, 4, 8, 4, 8, 0],
        [8, 4, 8, 4, 8, 4, 8],
        [4, 8, 4, 8, 4, 8, 4],
        [8, 4, 8, 4, 8, 4, 8],
        [0, 8, 0, 8, 0, 8, 4],
        [8, 0, 8, 0, 8, 4, 8]
      ]
    },
     {
      "input": [
          [0,0,0,0,0,0,0,0],
          [0,0,4,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,4,0],
          [0,0,0,0,0,0,0,0]
      ],
      "output":[
          [8,0,4,0,8,0,8,0],
          [0,8,4,8,0,8,0,8],
          [8,4,8,4,8,0,8,0],
          [4,8,4,8,0,8,4,8],
          [8,4,8,0,8,4,8,0],
          [0,8,0,8,4,8,0,8],
          [8,0,8,4,8,0,8,0],
          [0,8,4,8,0,8,0,8]
      ]
    }
  ]
}

analysis_results = analyze_examples(task)
for result in analysis_results:
    print(f"Example {result['example']}:")
    print(f"  Input Dimensions: {result['input_dimensions']}")
    print(f"  Output Dimensions: {result['output_dimensions']}")
    print(f"  Input Yellow Positions: {result['input_yellow_positions']}")
    print(f"  Output Yellow Positions: {result['output_yellow_positions']}")
    print(f"  Checkerboard: {result['checkerboard']}")
    print("-----")