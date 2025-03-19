import numpy as np

def analyze_grid_diff(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    if input_grid.shape != output_grid.shape:
        return "Different Shapes"

    diff = input_grid != output_grid
    changed_pixels = np.where(diff)
    num_changed = len(changed_pixels[0])
    change_details = []

    for i in range(num_changed):
        row, col = changed_pixels[0][i], changed_pixels[1][i]
        initial_val = input_grid[row, col]
        final_val = output_grid[row, col]
        change_details.append(
            {
                "row": row,
                "col": col,
                "initial_color": int(initial_val),
                "final_color": int(final_val),
            }
        )

    return {
        "num_changed": num_changed,
        "change_details": change_details,
    }

def get_object_locations(grid, object_color):
    grid = np.array(grid)
    object_indices = np.where(grid == object_color)
    locations = []
    for i in range(len(object_indices[0])):
      locations.append((object_indices[0][i],object_indices[1][i]))

    return locations

train_ex = task["train"]
results = {}
for i, ex in enumerate(train_ex):
  input_grid = ex["input"]
  output_grid = ex["output"]
  predicted = transform(input_grid)

  results[f"Example {i+1}"] = {
      "diff_actual": analyze_grid_diff(input_grid, output_grid),
      "diff_predicted": analyze_grid_diff(predicted, output_grid)
  }
  print(f"Example {i+1}:")
  print(f"Blue Objects: {get_object_locations(input_grid, 1)}")
  print(f"Azure Objects: {get_object_locations(output_grid, 8)}")
  print(f"Red Objects: {get_object_locations(input_grid, 2)}")


print(results)
