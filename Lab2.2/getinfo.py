from flask import Flask
from flask import jsonify
import sys,os,glob
from re import findall

def getAddr(str):
    hostAdrrDict = {}
    expAddr = 'interface +(.+) *\n(.*\n(?!!))* *ip address (([0-9]\.?)*) +(([0-9]\.?)*)'
    expHost = ' *hostname +(.+)'
    hostname = findall(expHost,str)
    if hostname:
        result = findall(expAddr,str)
        if result:
            hostAdrrDict.setdefault(hostname[0])
            hostAdrrDict[hostname[0]] = result
            return hostAdrrDict
    else:
        return False

def getPath():
    path = os.getcwd()
    print('Default filepath is: '+path)
    tmp = input('Press Enter to use the default filepath or enter the path manually:')
    if tmp != '':
        path = tmp
    return path

def getFileList(path):
    fileList = []
    while len(fileList) == 0:
        fileList = glob.glob(path + '*.txt')
        if len(fileList) == 0:
            print('\nNo txt files found under the specified path.')
            path = getPath()
    return fileList

def getAddressList(fileList):
    addressList = []
    for filePath in fileList:
        with open(filePath) as file:
            data = file.read()
            addresses = getAddr(data)
            if addresses:
                addressList.append(addresses)
    return addressList

def addressListToStr(addressList):
    resultStr = ''
    for dictionary in addressList:
        for item in dictionary:
            resultStr += (str(item)+' = '+str(dictionary[item])+'\n')
    return resultStr

# def getPrintableStr():
#     path = 'C:\\python_local\\projects\\p4ne\Lab1.5\\config_files\\'
#     fileList = getFileList(path)
#     addressList = getAddressList(fileList)
#     printableStr = addressListToStr(addressList)
#     return printableStr

# printableStr = getPrintableStr()

path = 'C:\\python_local\\projects\\p4ne\Lab1.5\\config_files\\'
fileList = getFileList(path)
addressList = getAddressList(fileList)
printableStr = addressListToStr(addressList)

app = Flask(__name__)

@app.route('/')
def info():
    return 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent quis massa tincidunt, auctor odio quis, semper arcu. Cras sit amet condimentum ante. Quisque vel velit nisi. Donec et rhoncus libero, sit amet gravida sem. Ut sodales libero lobortis felis tristique varius. Ut consectetur lacus eget turpis dictum sagittis. Proin vehicula blandit quam ac congue. Integer efficitur metus sed elit rutrum tincidunt. Vivamus at facilisis risus, lacinia convallis orci. Integer in gravida lectus, eget viverra dui. Sed blandit lacinia porta. Suspendisse lacus libero, rutrum a lorem ac, placerat rhoncus metus. Nam sit amet ex tortor. Proin eget felis tortor.'

@app.route('/python')
def python():
    return jsonify(str(sys.__dict__))

@app.route('/configs')
def configs():
    hostList = []
    for dictionary in addressList:
        for hostname in dictionary.keys():
            hostList.append(hostname)
    return jsonify(hostList)

@app.route('/configs/<hostname>')
def ip_info(hostname):
    for dictionary in addressList:
        for h in dictionary.keys():
            if h == hostname:
                return jsonify(dictionary[h])
    return jsonify('Not found')

@app.route('/iplist')
def ipList():
    return printableStr

if __name__=='__main__':
    app.run(debug=True)


