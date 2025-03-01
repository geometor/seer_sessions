import numpy as np

# Provided Example Input and Output grids are in previous message

# Helper function to simulate object finding
def simulate_find_objects(grid):
    # simplified object finding for simulation
    objects = {}
    object_id = 0
    for r in range(grid.shape[0]):
      for c in range(grid.shape[1]):
        if grid[r,c] != 0: # simplify by only counting colored cells
          objects.setdefault(object_id, []).append((r,c))
          object_id +=1
    return objects
    

def analyze_example(input_grid, output_grid, predicted_output):

    input_objects = simulate_find_objects(input_grid)
    output_objects = simulate_find_objects(output_grid)
    predicted_objects = simulate_find_objects(predicted_output)

    print(f"Input objects: {len(input_objects)}")
    print(f"Output objects: {len(output_objects)}")
    print(f"Predicted objects: {len(predicted_objects)}")

    input_nonzero_count = np.count_nonzero(input_grid)
    output_nonzero_count = np.count_nonzero(output_grid)
    predicted_nonzero_count = np.count_nonzero(predicted_output)

    print(f"Input Non-zero Pixels: {input_nonzero_count}")
    print(f"Output Non-zero Pixels: {output_nonzero_count}")
    print(f"Predicted Non-zero Pixels: {predicted_nonzero_count}")


    diff_with_output = np.sum(output_grid != predicted_output)
    print(f"Differences between predicted and expected output: {diff_with_output}")

    # check leftmost columns
    #for obj_id, coords in input_objects.items():
    #    leftmost_col = min(c for _, c in coords)
    #    print(f"Object {obj_id} Leftmost Column: {leftmost_col}")


examples = [
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 5, 5, 5, 0, 0],
            [0, 0, 0, 5, 5, 5, 0, 0],
            [0, 0, 0, 5, 5, 5, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 5, 5, 5, 0, 0],
            [0, 0, 0, 5, 5, 5, 0, 0],
            [0, 0, 0, 5, 5, 5, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]),
         "predicted": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 5, 0, 0],
            [0, 0, 0, 0, 5, 5, 0, 0],
            [0, 0, 0, 0, 5, 5, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ])
    },
     {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 5, 5, 0, 0, 7, 7, 0],
            [0, 5, 5, 5, 0, 0, 7, 7, 0],
            [0, 5, 5, 5, 0, 0, 7, 7, 0],
            [0, 5, 5, 5, 0, 0, 7, 7, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 5, 5, 0, 0, 7, 7, 0],
            [0, 0, 5, 5, 0, 0, 7, 7, 0],
            [0, 0, 5, 5, 0, 0, 7, 7, 0],
            [0, 0, 5, 5, 0, 0, 7, 7, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        "predicted": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 5, 5, 0, 0, 0, 7, 0],
            [0, 0, 5, 5, 0, 0, 0, 7, 0],
            [0, 0, 5, 5, 0, 0, 0, 7, 0],
            [0, 0, 5, 5, 0, 0, 0, 7, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
    },
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 8, 8, 8, 0, 0, 0, 0, 3, 3, 0],
            [0, 8, 8, 8, 8, 0, 0, 0, 0, 3, 3, 0],
            [0, 8, 8, 8, 8, 0, 0, 0, 0, 3, 3, 0],
            [0, 8, 8, 8, 8, 0, 0, 0, 0, 3, 3, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 8, 8, 8, 0, 0, 0, 0, 3, 3, 0],
            [0, 0, 8, 8, 8, 0, 0, 0, 0, 3, 3, 0],
            [0, 0, 8, 8, 8, 0, 0, 0, 0, 3, 3, 0],
            [0, 0, 8, 8, 8, 0, 0, 0, 0, 3, 3, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        "predicted" : np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 3, 0],
            [0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 3, 0],
            [0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 3, 0],
            [0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 3, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])
    },
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 7, 7, 7, 7, 0, 0, 0, 0],
            [0, 0, 0, 7, 7, 7, 7, 0, 0, 0, 0],
            [0, 0, 0, 7, 7, 7, 7, 0, 0, 4, 4],
            [0, 0, 0, 7, 7, 7, 7, 0, 0, 4, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 7, 7, 7, 7, 0, 0, 0, 0],
            [0, 0, 0, 7, 7, 7, 7, 0, 0, 0, 0],
            [0, 0, 0, 7, 7, 7, 7, 0, 0, 4, 4],
            [0, 0, 0, 7, 7, 7, 7, 0, 0, 4, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        "predicted": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0],
            [0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0],
            [0, 0, 0, 0, 7, 7, 7, 0, 0, 4, 4],
            [0, 0, 0, 0, 7, 7, 7, 0, 0, 4, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])
    },
]

for i, example in enumerate(examples):
  print(f"Example {i+1}:")
  analyze_example(example["input"], example["output"], example["predicted"])
  print("-" * 20)
