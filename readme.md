# SQLite Data Filler

This script functions to enter a lot of data into the SQL Lite 3 database. This program is specifically designed to test the maximum capabilities of the Raspberry Pi 3 in processing (inserting data). This program is made to test the smart door lock gateway application.

To run this application install all required library

```
pip install -r lib.txt
```

Genrate data and inserting the data to database

```
python main.py <number of itteration>
```

Please keep mind, when you creating data first it will take long time to finish. If you already have dataset or want to use already exist dataset in /data-source folder, you can use this script.

```
python insertOnly.py <path to sqlite databse>
```
