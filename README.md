# PA-HMDB51
This is the repo for PA-HMDB51 (privacy attribute HMDB51) dataset published in our paper http://arxiv.org/abs/1906.05675

This dataset is collected and maintained by the [VITA group] (https://www.atlaswang.com/group) at the CSE department of Texas A&M University.


## Overview
PA-HMDB51 is the very first human action video dataset with both privacy attributes and action labels provided. The dataset contains 592 videos selected from HMDB51 [1], each provided with frame-level annotation of five privacy attributes. We evaluated the visual privacy algorithms proposed in [3] on PA-HMDB51.

## Privacy attributes
We carefully selected five privacy attributes, which are originally from the 68 privacy attributes defined in [2], to annotate. The definition of the five attributes can be found in the following table. 

![PA def table](https://github.com/htwang14/PA-HMDB51/blob/master/imgs/def_table.PNG)

## Examples
| Frame             |  Action | Privacy Attributes | 
|:-------------------------:|:-------------------------:|:----------------------:|
| ![](https://github.com/htwang14/PA-HMDB51/blob/master/imgs/brush_hair.png) | brush hair | skin color: white <br> face: no <br> gender: female <br> nudity: level 2 <br> relationship: no |
| ![](https://github.com/htwang14/PA-HMDB51/blob/master/imgs/pullup.png) | pullup | skin color: white <br> face: no <br> gender: male <br> nudity: level 1 <br> relationship: no |

## Download link
[Google drive](https://drive.google.com/drive/u/0/folders/1OtQLtq9QxdPHaH1gUcFZiylBMXJhn2dm)

## Label format
The attributes usually don't change that much across a video, so we only need to label the starting and ending frame index of each attribute. 
For example, if a video has 100 frames, and we can see a complete human face in the first 50 frames while a partial face in the next 50 frames, we would label [face: complete, s: 0, e: 49], [face: partial, s: 50, e: 99], where 's' is for 'starting' frame and 'e' is for 'ending' frame. 
Note that each attribute is labeled separately.
For instance, if the actor's skin color is visible in all 100 frames in the same video (assume the actor is white), we will label [skin color: white, s: 0, e: 99]. 
The privacy attributes for all 'brush hair' videos are in brush_hair.json, similar with all other actions.

## Citation
If you use this dataset, please cite the following
```
@article{wang2019privacy,
 title={Privacy-Preserving Deep Visual Recognition: An Adversarial Learning Framework and A New Dataset},
 author={Wang, Haotao and Wu, Zhenyu and Wang, Zhangyang and Wang, Zhaowen and Jin, Hailin},
 journal={arXiv preprint arXiv:1906.05675},
 year={2019}
}
```

## Acknowledgements
We sincerely thank Scott Hoang, James Ault, Prateek Shroff, [Zhenyu Wu](https://wuzhenyusjtu.github.io/) and Haotao Wang for labeling the dataset.

## Reference
[1] H. Kuehne, H. Jhuang, E. Garrote, T. Poggio, and T. Serre, “Hmdb:
a large video database for human motion recognition,” in Proceedings of the IEEE International Conference on Computer Vision (ICCV),
2011, pp. 2556–2563. <br />
[2] T. Orekondy, B. Schiele, and M. Fritz, “Towards a visual privacyadvisor: Understanding and predicting privacy risks in images,” in Proceedings of the IEEE International Conference on Computer Vision(ICCV), 2017, pp. 3686–3695. <br />
[3] Z. Wu, Z. Wang, Z. Wang, and H. Jin, “Towards privacy-preservingvisual recognition via adversarial training: A pilot study,” in Proceedings of the European Conference on Computer Vision (ECCV), 2018, pp. 606–624. <br />
