class Viga():
    def __init__(self, length:float, reactions:list, single_loads: list, distributed_loads:list, moments: list):
        self.length = length # cria um atributo à viga, contendo o comprimento da viga
        self.reactions = reactions # cria um atributo, com as reações à serem calculadas, juntamente com suas posições já definidas pelo usuário
        self.single_loads = single_loads # cria um atributo com as forças e posições informadas pelo usuário
        self.distributed_loads = distributed_loads # cria um atributo, com as cargas distribuídas informadas pelo usuário
        self.moments = moments # cria um atributo com os momentos de inércia e suas respectivas posições, também informados pelo usuário
        self.forceBalance()
        for i in  self.reactions:
            i.shear_moment_equations()
        self.sectionsData = []
        self._sections()

    #função responsável pelo cálculo do equilíbrio de forças, isto é, calculo das reações  
    def forceBalance(self):
        self.reactions[1].intensity = (-self._inertiaSum(self.reactions[0].position))/(self.reactions[1].position-self.reactions[0].position)
        self.reactions[0].intensity = -(self._forceSum()+self.reactions[1].intensity)

    #função responsável por realizar, o somatório das forças conhecidas
    def _forceSum(self):
        fs = 0
        for i in range(len(self.single_loads)):
            fs+=self.single_loads[i].intensity
        for i in range(len(self.distributed_loads)):
            fs+=self.distributed_loads[i].load.intensity
        return fs    

    #função responsável por realizar, o somatório dos momentos conhecidos
    def _inertiaSum(self, relative_posi:float):
        fs = 0
        for i in range(len(self.single_loads)):
            fs+=(self.single_loads[i].intensity)*(self.single_loads[i].position - relative_posi)
        for i in range(len(self.distributed_loads)):
            fs+=self.distributed_loads[i].load.intensity*(self.distributed_loads[i].load.position - relative_posi)
        for i in range(len(self.moments)):
            fs+=self.moments[i].intensity
        return fs

    def _sections(self):
        a = list()
        for i in self.reactions:
            a.append(i.position)
        for i in self.single_loads:
            a.append(i.position)
        for i in self.distributed_loads:
            a.append(i.xi)
            a.append(i.xf)
        for i in self.moments:
             a.append(i.position)    
        a = list(set(a))
        a.sort()
        if a[0]==0:
            a.remove(0)
        for i in range(len(a)):
            if (i==0):
                self.sectionsData.append({
                    'position':[0,a[i]],
                    'shear':{'a':0,'b':0,'c':0,'d':0},
                    'moment':{'a':0,'b':0,'c':0,'d':0}
                })
            else:
                self.sectionsData.append({
                    'position':[a[i-1],a[i]],
                    'shear':{'a':0,'b':0,'c':0,'d':0},
                    'moment':{'a':0,'b':0,'c':0,'d':0}
                })
        if (self.sectionsData[-1]['position'][1]!=self.length):
            self.sectionsData.append({
                'position':[self.sectionsData[-1]['position'][1],self.length],
                'shear':{'a':0,'b':0,'c':0,'d':0},
                'moment':{'a':0,'b':0,'c':0,'d':0}
            })
    def calcShearAndMoment(self):
        for i in self.sectionsData:
            lim_inf = i['position'][0]
            lim_sup = i['position'][1]
            for j in self.reactions:
                if ((j.position>=lim_inf) and (j.position<lim_sup)):
                    i['shear']['a'] -= j.shearEquation['a']
                    i['moment']['a'] -= -j.momentEquation['a']
                    i['moment']['b'] -= j.momentEquation['b']
                if (j.position<lim_inf):
                    i['shear']['a'] -= j.shearEquation['a']
                    i['moment']['a'] -= j.intensity*j.position
                    i['moment']['b'] -= -j.intensity
            for j in self.single_loads:
                if ((j.position>=lim_inf) and (j.position<lim_sup)):
                    i['shear']['a'] -= j.shearEquation['a']
                    i['moment']['a'] -= -j.momentEquation['a']
                    i['moment']['b'] -= j.momentEquation['b']
                if (j.position<lim_inf):
                    i['shear']['a'] -= j.shearEquation['a']
                    i['moment']['a'] -= j.intensity*j.position
                    i['moment']['b'] -= -j.intensity  
            for j in self.distributed_loads:
                if ((j.xi>=lim_inf) and (j.xf<=lim_sup)):
                    i['shear']['a'] += j.shearEquation['a']
                    i['shear']['b'] += j.shearEquation['b']
                    i['shear']['c'] += j.shearEquation['c']
                    i['moment']['a'] += j.momentEquation['a']
                    i['moment']['b'] += j.momentEquation['b']
                    i['moment']['c'] += j.momentEquation['c']
                    i['moment']['d'] += j.momentEquation['d']
                if (j.xf<=lim_inf):
                    i['shear']['a'] -= j.load.shearEquation['a']
                    i['moment']['a'] -= j.load.intensity*j.load.position
                    i['moment']['b'] -= -j.load.intensity
            for j in self.moments:
                if (not(j.position>=lim_sup)):
                    i['moment']['a'] += -j.intensity

    #Código de teste
# import forces as rm
# r = [
#     rm.SingleLoad(0,0),
#     rm.SingleLoad(10,0)
# ]
# l = [
#     rm.SingleLoad(2,-10),
#     rm.SingleLoad(9,-20)
# ]
# d = [
#     rm.LinearDistributedLoad(3,6,-10,-30)
# ]
# i = [
#     rm.Moment(7,45)
# ]

# viga = Viga(10,r,l,d,i)
# print(f"Reação 1 = {viga.reactions[0].intensity}")
# print(f"Reação 2 = {viga.reactions[1].intensity}")
# print()
# viga.calcShearAndMoment()
# for i in range(len(viga.sectionsData)):
#     print()
#     print("-------------------------------------------------------------------------------------------")
#     print(f"----------------------------------------- Seção {i+1} -----------------------------------------")
#     print(f"--------------------------------------- {viga.sectionsData[i]['position'][0]} <= X < {viga.sectionsData[i]['position'][1]} ---------------------------------------")
#     print()
#     print(f"Esforço Cortante: {viga.sectionsData[i]['shear']['d']}x³ + {viga.sectionsData[i]['shear']['c']}x² + {viga.sectionsData[i]['shear']['b']}x + {viga.sectionsData[i]['shear']['a']}")
#     print(f"Momento Fletor: {viga.sectionsData[i]['moment']['d']}x³ + {viga.sectionsData[i]['moment']['c']}x² + {viga.sectionsData[i]['moment']['b']}x + {viga.sectionsData[i]['moment']['a']}")
#     print()
#     print()