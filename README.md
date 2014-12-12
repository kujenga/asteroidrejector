# Asteroid Rejector

Aaron Taylor - Data Mining Final Project

#### [Asteroid Data Hunter microsite](http://www.topcoder.com/asteroids/asteroiddatahunter/)

#### [AsteroidRejector Problem Statement](http://community.topcoder.com/longcontest/?module=ViewProblemStatement&rd=15948&pm=13093)

## My approach

I will be using python analysis libraries along with the original java testing program to evaluate my results.

The program currently reads in the data for each image sequence and the detections list and feeds it into the train method.

This approach uses the stdin/stdout approach given by the provided java test program in order to receive the data.

## Setup

I am rewriting the `AsteroidRejectTester.java` file provided byt the competition in python to eliminate the issues with the inter-process communication from the original program that were intended to make it language-independant. This should speed up the execution of the program significantly, and eliminate previously seen issues with blocking on the stdin and stdout streams.

## My Algorithm

The training phase of the algorithm simply import the data and stores it in array format. The 4-image time series data is transformed into a single stream of data that represents more accurately what the progression of changes is between the image. There are a variety of methods to do this which are currently being explored.

After all the training data is inputted, the test data is inputted and stored in a similar format.

Finally, when the getAnswer method is called, the heart of the analysis is performed. 

First, the data is proprocessed in an attempt to remove irrelevant information that may be in the frame, especially anything that does not move over the course of the time series. I subtracted the average pixel over the time series form each corresponding pixel in the picture. I also looked into the scikit learn library's image pre-processing libraries, which deal with pixel graphs and feature patch extraction, although those were not used in my final solution.

For classification, after testing a wide variety of methods I determined that an AdaBoost ensemble classivier using Support Vector Classifiers as base classifiers produced the best result by far. This was a suprise to me as I had expected that a more specific approach, such as the [Linear Discriminant Analysis](http://sebastianraschka.com/Articles/2014_python_lda.html), would perform better because it is more application-specific.

### Other Ideas
- subtract mean pixel value from each image from the total to eliminate anything that is uniform throughout the image
- lots of low-information pixel values left over, eliminate these

## Server background execution
- start program: `screen ./py_run.sh`
- exit screen: `ctrl-a d`
- return `screen -r` (or if `-r` doesn't work `screen -r -x`)

### pyenv on the server
- pyenv activate py3env

## Reference Material

- libraries
  - [Sci-kit Learn LDA tool](http://scikit-learn.org/stable/modules/generated/sklearn.lda.LDA.html)
  - LDA step-through: http://sebastianraschka.com/Articles/2014_python_lda.html
  - [matplotlib PCA](http://matplotlib.org/api/mlab_api.html#matplotlib.mlab.PCA)
  - [scikit-learn PCA](http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)
- research
    - http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=4293066&url=http%3A%2F%2Fieeexplore.ieee.org%2Fxpls%2Fabs_all.jsp%3Farnumber%3D4293066
    - http://stackoverflow.com/questions/1730600/principal-component-analysis-in-python
    -  

#### image files

raw image data extracted from 4 (FITS) images of the sky, taken roughly 10 minutes apart. The resolution of these extracted patches is fixed (64 x 64 pixels) and the data contains 16 bit values. Each extracted image patch is centered on a detected object. The resolution of the original FITS images are 4110 pixels wide and 4096 pixels in height. If one of the pixels in the 64 x 64 image patch falls outside the bounds of the original FITS image, the pixel value was set to 65535.

#### .det file information

1. Unique ID -- An identifier for what detected object a row belongs to
2. Detection Number -- sequential numbering of detection output of the currently used detection software
3. Frame Number -- which observation is this row relevant to (1, 2, 3 or 4)
4. Sexnum -- Source extractor number of the object
5. Time -- Julian date
6. RA -- right ascension of object in decimal hours
7. DEC -- declination in decimal degrees
8. X -- location in pixels of the object in the original FITS image
9. Y -- location in pixels of the object in the original FITS image
10. Magnitude -- brightness of the object in magnitudes
11. FWHM -- full width at half maximum of Gaussian fit in pixels
12. Elong -- ratio of long axis to short axis
13. Theta -- position angle of the long axis
14. RMSE -- error in fit to straight line
15. Deltamu -- from Source Extractor, peak value minus threshold over background
16. Rejected -- this value will be 1 if the operator rejected the detection, 0 otherwise. This column will only be available during the training phase. You need to predict this column


## Results

- pure LDA with raw data in single vectors
    + small score: ``
- pure LDA (normalized data)
    + small score: `score on 762 records:  0.782152230971`
}
- Bagging with LDA as the base classifiers (normalized data)
    + small score: `score on 762 records:  0.793963254593 `
- AdaBoost with Perceptron (normalized data)
    + small score: `score on 762 records: 0.8070866141732284`
- AdaBoost with Stochastic Gradient Descent (normalized data)
    + small score: `score on 762 records: 0.8070866141732284`
- AdaBoost with Support Vector Classifier (normalized data)
    + small score: `score on 762 records: 0.9763779527559056`
    + example score: `score on 4618 records: 0.9653529666522304`
    + example test program score: `Score =  36498.17058103175`

## Conclusions

Support Vector Machines are awesome! Very suprised that AdaBoost performed as well as it did with SVC base classifiers. Would like to get the provided scoring example working to validate the result with their code. 
