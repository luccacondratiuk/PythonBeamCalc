class SingleLoad():
    def __init__(self, intensity:float, position:float):
        super().__init__()
        self.intensity = intensity
        self.position = position

    def calcMomento(self, relative_position:float):
        return ((self.intensity)*(self.position-relative_position))


class DistributedLoad():
    def __init__(self, initial_position:float, final_position:float):
        self.xi = initial_position
        self.xf = final_position
        self.load = SingleLoad(0,0)

    def calcMomento(self, relative_position:float):
        return (self.load.calcMomento(relative_position))


class ConstantDistributedLoad(DistributedLoad):
    def __init__(self, initial_position:float, final_position:float, intensity:float):
        super(ConstantDistributedLoad, self).__init__(initial_position, final_position)
        self.load = SingleLoad((intensity*(final_position-initial_position)), (((final_position-initial_position)/2)+initial_position))


class LinearDistributedLoad(DistributedLoad):
    def __init__(self, initial_position:float, final_position:float, initial_intensity:float, final_intensity:float):
        super(LinearDistributedLoad, self).__init__(initial_position, final_position)
        self.fi = initial_intensity
        self.ff = final_intensity
        self.load = SingleLoad(((initial_intensity+final_intensity)*(final_position-initial_position)/2),self._calcCentroid()+self.xi)

    def _calcCentroid(self):
        if ((self.fi*self.ff)!=0):
            _h1 = min([self.fi, self.ff])
            _area1 = _h1*(self.xf - self.xi)
            _xc1 = (self.xf - self.xi)/2
            _h2 = abs(self.fi-self.ff)
            _area2 = _h2*(self.xf - self.xi)/2
            if (self.fi-self.ff < 0):
                _xc2 = ((2/3)*(self.xf - self.xi))
            else:
                _xc2 = ((1/3)*(self.xf - self.xi))
            return ((((_area1*_xc1)+(_area2*_xc2))/(_area1+_area2)))
        else:
            if (self.ff-self.fi < 0):
                return ((2/3)*(self.xf - self.xi))
            else:
                return ((1/3)*(self.xf - self.xi))

# ab = ConstantDistributedLoad(0,3,10)
# print(ab.load.intensity,ab.load.position)
# print(ab.xi)
# print(ab.xf)
# ab = LinearDistributedLoad(0,6,10,5)
# print(ab.load.intensity,ab.load.position)