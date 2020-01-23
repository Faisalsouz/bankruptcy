# Bankruptcy prediciton

## Project structure

<pre>
.
|-- src
|-- model (local only)
|-- data
    |-- Compustat
    |-- Eikon
    |-- PolishData
    |-- processed
    |-- raw
|-- notebook
    |-- eda (Exploratory Data Analysis)
    |-- poc (Proof-of-Concept)
    |-- modeling
    |-- evaluation
</pre>



## Installation instructions
## Start from scratch
1. Clone this repository on your machine
```
git clone https://github.com/shrnkm/bankruptcy.git
```
2. Install Python: Download and install Anaconda from https://www.anaconda.com/distribution/ that contains all important Python packages.
3. Create your environment: Go to your repository folder and run the following command:
```
conda env create -f install.yml
```

After a successful installation, you should be able to activate the environment
 * On Linux/Mac OS type
```
source activate bank
```
 * On Windows type
```
activate bank
```
## Update your environment
If you just need to update your environment run the following command:
```
conda env update -f install.yml
```

## Dependencies
This list shows all the necessary dependencies to run the Machine Learning Prediction script(s) with the respective version to use (please make sure your version matches :wink:, otherwise we might run into troubles later on):
- keras: 2.3.1
- imblearn: 0.5.0
- matplotlib: 3.1.1
- numpy : 1.17.4
- pandas : 0.25.3
- sklearn: 0.21.3



## Running the Data Extraction script 
In case you are running the extract_data.py script, please make sure to provide at least the (full!) path to the source folder containing the data (you can optionally set the destination folder as a third argument). Don't use relative paths like "../Data". An example would be:
```
python3 extract_data.py /Users/Anna/Documents/Data/ /Users/Anna/Documents/ExtractedData/
```
The source folder must match the following structure (which it should automatically):

<pre>
|-- Data
    |-- Company X's CIK number
        |-- Company's SEC number
                |-- 10-K
                        |-- Actual text file of format: SEC access number - yy - xxx.txt
                |-- 10-Q
</pre>
