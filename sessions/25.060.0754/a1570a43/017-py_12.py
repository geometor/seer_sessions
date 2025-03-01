import numpy as np

def analyze_example(input_grid, output_grid):
    print(f"Input Grid:\n{input_grid}")
    print(f"Output Grid:\n{output_grid}")

    for color in [2, 3]:  # Focus on red and green
        input_coords = np.argwhere(input_grid == color)
        output_coords = np.argwhere(output_grid == color)

        print(f"Color: {color}")
        print(f"  Input coords: {input_coords.tolist()}")
        print(f"  Output coords: {output_coords.tolist()}")

        if len(input_coords) > 0 and len(output_coords) > 0:
            input_center = np.mean(input_coords, axis=0)
            output_center = np.mean(output_coords, axis=0)
            print(f"  Input center: {input_center}")
            print(f"  Output center: {output_center}")
            print(f"  Center shift: {output_center - input_center}")
        elif len(input_coords) == 0 and len(output_coords) == 0:
            print("   No objects of this color in input and output")
        elif len(input_coords) == 0:
            print("   No objects of this color in input")
        else:
             print("   No objects of this color in output")

# Load the example data (replace with actual data loading)
task_data = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 0],
        [0, 2, 2, 2, 3, 2, 0],
        [0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 2, 0, 0, 0],
        [0, 0, 2, 3, 2, 2, 0],
        [0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
      ]
    },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 3, 0, 0, 0, 0, 0],
                [0, 0, 2, 2, 2, 0, 0, 0, 0],
                [0, 0, 0, 2, 0, 0, 0, 0, 0],
                [0, 0, 0, 2, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 3, 0, 0, 0, 0, 0],
                [0, 0, 0, 2, 0, 0, 0, 0, 0],
                [0, 0, 0, 2, 0, 0, 0, 0, 0],
                [0, 0, 2, 2, 2, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 3, 0, 0],
                [0, 0, 0, 0, 0, 2, 2, 2, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 3, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 2, 2, 2, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        }
  ]
}

for example in task_data["train"]:
    analyze_example(np.array(example["input"]), np.array(example["output"]))
