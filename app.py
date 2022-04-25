from PDF_reader import PdfReader


def main():
    input_files = ["/home/janneke/Documents/Data_integratie/PGPC-13.pdf"]
    pdf_data = PdfReader(input_files=input_files)
    # Inserter.insert(pdf_data)
    
    
def reformat_data(pdf_data: dict[str, dict[str, str]]):
    """Format data to 2d lists with uuid's"""
    pass
    
if __name__ == "__main__":
    main()