# coin_machine

本代码对应的推送文章：  
  
[硬币系列二 | 从照片中自动检测硬币](https://mp.weixin.qq.com/s?__biz=MzUzNzI4OTAzMQ==&mid=2247484922&idx=1&sn=44c70b760c03d457569721ff2bcd44b3&chksm=fae80dd2cd9f84c42677274e21b8b4a867536bcc3f03196533ca47b38f27cc71538227e08420&token=1953735492&lang=zh_CN#rd)

[硬币系列三 | 硬币自动分类的一个论文复现](https://mp.weixin.qq.com/s?__biz=MzUzNzI4OTAzMQ==&mid=2247484951&idx=1&sn=166db63fc357fe03b9c33c5661ddbb67&chksm=fae80e3fcd9f8729b07f9919d3492f618eb570ec7eea5d8c4798b7c8c9ccf8c7e80205e3e121&token=1953735492&lang=zh_CN#rd)


**简要说明**  
  
* [RFR_GM](https://github.com/divertingPan/coin_machine/tree/master/RFR_GM)：
这篇论文的MATLAB复现：[Image-based coin recognitionusing rotation-invariant region binary patterns based on gradient magnitudes](https://www.sciencedirect.com/science/article/pii/S1047320315001546)

* [classification](https://github.com/divertingPan/coin_machine/tree/master/classification)：
一些其他的分类方法尝试，效果均不好

* [crawler](https://github.com/divertingPan/coin_machine/tree/master/crawler)：
网络爬虫，试图爬取[Ucoin](https://zh-cn.ucoin.net/catalog)网站上的所有硬币图片，但是反爬比较严

* [dataset](https://github.com/divertingPan/coin_machine/tree/master/dataset)：
本次toy项目的自用数据集，其中包括200对自己拍的图片和对应的网站上的图片，已标注。

* [img_test](https://github.com/divertingPan/coin_machine/tree/master/img_test)：
众多杂乱的实验小脚本，提取边缘，图像切割等。包括canny，gabor，hough，lbp，otsu，pHash，polar，resnet，segmemt，sift

* [segmentation](https://github.com/divertingPan/coin_machine/tree/master/segmentation)：
自动裁剪硬币照片周围多余空白
