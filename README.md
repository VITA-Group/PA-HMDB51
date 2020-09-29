# PA-HMDB51 Dataset
This is the repo for PA-HMDB51 (privacy annotated HMDB51) dataset published in our TPAMI paper http://arxiv.org/abs/1906.05675.

The dataset is collected and maintained by the [VITA group](https://vita-group.github.io/) at the University of Texas at Austin.


## Overview
PA-HMDB51 is the very first human action video dataset with both privacy attributes and action labels provided. The dataset contains 515 videos selected from [HMDB51](https://serre-lab.clps.brown.edu/resource/hmdb-a-large-human-motion-database/), each provided with frame-level annotation of five privacy attributes. 
We carefully designed and benchmarked three privacy presenving learning algorithms on our new dataset.

## Privacy attributes
We carefully selected five privacy attributes to annotate. The definition of the five attributes can be found in the following table. 

<!-- ![PA def table](https://github.com/htwang14/PA-HMDB51/blob/master/imgs/def_table.PNG)-->

<table id="Main table">
    <thead>
        <tr>
            <th>Attribute</th>
            <th>Possible Values & Meaning</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=5> Skin Color </td>
            <td> 0: Skin color of the person(s) is/are unidentifiable. </td> 
        </tr>
        <tr>
            <td> 1: Skin color of the person(s) is/are white. </td> 
        </tr>
        <tr>
            <td> 2: Skin color of the person(s) is/are brown/yellow. </td> 
        </tr>
        <tr>
            <td> 3: Skin color of the person(s) is/are black. </td> 
        </tr>
        <tr>
            <td> 4: Skin color of the person(s) is/are black. </td>
        </tr>
        <tr>
            <td rowspan=3> Face </td>
            <td> 0: Invisible (< 10% area is visible). </td> 
        </tr>
        <tr>
            <td> 1: Partially visible (≥ 10% but ≤ 70% area is visible). </td> 
        </tr>
        <tr>
            <td> 2: Partially visible (≥ 10% but ≤ 70% area is visible) </td> 
        </tr>
        <tr>
            <td rowspan=4> Gender </td>
            <td> 0: The gender(s) of the person(s) is/are unidentifiable. </td> 
        </tr>
        <tr>
            <td> 1: The person(s) is/are male. </td> 
        </tr>
        <tr>
            <td> 2: The person(s) is/are female </td> 
        </tr>
        <tr>
            <td> 3: Persons with different genders are coexisting. </td> 
        </tr>
        <tr>
            <td rowspan=3> Nudity </td>
            <td> 0: No-nudity w/ long sleeves and pants. </td> 
        </tr>
        <tr>
            <td> 1: Partial-nudity w/ short sleeves, skirts, or shorts. </td> 
        </tr>
        <tr>
            <td> 2: Semi-nudity w/ half-naked body. </td> 
        </tr>
        <tr>
            <td rowspan=2> Relationship </td>
            <td> 0: Relationship is unidentifiable. </td> 
        </tr>
        <tr>
            <td> 1 Relationship is identifiable. </td> 
        </tr>
    </tbody>
</table>


## Examples
| Frame             |  Action | Privacy Attributes | 
|:-------------------------:|:-------------------------:|:----------------------:|
| ![](https://github.com/htwang14/PA-HMDB51/blob/master/imgs/brush_hair.png) | brush hair | skin color: white <br> face: Invisible <br> gender: female <br> nudity: Semi-nudity <br> relationship: unidentifiable |
| ![](https://github.com/htwang14/PA-HMDB51/blob/master/imgs/pullup.png) | pullup | skin color: white <br> face: Completely visible <br> gender: male <br> nudity: Partial-nudity <br> relationship: unidentifiable |

## Download link
[Google drive](https://drive.google.com/drive/folders/1NH71LxF3rTwTSnxXcA3Wy8GOn6JluGNr?usp=sharing)

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
    title={Privacy-Preserving Deep Action Recognition: An Adversarial Learning Framework and A New Dataset},
    author={Wu, Zhenyu and Wang, Haotao and Wang, Zhaowen and Jin, Hailin and Wang, Zhangyang },
    journal={IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)},
    year={2020}
}
```

## Acknowledgements
We sincerely thank Scott Hoang, James Ault, Prateek Shroff, [Zhenyu Wu](https://wuzhenyusjtu.github.io/) and [Haotao Wang](http://people.tamu.edu/~htwang/) for labeling the dataset.

