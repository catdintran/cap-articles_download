# PDF to HTML (or TXT - commented out) formats with pdfminer.six
import os, platform
import subprocess
import shutil


def changeNameToCountry():
    # clear/retrieve txt file
    txt_list = [txt for txt in os.listdir(output) if txt.endswith('.txt')]
    newOutput = os.getcwd() + '\\txt\\'
    # iterate and process txt_list to new txt folder
    for f in txt_list:
        fp = open(output + f)
        fileName = ''
        docDate = ''
        for i, line in enumerate(fp):
            # retrieve doc date from 1st line
            if i == 0:
                # print(line.replace('\n', ''))
                docDate = line.replace('\n', '')
                # retrieve doc title from range(2,4)
            if i in range(2, 4) and 'IMF' not in line:
                # make sure line is not an empty line
                if line.strip():
                    fileName = line.replace('\n', '') + '--' + docDate
            if i > 4:
                break
        fp.close()

        if not os.path.exists(newOutput):
            os.makedirs(newOutput)

        shutil.copy(output + f, newOutput + fileName + '.txt')


def processPdfToTxt():
    # check platform system Windows/Macs
    xpdfPath = ''
    if platform.system() == 'Windows':
        xpdfPath = os.getcwd() + '\\xpdfbin-win-3.04\\bin64\\'
    else:
        xpdfPath = os.getcwd() + '\\xpdfbin-mac-3.04\\bin64\\'

    # store .pdf files from input
    doc_list = [pdf for pdf in os.listdir(input) if pdf.endswith('.pdf')]
    # iterate and process doc_list to txt file
    for doc in doc_list:
        subprocess.call('pdftotext ' + input + doc + ' ' + output + doc.replace('.pdf', '.txt'), cwd=xpdfPath,
                        shell=True)


if __name__ == "__main__":
    # pdf files dir
    input = os.getcwd() + '\\pdf\\'
    # final dir after converted
    output = os.getcwd() + '\\tmp\\'

    # check/create if output folder exist
    if not os.path.exists(output):
        os.makedirs(output)

    processPdfToTxt()

    #######################################
    # format txt file name to country name
    #######################################

    changeNameToCountry()