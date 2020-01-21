# A small Python - SFTP client



## Description

This is a small Python script to upload / download file or folder between remote server and local filesystem. SSH and SFTP are based on the [Paramiko](http://www.paramiko.org/) Python package. 

## Requirements

+ [Python](http://www.python.org/) 3 

+ [Paramiko](http://www.paramiko.org/)

## Usage

Simply run the script and follow the instructions. 

```shell
python small_sftp.py
```

## Known issues

+ Currently only support single file or single folder, you can edit the code for batch processing.
+ Currently only support single remote server. 
+ There may be permission problems for files and folders in Linux / Unix. 
+ There my be other unknown bugs.

A better version will come soon. Your attention, comments and corrections are welcome.