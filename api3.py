import time
import difflib
from PyPDF2 import PdfReader

class PDFComparator:
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2
    
    def read_pdf(self, file):
        reader = PdfReader(file)
        text = []
        for page in reader.pages:
            text.append(page.extract_text())
        return "\n".join(text)
    
    def compare_texts(self, text1, text2):
        d = difflib.Differ()
        diff = list(d.compare(text1.splitlines(), text2.splitlines()))
        changes = []
        current_change = []
        for line in diff:
            if line.startswith('- ') or line.startswith('+ '):
                current_change.append(line)
            elif current_change:
                changes.append("\n".join(current_change))
                current_change = []
        if current_change:
            changes.append("\n".join(current_change))
        return changes
    
    def compare_pdfs(self):
        try:
            text1 = self.read_pdf(self.file1)
            text2 = self.read_pdf(self.file2)
            changes = self.compare_texts(text1, text2)
            return {'changes': changes}
        except Exception as e:
            return {'error': str(e)}

if __name__ == "__main__":
    st = time.time()
    comparator = PDFComparator('version1.pdf', 'version2.pdf')
    diffs = comparator.compare_pdfs()
    et = time.time()
    print(diffs)
    print(f"total script runtime {(et-st)/60} minutes")
