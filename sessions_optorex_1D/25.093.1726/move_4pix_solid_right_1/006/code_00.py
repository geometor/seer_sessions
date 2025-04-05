import numpy as np

def analyze_shift(input_str, output_str):
    input_arr = np.array(list(map(int, input_str.split())))
    output_arr = np.array(list(map(int, output_str.split())))

    input_indices = np.where(input_arr != 0)[0]
    output_indices = np.where(output_arr != 0)[0]

    shifts = []
    if len(input_indices) == len(output_indices) and len(input_indices) > 0:
        # Assuming order is preserved
        shifts = output_indices - input_indices

    values_match = np.array_equal(input_arr[input_indices], output_arr[output_indices])
    length_match = len(input_arr) == len(output_arr)
    is_1d = input_arr.ndim == 1 # Check if input *string* parses to 1D

    return {
        "input_indices": input_indices.tolist(),
        "output_indices": output_indices.tolist(),
        "shifts": shifts.tolist() if isinstance(shifts, np.ndarray) else shifts,
        "all_shifts_equal_4": all(s == 4 for s in shifts) if shifts else True,
        "values_match": bool(values_match),
        "length_match": length_match,
        "length": len(input_arr),
        "is_1d_parse": is_1d
    }

train_inputs = [
    "0 0 0 0 0 0 8 0 0 0 0 0",
    "0 0 9 0 0 0 0 0 0 0 0 0",
    "2 2 2 2 2 2 0 0 0 0 0 0",
    "0 0 0 0 2 0 0 0 0 0 0 0",
    "0 0 0 0 0 3 3 0 0 0 0 0",
    "0 0 0 0 0 7 0 0 0 0 0 0",
    "0 0 3 3 3 3 3 3 0 0 0 0"
]

train_outputs = [
    "0 0 0 0 0 0 0 0 0 0 8 0",
    "0 0 0 0 0 0 9 0 0 0 0 0",
    "0 0 0 0 2 2 2 2 2 2 0 0",
    "0 0 0 0 0 0 0 0 2 0 0 0",
    "0 0 0 0 0 0 0 0 0 3 3 0",
    "0 0 0 0 0 0 0 0 0 7 0 0",
    "0 0 0 0 0 0 3 3 3 3 3 3"
]

results = []
for i in range(len(train_inputs)):
    analysis = analyze_shift(train_inputs[i], train_outputs[i])
    results.append(analysis)

print(results)
