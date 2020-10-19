import pickle
class PickleData:
    def __init__(self,fil):
        self.file = fil
    def dump_object(self,obj):
        with open(self.file,'wb') as destination:
            pickle.dump(obj,destination)
    def depickle(self):
        with open(self.file,'rb') as f:
            Pikl = pickle.load(f)
        return Pikl