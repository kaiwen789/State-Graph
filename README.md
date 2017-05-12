# Simulation Trace to GML
This is a Python program translating the trace of the simulator (https://github.com/kaiwen789/simulator_java) into Geography Markup Language (.gml) file.

Usage:

1. Choose 2 for the output mode for the simulator, and generate the simulation trace file.

2. Run the program using Python 3 with the following command:
   python Trace_to_GML.py [trace file] [element list] [output name]
   [Trace file] should be the same format as the input of model checker (mode 2)
   [Element list] is a list of elements of interest, each of them seperate by space
   [Output name] should include .gml

3. Visualize the .gml file using other programs such as yEd graph editor (https://www.yworks.com/products/yed).

* Example: python Trace_to_GML.py trace.txt elements test.gml
![alt text](https://github.com/kaiwen789/State-Graph/blob/master/result.png)
