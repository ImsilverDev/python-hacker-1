# Python-Hacker 1

This is a Python script that allows you to view and kill running processes on your system. It uses the `psutil` library to get information about running processes and PyQt5 to create the GUI, a simple replica of the famous Process Hacker 2, but in Python.

## Requirements

- Python 3.x
- PyQt5
- psutil

## Usage

To run the script, simply execute the following command:

```
python main.py
```

The script will open a window displaying a list of running processes. You can search for a specific process by typing in the search box. To kill a process, enter its PID in the "Kill Process" section and click the "Kill" button, you can also see various system usages.

The process list is updated every second, so you can see any new processes that start or existing processes that end.

## Images

![image](https://user-images.githubusercontent.com/44844515/226636855-2f3310ee-ab0c-4ce0-9d65-c80133902ae5.png)

## License

This script is licensed under the MIT License. Feel free to use and modify it as you see fit.
