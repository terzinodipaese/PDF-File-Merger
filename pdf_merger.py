import PyPDF2
import sys
import os

def print_helper():
    print("Usage: .\\pdf_merger [--help]")
    print("       .\\pdf_merger --list file1.pdf file2.pdf [file3.pdf ...] --output output.pdf")
    print("> Specify the files to merge with the full path, not just the filename.")
    print("> Use double or single quotes if full path contains empty spaces.")
    print("> Specify just a file name after --output option. If you specify more than one, only the first one will be used.")
    exit()

# verify if --list and --output are both present, otherwise exit
isListOptionPresent = False
isOutputOptionPresent = False
isHelperOptionPresent = False
for arg in sys.argv:
    if arg == "--list":
        isListOptionPresent = True
    if arg == "--output":
        isOutputOptionPresent = True
    if arg == "--help":
        isHelperOptionPresent = True

# --help is used, print usage of pdf_merger script
if isHelperOptionPresent == True:
    print_helper()
    
if isListOptionPresent == False or isOutputOptionPresent == False:
    print("Both --list and --output options are required and mandatory. Please try again.")
    exit()

# if you specify --help, you cannot use --list or --outut as well
if (isHelperOptionPresent == True and isListOptionPresent == True) or (isHelperOptionPresent == True and isOutputOptionPresent == True):
    print("--help option has to be used alone, using --list or --output is not allowed.")
    exit()

# here, we extract pdf files to merge
# just take parameters from 3rd position, since 1st element is script name 
# and 2nd parameter is --list, to introduce list of PDF files to merge
# example: python3 .\pdf_merger --list sample.pdf example.pdf --output fusion.pdf
counter = 2
pdfFiles = []
while sys.argv[counter] != "--output":
    pdfFiles.append(sys.argv[counter])
    counter += 1

# one step forward to take --output option
counter += 1
try:
    outputPdfFile = sys.argv[counter]
# no file after --output option
except IndexError:
    print("Specify a pdf output file.")
    exit()


# user specified no pdf files, therefore nothing to do
if len(pdfFiles) == 0:
    print("No files given on --list option, please perform another attempt with 2 or more files :P")
    exit()

# user just specified a single pdf file, hence nothing to do
if len(pdfFiles) == 1:
    print("It was just specified a single file, merge operation does not make any sense this way. Please try with at least 2 files :)")
    exit()

for pdfFile in pdfFiles:
    if os.path.isfile(pdfFile) == False or os.path.exists(pdfFile) == False:
        print(f'Specified path ({pdfFile}) does not point to a file or the path does not exist. Please check again and retry!')
        exit()

# check if all PDF files on --list option are real PDF files
for pdfFile in pdfFiles:
    try:
        PyPDF2.PdfReader(pdfFile, strict=True)
    except PyPDF2.errors.PdfReadError:
        print(f'Seems like {pdfFile} is not a valid PDF file, even if file extension is .pdf XD')
        exit()

merger = PyPDF2.PdfMerger()

for pdfFile in pdfFiles:
    merger.append(pdfFile)

merger.write(outputPdfFile)

print(f'{outputPdfFile} created successfully')
