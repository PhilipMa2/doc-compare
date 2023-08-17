from pypdf import PdfReader
import re

def increase_left(sec):
    pos = sec.find('\\')
    return str(int(sec[:pos])+1) 

def increase_right(sec):
    pos = sec.rfind('\\')
    return sec[:pos+2] + str(int(sec[pos+2:])+1)

def sync_mid(sec2, sec3):
    pos = sec3.find('\\')
    mid = sec2[sec2.find('.')+1:]
    return sec3[:pos+2] + mid

if __name__ == "__main__":
    old_pdf = PdfReader('A.pdf')
    new_pdf = PdfReader('B.pdf')
    old_text = ''
    new_text = ''
    for page in old_pdf.pages:
        old_text += page.extract_text()
    for page in new_pdf.pages:
        new_text += page.extract_text()
    
    old_text = old_text[re.search('1 \S', old_text).start():]
    old_texts = []
    delimiter = ['2','1\.1','1\.1\.1']
    next_section = re.search(r'[^表\.](?:' + '|'.join(delimiter) + r') \S', old_text)
    while next_section:
        curr_section = old_text[:next_section.start()+1]
        old_texts.append(curr_section)
        old_text = old_text[next_section.start()+1:]
        section_num = old_text[:old_text.find(' ')]
        counts = section_num.count('.')
        if counts == 0:
            delimiter[0] = str(int(delimiter[0])+1)
            delimiter[1] = increase_left(delimiter[1]) + '\.1'
            delimiter[2] = increase_left(delimiter[2]) + '\.1\.1'
        elif counts == 1:
            delimiter[2] = sync_mid(delimiter[1], delimiter[2]) + '\.1'
            delimiter[1] = increase_right(delimiter[1])
        else:
            delimiter[2] = increase_right(delimiter[2])
        next_section = re.search(r'[^表\.](?:' + '|'.join(delimiter) + r') \S', old_text)

        
    with open('out.txt', 'w') as f:
        for t in old_texts:
            f.write(t)
            f.write('\n')
            f.write('\n')
    