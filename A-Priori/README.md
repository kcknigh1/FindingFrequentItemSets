A-Priori Algorithem

This prigram uses the A-Priori algorithem fo find the frequent item set
Uses s values of 2, 5, 10, 25, and 50
It calculates the memory requirments and time for the s values
The results are stored in the results dir


src/input_generater.py 
This is used to create the data that will be run through both algorithems.  It creates that file with the data in data/test_data.txt
run with
$ python src/input_generater.py

src/a_priori.py
This is the main file to run it contains the algorithm and it uses the input from the test_data.txt that was created above.
The indivadule results are printed to files labled with there S value the results_all
file contains a compiled list of all values from all that differnt S Vaules
usage: $ python src/a_priori.py
