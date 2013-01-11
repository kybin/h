import hou

def setVariable(name, value):
    hou.hscript("set -g {name} = {value}".format(name=name, value=value))
    print("set {name} = {value}".format(name=name, value=value))

