## Perception

The input and output are sequences of single digits, specifically 0 and 2 in the input, and 0, 2, and 8 in the output. The sequences appear to be space-separated strings representing lists of integers. The core transformation involves changing certain occurrences of the digit '2' in the input sequence to '8' in the output sequence. The digit '0' remains unchanged. The change from '2' to '8' seems conditional, based on the value of the preceding element in the sequence. Specifically, a '2' changes to an '8' if and only if the element immediately before it in the input sequence is also a '2'. The first element of the sequence, having no predecessor, is never changed to '8'. All other elements remain the same as in the input.

## Facts


```yaml
objects:
  - name: sequence_element
    properties:
      - value: integer (0, 2, or 8)
      - position: index (integer >= 0)
  - name: input_sequence
    properties:
      - elements: list of sequence_element (containing only 0s and 2s)
  - name: output_sequence
    properties:
      - elements: list of sequence_element (derived from input_sequence)

relationships:
  - type: precedes
    subject: sequence_element
    object: sequence_element
    details: An element at index i-1 precedes the element at index i.

actions:
  - name: transform_element
    input: current_element (sequence_element from input_sequence)
    input: previous_element (sequence_element from input_sequence, optional)
    output: transformed_element (sequence_element for output_sequence)
    condition: If current_element.value is 2 AND previous_element exists AND previous_element.value is 2
    result_if_true: transformed_element.value is 8
    result_if_false: transformed_element.value is current_element.value

process:
  - name: generate_output_sequence
    steps:
      - Iterate through the input_sequence element by element, keeping track of the index.
      - For each element at index i > 0:
          - Get the current_element (input_sequence[i]).
          - Get the previous_element (input_sequence[i-1]).
          - Apply the transform_element action.
      - For the first element (index 0):
          - The output element value is the same as the input element value.
      - Collect the transformed elements to form the output_sequence.
```


## Natural Language Program

1.  Initialize an empty output sequence.
2.  Iterate through the input sequence of digits from the first element to the last, keeping track of the index of the current element.
3.  For the first element (at index 0), append its value directly to the output sequence.
4.  For each subsequent element (at index `i` > 0):
    a.  Examine the current element's value (`input[i]`) and the previous element's value (`input[i-1]`).
    b.  If the current element's value is `2` AND the previous element's value is also `2`, append `8` to the output sequence.
    c.  Otherwise (if the current element is not `2`, or the previous element is not `2`), append the current element's original value (`input[i]`) to the output sequence.
5.  Return the completed output sequence.