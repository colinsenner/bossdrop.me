var d2data = {};

$.getJSON("results.json", function (data) {
  d2data = data;
});

function searchresult_onclick(data) {
  let search_input = document.getElementById("search");
  search_input.value = data;

  clear_search_results();
  search_onsubmit();
}

function clear_search_results() {
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

    bosses.forEach((boss) => {
      if (boss["difficulty"].some((x) => x)) {
        let row = "";

        row += `<div class="boss_name">${boss["name"]}</div>`;

        for (let index = 0; index < 3; index++) {
          if (boss["difficulty"][index]) {
            row += `<div class="item-result"><svg class="w-6 h-6 mx-auto fill-diablo-yellow-darker dark:fill-diablo-yellow" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2024 Fonticons, Inc. --><path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z"/></svg></div>`;
          } else {
            row += `<div class="item-result no-drop opacity-20"><svg class="w-6 h-6 mx-auto dark:fill-slate-200" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><!--! Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2024 Fonticons, Inc. --><path d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z"/></svg></div>`;
          }
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

  let item = all_items.filter((item) => item["index"] == item_name)[0];

  if (item !== undefined) {
    // Found the item
    let bosses = [];

    all_monsters.forEach((boss) => {
      let boss_entry = {
        name: boss["NameStr"],
        Level: boss["Level"],
        "Level(N)": boss["Level(N)"],
        "Level(H)": boss["Level(H)"],
        difficulty: [false, false, false],
      };

      ["", "(N)", "(H)"].forEach((difficulty) => {
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

        // Hack
        // The game does not allow Cow King items to be dropped by other bosses
        // Even though, for instance, "Cow King's Hide" is lvl 20 and in TC 9
        // No other bosses can drop it. (Could also filter out TCs which don't contain "Cow King")
        let set_is_cow_king = item["index"].startsWith("Cow King's");
        let boss_is_cow_king = boss_entry["name"] === "The Cow King";

        if (
          boss_is_high_enough_level &&
          boss_can_drop_that_treasure_class &&
          (!set_is_cow_king || boss_is_cow_king)
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

  let items = d2data["items"].map((x) => x["index"]);

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
        '<li class="item-search-result" tabindex="0" onkeypress="searchresult_onclick(this.innerHTML)" onclick="searchresult_onclick(this.innerHTML)">' +
        terms[i] +
        "</li>";
    }
  } else if (val !== "") {
    list += '<li tabindex="-1">Item not found</li>';
  }

  res.innerHTML = "<ul>" + list + "</ul>";

  search_onsubmit();
  return false;
}

function removeAllChildNodes(parent) {
  while (parent.firstChild) {
    parent.removeChild(parent.firstChild);
  }
}

// Performs the logic of setting classnames in our DOM for the light / dark theme
function setMode(mode) {
  // Update our html element to have the correct classname
  document.getElementsByTagName("html")[0].classList.remove("light");
  document.getElementsByTagName("html")[0].classList.remove("dark");
  document.getElementsByTagName("html")[0].classList.add(mode);
}

// Find the mode we're toggling to, set it in local storage
function toggleDarkMode() {
  const mode =
    localStorage.mode === "light" || !localStorage.mode ? "dark" : "light";
  localStorage.mode = mode;
  setMode(mode);
}

// Find the mode from local storage and update our html to match
function initialiseMode() {
  const mode =
    localStorage.mode === "light" || !localStorage.mode ? "light" : "dark";
  setMode(mode);
}

window.onload = initialiseMode;
