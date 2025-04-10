
## REAL-TIME FACE DETECTORS AND CLASSIFICATION PERFORMANCE IMPLEMENTING RESNET-50 MODEL FOR FACE MASK-WEARING CONDITIONS

The World Health Organization requires the community to wear a face mask to
avoid transmission of COVID-19. The study investigates the performance of face
detectors and evaluates the classification performance based on face maskwearing conditions. The study built a total of 13,806 datasets that recorded an
overall classification performance of 98%. The findings show that Multi-task
Cascade Convolutional Neural Networks outperformed the other face detectors
with an average score of 70% in accordance to distance, angles, occlusions, and
multiple detections across given set conditions. Furthermore, the model recorded
an accuracy performance of 83% for “correct wearing of face mask”, 91% for
“incorrect wearing of face mask”, and 95% for “no face mask”. However, despite
the promising performance rates, the identified best face detector decreases when
the given conditions are set to a higher level. To further improve and optimize
the face mask-wearing conditions, the study highly recommends employing both
statistical and mathematical analysis.

[Click here to read paper](https://jestec.taylors.edu.my/Speccial%20Issue%20ICITE2021/Special%20issue%20ICITE21_01.pdf)




### Conceptual Framework

The resizing of each image and the creation of multiple copies are achieved through the image pyramid method. This method facilitates the generation of bounding boxes and five landmark points for each detected face, a process further enhanced by utilizing Multi-task Cascade Convolutional Neural Networks (MTCNN). The MTCNN operates with 12x12 input size images, surpassing the performance of the P-net by producing bounding boxes with higher confidence values. These high-confidence bounding boxes are then refined by the R-net, which operates with a 24×24 input size, resulting in more precise bounding boxes. Subsequently, these refined bounding boxes are inputted into the O-net, which utilizes a 48×48 input size, and the output from this network is used to categorize face mask-wearing conditions alongside the ResNet-50 object classification model.

![Conceptual Framework]([screenshots/conceptual-framework.png](https://github.com/Senpaixyz/facemask-detection-system/blob/9085ee9e3be1ba2cee45518c3ca94a52db137e3a/screenshots/conceptual-framework.png)


### Datasets Processing
The dataset creation process involved capturing images in various lighting conditions like direct sunlight, indirect sunlight, and dimly lit areas. Images were taken from different angles such as slightly-sided left and right, full-sided left and right, and various angles of looking upward and downward. Occasional obstructions like hair, face shields, and sunglasses were also considered, leading to partial face obstructions. The total dataset consisted of 13,806 images categorized into 8,155 images showing correct face mask wearing (CWFM), 4,122 images depicting improper face mask wearing (IWFM), and 1,529 images showing no face mask (NFM). These images were saved and annotated using XML files, where annotations were done by dragging rectangular bounding boxes to the areas of interest and saving them in their respective XML files.

![Datasets](https://raw.githubusercontent.com/Senpaixyz/facemask-detection-system/master/screenshots/datasets-collection.png?token=GHSAT0AAAAAACKFESKF7PC2SI6QUV2MOJX6ZRXC7FQ)


### CNN Algorithms Analysis

The table presents results from CNN-based object classifiers for different categories including "Correct Wearing," "Incorrect Wearing," and "No Face mask." Each category is evaluated based on precision, recall, F1-score, and overall accuracy across various CNN models such as ResNet-50, InceptionV3, and MobileNetV2. For instance, the "Incorrect Wearing" category shows relatively high precision and recall scores across all models, indicating good performance in identifying instances where masks are worn incorrectly. Conversely, the "No Face mask" category generally has lower precision and recall scores, suggesting challenges in accurately identifying instances where masks are not worn. Overall, ResNet-50 and InceptionV3 demonstrate strong performance across multiple categories, while MobileNetV2 shows slightly lower scores, particularly in the "No Face mask" category.

![Algorithms Analysis](https://raw.githubusercontent.com/Senpaixyz/facemask-detection-system/master/screenshots/results.png?token=GHSAT0AAAAAACKFESKEYXPKZPTZ24O3RSMAZRXDG6A)




### Experimental Analysis

The table provides a comparative analysis of four face detection and recognition algorithms—Haar, DLIB, FaceNet, and MTCNN—across various scenarios, with Precision (Pre) and Accuracy (Acc) measured in percentages. It evaluates their performance at different distances (1m and 2m), angles (0°, 45°, 90°), and under occlusion conditions (Partial Occlusion, Half Face Occlusion). Additionally, it assesses their capability for multiple face detection. MTCNN generally shows superior performance with high Precision and Accuracy percentages, especially in detecting faces at different distances, angles, and under occlusion. However, other algorithms like DLIB and FaceNet exhibit variable performance, with differences in their Precision and Accuracy percentages based on the specific scenario being evaluated.

![Results](https://raw.githubusercontent.com/Senpaixyz/facemask-detection-system/master/screenshots/model-results.png?token=GHSAT0AAAAAACKFESKEN7WWM76QYVQIOQV2ZRXDC2A)




## Conclusion

The study's findings highlight MTCNN as the top-performing face detector. Among object classifiers, ResNet-50 achieved an average classification score of 72.5% for distances and angles, 78% for multiple detections, and 58% for occlusions, indicating limitations in detection under these conditions. Therefore, additional mathematical analysis and algorithms are recommended. However, ResNet-50 excelled with a notable 98% classification performance, especially in detecting specific categories. Specifically, it achieved an average classification performance of 88% in Correct Wearing, 89% in Incorrect Wearing, and 89% in No Face Mask categories across various conditions, demonstrating its effectiveness in these scenarios.

![Conclusion](https://raw.githubusercontent.com/Senpaixyz/facemask-detection-system/master/screenshots/application-interface.png?token=GHSAT0AAAAAACKFESKEGTVEB6MKYLJJYBS4ZRXDJJA)

### Youtube Demo Link

[![IMAGE ALT TEXT HERE](https://i3.ytimg.com/vi/EBQZLtu2o_g/maxresdefault.jpg)](https://www.youtube.com/watch?v=EBQZLtu2o_g&t=36s)

## Tech Stack

**Client:**  KivyMD, Kivy

**Server:** Python3, Tensorflow, OPENCV, PYDL2


## Authors

- [@senpaixyz](https://jestec.taylors.edu.my/Speccial%20Issue%20ICITE2021/Special%20issue%20ICITE21_01.pdf)

