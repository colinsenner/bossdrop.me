var d2data = {};

$.getJSON("results.json", function (data) {
    d2data = data;

    console.log("Huge thanks to Goretusk and Sinny!");
});

function searchresult_onclick(data) {
    let search_input = document.getElementById("search");
    search_input.value = data;

    clear_search_results();
    search_onsubmit();
}

function clear_search_results() {
    document.querySelector("#search_results").classList.remove("has-items");
    removeAllChildNodes(document.querySelector("#search_results"));
}

function clear_results() {
    removeAllChildNodes(document.querySelector("#boss_results"));
}

function search_onsubmit() {
    var search = document.getElementById("search");
    var results = document.getElementById("boss_results");

    var bosses = get_bosses_that_can_drop(search.value);

    // Sort bosses based on their normal level
    bosses.sort((a, b) => a["Level"] - b["Level"]);

    results.innerHTML = "";

    if (bosses.length > 0) {
        showDisclaimer();

        let table_header = `
            <div class="boss_name header">Boss</div>
            <div class="header">N</div>
            <div class="header">NM</div>
            <div class="header">Hell</div>
        `;

        bosses.forEach(boss => {
            if (boss["difficulty"].some(x => x)) {
                let row = "";

                row += `<div class="boss_name">${boss["name"]}</div>`;

                for (let index = 0; index < 3; index++) {
                    if (boss["difficulty"][index]) row += `<div>✔️</div>`;
                    else row += `<div class="opacity-20">✖</div>`;
                }

                table_header += row;
            }
        });

        results.innerHTML = table_header;
    } else {
        hideDisclaimer();
    }

    return false;
}

function showDisclaimer() {
    var disclaimer = document.getElementById("disclaimer");
    disclaimer.classList.remove("hidden");
}

function hideDisclaimer() {
    var disclaimer = document.getElementById("disclaimer");
    disclaimer.classList.add("hidden");
}

function get_bosses_that_can_drop(item_name) {
    let all_monsters = d2data["monsters"];
    let all_items = d2data["items"];

    let item = all_items.filter(item => item["index"] == item_name)[0];

    if (item !== undefined) {
        // Found the item
        let bosses = [];

        all_monsters.forEach(boss => {
            let boss_entry = {
                name: boss["NameStr"],
                Level: boss["Level"],
                "Level(N)": boss["Level(N)"],
                "Level(H)": boss["Level(H)"],
                difficulty: [false, false, false],
            };

            ["", "(N)", "(H)"].forEach(difficulty => {
                difficulty_str = {
                    "": "Normal",
                    "(N)": "Nightmare",
                    "(H)": "Hell",
                };
                let difficult_name = difficulty_str[difficulty];

                let boss_level = boss["Level" + difficulty];
                let boss_dropped_tcs = boss["TC" + difficulty];
                let item_tc_group = item["tc_group"];

                let boss_is_high_enough_level = boss_level >= item.lvl;
                let boss_can_drop_that_treasure_class =
                    boss_dropped_tcs.includes(item_tc_group);

                if (
                    boss_is_high_enough_level &&
                    boss_can_drop_that_treasure_class
                ) {
                    if (difficult_name === "Normal") {
                        boss_entry["difficulty"][0] = true;
                    }
                    if (difficult_name === "Nightmare") {
                        boss_entry["difficulty"][1] = true;
                    }
                    if (difficult_name === "Hell") {
                        boss_entry["difficulty"][2] = true;
                    }
                }
            });

            bosses.push(boss_entry);
        });

        return bosses;
    }

    // Couldn't find the item
    clear_results();
    return [];
}

function autocompleteMatch(input) {
    if (input == "") {
        return [];
    }
    var reg = new RegExp(input, "i");

    let items = d2data["items"].map(x => x["index"]);

    return items.filter(function (term) {
        if (term.match(reg)) {
            return term;
        }
    });
}

function searchFocus() {
    let search_box = document.getElementById("search");

    if (search_box !== undefined) search_box.value = "";
}

function showSearchResults(val) {
    res = document.getElementById("search_results");
    res.innerHTML = "";
    let list = "";
    let terms = autocompleteMatch(val);

    if (terms.length !== 0) {
        for (i = 0; i < terms.length; i++) {
            list +=
                '<li tabindex="0" onkeypress="searchresult_onclick(this.innerHTML)" onclick="searchresult_onclick(this.innerHTML)">' +
                terms[i] +
                "</li>";
        }
    } else if (val !== "") {
        list += '<li tabindex="0">Item not found</li>';
    }

    res.innerHTML = "<ul>" + list + "</ul>";

    if (document.getElementsByTagName("li")) {
        res.classList.add("has-items");
    } else {
        res.classList.remove("has-items");
    }

    search_onsubmit();
    return false;
}

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }

}
