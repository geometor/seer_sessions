def get_grid_shape(grid):
    return (len(grid), len(grid[0]))

examples = [
    {
        "input": [
            [5, 0, 5, 5, 5],
            [0, 0, 5, 0, 0],
            [0, 0, 5, 0, 0],
        ],
        "output": [
            [0, 0, 5],
            [0, 0, 0],
            [5, 5, 5],
            [0, 0, 0],
            [0, 0, 5],
        ]
    },
    {
        "input": [
          [8, 8, 8, 8, 8, 8, 8],
          [8, 8, 0, 0, 0, 8, 8],
          [8, 8, 0, 0, 0, 8, 8],
          [8, 8, 0, 0, 0, 8, 8],
          [8, 8, 0, 0, 0, 8, 8],
          [8, 8, 0, 0, 0, 8, 8],
          [8, 8, 8, 8, 8, 8, 8]
        ],
        "output": [
          [8, 8, 8, 8, 8, 8, 8],
          [8, 8, 8, 8, 8, 8, 8],
          [8, 0, 0, 0, 0, 0, 8],
          [8, 0, 0, 0, 0, 0, 8],
          [8, 0, 0, 0, 0, 0, 8],
          [8, 8, 8, 8, 8, 8, 8],
          [8, 8, 8, 8, 8, 8, 8]
        ]
    },
    {
       "input":[
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
       ],
       "output": [
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
       ]
    }
]

for example in examples:
    input_shape = get_grid_shape(example["input"])
    output_shape = get_grid_shape(example["output"])
    print(f"Input Shape: {input_shape}, Output Shape: {output_shape}")
