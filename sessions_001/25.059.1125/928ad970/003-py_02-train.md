
## example 1
*input:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 1 0 1 0 0 0 0 0
0 5 0 0 0 1 0 1 0 0 0 5 0
0 0 0 0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 1 0 0
0 0 1 0 0 0 0 0 0 0 1 0 0
0 0 1 0 0 1 1 1 0 0 1 0 0
0 0 1 0 0 1 0 1 0 0 1 0 0
0 5 1 0 0 1 0 1 0 0 1 5 0
0 0 1 0 0 1 1 1 0 0 1 0 0
0 0 1 0 0 0 0 0 0 0 1 0 0
0 0 1 0 0 0 0 0 0 0 1 0 0
0 0 1 1 1 1 1 1 1 1 1 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 0 0 0 0 0
0 0 0 0 1 1 1 1 1 0 0 0 0
0 0 0 0 1 1 1 1 1 0 0 0 0
0 5 0 0 1 1 1 1 1 0 0 5 0
0 0 0 0 1 1 1 1 1 0 0 0 0
0 0 0 0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 48
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 3 0 3 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0
0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 3 0 0 0 0 0 0 3 0 0 0
0 5 3 0 3 3 3 0 0 3 0 0 0
0 0 3 0 3 0 3 0 0 3 0 0 0
0 0 3 0 3 3 3 0 0 3 0 0 0
0 0 3 0 0 0 0 0 0 3 5 0 0
0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0
0 5 0 3 3 3 3 3 0 0 0 0 0
0 0 0 3 3 3 3 3 0 0 0 0 0
0 0 0 3 3 3 3 3 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 45
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 4 0 0 0 0 0 0
0 0 0 0 4 0 0 4 0 0 0 0 5 0
0 0 0 0 4 0 0 4 0 0 0 0 0 0
0 5 0 0 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 4 4 4 0 0
0 0 4 0 0 0 0 0 0 0 0 4 0 0
0 0 4 0 4 4 4 4 0 0 0 4 0 0
0 0 4 0 4 0 0 4 0 0 0 4 5 0
0 0 4 0 4 0 0 4 0 0 0 4 0 0
0 5 4 0 4 4 4 4 0 0 0 4 0 0
0 0 4 0 0 0 0 0 0 0 0 4 0 0
0 0 4 0 0 0 0 0 0 0 0 4 0 0
0 0 4 0 0 0 0 0 0 0 0 4 0 0
0 0 4 4 4 4 4 4 4 4 4 4 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 4 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 4 4 0 0 0 5 0
0 0 0 4 4 4 4 4 4 0 0 0 0 0
0 5 0 4 4 4 4 4 4 0 0 0 0 0
0 0 0 0 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 56
**FAILED!**
