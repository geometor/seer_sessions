task = 'training_1'
input_grid = task_data[task]['input']
output_grid = task_data[task]['output']
predicted_grid = transform(input_grid)
print(f"example:{task}")
compare_grids(input_grid,output_grid)
compare_grids(input_grid,predicted_grid)
print("---")
