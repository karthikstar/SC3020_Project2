## SC3020 Group 17 - SQL Query Explainer


## Prerequisites
### Software
1. PostgreSQL [Download](https://www.postgresql.org/download/) (**Remember to note down the password & port number inputted during installation**)
2. pgAdmin4 [Download](https://www.pgadmin.org/download/) (for uploading databases into PostgreSQL)
3. Python IDE [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/?section=windows) (Optional - if running project from terminal)
4. Python Installment [Download](https://www.python.org/downloads/) (compatible up to 3.11)
#### Uploaded Databases to be loaded into PostgreSQL: [Database Folder](https://drive.google.com/drive/folders/103s8UBb36gKkrH6ORD5Vh8oYhqHZt1hN?usp=drive_link)

## Before running our Project Code
1. Ensure that you have installed the above software into your system.
2. Open up the Database Folder link above & download the files in (.zip).
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/1e730d25-0a9a-4877-88a7-22489c7037fd>
</p>

3. Unzip the downloaded .zip file & ensure that you have the 8 .csv databases below. 
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/175b73a8-48e1-46a3-b43c-9d318ea73398>
</p>

4. Open up pgAdmin4.
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/159fc926-e493-4622-93e5-268e85c2866d>
</p>

5. Access your PostgreSQL through the left menu & expand the menu to see the 'Databases' Icon.
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/3a847a1d-8b01-42ce-83fc-338f104fee07>
</p>

<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/5db4d601-55fe-48d6-9741-5ac9b4c72f0c>
</p>

6. Right-click 'Databases' to show the menu and access the database creation menu. 
<p align="center">
<img src = >
</p>

7. Enter 'TPC-H' as the database name (or any names you like) & click 'Save'.
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/217d1f6e-9906-410c-8dbc-0e29efda482a>
</p>
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/4bb3de2d-9f2c-4489-b6cb-3e1fe1d8f141>
</p>

8. Now, you should see your created database name in the left menu. Right click on it & access the 'Query Tool' option.
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/026d3b74-575f-44c9-b0f6-d6abb93e0e33>
</p>
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/0b20f1ba-1773-4c3f-9449-2266173663dd>
</p>

9. Access the code stored in the file schema.sql under our project directory's database folder. Copy this code into the Query Tool and hit the run/F5 button.
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/9c8e11ae-298d-4820-8b9c-3650b0dfd565>
</p>
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/5f90d9cb-25b9-4e46-a294-d936464414e4>
</p>

10. Now, the respective tables should be created under the created 'TPC-H' database in the left menu.
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/87fa1e7d-0a19-4a72-8397-9cde53bdfda5>
</p>

11. Right-click any of the table names & access the 'Import/Export Data..' menu.
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/56932759-bd04-4f70-88d7-183a49863ae9>
</p>

12. Enter the entries in the menu with the following configurations.
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/c9355613-d375-4123-928e-814d81888637>
</p>

<p align="center">
Filename: Select the correct respective .csv database file for your selected table, then click 'Ok'.  <br>   
Format: CSV
</p>

<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/bfc510b7-526c-4dc0-a1c7-c595accfb0a9>
</p>

<p align="center">
OID: Off <br>
Header: Off <br>
Delimiter: | <br>
Quote: " <br>
Escape: ' <br>
NULL Strings: <br>
</p>

<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/d5a202fc-0128-43f1-bc86-cb04d93dc8be>
</p>

13. Repeat Steps 11-12 for all 7 other tables in the database **IN THR ORDER region, nation, customer, supplier, part, partsupp, orders, lineitem**!
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/e0206743-9b9c-497f-a34e-98343acf1abb>
</p>

14. Congrats! Now all 8 databases should be loaded into your PostgreSQL database. Our project is now ready to be ran!


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
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/4310fcb1-c2d6-45de-8272-eb419563ee26>
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

13. Login to the app using the login details you created during your installation of PostgreSQL, the password & port number. Default options for host and username would be pre-filled in the window.
<p align="center">
<img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/250db4e8-579a-488a-88c9-43e5b03c0e55>
</p>

14. You should now be on the main page of our application. Ready to run your own queries?
<p align="center">
  <img src = https://github.com/karthikstar/SC3020_Project2/assets/22176064/260c050e-8b43-4f75-add2-688966725b7e>
</p>
