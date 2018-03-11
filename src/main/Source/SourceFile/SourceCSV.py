from SourceFile import SourceFile

class SourceCSV(SourceFile):

    def __init__(self, path, file_name,delimitator,header):
        super(SourceFile, self).__init__(path, file_name)
        self._delimitador = delimitator
        self_header = header

    def Load(self):
        pass