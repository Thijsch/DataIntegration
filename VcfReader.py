import tabula as t
import os

class PdfReader:
    def __init__(self, input_files: list[str]):
        self.input_files = input_files        
        self.vcf_data = {}
        
    def read_vcfs(self) -> dict:
        for input_file in self.input_files:
            pass
        return self.vcf_data

	def read_vcf(self, file):
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