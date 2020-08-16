# Ler arquiv json e converter a list de dict, um para cada processo
# aplicado a riscos LGPD, para anáĺise de medição de riscos e frequencias de recomendações
# Arquivo default = riscos.json
import json

def myFunc(e): return e[1]

def imprimirl(simounao, lista, mensagem): # imprimir lista
	if simounao:
		print(mensagem)
		for p in lista: print(p); print()

def to_bool(value):
    if str(value).lower() in ("yes", "y", "true",  "t", "1", "sim", "s"): return True
    if str(value).lower() in ("no",  "n", "false", "f", "0", "0.0", "", "none", "[]", "{}", "nao", "n"): return False
    raise Exception('Invalid value for boolean conversion: ' + str(value))

Arquivo = input("Nome do arquivo [riscos.json]: ") or 'riscos.json'    # ler o arquivo json de riscosjson
print("Arquivo json a converter a dict Python: ", Arquivo)
JsonFile = open(Arquivo,"r+")  
JList = json.loads(JsonFile.readlines()[0])    # ler em JList, tirar os "[]" e converter json a list ==> conferir se o 0 tira os []
JsonFile.close()
Modulo = input("Nome do Modulo [SEGURADORA]: ") or 'SEGURADORA'    # MList contem só os jsons do Modulo escolhido
print("Modulo selecionado: ", Modulo)
Verboso = to_bool(input("Verboso [No]:") or "No");

# Criar lista com riscos deste módulo
MList = []
for p in JList:
	if p['Module'] == Modulo: MList.append(p)
imprimirl(Verboso,MList, "MList, só riscos deste módulo:");
# Criar lista com processo e risco
TRisc = []
for p in MList: TRisc.append([p['Process'], p['Height']])   # observar que o número vem com ponto, não vírgula; corrigido lá no final. Se corrigir aqui dá êrro no csv
imprimirl(Verboso,TRisc, "TRisc, só com o processo e o risco chamado Height:")
# Converter a formato csv; um string; ver exemplo em riscos.csv; 
Tcsv = ""
for p in TRisc:
	Tcsv = Tcsv + p[0] + "; " + str(p[1]) + "\n"
# print("Tcsv, csv legível por planilha:"); print(Tcsv);
# Converter a lista TRisc a lista em ordem de processos
TRisc.sort()    # pelo primeiro item que é o nome do processo
imprimirl(Verboso,TRisc, "TRisc sorted:");
# Nova lista só com os totais por processo; calcula total a cada quebra de área, e ao final
TTot = []
anterior = TRisc[0][0]
tot = 0
m = []
for p in TRisc:
	if p[0] == anterior:
		tot = tot + p[1]
	else:
		m = [anterior, tot]
		TTot.append(m)
		anterior = p[0]
		tot = p[1]
m = [anterior, tot]    # caso último elemento, não há quebra de total
TTot.append(m)
imprimirl(Verboso,TTot, "TTot com totais por processo:");
# Agora lista com os totais por area. Em cada area guardo o total, para o sort, os processos, e o nome
TArea = []
anterior = TTot[0][0][0:6]
tot = 0
TProcs = []
for p in TTot:
	if p[0][0:6] == anterior:
		tot = tot + p[1]
		TProcs.append(p)
	else:
		TProcs.sort(reverse=True, key=myFunc)
		TArea.append([tot, [anterior, tot], TProcs, ["Total", tot]])
		anterior = p[0][0:6]
		tot = p[1]
		TProcs = [p];
TProcs.sort(reverse=True, key=myFunc)
TArea.append([tot, [anterior, tot], TProcs, ["Total", tot]])
imprimirl(Verboso,TArea, "TArea não sorted:")
# Classificar e inserir cabeçalho de área onde havia o total repetido; a melhorar depois, fazer antes talvez
TArea.sort(reverse=True)
i = 0
for p in TArea:
	nomep = p[2][0][0]
	f = nomep.find('- ')
	if (f == -1): nomeprocess = nomep[9:]
	else: nomeprocess = nomep[9:f]
	TArea[i][1] = [p[1][0] + ' ' + nomeprocess , " "]
	i = i + 1
imprimirl(Verboso,TArea, "TArea já no formato final, como lista:")
# Emitir o .csv
TFinalcsv = ""
for p in TArea:
	TFinalcsv = TFinalcsv + p[1][0] + "; " + str(p[1][1]).replace(".", ",") + "\n"
	for q in p[2]:
		TFinalcsv = TFinalcsv + q[0] + "; " + str(q[1]).replace(".", ",") + "\n"
	TFinalcsv = TFinalcsv + p[3][0] + "; " + str(p[3][1]).replace(".", ",") + "\n"
# print("TFinalcsv: ", TFinalcsv)
# Gravar
f= open("Riscoscsv.csv","w+")
f.write(TFinalcsv)
f.close() 
print("Gravado arquivo Riscoscsv.csv com os riscos por processo")
