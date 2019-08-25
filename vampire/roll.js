var dice = 6
var dc = 3
var hunger = 3

function getRange(n) {
	var arr = [];
	for (var i = 0; i <= n; i++) {
		arr.push(i)
	}

	return arr;
}

function getRoll(die, n) {
	var roll = [];
	for (var i=0; i<n; i++) {
		roll.push(die[Math.floor(Math.random() * die.length)]);
	}
	return roll
}

function getTotalSuccesses(crit, normal) {
	var total = crit*2 + normal;
	return total
}

function rollSim(dice, dc, hunger=1, runs=100) {
    dice = document.getElementById('dice').value
    dc = document.getElementById('dc').value

	wins = 0;
	warr = []
    crit = 0;
    messy = 0;
    bestial = 0;
    die = [-1,0,0,0,0,1,1,1,1,2];

    for (var i=0; i <= runs; i++) {
    	roll = getRoll(die, dice);
    	c = 0;
    	r = 0;
    	for (d in roll) {
    		if (roll[d] == 2) {
    			c++;
    		} else if (roll[d] == 1) {
    			r++;
    		}
    	}
    	if (Math.floor(c/2) != c/2) {
    		c--;
    		r++;
    	}
    	total = getTotalSuccesses(c, r);
    	if (total >= dc) {
    		wins += 1;
    	}
    }
    console.log("Wins", wins, "out of", runs)
}

document.addEventListener("DOMContentLoaded", function(event) { 
  let btn = document.getElementById('rollBtn')
  btn.onclick = rollSim
});


