
## example 1
*input:*
```
0 0 0 0 0 0
0 0 3 0 0 0
0 3 0 3 0 0
0 0 3 0 3 0
0 0 0 3 0 0
0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0
0 0 3 0 0 0
0 3 4 3 0 0
0 0 3 4 3 0
0 0 0 3 0 0
0 0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0 0
0 0 4 0 0 0
0 4 0 4 0 0
0 0 4 0 4 0
0 0 0 4 0 0
0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 8
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 0 0 0 0
0 0 0 3 0 3 0 0 0 0
0 0 3 0 0 0 3 0 0 0
0 0 0 0 0 3 0 3 0 0
0 0 0 3 0 3 3 0 0 0
0 0 3 3 3 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 0 0 0 0
0 0 0 3 0 3 0 0 0 0
0 0 3 0 0 0 3 0 0 0
0 0 0 0 0 3 4 3 0 0
0 0 0 3 0 3 3 0 0 0
0 0 3 3 3 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0 0 0 0 0 0
0 0 4 0 4 0 0 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 4 0 0 0 4 0 0 0
0 0 0 0 0 4 4 4 0 0
0 0 4 4 4 4 4 0 0 0
0 0 4 4 4 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 19
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0 3 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 3 3 0 3 3 0 3 0 0
3 0 0 3 0 0 3 0 3 0
0 0 0 3 0 0 3 3 0 0
0 0 0 3 0 0 3 0 0 0
0 0 0 3 0 0 3 0 0 0
0 0 0 0 3 3 0 3 0 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 3 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 3 3 0 3 3 0 3 0 0
3 0 0 3 4 4 3 4 3 0
0 0 0 3 4 4 3 3 0 0
0 0 0 3 4 4 3 0 0 0
0 0 0 3 4 4 3 0 0 0
0 0 0 0 3 3 0 3 0 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0 4 0 0 0 0
0 0 0 0 4 4 0 0 0 0
0 4 4 0 4 4 0 4 0 0
4 0 0 4 0 0 4 4 4 0
0 0 0 4 0 0 4 4 0 0
0 0 0 4 0 0 4 4 0 0
0 0 0 4 0 0 4 4 0 0
0 0 0 0 4 4 0 4 0 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 33
**FAILED!**

## example 4
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0
0 0 3 0 0 3 0 0 0 0
0 0 3 0 0 3 0 3 0 0
0 0 3 3 3 3 3 3 3 0
0 0 0 3 0 0 0 0 3 0
0 0 0 3 0 0 0 3 3 0
0 0 0 3 3 0 0 3 0 3
0 0 0 3 0 3 0 0 3 0
0 0 0 0 3 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0
0 0 3 4 4 3 0 0 0 0
0 0 3 4 4 3 0 3 0 0
0 0 3 3 3 3 3 3 3 0
0 0 0 3 0 0 0 0 3 0
0 0 0 3 0 0 0 3 3 0
0 0 0 3 3 0 0 3 4 3
0 0 0 3 4 3 0 0 3 0
0 0 0 0 3 0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 0
0 0 4 4 4 4 4 4 4 0
0 0 4 4 4 4 4 4 4 0
0 0 4 4 4 4 4 4 4 0
0 0 4 4 4 4 4 4 4 0
0 0 4 4 4 4 4 4 4 0
0 0 4 4 4 4 4 4 4 4
0 0 4 4 4 4 4 4 4 0
0 0 0 0 4 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 52
**FAILED!**

## example 5
*input:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 0 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 3 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 3 0 0 0 3 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 3 0 0 0 0
0 0 3 0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 3 3 0 0 3 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 3 3 0 0 3 0 0 3 0 0
0 0 0 0 0 0 0 3 3 3 3 0 3 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 4 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 4 3 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 3 4 4 4 4 4 4 3 0 0 0 0
0 0 0 0 3 0 0 0 3 4 4 4 4 4 4 3 0 0 0 0
0 0 0 0 0 0 0 0 3 4 4 4 4 4 4 3 0 0 0 0
0 0 0 0 0 0 0 0 3 4 4 4 4 4 4 3 0 0 0 0
0 0 3 0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 3 3 4 4 3 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 3 4 4 3 3 0 0 3 0 0 3 0 0
0 0 0 0 0 0 0 3 3 3 3 0 3 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 4 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 4 0
0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0
0 0 0 0 4 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0
0 0 4 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 4 0 0
0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 4 0 0
0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 4 0 0
0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 127
**FAILED!**
