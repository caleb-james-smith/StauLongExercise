class ObjectSelector:
    def __init__(self, _year = "None" ):
        self.year = _year

class TauSelector(ObjectSelector):
    def __init__(self, _minPt = 20):
        self.minPt = _minPt

    def evalTau(self, tau):
        if tau.pt < self.minPt: return False
        if abs(tau.eta) > 2.3: return False
        if abs(tau.dz) > 0.2: return False
        # CHANGE select only taus reconstructed in the decay modes 0, 1, 10, or 11
        if tau.idDeepTau2018v2p5VSe<1: return False # VVVLoose
        if tau.idDeepTau2018v2p5VSmu<1: return False # VLoose
        if tau.idDeepTau2018v2p5VSjet<1: return False # VVVLoose

        return True


class ElectronSelector(ObjectSelector):
    def __init__(self, _minPt = 10):
        self.minPt = _minPt

    def evalElectron(self, el):
        
        isEBEE = True if abs(el.eta)>1.4442 and abs(el.eta)<1.5660 else False
        
        if isEBEE: return False
        if el.pt < self.minPt: return False
        if abs(el.eta) > 2.4: return False
        if abs(el.dxy) > 0.1 or abs(el.dz) > 0.2: return False
        if not el.mvaIso_WP90: return False

        return True
        
class MuonSelector(ObjectSelector):
    def __init__(self, minPt = 10):
        self.minPt = minPt

    def evalMuon(self, mu):
        if mu.pt < self.minPt: return False
        if abs(mu.eta) > 2.4: return False
        if mu.pfRelIso04_all>0.15: return False
        if abs(mu.dxybs) > 0.1 or abs(mu.dz) > 0.2: return False
        if not mu.mediumId: return False
        return True
        
