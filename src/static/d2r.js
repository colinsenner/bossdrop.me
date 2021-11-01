var d2data = {}

$.getJSON('results.json', function(data) {
    console.log('results.json loaded');
    d2data = data;
});

function searchresult_onclick(data) {
    let search_input = document.getElementById("search");
    search_input.value = data;

    clear_search_results();
    search_onsubmit();
};

function clear_search_results() {
    removeAllChildNodes(document.querySelector('#searchresult'));
}

function clear_results() {
    removeAllChildNodes(document.querySelector('#results'));
}

function search_onsubmit() {
    var search = document.getElementById("search");
    var results = document.getElementById("results");

    var bosses = get_bosses_that_can_drop(search.value);

    var items = ""
    bosses.forEach((boss) => {
        items += "<li>" + boss + "</li>"
    });
    results.innerHTML = "<ul>" + items + "</ul>";

    return false;
}

function get_bosses_that_can_drop(item_name) {
    let all_bosses = d2data['bosses']
    let all_items = d2data['uniqueitems'];

    let item = all_items.filter(item => item['index'] == item_name)[0];

    if (item !== undefined) {
        // Found the item
        let ilvl = item.lvl;
        let bosses = []

        all_bosses.forEach((boss) => {
            // Normal difficulty
            if (boss['Level'] >= ilvl) {
                bosses.push(boss['Id']);
            }
            // Nightmare difficulty
            if (boss['Level(N)'] >= ilvl) {
                bosses.push(boss['Id'] + " (NM)");
            }
            // Hell difficulty
            if (boss['Level(H)'] >= ilvl) {
                bosses.push(boss['Id'] + " (H)");
            }
        });

        return bosses;
    }

    // Couldn't find the item
    clear_results();
    return [];
}

function autocompleteMatch(input) {
    if (input == '') {
        return [];
    }
    var reg = new RegExp(input, "i")

    let unique_items = d2data['uniqueitems'].map(x => x['index']);

    return unique_items.filter(function(term) {
        if (term.match(reg)) {
        return term;
        }
    });
}

function showSearchResults(val) {
    res = document.getElementById("searchresult");
    res.innerHTML = '';
    let list = '';
    let terms = autocompleteMatch(val);

    if (terms.length !== 0) {
        for (i=0; i < terms.length; i++) {
            list += '<li tabindex="0" onkeypress="searchresult_onclick(this.innerHTML)" onclick="searchresult_onclick(this.innerHTML)">' + terms[i] + '</li>';
        }
    }
    else if (val !== '') {
        list += '<li tabindex="0">Item not found</li>';
    }

    res.innerHTML = '<ul>' + list + '</ul>';
    return false;
}

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}