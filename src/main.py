import sys
from repository import repo, _Repository
import os


def splitLine(line):
    temp = line.split(",")
    return temp


def createDB(firstline, cofigfile):
    repo.create_tables()
    vacindex = int(firstline[0]) + 1
    suppindex = int(firstline[1]) + vacindex
    clinindex = int(firstline[2]) + suppindex
    logiindex = int(firstline[3]) + clinindex
    for x in range(1, vacindex):
        temp = splitLine(cofigfile[x])
        repo.vaccines.insert(temp)

    for x in range(vacindex, suppindex):
        temp = splitLine(cofigfile[x])
        repo.suppliers.insert(temp)

    for x in range(suppindex, clinindex):
        temp = splitLine(cofigfile[x])
        repo.clinics.insert(temp)

    for x in range(clinindex, logiindex):
        temp = splitLine(cofigfile[x])
        repo.logistics.insert(temp)


def Orders(ordersfile, outputfile):
    outputlist = 0
    length = len(ordersfile)
    for x in range(0, length):
        temp = splitLine(ordersfile[x])
        if len(temp) == 2:
            outputlist = repo.sendOrder(temp)
        else:
            outputlist = repo.reciveOrder(temp)

        outputfile.write(str(
            str(outputlist[0]) + ',' + str(outputlist[1]) + ',' + str(outputlist[2]) + ',' + str(outputlist[3]) + '\n'))


def main(argv):
    configfile = open(argv[1], "r")
    configfile = configfile.readlines()
    ordersfile = open(argv[2], "r")
    ordersfile = ordersfile.readlines()
    outputfile = open(argv[3], "w")
    firstlineSplited = splitLine(configfile[0])
    createDB(firstlineSplited, configfile)
    Orders(ordersfile, outputfile)
    repo.close()


if __name__ == '__main__':
    main(sys.argv)
    # repository = _Repository()
    # repository.create_tables()
