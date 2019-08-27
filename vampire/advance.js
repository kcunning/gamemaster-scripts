function mult(xp, n, levels=[1,2,3,4,5]) {
	var poss = [];
	for (i in levels) {
		var level = levels[i];
		if (level * n <= xp) {
			poss.push(`${level-1} -> ${level} x ${Math.floor(xp / level / n)}`)
		}
	}
	return poss
}

function straight(xp, n) {
	return [`${Math.floor(xp / n)} total`]
}

function calcXP(xp) {
	var costs = [
		["Increase Attribute (5 per level)", mult(xp, 5, levels=[2,3,4,5])],
		["Increase Skill (3 per level)", mult(xp,3)],
        ["New Specialty (3 each)", straight(xp,3)],
        ["Clan Discipline (5 per level)", mult(xp,5)],
        ["Other Discipline (7 per level)", mult(xp,7)],
        ["Caitiff Discipline (6 per level)", mult(xp,6)],
        ["Blood Sorcery Ritual (3 per level)", mult(xp,3)],
        ["Thin-blood Formula (3 per level)", mult(xp,3)],
        ["Advantage (3 each)", straight(xp,3)],
        ["Blood Potency (10 per level)", mult(xp,10, levels=[...Array(12).keys()].slice(1,12))],
	]

	return costs
}

function displayCosts() {
	// Get the XP
	xp = document.getElementById("xp").value;

	// Find the div for results and nuke the contents
	var div = document.getElementById('results');
	for (var c in [...Array(div.childrenElementCount).keys()]) {
		div.removeChild(div.firstChild)
	}

	// Get dem xps
	var results = calcXP(xp);
	var ul = document.createElement('ul')
	for (i in results) {
		var oli = document.createElement('li');
		oli.innerText = results[i][0] + ":"
		if (results[i][1].length == 0) {
			results[i][1].push("None")
		}
		var innerUl = document.createElement('ul');
		for (j in results[i][1]) {
			var innerLi = document.createElement('li');
			innerLi.innerText = results[i][1][j];
			innerUl.appendChild(innerLi)
		}
		oli.appendChild(innerUl);
		ul.appendChild(oli);
	}
	div.appendChild(ul)
}

document.addEventListener("DOMContentLoaded", function(event) { 
  let btn = document.getElementById('submitBtn');
  btn.onclick = displayCosts;
});