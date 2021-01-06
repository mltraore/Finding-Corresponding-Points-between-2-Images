# Finding Corresponding Points between 2 Images
Programmed from scracth using python  
# Algorithms
- Harris Corner Detector  
- Normalized Cross Correlation  
# How to use this code
## Finding Corners using HCD Algorithm
```
 python3 harris.py --image image_name --sigma sigma_value --threshold threshold_value   
```
### Example:
```
 python3 harris.py --image images/01.png --sigma 3 --threshold 0.1
```   
## Finding Corresponding Points using HCD and NCC Algorithms
```
python3 demo.py \  
       --image1        image1_name    \  
       --image2        image2_name    \  
       --sigma         sigma value    \  
       --threshold_h   threshold value for harris corner detector \  
       --threshold_d   threshold vaşue for point descriptor       \  
       --min_dist      minimum distance value between points      \  
       --wid           wid value                                  \  
       --graph         graph type [line or point]                       
```
### Example 1: graph = line

```
python3 demo.py --sigma 3 --threshold_h 0.05 --threshold_d 0.5 --graph line
```

### Example 2: graph = point

```
python3 demo.py --sigma 3 --threshold_h 0.05 --threshold_d 0.5 --graph point
```
