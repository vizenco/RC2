var express = require('express');
const fs = require('fs')
const path = require('path')
var port = 8080


var liste5elem;
var liste;
var classementKW = [];

var app = express();
app.listen(port, () => console.log(`serveur en ecoute sur le port ${port} !`));
app.use(express.static(path.join(__dirname,'public')));
app.set('views', __dirname+"/views")
app.set('view engine', 'ejs');

var spawn = require("child_process").spawn;


//Pour tester si on a déja importer les données sur la BD
function dejaInitialise() {

	return new Promise((resolve, reject) => {

		const test = spawn('python3', [path.join(__dirname,"python/dejaInitialise.py")]);
		test.stdout.on('data', function (data) {
				
			dejaInit = data.toString();
		});
		test.on('close', function(code) {
			resolve(dejaInit)
		});
		test.on('error', function(err) { reject(err) })
	})
}

//Choisis 5 labo aléatoires
function script1() {

	return new Promise((resolve, reject) => {
		
		const pythonProcess = spawn('python3', [path.join(__dirname,"python/nbPublications.py"), "liste5"]);
		var result = ''

		pythonProcess.stdout.on('data', function (data) {
			
			liste5elem = JSON.parse(data.toString());
			console.log(data.toString());
		});
		pythonProcess.on('close', function(code) {
			resolve(result)
		});
		pythonProcess.on('error', function(err) { reject(err) })
	})
}

//Liste tous les labos
function script2() {

	return new Promise((resolve, reject) => {
		
		const pythonProcess2 = spawn('python3', [path.join(__dirname,"python/nbPublications.py"), "liste"]);
		var result = ''

		pythonProcess2.stdout.on('data', function (data) {
			liste = JSON.parse(data.toString());
		});
		pythonProcess2.on('close', function(code) {
			resolve(result)
		});
		pythonProcess2.on('error', function(err) { reject(err) })
	})
}
function scriptKeyWords() {

	return new Promise((resolve, reject) => {
		
		const pythonProcess3 = spawn('python3', [path.join(__dirname,"python/keywords.py")]);
		var result = ''

		pythonProcess3.stdout.on('data', function (data) {

			classementKW=data.toString();		
					
		});
		pythonProcess3.on('close', function(code) {
			resolve(result)
		});
		pythonProcess3.on('error', function(err) { reject(err) })
	})
}

//Supprime les articles mal renseignés et edite les informations de collaborations
function graphe() {

	return new Promise((resolve, reject) => {

		const json_graphe = spawn('python3', [path.join(__dirname,"python/nodes_et_edges.py")]);
		var result = ''

		json_graphe.stdout.on('data', (data) => {
		});
		json_graphe.on('close', function(code) {
			resolve(result)
		});
        json_graphe.on('error', function(err) { reject(err) })
	})
}

//Importe les données dans la BD
function initialisation() {

    return new Promise((resolve, reject) => {

		console.log("Début de la récupération des données")
        var init = spawn('python3', [path.join(__dirname,"python/launch.py")])
        var result = ''
        init.stdout.on('data', function(data) {
            result += data.toString()
			console.log("En cours...")
        })
        init.on('close', function(code) {
            resolve(result)
        })
        init.on('error', function(err) { reject(err) })
    })
}


//Si on a déjà initialisé les données, on n'execute que les scripts nécessaires
dejaInitialise().then(function(result) {

	if(result == "false\n") {

		initialisation().then(function(result) {
				console.log("Fin initialisation");
			})
			.then(function(result2) {
				console.log("Gestion problèmes et création graphe");
				return graphe(result2);
			})
			.then(function(result3) {
				console.log("Lancement du 1er script");
				return script1(result3);
			})
			.then(function(result4) {
				console.log("Lancement du 2ème script");
				return script2(result4);
			})
			.then(function(result5) 
			{
				console.log("classement des mots clés...");
				return scriptKeyWords(result5);
			})
			.then(function(result6) {
				console.log("Les données sont prêtes à être consultées");
			})
			.catch(failureCallback);
	} else {

		script1().then(function(result) {
			console.log("Lancement du 1er script");
			})
			.then(function(result2) {
				console.log("Lancement du 2ème script");
				return script2(result2);
			})
			.then(function(result3) 
			{
				console.log("classement des mots clés...");
				return scriptKeyWords(result3);
			})
			
			.then(function(result5) {
				console.log("Les données sont prêtes à être consultées");
			})
			.catch(failureCallback);
	}
})
.catch(failureCallback);

function failureCallback(erreur) {
  console.log("L'opération a échoué avec le message : " + erreur);
}

app.get('/', function (req, res) {

    res.setHeader('Content-Type', 'text/html');
    res.render('accueil.ejs',{liste5elem : liste5elem,liste : liste ,keywords: classementKW});

})
.get('/listeStructures', function (req, res) {

    res.setHeader('Content-Type', 'text/html');
    res.render('liste.ejs', { liste: liste });

})
.get("/structure/:name", function (req, res) {
        
		res.setHeader('Content-Type', 'text/html');
        res.render("structure.ejs", {struct : req.params.structure, nbPublications : "7"});

})
.get('/rechercher', function (req, res) {

        res.setHeader('Content-Type', 'text/html');
		res.render("rechercheRes.ejs", { liste : liste });
        
});




