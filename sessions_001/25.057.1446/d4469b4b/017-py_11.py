import numpy as np

def analyze_example(example):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])

    input_dims = input_grid.shape
    output_dims = output_grid.shape

    green_coords = np.argwhere(input_grid == 3)
    has_green = green_coords.size > 0
    bbox = None
    if has_green:
        min_row = np.min(green_coords[:, 0])
        max_row = np.max(green_coords[:, 0])
        min_col = np.min(green_coords[:, 1])
        max_col = np.max(green_coords[:, 1])
        bbox = (min_row, max_row, min_col, max_col)
    
    is_subgrid = output_dims != input_dims
    
    # count changed pixels - compare input and output, count number of differences
    changed_pixels = 0
    if is_subgrid:
        # if it is a subgrid, then compare only the relevant parts of the input
        subgrid = input_grid[bbox[0]:bbox[2]+1, bbox[1]:bbox[3]+1]
        changed_pixels = np.sum(subgrid != output_grid)
    else:
        changed_pixels = np.sum(input_grid != output_grid)

    print(f"  Input Dimensions: {input_dims}")
    print(f"  Output Dimensions: {output_dims}")
    print(f"  Has Green: {has_green}")
    print(f"  Bounding Box: {bbox}")
    print(f"  Is Subgrid: {is_subgrid}")
    print(f"  Changed Pixels: {changed_pixels}")


task = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [5]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [5]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [5]
      ]
    },
     {
      "input": [
        [0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [5]
      ]
    }
  ],
  "test": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0]
      ]
    }
  ]
}

for i, example in enumerate(task['train']):
    print(f"Example {i+1}:")
    analyze_example(example)