import textract
import docx 
import re 
import difflib

# Find the first entry by skipping table of contents
def find_2nd(string, substring):
    return string.find(substring, string.find(substring) + 1)

# Return list of strings such that each string is one entry in the document
def preprocess(name):
    file = textract.process(name)
    text = file.decode()
    text = text[find_2nd(text, "第一章"):]
    texts = re.findall(r'第.{1,5}[章|条][\s\S]*?\s(?=第.+[章|条])', text)
    texts.append(text[text.rfind('第'):])
    return texts

if __name__ == "__main__":
    # specify file name to compare
    old_texts = preprocess("中华人民共和国安全生产法（2014年修订）.docx")
    new_texts = preprocess("中华人民共和国安全生产法（2021年修订）.docx")

    # create output document for comparison
    output = docx.Document()
    table = output.add_table(rows=1, cols=2, style="Table Grid")
    row = table.rows[0]
    # manually enter the year of each document
    row.cells[0].text = '2014'
    row.cells[1].text = '2021'
    # i keeps track of old document law and j keeps track of new document law
    i = 0
    j = 0
    while i < len(old_texts) and j < len(new_texts):
        cells = table.add_row().cells
        oldp = cells[0].add_paragraph()
        newp = cells[1].add_paragraph()
        diff = difflib.ndiff(old_texts[i], new_texts[j])
        # find the difference ratio of two entries
        seq_mat = difflib.SequenceMatcher()
        seq_mat.set_seqs(old_texts[i], new_texts[j])
        ratio = seq_mat.ratio()
        len_diff = abs(len(old_texts[i]) - len(new_texts[j]))
        # if the lengths of two entries are substantially different, then it's 
        # possible for them to be the same entry even if difference ratio is less
        # than 0.5. For example, see entry 113 (2021) and 108 (2014)
        if (ratio < 0.5 and len_diff < 200)  \
            or (len_diff >= 200 and ratio < 0.1):
            run = newp.add_run(new_texts[j])
            run.font.color.rgb = docx.shared.RGBColor(128,21,0)
            run = oldp.add_run('新 增')
            run.font.color.rgb = docx.shared.RGBColor(0,102,51)
            j += 1
        else:
            for k, s in enumerate(diff):
                # same content
                if s[0] == ' ': 
                    newp.add_run(s[-1])
                    oldp.add_run(s[-1])
                # if content is added in 2021, make it red in 2021
                elif s[0] == '+':
                    run = newp.add_run(s[-1])
                    run.font.color.rgb = docx.shared.RGBColor(128,21,0)
                # if content is deleted in 2021, make it green in 2014
                elif s[0] == '-':
                    run = oldp.add_run(s[-1])
                    run.font.color.rgb = docx.shared.RGBColor(0,102,51)
            i += 1
            j += 1
        
    output.save("output.docx")