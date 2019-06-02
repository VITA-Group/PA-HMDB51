# PA-HMDB51
This is the repo for PA-HMDB51 (privacy attribute HMDB51) dataset.


## Overview
PA-HMDB51 is the very first human action video dataset with both privacy attributes and action labels provided. The dataset contains 592 videos selected from HMDB51, each provide with frame-level annotation of five privacy attributes.

## Privacy attributes
We carefully selected five privacy attributes, which are originally from the 68 privacy attributes defined in [1], to annotate. The definition of the five attributes can be found in the following table. 

![PA def table](https://github.com/htwang14/PA-HMDB51/blob/master/imgs/def_table.PNG)

## Examples
| Frame             |  Action | Privacy Attributes | 
|:-------------------------:|:-------------------------:|:----------------------:|
| ![](https://github.com/htwang14/PA-HMDB51/blob/master/imgs/brush_hair.png) | brush hair | skin color: white <br> face: no <br> gender: female <br> nudity: level 2 <br> relationship: no |
| ![](https://github.com/htwang14/PA-HMDB51/blob/master/imgs/pullup.png) | pullup | skin color: white <br> face: no <br> gender: male <br> nudity: level 1 <br> relationship: no |

## Download link


## Citation
If you use this dataset, please cite the following
```
@article{
    blablabla
}
```

## Reference
 [1] T. Orekondy, B. Schiele, and M. Fritz, “Towards a visual privacyadvisor: Understanding and predicting privacy risks in images,” in Proceedings of the IEEE International Conference on Computer Vision(ICCV), 2017, pp. 3686–3695.