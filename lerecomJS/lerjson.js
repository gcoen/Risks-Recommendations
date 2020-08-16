// Lersjcon, versão js
// Recebe como paramentros na chamada node r2.js o nome do arquivo de riscos e o nome do módulo a tratar
//	exemplo: node r2.js 'riscos.json' 'Banco Alfa de Investimento'

var fs = require('fs');

Arquivo = process.argv[2]   // ler o arquivo de riscos
try {var data = fs.readFileSync(Arquivo, 'utf8'); } catch(e) {console.log('Error:', e.stack);};
var JList = data.toString();
Modulo = process.argv[3];
console.log('Será tratado o módulo ', Modulo, 'no arquivo ', Arquivo);

var obj = JSON.parse(JList);    // Json a tratar

var MList = [];    // será a lista só com o modulo escolhido
for (i in obj) { if (obj[i].Module == Modulo) {MList.push(obj[i]) }; };

var TRisc = [];    // será a lista só com o processo e o risco
for (i in MList) { TRisc.push([MList[i].Process, MList[i].Height]) };    // Observar que TRisc é um array de arrays, não de {}
// observar que o número vem com ponto, não vírgula; corrigido lá no final. Se corrigir aqui dá êrro no csv

TRisc.sort()    // Classificar por número do processo. Numeração no começo do string processo

TTot = [];    // Nova lista só com os totais por processo; calcula total a cada quebra de área, e ao final
anterior = TRisc[0][0];
tot = 0;
m = [];
TRiscLen = TRisc.length;
for (i = 0; i < TRiscLen; i++) { 
	if (TRisc[i][0] == anterior) { tot = tot + TRisc[i][1] } else {
        m = [anterior, tot];
		TTot.push(m);
		anterior = TRisc[i][0];
		tot = TRisc[i][1];	} }
m = [anterior, tot]; TTot.push(m);    // caso último elemento, não há quebra de total

TArea = [];    // Agora lista com os totais por area. Em cada area guardo o total, para o sort, os processos, e o nome. Inverte colcoando o total por processo antes do nome para o sort seguinte funcionar.
anterior = TTot[0][0].slice(0,6);
tot = 0;
TProcs = [];
TProv = [];
Vazio = []
TTotLen = TTot.length;
for (i = 0; i < TTotLen; i++) { 
	if (TTot[i][0].slice(0,6) == anterior) {
		tot = tot + TTot[i][1];
		TProcs.push([TTot[i][1], TTot[i][0]]); }
	else {
		TProcs.sort((function(a, b){return b[0] - a[0]}));    // reverse sort, por valor do risco
		TProv.push([tot, anterior]);
		TProcsLen = TProcs.length; for (j = 0; j < TProcsLen; j++) { TProv.push(TProcs[j]); };
		TProv.push(["Total", tot]);
		TArea.push(TProv);    // TProvLen = TProv.length; for (j = 0; j < TProvLen; j++) { TArea.push(TProv[j]) };
		anterior = TTot[i][0].slice(0,6);
		tot = TTot[i][1];
		TProcs = [[TTot[i][1], TTot[i][0]]];
		TProv = []; };
		};
TProcs.sort(function(a, b){return b[0] - a[0]});    // ordem descendente, pelo primeiro elemento dos elementeos do array
TProv.push([tot, anterior]); 
TProcsLen = TProcs.length; for (j = 0; j < TProcsLen; j++) { TProv.push(TProcs[j]); }; 
TProv.push(["Total", tot]);
TArea.push(TProv);    // TProvLen = TProv.length; for (j = 0; j < TProvLen; j++) { TArea.push(TProv[j]) };
// Classificar e inserir cabeçalho de área onde havia o total repetido; a melhorar depois, fazer antes talvez
TArea.sort(function(a, b){return b[0][0] - a[0][0]});
TAreaLen = TArea.length;
for (i = 0; i < TAreaLen; i++) {
	for (j = 0; j < TArea[i].length; j++) {
		if (j == 0) { TArea[i][j][0] = TArea[i][j][1]; TArea[i][j][1] = ""; continue; };
		if (TArea[i][j][0] == "Total") { continue; };
		troca = TArea[i][j][0]; TArea[i][j][0] = TArea[i][j][1]; TArea[i][j][1] = troca; }; };
TFinalcsv = "";    // Emitir o .csv
TAreaLen = TArea.length;
for (i = 0; i < TAreaLen; i++) {
	for (j = 0; j < TArea[i].length; j++) {
		if (j == 0) {
			nomep = TArea[i][j+1][0];
			f = nomep.search("-");
			if (f == -1) {nomeprocess = nomep.slice(9)} else {nomeprocess = nomep.slice(9, f)};
			TFinalcsv = TFinalcsv + nomeprocess + ";" + " " + "\n"; }
		else {TFinalcsv = TFinalcsv + TArea[i][j][0] + "; " + TArea[i][j][1].toString().replace(".", ",") + "\n";};
	}
};
// Gravar arquivo riscos.csv. Melhorar: testar se arquivo existe, perguntar se pode apagar, etc...
fs.appendFile('riscos.csv', TFinalcsv, function (err) { if (err) console.log("êrro de gravação do arquivo.csv");  console.log('Gravado: riscos.csv'); });
