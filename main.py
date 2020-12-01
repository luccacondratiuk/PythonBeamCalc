comprimento = int(input("Digite o comprimento da viga: "))
x_apoio1 = int(input("Digite o ponto do primeiro apoio: "))
x_apoio2 = int(input("Digite o ponto do segundo apoio: "))
n_forcas = int(input("Digite o número de forças pontuais conhecidas: "))
n_cargas_distribuidas = int(input("Digite o número de cargas distribuídas conhecidas: "))
n_momentos = int(input("Digite o número de momentos conhecidos: "))

print("------------------------")
print("---------Forças---------")
print("------------------------")
forcas = []
for i in range(n_forcas):
    force = {}
    force["Intensidade"] = float(input("Digite a intensidade da força {$}"))
    force["Posição"] = float(input("Digite a posição da força {$}"))
    forcas.append(force)

print("------------------------")
print("--Equilíbrio de Forças--")
print("------------------------")

somatorio_forcas = 0
somatorio_momentos = 0
for i in range(len(forcas)):
    somatorio_forcas+=forcas[i]["Intensidade"]
    somatorio_momentos+=((forcas[i]["Intensidade"])*(forcas[i]["Posição"]-x_apoio1))

apoio2 = ((-(somatorio_momentos)))/(x_apoio2-x_apoio1)
apoio1 = -(somatorio_forcas+apoio2)

print(apoio1, apoio2)