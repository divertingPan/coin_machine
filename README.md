# coin_machine

main blog (Chinese)：  
  
[硬币系列二 | 从照片中自动检测硬币](https://divertingpan.github.io/post/coin_detect/)

[硬币系列三 | 硬币自动分类的一个论文复现](https://divertingpan.github.io/post/coin_classifier/)


**Instruction**  
  
* [RFR_GM](https://github.com/divertingPan/coin_machine/tree/master/RFR_GM)：
MATLAB implementation of the paper：[Image-based coin recognitionusing rotation-invariant region binary patterns based on gradient magnitudes](https://doi.org/10.1016/j.jvcir.2015.08.011)

* [classification](https://github.com/divertingPan/coin_machine/tree/master/classification)：
some attempts of classification models

* [crawler](https://github.com/divertingPan/coin_machine/tree/master/crawler)：
a web spider on [Ucoin](https://zh-cn.ucoin.net/catalog) to get the coin image, but the anti-robot rule is strict.

* [dataset](https://github.com/divertingPan/coin_machine/tree/master/dataset)：
a toy dataset with 200 pairs of coins with label

* [img_test](https://github.com/divertingPan/coin_machine/tree/master/img_test)：
some tookits for image processing: canny，gabor，hough，lbp，otsu，pHash，polar，resnet，segmemt，sift

* [segmentation](https://github.com/divertingPan/coin_machine/tree/master/segmentation)：
cut the main body of coin from a picture
