![image](https://github.com/karthikstar/SC3020_Project2/assets/22176064/656dccc2-31d4-423a-bec6-4c7abfae6b6c)## SC3020 Group 17 - SQL Query Explainer
<p align="center">
  <img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/260c050e-8b43-4f75-add2-688966725b7e>
</p>


## Prerequisites
### Software
1. PostgreSQL [Download](https://www.postgresql.org/download/)
2. pgAdmin4 [Download](https://www.pgadmin.org/download/) (for uploading databases into PostgreSQL)
3. Python IDE [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/?section=windows) (Optional - if running project from terminal)
4. Python Installment [Download](https://www.python.org/downloads/) (compatible up to 3.11)
#### Uploaded Databases to be loaded into PostgreSQL: [Database Folder](https://drive.google.com/drive/folders/103s8UBb36gKkrH6ORD5Vh8oYhqHZt1hN?usp=drive_link)

## Before running our Project Code
1. Ensure that you have installed the above software into your system.
2. Open up the Database Folder link above & download the files in (.zip).
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/8c4f8f18-e571-4ea7-b08d-ef69eb39fd84>
</p>
3. Unzip the downloaded .zip file & ensure that you have the 8 .csv databases below. 
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/8c4f8f18-e571-4ea7-b08d-ef69eb39fd84>
</p>
4. Open up pgAdmin4.
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/8c4f8f18-e571-4ea7-b08d-ef69eb39fd84>
</p>
5. Access your PostgreSQL through the left menu & expand the menu to see the 'Databases' Icon.
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/8c4f8f18-e571-4ea7-b08d-ef69eb39fd84>
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/8c4f8f18-e571-4ea7-b08d-ef69eb39fd84>
</p>
6. Right click 'Databases' to show the menu and access the database creation menu. 
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/8c4f8f18-e571-4ea7-b08d-ef69eb39fd84>
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/8c4f8f18-e571-4ea7-b08d-ef69eb39fd84>
</p>
7. Enter 'TPC-H' as the database name (or any names you like) & click 'Save'.
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/8c4f8f18-e571-4ea7-b08d-ef69eb39fd84>
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/8c4f8f18-e571-4ea7-b08d-ef69eb39fd84>
</p>
8. Now, you should see your created database name in the left menu. Right click on it & access the 'Query Tool' option.
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/8c4f8f18-e571-4ea7-b08d-ef69eb39fd84>
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/8c4f8f18-e571-4ea7-b08d-ef69eb39fd84>
</p>

## How to Run our Project (2 Ways)

### Using Terminal/Command Prompt
1. Open Terminal/Command Prompt

<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/8c4f8f18-e571-4ea7-b08d-ef69eb39fd84>

<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/cce40d56-9545-470d-9298-d668015ed6e7>
</p>

2. Enter the following commands in order:
```sh
cd C:/[file_directory_of_project]
pip install -r requirements.txt
python project.py
```

### Using a Python IDE (eg. PyCharm)
1.	Ensure that there is a requirements.txt file in the same folder as the 3 python files containing the following:
```sh
numpy==1.26.2
psycopg2==2.9.5
PyQt6==6.4.0
PyQt6-Qt6==6.6.0
PyQt6-sip==13.6.0
pyqtgraph==0.13.1
```

2.	Open the Project Folder in your IDE
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/cab0d4ca-62dc-4950-ae4b-8d3484ea8f55>
</p>


3.	Two warnings should appear in yellow highlights at the top of the code. Click 'Configure Python Interpreter'.
<p align="center">
<img src = https://user-images.githubusercontent.com/49341007/202510527-1cdf72ed-2617-4776-8930-6fc6fa16ffb4.png>
</p>


4.	Click Add New Interpreter > Add Local Interpreter
<p align="center">
<img src = https://user-images.githubusercontent.com/49341007/202510538-297c0729-3176-4d0f-86bb-05db3daa99a3.png>
</p>


5.	Select Virtualenv Environment, location is current directory \venv and base interpreter is your latest Python Interpreter found in your system (avoid Python 3.12).
<p align="center">
</p>


6.	Select 'OK' and 'venv' folder should be created
<p align="center">
<img src = https://user-images.githubusercontent.com/49341007/202510596-4a0d2141-882c-4f39-ac0e-dd9714f70503.png>
</p>


7.	Wait for Indexing to Finish
<p align="center">
<img src = https://user-images.githubusercontent.com/49341007/202510617-7159ca4a-e933-4cab-9236-667796b0ca80.png>
</p>


8.	The other warning will be fixed through installing the required packages.
<p align="center">
</p>


9.	Click 'Install requirements'.
<p align="center">
<img src = https://user-images.githubusercontent.com/49341007/202510640-3fc33701-54d6-418d-957e-e9ea4aa612f6.png>
</p>


10.	Install all requirements.
<p align="center">
</p>


11.	Wait for the installation to finish.
<p align="center">
</p>


12.	Run the Project from our 'project.py' file.
<p align="center">
<img src = https://user-images.githubusercontent.com/49341007/202510687-2fef0618-6001-472b-933b-8ff4ed9c1b27.png>
</p>
