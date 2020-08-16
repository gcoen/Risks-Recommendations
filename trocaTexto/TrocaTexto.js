// TrocaTexto versão ts
// Programa que lê recomendações e troca usando 2 funções: AchaSemelhnate e TrocaFrase
require('typescript-require'); // instalar typescript-require e colocar este comando ###
var readlineSync = require('readline-sync');
var levenshtein = require('js-levenshtein');
var parametro = ""; // Ler o paramentro de corte Levenshtein
var parametroL = 0;
parametro = readlineSync.question('Parametro de corte Levenshtein [41]: '); // falta validar entrada só de número inteiro
if (parametro === "") {
    parametroL = 41;
}
else {
    parametroL = parseInt(parametro);
}
;
var recomendas = [""]; // Ler recomendação (do teclado, depois será dentro do Regente). Para testes, ler só 30 recomendações
var lida = "";
var existe = "";
var decisao = "";
var retornoAS = { aceitar: false, existe: "", indice: 0 };
for (var i = 0; i < 30; i++) { // ler recomendações
    lida = readlineSync.question("Qual é a recomendação? [fim]: ");
    if ((lida === "fim") || (lida === "")) {
        break;
    }
    ; // Terminar com "fim" ou não digitando nada
    if (i === 0) {
        recomendas[i] = lida;
        console.log("Lista: ", recomendas);
        continue;
    } // caso da primeira recomendação
    else {
        retornoAS = AchaSemelhante(parametroL, recomendas, lida);
    }
    ; // procurar semelhante e retornar
    if (retornoAS.aceitar) {
        recomendas[i] = lida;
    } // Aceitar a recomendação
    else { // ou decidir conforme input do usuário
        decisao = "";
        existe = retornoAS.existe;
        console.log("existe texto semelhante: ", existe);
        while (!["M", "S", "A"].includes(decisao)) { // validar input M, S, A
            decisao = readlineSync.question("Manter seu texto (M), substituir pelo existente (S) ou substituir o existente pelo atual (A)? ");
        }
        TrocaFrase(decisao, recomendas, lida, i, existe);
    }
    ;
    console.log("Lista: ", recomendas); // Mostra a lista
}
console.log("Lista final: ", recomendas); // Mostra a lista final
function AchaSemelhante(parametro, recomendas, lida) {
    // percorre o array de recomendações comparando com a recomendação lida. No caso da primeira, não chamar esta função
    var aceitar; // Retorna boolean true se é o caso de aceitar a recomendação, false se não é
    var existe; // frase semelhante
    var indice; // indice da frase semelhante (é usado?)
    var jaTemIgual = false;
    var noMenor = true;
    var distance = 0;
    for (indice = 0; indice < recomendas.length; indice++) {
        existe = recomendas[indice];
        distance = levenshtein(lida, existe);
        if (distance === 0) {
            jaTemIgual = true;
            break;
        }
        ;
        if (distance < parametro) {
            noMenor = false;
            break;
        }
    }
    ;
    if (jaTemIgual || noMenor) {
        jaTemIgual = false;
        aceitar = true;
    } // caso tem uma recomendação igual ou não tem nenhuma parecida
    else {
        aceitar = false;
    }
    ; // caso tem uma recomendação semelhante
    var retorno = { aceitar: aceitar, existe: existe, indice: indice };
    return retorno;
}
;
function TrocaFrase(decisao, recomendas, lida, indice, existe) {
    switch (decisao) {
        case "M":
            recomendas[indice] = lida; // a principio desnecessário, a frase já estaria lá. Ou não, depende de como é tratada na leitura.
            break;
        case "S":
            recomendas[indice] = existe;
            break;
        case "A": // nota: neste caso, se deve substituir todos os existentes
            recomendas[indice] = lida;
            for (var j = 0, l = recomendas.length; j < l; j++) {
                if (recomendas[j] === existe) {
                    recomendas[j] = lida;
                }
            }
            ;
            break;
    }
    ;
}
