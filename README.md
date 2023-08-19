# doc-compare
### compare.py usage
1. Make sure the files that need to be compared are in the same directory as `compare.py`
2. Files can now be in docx or pdf, but extensions are still required
3. If the `-basic` flag is added, then the output will not distinguish explicitly between laws that existed before and the ones that got newly added
4. Run `python3 compare.py <-basic> old_file_name.[docx|pdf] new_file_name.[docx|pdf]`
5. Output file is named `output.docx`

### comparePDF.py usage
1. Change the new of pdf files to be compared in line 87, 88
2. Run `python3 comparePDF.py`
3. Output file is named `output.docx`
