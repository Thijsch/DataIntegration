# Author: Janneke Nouwen
# Date: 7-6-22
# Run snpEff on the .vcf files

import subprocess
import glob
import os


class SnpEff:
    def __init__(self, input_path: str, snpeff_path: str):
        self.snpeff_path = snpeff_path
        self.input_path = input_path if not input_path.endswith('/') else input_path[:-1]
        self.output_path = self.input_path + "/output"
        try:
            os.mkdir(self.output_path)
        except FileExistsError:
            raise Exception(f"Make sure directory {self.output_path} does not yet exist. Outputfiles will be placed here.")
        
    def run(self):
        """Run snpeff in input vcf files."""
        processes = []
        input_files = [name for name in glob.glob(f'{self.input_path}/*.vcf')]
        
        for input_file in input_files:
            self.bash_cmd = [
                "java", "-Xmx8g", "-jar", f"{self.snpeff_path}", "GRCh37.75", "-no-downstream", "-no-intergenic",
                "-no-intron", "-no-upstream", "-no-utr", "-verbose", "-noStats", f"{self.input_path}/{input_file}", ">", f"{self.output_path}_out.vcf"
            ]
            processes.append(subprocess.Popen(self.bash_cmd, stdout=subprocess.PIPE))
        
        for process in processes:
            process.wait()
