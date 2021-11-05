import os
import sys
import xlsxwriter
from xml.dom import minidom
from colorama import Fore, Back, Style, init, deinit


def get_text(el):
    msg = ''
    for n in el.childNodes:
        if n.nodeType == n.TEXT_NODE:
            msg += n.nodeValue
        elif n.nodeType == n.ELEMENT_NODE:
            msg += get_text(n)
    return msg


init()  # init colorama
dictionaries = []
emptyKeys = []
enKeys = []
prevLang = ""
prevApp = ""
wtf = 0
rootFolder = os.path.dirname(__file__)
appFolders = [
    f.path for f in os.scandir(rootFolder) if f.is_dir()]

print(Fore.LIGHTYELLOW_EX + rootFolder + Style.RESET_ALL)

for appFolder in appFolders:
    fileIndex = 0
    appName = os.path.basename(os.path.normpath(appFolder))
    enKeys = []
    dictionary = dict()
    emptyKeys = []
    prevLang = ""
    langNum = 0
    languages = list(["key"])
    print(Fore.GREEN + "App : " + appName + Style.RESET_ALL)
    for root, dirs, files in os.walk(appFolder):
        for file in files:
            if (file.endswith('.xml')):
                if "string" in file or "array" in file:
                    # print(Fore.GREEN)
                    # print(emptyKeys)
                    # print(Style.RESET_ALL)
                    splitPath = os.path.basename(root).split("-")
                    splitPath.pop(0)  # remove "values" part
                    if len(splitPath) == 2:
                        resLang = splitPath[0] + "-" + splitPath[1]
                    elif len(splitPath) == 1:
                        resLang = splitPath[0]
                    elif len(splitPath) == 0:
                        resLang = "en"
                    else:
                        sys.exit("Unexpected resource folder name.")

                    if(prevLang != resLang):
                        langNum += 1
                        languages.append(resLang)

                    if(prevLang == "en" and resLang != "en"):
                        print(Fore.LIGHTCYAN_EX +
                              "Language switched from default." + Style.RESET_ALL)
                        enKeys = list(dictionary.keys())
                        emptyKeys = list(enKeys)
                    if(prevLang != "en" and prevLang != "" and prevLang != resLang):
                        print(Fore.LIGHTCYAN_EX + "Language switched from " + Fore.LIGHTYELLOW_EX +
                              "non" + Fore.LIGHTCYAN_EX + "-default." + Style.RESET_ALL)
                        for key in emptyKeys:
                            dictionary[key].append("-")
                        emptyKeys = []
                        emptyKeys = list(enKeys)

                    print(Fore.WHITE + resLang + " : " + Style.RESET_ALL + file)
                    xmldoc = minidom.parse(os.path.join(root, file))
                    itemlist = xmldoc.getElementsByTagName('string')
                    arrayStrings = xmldoc.getElementsByTagName('string-array')
                    itemlist = itemlist + arrayStrings
                    prevLang = resLang
                    for item in itemlist:
                        if(item.hasAttribute('translatable') and item.attributes['translatable'].value == "false"):
                            continue
                        if(item.tagName == "string-array"):
                            key = item.attributes['name'].value + " (array)"
                        else:
                            key = item.attributes['name'].value
                        if(len(item.childNodes) > 0):
                            if(item.tagName == "string-array"):
                                value = get_text(item).replace(
                                    "\"", "").replace("\n\n", "|").replace("\n", "|").replace("        ", "")
                            else:
                                value = get_text(item).replace("\"", "")
                            if("@string" in value):
                                continue
                        else:
                            value = " "
                        if key not in dictionary:
                            if(resLang == "en"):
                                dictionary[key] = [value]
                            else:                                       # Item is not already in the dictionary but the language isn't English
                                wtf += 1                                # It doesn't exist under values/strings.xml but there are translations of it
                                print(Fore.RED + str(wtf) + " : " +     # This should not happen normally, herefore the wtf incrementation.
                                      item.attributes['name'].value + Style.RESET_ALL )
                        else:
                            if(len(dictionary[key]) < langNum):
                                dictionary[key].append(value)
                            if key in emptyKeys:
                                emptyKeys.remove(key)
    for key in emptyKeys:
        dictionary[key].append("-")
    emptyKeys = []
    emptyKeys = list(enKeys)
    nameDict = [appName, dictionary, languages]
    dictionaries.append(nameDict)

workbook = xlsxwriter.Workbook(rootFolder + 'data1.xlsx')

for d in dictionaries:
    worksheet = workbook.add_worksheet(d[0])
    dc = d[1]

    row = 0
    col = 0
    for ln in d[2]:
        worksheet.write(row, col, ln)
        col += 1

    col = 0
    row += 1
    for key in dc.keys():
        worksheet.write(row, col, key)
        for item in dc[key]:
            col += 1
            worksheet.write(row, col, item)
        col = 0
        row += 1

workbook.close()
# print(dictionary)
deinit()  # deinit colorama
