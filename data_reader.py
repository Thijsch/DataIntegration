# Thijs Ermens
# 20-4-2022
# This script will read in a vcf file and extract the important rows
from os import listdir
from os.path import isfile, join


def vcf_reader(file):
    """
    Functie die een file als input neemt en als output een lijst met
    variabelen uit een vcf file geeft
    :param file: string, pad naar het vcf file
    """
    lijst = []
    chr21 = []
    file = open(file)
    for line in file:
        split = line.split('\t')
        if split[0].startswith("c"):
            lijst.append(split)
            if split[0] == 'chr21':
                chr21.append(split)


if __name__ == '__main__':
    path = "vcfs"
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for file in onlyfiles:
        file = "vcfs/" + file
        vcf_reader(file)
