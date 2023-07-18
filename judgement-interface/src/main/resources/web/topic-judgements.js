let currentPage = 0;

const annotatorId = (new URLSearchParams(window.location.search)).get('annotatorId');
if (annotatorId === null) {
  alert("No annotatorId provided! Please consult the examiner for a new link!");
}
Math.seedrandom(annotatorId);

Array.from(document.querySelectorAll(".number-of-documents")).forEach(
    element => element.textContent = String(Object.keys(documentTexts).length));

const methods = new Set(Object.values(topicSuggestions).flatMap(topicSuggestionsForDocument => Object.values(topicSuggestionsForDocument)).map(topicSuggestion => topicSuggestion.method));
const ontologies = new Set(Object.values(topics).map(topic => topic.ontology));

for (const documentId in topicSuggestions) {
  const topicIds = new Set();

  const topicSuggestionsForDocument = topicSuggestions[documentId];
  methods.forEach(method => {
    const topicSuggestionsForMethod = topicSuggestionsForDocument.filter(topicSuggestion => topicSuggestion.method == method);
    ontologies.forEach(ontology => {
      const topicSuggestionsForOntology = topicSuggestionsForMethod.filter(topicSuggestion => getTopic(topicSuggestion.topicId).ontology == ontology);
      getTopTopicSuggestions(topicSuggestionsForOntology).forEach(topicId => topicIds.add(topicId));
    });
  });

  const topicEntries = [];
  Array.from(topicIds).forEach(topicId => topicEntries.push({"id":topicId,"topic":getTopic(topicId)}));
  topicEntries.sort(function(a, b) {
    return a.topic.name > b.topic.name;
  }).forEach(topicEntry => {addTopicSuggestion(documentId, topicEntry.id, topicEntry.topic)});
}

const pages = Object.keys(documentTexts);

function sendSelection(evt) {
  const button = evt.target;
  if (button.checked) {
    const isRelevant = button.getAttribute("value") === "relevant";
    const data = {
      "documentId":button.closest(".page").getAttribute("data-document-id"),
      "topicId":button.closest(".topic-suggestion").getAttribute("data-topic-id"),
      "annotatorId":annotatorId,
      "isRelevant":isRelevant
    };
    console.log("sending " + JSON.stringify(data));

    const request = new XMLHttpRequest();
    const url = "judgements";
    request.open("PUT", url);
    request.setRequestHeader("Content-type", "application/json");
    request.send(JSON.stringify(data));

    const suggestion = button.closest(".topic-suggestion");
    suggestion.classList.remove("negative", "positive");
    if (isRelevant) {
      suggestion.classList.add("positive");
    } else {
      suggestion.classList.add("negative");
    }
  }
}

