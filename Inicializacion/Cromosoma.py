class Cromosoma:
    def __init__(self,genes):
        self.genes = genes
        self.leves_score = 0
        self.graves_score = 0
        self.total_score = 0
    
    def GetGenes(self):
        return self.genes

    def AddLevesScore(self,value):
        self.leves_score += value

    def AddGravesScore(self,value):
        self.graves_score += value
    
    def GetLevesScore(self):
        return self.leves_score

    def GetGravesScore(self):
        return self.graves_score

    def GetTotalScore(self):
        self.total_score = self.graves_score + self.leves_score
        return self.total_score
    
