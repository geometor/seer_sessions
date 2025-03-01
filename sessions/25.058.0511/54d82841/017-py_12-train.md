
## example 1
*input:*
```
0 6 6 6 0 0 0 0
0 6 0 6 0 0 0 0
0 0 0 0 0 6 6 6
0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```
*expected output:*
```
0 6 6 6 0 0 0 0
0 6 0 6 0 0 0 0
0 0 0 0 0 6 6 6
0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 0 0 0 4 0
```
*transformed output:*
```
0 6 6 6 0 0 0 0
0 6 0 6 0 0 0 0
4 6 4 6 4 4 4 4
0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 10
**FAILED!**

## example 2
*input:*
```
0 3 3 3 0
0 3 0 3 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```
*expected output:*
```
0 3 3 3 0
0 3 0 3 0
0 0 0 0 0
0 0 0 0 0
0 0 4 0 0
```
*transformed output:*
```
0 3 3 3 0
0 3 0 3 0
4 3 4 3 4
0 0 0 0 0
0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 6
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0 0 0
0 8 8 8 0 0 0
0 8 0 8 6 6 6
0 0 0 0 6 0 6
0 0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0 0
0 8 8 8 0 0 0
0 8 0 8 6 6 6
0 0 0 0 6 0 6
0 0 4 0 0 4 0
```
*transformed output:*
```
0 0 0 0 0 0 0
0 8 8 8 0 0 0
4 0 0 0 4 4 4
0 0 0 0 6 0 6
0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 8
**FAILED!**
