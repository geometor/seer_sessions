
## example 1
*input:*
```
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0
0 2 0 2 0 2 0 0 0
0 2 0 2 0 2 0 2 0
0 2 0 2 0 2 0 2 0
0 2 0 2 0 2 0 2 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0
0 2 0 2 0 2 0 0 0
0 8 0 2 0 2 0 2 0
0 8 0 8 0 8 0 2 0
0 8 0 8 0 8 0 8 0
```
*transformed output:*
```
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 8 0 2 0 0 0 0 0
0 8 0 8 0 2 0 0 0
0 8 0 8 0 8 0 2 0
0 8 0 8 0 8 0 8 0
0 8 0 8 0 8 0 8 0
```
size: True
palette: True
color count: False
pixels off: 6
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 2 0
0 2 0 2 0 0 0 2 0
0 2 0 2 0 0 0 2 0
0 2 0 2 0 2 0 2 0
0 2 0 2 0 2 0 2 0
0 2 0 2 0 2 0 2 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 2 0
0 2 0 2 0 0 0 2 0
0 2 0 2 0 0 0 2 0
0 8 0 2 0 2 0 8 0
0 8 0 8 0 2 0 8 0
0 8 0 8 0 8 0 8 0
```
*transformed output:*
```
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 8 0 0 0 0 0 2 0
0 8 0 2 0 0 0 8 0
0 8 0 8 0 0 0 8 0
0 8 0 8 0 2 0 8 0
0 8 0 8 0 8 0 8 0
0 8 0 8 0 8 0 8 0
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
0 0 0 0 0 0 0 2 0
0 2 0 0 0 0 0 2 0
0 2 0 0 0 0 0 2 0
0 2 0 0 0 0 0 2 0
0 2 0 0 0 2 0 2 0
0 2 0 2 0 2 0 2 0
0 2 0 2 0 2 0 2 0
0 2 0 2 0 2 0 2 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0
0 2 0 0 0 0 0 2 0
0 2 0 0 0 0 0 2 0
0 2 0 0 0 0 0 2 0
0 2 0 0 0 2 0 8 0
0 8 0 2 0 2 0 8 0
0 8 0 2 0 8 0 8 0
0 8 0 8 0 8 0 8 0
```
*transformed output:*
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0
0 2 0 0 0 0 0 8 0
0 8 0 0 0 0 0 8 0
0 8 0 0 0 0 0 8 0
0 8 0 0 0 2 0 8 0
0 8 0 2 0 8 0 8 0
0 8 0 8 0 8 0 8 0
0 8 0 8 0 8 0 8 0
```
size: True
palette: True
color count: False
pixels off: 8
**FAILED!**
