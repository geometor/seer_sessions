def analyze_grid_pair(input_grid, output_grid):
    """
    Analyzes an input-output grid pair and returns a detailed report.
    """
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = output_grid.shape

    report = {
        "input_dimensions": (input_rows, input_cols),
        "output_dimensions": (output_rows, output_cols),
        "input_pixels": [],
        "output_pixels": [],
        "differences": []
    }

    for r in range(input_rows):
        for c in range(input_cols):
            if input_grid[r, c] != 0:
                report["input_pixels"].append({
                    "color": int(input_grid[r, c]),
                    "position": (r, c)
                })

    for r in range(output_rows):
        for c in range(output_cols):
            if output_grid[r, c] != 0:
                report["output_pixels"].append({
                    "color": int(output_grid[r, c]),
                    "position": (r, c)
                })

    # find the moved pixels - compare input and output pixels
    for ip in report["input_pixels"]:
      found = False
      for op in report["output_pixels"]:
        if ip["color"] == op["color"] and ip["position"] == op["position"]:
          found = True
          break
      if not found:
          # find the color in output_pixels
          for op in report["output_pixels"]:
              if ip["color"] == op["color"]:
                  report["differences"].append({"color":ip["color"], "from":ip["position"], "to":op["position"]})
                  break
    
    return report

# now use this function for each example:
results = []
task_data = task["train"]
for example in task_data:
  results.append(analyze_grid_pair(example["input"], example["output"]))

print (results)