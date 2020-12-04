class Moment():
    def __init__(self, position:float, intensity:float):
        self.intensity = intensity
        self.position = position

class SingleLoad():
    def __init__(self, position:float, intensity:float):
        super().__init__()
        self.intensity = intensity
        self.position = position
        self.shearEquation = {}
        self.momentEquation = {}
        self.shear_moment_equations()
        

    def calcMomento(self, relative_position:float):
        return ((self.intensity)*(self.position-relative_position))

    def shear_moment_equations(self):
        self.shearEquation = {"a": -self.intensity}
        self.momentEquation = {"b":-self.intensity, "a":-self.intensity*self.position}

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
        self.load = SingleLoad((((final_position-initial_position)/2)+initial_position), (intensity*(final_position-initial_position)))
        self.shearEquation = {"c":0,"b":intensity, "a":(-intensity*initial_position)}
        self.momentEquation = {"d":0,"c":(intensity/2),"b":-(intensity*initial_position), "a":(initial_position*initial_position*intensity/2)}


class LinearDistributedLoad(DistributedLoad):
    def __init__(self, initial_position:float, final_position:float, initial_intensity:float, final_intensity:float):
        super(LinearDistributedLoad, self).__init__(initial_position, final_position)
        self.fi = initial_intensity
        self.ff = final_intensity
        self.trapezoidal = ((initial_intensity*final_intensity)!=0) #Verifica se a carga é triangular ou trapezoidal
        self.load = SingleLoad((self._calcCentroid()+self.xi), ((self.fi+self.ff)*(self.xf-self.xi)/2)) # Calcula a força pontual equivalente
        if (self.trapezoidal):                       #Verificação se a carga é trapezoidal ou triangular
            w = (self.ff-self.fi)/(2*(self.xf-self.xi))
            self.shearEquation = {"c":w,"b":(self.fi - (2*w*self.xi)),"a":((w*self.xi*self.xi)-(self.fi*self.xi))}
            w = ((self.ff-self.fi)/(6*(self.xf-self.xi)))
            self.momentEquation = {"d":w, "c":((self.fi/2)-(3*w*self.xi)), "b":((3*w*self.xi*self.xi)-(self.fi*self.xi)), "a":((self.fi*self.xi*self.xi/2)-(w*self.xi*self.xi*self.xi))}
        else:                                        #Bloco de código para cálculo dos coeficientes da equações de momento  de inercia e esforço cortante, para cargas triangulares
            if (final_intensity-initial_intensity<0):#Verificação se a carga triangular é crescente
                w = ((self.ff)/(2*(self.xf-self.xi)))
                self.shearEquation = {"c":(w),"b":-(2*(self.xi)*(w)), "a":(w*(self.xi)*self.xi)}
                w = w/3
                self.momentEquation = {"d":(w),"c":-(w*(3*self.xi)),"b":-(w*(-self.xi*self.xi*3)), "a":-(w*(self.xi*self.xi*self.xi))}
            else:                                   #Bloco de código para cálculo dos coeficientes das equação de esforço cortante e momento fletor, para cargas triangulares decrescentes
                w = ((self.fi)/(2*(self.xf-self.xi)))
                self.shearEquation = {"c":(-w),"b":(self.fi+(2*(self.xi)*(w))), "a":-((self.fi*self.xi)+(w*(self.xi)*self.xi))}
                self.momentEquation = {"d":(-w/3),"c":((self.fi/2)+(self.xi*w)),"b":-((self.xi*self.fi)+(self.xi*self.xi*w)), "a":((self.fi*self.xi*self.xi/2)+(self.xi*self.xi*self.xi*w/3))}

                                                    #Função responsável por achar a coordenada x do centroide da carga distribuída
    def _calcCentroid(self):
        if (self.trapezoidal):                      #Condição para verificar se a carga é trapezoidal
            _h1 = min([self.fi, self.ff])
            _area1 = _h1*(self.xf - self.xi)
            _xc1 = (self.xf - self.xi)/2
            _h2 = abs(self.fi-self.ff)
            _area2 = _h2*(self.xf - self.xi)/2
            if (self.fi-self.ff < 0):               #Condição para verificar se a carga é trapezoidal crescente
                _xc2 = ((2/3)*(self.xf - self.xi))
            else:                                   #Condição para verificar se a carga é trapezoidal decrescente
                _xc2 = ((1/3)*(self.xf - self.xi))
            return ((((_area1*_xc1)+(_area2*_xc2))/(_area1+_area2)))
        else:
            if (self.ff-self.fi < 0):               #Condição para verificar se a carga é triangular crescente
                return ((2/3)*(self.xf - self.xi))
            else:                                   #Condição para verificar se a carga é triangular decrescente
                return ((1/3)*(self.xf - self.xi))


#Código de teste das classes
# ab = ConstantDistributedLoad(3,5,-10)
# print(ab.load.intensity,ab.load.position)
# print(f"{ab.shearEquation['b']}x + {ab.shearEquation['a']}")
# print(f"{ab.momentEquation['c']}x² + {ab.momentEquation['b']}x + {ab.momentEquation['a']}")
# print()
# print('---------------------------')
# print()
# ab = LinearDistributedLoad(3,6,0,-10)
# print(f"{ab.shearEquation['c']}x² + {ab.shearEquation['b']}x + {ab.shearEquation['a']}")
# print(f"{ab.momentEquation['d']}x³ + {ab.momentEquation['c']}x² + {ab.momentEquation['b']}x + {ab.momentEquation['a']}")