{
  const keysdown = {};

  const request = new XMLHttpRequest();
  const url = "judgements?annotatorId=" + annotatorId;
  request.addEventListener("load", resultObject => {
    const result = JSON.parse(resultObject.target.responseText);
    for (documentId in result) {
      const annotationsForDocument = result[documentId];
      for (topicId in annotationsForDocument) {
        const topicRow = document.querySelector(".page[data-document-id='" + documentId + "'] .topic-suggestion[data-topic-id='" + topicId + "']");
        if (topicRow !== null) {
          const isRelevant = annotationsForDocument[topicId];
          if (isRelevant) {
            topicRow.querySelector("input[value = 'relevant']").checked = true;
            topicRow.classList.add("positive");
          } else {
            topicRow.querySelector("input[value = 'not-relevant']").checked = true;
            topicRow.classList.add("negative");
          }
        }
      }
    }

    Array.from(document.querySelectorAll("input[type='radio']")).forEach(
        element => element.addEventListener("click", sendSelection));

    let p = 1;
    while (p < pages.length && isPageComplete(p)) { ++p; }
    showPage(p);
    activateNextMissingRow();

    Array.from(document.querySelectorAll(".topic-suggestion")).forEach(row => {
      row.addEventListener('click', evt => {
        activateRow(row);
      });
    });

    document.addEventListener('keydown', evt => {
      const activeRow = document.querySelector(".page.active .topic-suggestion.active");
      if (activeRow !== null) {
        if (evt.code === "ArrowUp") {
          const prev = activeRow.previousSibling;
          if (prev !== null) {
            activateRow(prev);
          } else if (currentPage > 1) {
            showPage(currentPage - 1);
            const rows = document.querySelectorAll(".page.active .topic-suggestion");
            activateRow(rows[rows.length - 1]);
          }
          evt.preventDefault();
        } else if (evt.code === "ArrowDown") {
          activateNextRow();
          evt.preventDefault();
        } else if (evt.code === "ArrowLeft") {
          evt.preventDefault();
          if (!(evt.key in keysdown)) {
            keysdown[evt.key] = true;
            activeRow.children[1].querySelector("input").click();
            activateNextMissingRow();
          }
        } else if (evt.code === "ArrowRight") {
          evt.preventDefault();
          if (!(evt.key in keysdown)) {
            keysdown[evt.key] = true;
            activeRow.children[2].querySelector("input").click();
            activateNextMissingRow();
          }
        }
      }
    });

  });

  document.addEventListener('keyup', evt => {
    delete keysdown[evt.key]; // based on https://stackoverflow.com/a/40551573
  });
  request.open("GET", url);
  request.send(null);
}

function getDocumentIdForPage(pageNumber) {
  if (pageNumber > pages.length) { return null; }
  return pages[pageNumber - 1];
}

function showPage(pageNumber) {
  Array.from(document.querySelectorAll(".current-document-number")).forEach(
      element => element.textContent = String(pageNumber));

  const documentId = getDocumentIdForPage(pageNumber);

  const oldPage = document.querySelector(".page.active");
  if (oldPage !== null) { oldPage.classList.remove("active"); }
  const page = document.querySelector(".page[data-document-id='" + documentId + "']");
  page.classList.add("active");

  document.querySelector("#documentText").textContent = documentTexts[documentId];

  const previous = document.querySelector(".page-item[data-page='previous']");
  if (pageNumber > 1) {
    previous.classList.remove("disabled");
  } else {
    previous.classList.add("disabled");
  }

  const next = document.querySelector(".page-item[data-page='next']");
  if (pageNumber < pages.length) {
    next.classList.remove("disabled");
  } else {
    next.classList.add("disabled");
  }

  currentPage = pageNumber;
}

document.querySelector(".page-item[data-page='previous']").addEventListener("click",
    evt => { if (currentPage > 1) { showPage(currentPage - 1); } });

document.querySelector(".page-item[data-page='next']").addEventListener("click",
    evt => { if (currentPage < pages.length) { showPage(currentPage + 1); } });


function isPageComplete(pageNumber) {
  const documentId = getDocumentIdForPage(pageNumber);

  const page = document.querySelector(".page[data-document-id='" + documentId + "']");
  if (page === null) {
    console.log(pageNumber + " -> " + documentId)
  }
  const numRadios = page.querySelectorAll("input[type='radio']").length;
  const numRadiosChecked = page.querySelectorAll("input[type='radio']:checked").length;
  return numRadios == numRadiosChecked * 2;
}

function activateNextMissingRow() {
  const hadPreviouslyActive = document.querySelector(".page.active .topic-suggestion.active") !== null;
  const candidates = hadPreviouslyActive
    ? document.querySelectorAll(".page.active .topic-suggestion.active ~ .topic-suggestion")
    : document.querySelectorAll(".page.active .topic-suggestion");
  for (let c = 0; c < candidates.length; ++c) {
    const candidate = candidates[c];
    if (candidate.querySelector("input[type='radio']:checked") === null) {
      activateRow(candidate);
      return;
    }
  }
  // no row left on page
  const nextPageButton = document.querySelector(".page-item[data-page='next']");
  if (!nextPageButton.classList.contains("disabled")) {
    showPage(currentPage + 1);
    activateNextMissingRow();
  }
}

