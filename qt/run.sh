#!/bin/bash
pyuic4 fileList.ui -o fileList.py
pyuic4 rootWindow.ui -o rootWindow.py
python3 app.py
