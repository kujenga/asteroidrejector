## My approach

I will be using python analysis libraries along with the original java testing program to evaluate my results.

The program currently reads in the data for each image sequence and the detections list and feeds it into the train method.

This approach uses the stdin/stdout approach given by the provided java test program in order to receive the data.


### [Asteroid Data Hunter microsite](http://www.topcoder.com/asteroids/asteroiddatahunter/)

### [AsteroidRejector Problem Statement](http://community.topcoder.com/longcontest/?module=ViewProblemStatement&rd=15948&pm=13093)

#### image files

raw image data extracted from 4 (FITS) images of the sky, taken roughly 10 minutes apart. The resolution of these extracted patches is fixed (64 x 64 pixels) and the data contains 16 bit values. Each extracted image patch is centered on a detected object. The resolution of the original FITS images are 4110 pixels wide and 4096 pixels in height. If one of the pixels in the 64 x 64 image patch falls outside the bounds of the original FITS image, the pixel value was set to 65535.

#### .det file information

1. Detection Number -- sequential numbering of detection output of the currently used detection software
2. Frame Number -- which observation is this row relevant to (1, 2, 3 or 4)
3. Sexnum -- Source extractor number of the object
4. Time -- Julian date
5. RA -- right ascension of object in decimal hours
6. DEC -- declination in decimal degrees
7. X -- location in pixels of the object in the original FITS image
8. Y -- location in pixels of the object in the original FITS image
9. Magnitude -- brightness of the object in magnitudes
10. FWHM -- full width at half maximum of Gaussian fit in pixels
11. Elong -- ratio of long axis to short axis
12. Theta -- position angle of the long axis
13. RMSE -- error in fit to straight line
14. Deltamu -- from Source Extractor, peak value minus threshold over background
15. Rejected -- this value will be 1 if the operator rejected the detection, 0 otherwise. This column will only be available during the training phase. You need to predict this column
