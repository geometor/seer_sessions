
## example 1
*input:*
```
0 2 0
0 0 0
0 0 0
```
*expected output:*
```
0 4 0
0 2 0
0 0 0
```
*transformed output:*
```
4 4 4
0 4 0
0 4 0
```
size: True
palette: True
color count: False
pixels off: 4
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0
0 0 0 0 0
0 0 6 0 0
0 0 0 0 0
0 0 0 0 0
```
*expected output:*
```
4 0 4 0 4
4 0 4 0 4
4 0 4 0 4
0 0 6 0 0
0 0 0 0 0
```
*transformed output:*
```
4 4 4 4 4
0 0 4 0 0
0 0 4 0 0
0 0 4 0 0
0 0 4 0 0
```
size: True
palette: True
color count: False
pixels off: 8
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
*expected output:*
```
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
4 4 4 4 4 4 4 4 4
0 0 4 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 24
**FAILED!**
