# Example Data (Recreated here for clarity)
train_ex = [
    (np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,2,2,2,0,0],[0,0,0,0,2,0,0,0,0],[0,0,0,0,0,0,0,0,0]]),
     np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,2,2,2,2,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]])),
     (np.array([[0,0,0,0,0,0,0],[0,0,0,2,2,0,0],[0,0,0,2,0,0,0],[0,0,0,0,0,0,0]]),
     np.array([[0,0,0,0,0,0,0],[0,0,2,2,2,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])),
      (np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,2,2,2,2,0,0],[0,0,0,2,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]),
       np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,2,2,2,2,2,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]))
]

results = []
for i, (input_grid, expected_output) in enumerate(train_ex):
    predicted_output = transform(input_grid)
    
    red_objects_input = find_objects(input_grid, 2)
    red_moved_pixels = []
    for obj in red_objects_input:
        for r,c in obj:
            adj_colors = get_adjacent_colors(input_grid,r,c)
            if input_grid[r,c] != predicted_output[r,c]:
                red_moved_pixels.append( ((r,c), adj_colors))


    results.append(
        {
            "example": i + 1,
            "input_grid_desc": describe_grid(input_grid),
            "expected_output_desc": describe_grid(expected_output),
            "predicted_output_desc": describe_grid(predicted_output),
            "red_objects_input": red_objects_input,
            "red_moved_pixels_adjacencies": red_moved_pixels,
            "correct": np.array_equal(predicted_output, expected_output),
        }
    )

for r in results:
    print(r)