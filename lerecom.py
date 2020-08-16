# Ler arquiv json e converter a list de recomendações
import json

def myFunc(e): return e[1]

def imprimirl(simounao, lista, mensagem): # imprimir lista
	if simounao:
		print(mensagem)
		for p in lista: print(p); print()
		print("########## Fim de: ", mensagem)

def to_bool(value):
    if str(value).lower() in ("yes", "y", "true",  "t", "1", "sim", "s"): return True
    if str(value).lower() in ("no",  "n", "false", "f", "0", "0.0", "", "none", "[]", "{}", "não", "nao", "n"): return False
    raise Exception('Invalid value for boolean conversion: ' + str(value))

Arquivo = input("Nome do arquivo [riscos.json]: ") or 'riscos.json'    # ler o arquivo json de riscosjson
print("Arquivo json a converter a dict Python: ", Arquivo)
JsonFile = open(Arquivo,"r+")  
JList = json.loads(JsonFile.readlines()[0])    # ler em JList, tirar os "[]" e converter json a list ==> conferir se o 0 tira os []
JsonFile.close()
Modulo = input("Nome do Modulo [SEGURADORA]: ") or 'SEGURADORA'    # MList contem só os jsons do Modulo escolhido
print("Modulo selecionado: ", Modulo)
Verboso = to_bool(input("Verboso [No]:") or "No");
Param = int(input("Parametro de corte Leuvenshtein [41]: ") or 41)
# Criar lista com recomendaçoes deste módulo
MList = []
for p in JList:
	if p['Module'] == Modulo: MList.append(p)
imprimirl(Verboso, MList, "MList, só recomendações deste módulo:");
# Criar lista com processo e recomendação
TRecom = []; semrec = 0; Psem = []
for p in MList:
	if 'Recommendation' in p:
		TRecom.append([p['Process'], p['Recommendation']])
	else:
		semrec = semrec + 1
		Psem.append(p['Process'])
imprimirl(Verboso, TRecom, "TRecom, só com o processo e a recomendação:")
print("Processos sem recomendação: ", semrec); print(Psem); print();
# Converter a lista TRecom a lista em ordem de processo
TRecom.sort()
imprimirl(Verboso, TRecom, "TRecom sorted:");
# Converter a formato csv; um string; ver exemplo em riscos.csv; 
Tcsv = ""
for p in TRecom:
	Tcsv = Tcsv + p[1] + "; " + p[0] + "\n"
if Verboso: print("Tcsv, csv legível por planilha:"); print(Tcsv);
# Gravar
f= open("Recomcsv.csv","w+")
for p in TRecom:
	f.write(p[1] + "; " + "\n")
f.close() 
if Verboso: print("Gravado arquivo Recomcsv.csv com as recomendações")
#
# Agora melhorar a lista de frases separando recomendações multiplas. Programa separador.py
#
Lista = []
for f in TRecom: Lista.append(f[1])
if Verboso:
	print("Lista: ", Lista); input
Lsep = []	# lista com frases separadas e sem número
for p in Lista:    # eliminar numeração
	s = p
	s.strip()	# retirar brancos no começo e fim
	if s[0] == " ": s = s[1:]
	x = s.splitlines()
	for t in x:
		if t == "": continue
		t.strip()
		if t[0] == " ": t = t[1:]
		if not (t[0:3] in ["1) ", "2) ", "3) ", "4) ", "1. ", "2. ", "3. ", "4. "]):
			Lsep.append(t)
		else:
			Lsep.append(t[3:])
String = ""
for l in Lsep:
	String = String + l + "\n"
if Verboso:
	print(Lsep); input()
if Verboso:
	for f in Lsep: print(f)
f = open("Separados.csv","w+"); f.write(String); f.close()
if Verboso: print("Gravado arquivo Separados.csv com as recomendações com itens separados e des-numerados")

############################# Separador

# Fazer lista, mas agora aplicar leuwenstin
import Levenshtein

# ler lista gerada pelo programa lerecom.py (seguide separador.py que separa recomendações com varios itens em varias recomendações
Aler = "Separados.csv"; f = open(Aler,"r+"); frases = f.readlines(); f.close()

if Verboso:
	for x in frases: print(x)	# frases é lista de strings com as recomendações
# Montar lista, para cada frase, com as distancias às outras: [['a frase a comparar', [['outra frase', distancia], ...],...]]
Listagrande = []; contad = 0; Repetidas = []; Repetidonas = []
for frase in frases:
	if frase in Repetidonas: continue
	Listadistancias = [[contad, frase]];
	# print("AAA", " ", frase); input();
	for p in frases:
		d = Levenshtein.distance(frase, p)
		Listadistancias.append([d, p])
		# print("BBB", d, " ", p); input();
	contad = 0
	vez1 = True
	for q in Listadistancias:	# conta ocorrências de repetições para esta frase
		if vez1:
			vez1 = False
			continue
		if q[0] < Param:
			contad = contad + 1
			Repetidas.append(q[1])
			# print("CCC", contad, " ", q[0], " ", q[1]); input();
	Listadistancias[0][0] = contad
	if contad >= 2:
		# print("YYY Repetidas", Repetidas); input()
		for u in Repetidas: Repetidonas.append(u)
		# print("ZZZ Repetidonas", Repetidonas), input()
	Listagrande.append(Listadistancias)	# !!!
	Repetidas = []
Listagrande.sort(reverse=True)
if Verboso:
	print("Lista grande lista a lista"); print()
	for p in Listagrande: print(p); print()
	for p in Listagrande: print(p[0][0], " - ", p[0][1]); print()
Scsv = ""
for p in Listagrande:
	Scsv = Scsv + str(p[0][0]) + ";" + p[0][1]	# Atenção, tem um \n ao final da frase de recomendação!
f = open("frequencias" + Modulo + ".csv","w+"); f.write(Scsv); f.close()
print("Gravado arquivo frequencias " + Modulo + ".csv com as frases e o score")
