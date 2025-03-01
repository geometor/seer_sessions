from arc.interface import Riddle

r = Riddle.from_json("d515c4bd.json")

inputs =  [d.input.grid for d in r.train_pairs]
outputs = [d.output.grid for d in r.train_pairs]

predictions = []
for input_data in inputs:
  predictions.append(transform(input_data))
results = code_execution(inputs, outputs, predictions)

for result in results:
    print(f"Example {result['example_index']}: Correct={result['correct']}")
    if not result['correct']:
        print(f"  Input Shape: {result['input_shape']}")
        print(f"  Output Shape: {result['output_shape']}")
        print(f"  Predicted Shape: {result['predicted_shape']}")
        print(f"Difference Array")
        print(result["diff"])