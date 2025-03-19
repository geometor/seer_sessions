report = {}
task_name = "93b581b8"
for i, example in enumerate(task[task_name]["train"]):

    input_grid = example["input"]
    output_grid = example["output"]
    input_height, input_width = len(input_grid), len(input_grid[0])
    output_height, output_width = len(output_grid), len(output_grid[0])

    height_factor = output_height / input_height
    width_factor = output_width / input_width
    report[i] = {
          "input_shape": (input_height, input_width),
          "output_shape": (output_height, output_width),
        "height_factor": height_factor,
        "width_factor": width_factor,
    }
print (report)
