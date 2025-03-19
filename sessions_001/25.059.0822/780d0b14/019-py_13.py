def get_input_shape(task, example_index, input_or_output):
    if input_or_output == "input":
        return task["train"][example_index]["input"].shape
    else:
        return task["train"][example_index]["output"].shape
        
def get_color_counts(grid):
    # Count occurrences of each color in the grid
    unique, counts = np.unique(grid, return_counts=True)
    return dict(zip(unique, counts))

def check_colors_present(task, example_index, input_or_output):
  if input_or_output == "input":
      grid = task["train"][example_index]["input"]
  else:
      grid = task["train"][example_index]["output"]
  
  colors = get_color_counts(np.array(grid))
  print(f'{input_or_output} colors: {colors}')