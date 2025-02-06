# SMS Spam Detector
Dan Lachance, Garret , Hal Williams 

## Requirements
Must use python 3 to execute all code 

Install matplotlib with pip 

``` pip install matplotlib ```

Ensure that each script (kNN.py, naive-bayes.py, thecounter.py, and SMSSpanCollection) are all in the same directory.

## Options

When running kNN.py you will be prompted for a number of stop words.
The Best results were found with 1000-1750 stop words. 
We also reccomend running the program with around 50 - 100 stop words

The results for both 1000 and 50 stop words can be found in our report.

## How to run

#### kNN.py 

Ensure all aditional requirements are read and preformed before running knn.py
Then you can run:

``` python3 kNN.py ```

kNN.py will also call 
``` thecounter.py ``` 
to obtain the number of specified Stop Words

#### naive-bayes.py

No additional requirements are needed for naive-bayes.py. 
All that must be run is:

``` python3 naive-bayes.py ```