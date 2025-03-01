input_grid = np.array([
    [8, 8, 8, 8, 8, 8, 8, 2, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
])
output_grid = np.array([
    [8, 8, 8, 8, 8, 8, 8, 2, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
])
predicted_grid = transform(input_grid)
print(f"input shape: {input_grid.shape}")
print(f"output shape: {output_grid.shape}")
print(f"predicted shape: {predicted_grid.shape}")
print("Correct Prediction" if np.array_equal(output_grid, predicted_grid)
    else "Incorrect Prediction")