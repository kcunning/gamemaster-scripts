var getDC = function(lvl, adjustment=null) {
    // Gets the leveled DC, given a level and applies DC adjustments if necessary. 
    // DC = level + (level / 3 rounded down) + 14
    var dc = lvl + Math.floor(lvl/3) + 14;

    switch(adjustment) {
        case 'incredibly easy':
            dc += -10;
            break;
        case 'very easy':
            dc += -5;
            break;
        case 'easy':
            dc += -2;
            break;
        case 'hard':
            dc += 2;
            break;
        case 'very hard':
            dc += 5;
            break;
        case 'incredibly hard':
            dc += 10;
            break;
        case 'uncommon':
            dc += 2;
            break;
        case 'rare':
            dc += 5;
            break;
        case 'unique':
            dc += 10;
            break;
        case 'standard':
            dc += 0;
            break
        default:
            dc += 0
            break;
    }

    return dc
}

var getSingleRitual = function(slug) {
    // Loops through ritual data to get a single ritual, because my dumbass made
    // it a list rather than an object. 
    for (var i in ritualData) {
        var ritual = ritualData[i];
        if (ritual.slug == slug) {
            return ritual;
        }
    }
}

var calcFeatMods = function() {
    // Loops through selected feats to find what mods need to be applied.
    // Returns a dictionary of just the mods. Only applies the highest modifier 
    // if more than one feat would apply.
    let allfeats = document.getElementsByClassName('ritual_checkbox');
    let selected = [];
    for (var i in allfeats) {
        if (allfeats[i].checked == true) {
            selected.push(allfeats[i].id);
        }
    }
    let ritualMods = {}
    for (var i in selected) {
        let arr = selected[i].split('-');
        let slug = arr[0];
        let mod = arr[1];
        let feat = getSingleRitual(slug);
        if (mod in ritualMods & ritualMods[mod] < feat.mods[mod][mod]) {
            ritualMods[mod] = feat.mods[mod];
        } else if (!(mod in ritualMods)) {
            ritualMods[mod] = feat.mods[mod][mod];
        }
    }
    return ritualMods;
}

var calcRitualDCs = function() {
    // Calculates the ritual DCs for both the primary and secondary casters.
    var elem = document.getElementById("ritual_level")
    if (elem.value == '') {
        let errElem = document.getElementById('error');
        errElem.innerHTML = "You have to select a level!";
        return null
    } else {
        let errElem = document.getElementById('error');
        errElem.innerHTML = "";
    }

    // First, get the selected feats
    var primDC = getDC(Number(elem.value * 2), 'very hard');
    var secDC = getDC(Number(elem.value * 2))
    let mods = calcFeatMods();
    let extra_text = "";

    // Apply the mods
    if ('primary_circumstance' in mods) {
        primDC -= mods['primary_circumstance'];
    }
    if ('secondary_circumstance' in mods) {
        secDC -= mods['secondary_circumstance'];
    }
    if ('primary_dc' in mods) {
        primDC += mods['primary_dc'];
    }

    //Show the mods and notes!
    var primElem = document.getElementById('primDC');
    primElem.textContent = primDC;
    var secElem = document.getElementById('secDC');
    secElem.textContent = secDC;
    updateNotesElem(mods);
}

var updateNotesElem = function(mods) {
    // To be nice, I show notes about what mods have been applied, and any additional info 
    // the user might need.
    let notesElem = document.getElementById('notes');
    notesElem.innerHTML = '';
    if (Object.keys(mods).length > 0) {
        noteHTML = `<p><em>Notes:</em><br />`;

        for (let i in mods) {
            switch(i) {
                case 'primary_circumstance':
                    noteHTML += `Primary circumstance: +${mods.primary_circumstance}<br />`;
                    break
                case 'secondary_circumstance':
                    noteHTML += `Secondary circumstance: +${mods.secondary_circumstance}<br />`;
                    break
                case 'primary_dc':
                    noteHTML += `Primary DC: Standard<br />`;
                    break
                case 'primary_value':
                    noteHTML += `The result for the primary caster will always be a critical success.`;
                    break
            }
        }

        notesElem.innerHTML = noteHTML;
    }
}

var getRitualDiv = function(ritual) {
    // Creates GML for ritual div
    let html = 
    `<div class="ritual" id="${ritual.slug}">
        <h3>${ritual.title}</h3>
            <p>${ritual.desc} [<a href="${ritual.link}" title="${ritual.title}" target="_blank" rel="noopener noreferrer">link</a>]</p>
            <p>
        `

    for (i in ritual.mods) {
        html += `<input type="checkbox" id="${ritual.slug}-${i}" class="ritual_checkbox">
        ${ritual.mods[i].explainer}<br>`
    }

    html += `
    </p>
    </div>`

    return html
}

var populateRituals = function() {
    // Puts all the rituals on the page, since they're stored in a JSON file
    var topElem = document.getElementById('rituals');
    for (i in ritualData) {
        let ritualHTML = getRitualDiv(ritualData[i]);
        topElem.innerHTML += ritualHTML;
    }
}

// Get the rituals from a JSON file!
fetch('pf2rituals.json')
    .then((response) => response.json())
    .then(data => {ritualData = data;populateRituals()})