class Viga():
    def __init__(self, length:float, reactions:list, single_loads: list, distributed_loads:list, moments_of_inertia: list):
        self.length = length # cria um atributo à viga, contendo o comprimento da viga
        self.reactions = reactions # cria um atributo, com as reações à serem calculadas, juntamente com suas posições já definidas pelo usuário
        self.single_loads = single_loads # cria um atributo com as forças e posições informadas pelo usuário
        self.distributed_loads = distributed_loads # cria um atributo, com as cargas distribuídas informadas pelo usuário
        self.moment_of_inertia = moments_of_inertia # cria um atributo com os momentos de inércia e suas respectivas posições, também informados pelo usuário
        self.sectionsData = []
        self.forceBalance()
        for i in  self.reactions:
            i.shear_moment_equations()
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
        for i in range(len(self.moment_of_inertia)):
            fs+=self.moment_of_inertia[i]
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
        # for i in self.moment_of_inertia:
        #     a.append(i.position)    
        a = list(set(a))
        a.sort()
        if a[0]==0:
            a.remove(0)
        if a[-1]==self.length:
            a.remove(self.length)
        for i in range(len(a)):
            if (i==0):
                self.sectionsData.append({
                    'position':[0,a[i]],
                    'shear':None,
                    'flector':None
                })
            elif (i==(len(a)-1)):
                self.sectionsData.append({
                    'position':[a[i-1],a[i]],
                    'shear':None,
                    'moment':None
                })
                self.sectionsData.append({
                    'position':[a[i],self.length],
                    'shear':None,
                    'moment':None
                })
            else:
                self.sectionsData.append({
                    'position':[a[i-1],a[i]],
                    'shear':None,
                    'moment':None
                })


#Código de teste
# import forces as rm
# r = [
#     rm.SingleLoad(0,3),
#     rm.SingleLoad(0,10)
# ]
# l = [
#     rm.SingleLoad(-10,2),
#     rm.SingleLoad(-20,9)
# ]
# d = [
#     rm.LinearDistributedLoad(3,6,-30,-10)
# ]
# i = [0,0]

# viga = Viga(10,r,l,d,i)
# print(viga.reactions[0].intensity)
# print(viga.reactions[1].intensity)
# print()
# print('----------------------')
# print('--------Seções--------')
# print('----------------------')
# for i in range(len(viga.sectionsData)):
#     print(f"Seção ${i+1}: ")
#     print()
#     print(f"{viga.sectionsData[i]['position'][0]}<=X<{viga.sectionsData[i]['position'][1]}")
#     print()