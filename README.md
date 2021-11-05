# VariousTools
Various tools and scripts I developed for my own use.

## auto_clicker.sh
This bash script auto clicks a chosen point every 5 seconds.\
Then restores the pointer location and focus back to the original window.\
If you want to pause the script, turn on Num Lock.\
Mouse will not be moved if a mouse button is pressed down.\
Script will retry in 0.5 seconds in that case.\
Works on Ubuntu 20.04.1 LTS

## export_strings.py
This Python script looks for application folders that contain resource folders.\
Ex. ./Application1/res/values ./Application2/res/values \
Exports all the strings (including string arrays) into an excel workbook. \
Different applications are exported to their own excel sheets. \
Works only on Windows because "os" package behaves differently on Linux. \
Tested with Windows 10 Pro 19043.1288, Python 3.8.2, XlsxWriter 1.3.7, colorama 0.4.4 \