function activateNextRow(addClass = null) {
  const activeRow = document.querySelector(".page.active .topic-suggestion.active");
  if (activeRow !== null) {
    const next = activeRow.nextSibling;
    if (next !== null) {
      activateRow(next, addClass);
    } else if (currentPage < pages.length) {
      showPage(currentPage + 1);
      const rows = document.querySelectorAll(".page.active .topic-suggestion");
      activateRow(rows[0], addClass);
    }
  }
}

function activateRow(row, addClass = null) {
  const previouslyActive = Array.from(document.querySelectorAll(".topic-suggestion.active"));
  previouslyActive.forEach(row => row.classList.remove("active"));

  row.classList.add("active");
  document.querySelector("body").classList.remove("last-positive", "last-negative");
  if (addClass != null) {
    document.querySelector("body").classList.add(addClass);
  }
  row.scrollIntoView();

  const topic = getTopic(row.getAttribute("data-topic-id"));
  const nameHeading = document.querySelector(".topic-name");
  nameHeading.textContent = topic.name;
  const descriptionPanel = document.querySelector(".topic-description");
  descriptionPanel.textContent = topic.description;
}

function getTopic(topicId) {
  const topic = topics[topicId];
  if (topic === undefined) {
    console.log("No such topic: " + topicId);
  }
  return topic;
}

function getTopTopicSuggestions(topicSuggestions, n = 5) {
  const topicIds = new Set();

  const sortedTopicSuggestions = topicSuggestions.sort(topicSuggestionComparator);
  let lastScore = Number.POSITIVE_INFINITY;
  for (let t = 0; t < sortedTopicSuggestions.length; ++t) {
    const topicSuggestion = sortedTopicSuggestions[t];
    if (t >= n && (lastScore - topicSuggestion.score) > 0.00000001) {
      break;
    }
    topicIds.add(topicSuggestion.topicId);
    lastScore = topicSuggestion.score;
  }

  return topicIds;
}

function topicSuggestionComparator(topicSuggestionA, topicSuggestionB) {
  return topicSuggestionB.score - topicSuggestionA.score;
}

function addTopicSuggestionsCard(documentId) {
  const card = document.createElement("div");
  card.setAttribute("data-document-id", documentId);
  card.classList.add("card", "page");
  card.innerHTML = "<h5 class='card-header'>Topic Suggestions</h5><div class='card-body topic-suggestions'></div>";

  const form = document.querySelector("form");
  const nav = document.querySelector("nav");
  form.insertBefore(card, nav);

  return card;
}

function getTopicSuggestionsCard(documentId) {
  const card = document.querySelector("[data-document-id='" + documentId + "']");
  if (card == null) {
    return addTopicSuggestionsCard(documentId);
  } else {
    return card;
  }
}

function addTopicSuggestion(documentId, topicId, topic = getTopic(topicId)) {
  const row = document.createElement("div");
  row.classList.add("topic-suggestion")
  row.setAttribute("data-topic-id", topicId);

  const topicNameCell = document.createElement("span");
  topicNameCell.innerText = topic["name"];
  row.appendChild(topicNameCell);

  row.appendChild(makeTopicSuggestionOptionCell(documentId, topicId, "relevant"));
  row.appendChild(makeTopicSuggestionOptionCell(documentId, topicId, "not-relevant"));

  const card = getTopicSuggestionsCard(documentId);
  const body = card.querySelector(".card-body");
  body.appendChild(row);
}

function makeTopicSuggestionOptionCell(documentId, topicId, value) {
  const cell = document.createElement("span");
  const radio = document.createElement("input");
  radio.setAttribute("type", "radio");
  radio.setAttribute("name", documentId + "-" + topicId);
  radio.setAttribute("value", value);
  cell.appendChild(radio);
  return cell;
}

/**
 * Shuffles array in place. ES6 version
 * @param {Array} a items An array containing the items.
 *
 * https://stackoverflow.com/a/6274381
 */
function shuffle(a) {
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}
