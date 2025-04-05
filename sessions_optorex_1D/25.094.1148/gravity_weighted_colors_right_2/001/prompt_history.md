
## train_1

**input:**
```
2 2 0 1 0 2 2 0 2 2 0 0
```


**output:**
```
2 2 2 2 2 2 1 0 0 0 0 0
```


## train_2

**input:**
```
2 0 2 2 0 0 0 0 2 2 1 2
```


**output:**
```
2 2 2 2 2 2 1 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 2 2 1 0 0 2 0 0 2
```


**output:**
```
2 2 2 2 1 0 0 0 0 0 0 0
```


## train_4

**input:**
```
2 0 0 1 2 1 1 0 2 2 1 0
```


**output:**
```
2 2 2 2 1 1 1 1 0 0 0 0
```


## train_5

**input:**
```
0 1 0 2 0 0 2 2 2 0 1 0
```


**output:**
```
2 2 2 2 1 1 0 0 0 0 0 0
```


## train_6

**input:**
```
0 1 1 0 0 2 0 1 2 2 2 0
```


**output:**
```
2 2 2 2 1 1 1 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 2 2 0 0 0 2
```


**output:**
```
2 2 2 0 0 0 0 0 0 0 0 0
```

**Perception of Task Elements:**

The task involves transforming a sequence of digits.
*   **Input:** A string containing 12 digits (0, 1, or 2) separated by spaces.
*   **Output:** A string containing the same 12 digits, also separated by spaces, but rearranged.
*   **Core Logic:** The transformation appears to be a sorting operation. Observing the examples, the digits in the output string are always arranged in descending order (all 2s first, then all 1s, then all 0s). The count of each digit (0, 1, 2) remains the same between the input and the output.

**Facts:**


```yaml
Objects:
  - InputSequence:
      Type: String
      Content: Sequence of digits (0, 1, 2) separated by spaces.
      Properties:
        - Length: Always 12 digits.
        - Elements: Digits 0, 1, 2.
  - OutputSequence:
      Type: String
      Content: Sequence of digits (0, 1, 2) separated by spaces.
      Properties:
        - Length: Always 12 digits.
        - Elements: Digits 0, 1, 2.
        - Order: Digits are sorted in descending order (2s, then 1s, then 0s).
  - Digit:
      Type: Integer
      PossibleValues: [0, 1, 2]

Relationships:
  - The OutputSequence contains the same digits as the InputSequence.
  - The count of each type of digit (0, 1, 2) is preserved between InputSequence and OutputSequence.
  - The OutputSequence is a reordering (specifically, a descending sort) of the digits present in the InputSequence.

Actions:
  - Parse: Extract individual digits from the InputSequence string.
  - Sort: Arrange the extracted digits in descending numerical order (2 > 1 > 0).
  - Format: Join the sorted digits back into a space-separated string to form the OutputSequence.
```


**Natural Language Program:**

1.  Read the input string representing a sequence of 12 digits separated by spaces.
2.  Extract the individual digits from the input string.
3.  Sort these digits in descending order (place all 2s first, followed by all 1s, and finally all 0s).
4.  Combine the sorted digits back into a string, separating each digit with a space.
5.  Output the resulting string.
