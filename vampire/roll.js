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

function rollSim() {
    dice = document.getElementById('dice').value;
    dc = document.getElementById('dc').value;
    hunger = document.getElementById('hunger').value;
    runs = 100;

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

        // Successes
    	total = getTotalSuccesses(c, r);
    	if (total >= dc) {
    		wins++;
    	}

        // Critical wins
        if (total >= dc & c > 0) {
            crit++;
        }

        // The next two checks involve hunger dice. We assume that
        // the first X dice are the hunger dice.
        var hdice = roll.slice(0, hunger);

        // Messy crits
        if (hdice.includes(2) & c > 0 & total >= dc) {
            messy++;
        }
        // Bestial failures
        if (hdice.includes(-1) & total < dc) {
            bestial++;
        }
    }

    var table = document.getElementById("results");
    var newRow = table.insertRow();
    var newCell = newRow.insertCell();
    newCell.innerText = wins + " / " + runs;
    var newCell = newRow.insertCell();
    newCell.innerText = crit + " / " + runs;
    var newCell = newRow.insertCell();
    newCell.innerText = messy + " / " + runs;
    var newCell = newRow.insertCell();
    newCell.innerText = bestial + " / " + runs;
}

function doRolls() {
    // reset the table
    table = document.getElementById('results');
    n = table.tBodies[0].childElementCount;
    for (var i=1; i<n ; i++) {
       table.deleteRow(1)
    }    
    
    // Do the rolls
    for (var i=0; i <= 20; i++) {
        rollSim();
    }
}

document.addEventListener("DOMContentLoaded", function(event) { 
  let btn = document.getElementById('rollBtn');
  btn.onclick = doRolls;
});


