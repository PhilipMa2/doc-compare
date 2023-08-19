# doc-compare
### compare.py usage
1. This program can only be used for files that have explicit entry delimiter 第...条
2. Make sure the files that need to be compared are in the same directory as `compare.py`
3. Files can now be in docx or pdf, but extensions are still required
4. If the `-basic` flag is added, then the output will not distinguish explicitly between laws that existed before and the ones that got newly added
5. Run `python3 compare.py <-basic> old_file_name.[docx|pdf] new_file_name.[docx|pdf]`
6. Output file is named `output.docx`

### comparePDF.py usage
1. This program can only be used for files with entry delimiter in 1, 1.1, 1.1.1, etc.
2. Change the name of pdf files to be compared in lines 87, 88
3. Run `python3 comparePDF.py`
4. Output file is named `output.docx`
