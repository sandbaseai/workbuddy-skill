const input = document.querySelector("#search");
const results = document.querySelector("#results");
const count = document.querySelector("#result-count");
const empty = document.querySelector("#empty");
const error = document.querySelector("#error");
const more = document.querySelector("#more");

let catalog = [];
let filtered = [];
let shown = 0;
const PAGE_SIZE = 40;

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
  })[character]);
}

function render(reset = true) {
  if (reset) {
    shown = 0;
    results.replaceChildren();
  }
  const next = filtered.slice(shown, shown + PAGE_SIZE);
  const markup = next.map((skill) => `
    <a class="result" href="${escapeHtml(skill.u)}" target="_blank" rel="noreferrer">
      <span class="result-name">${escapeHtml(skill.n)}</span>
      <span class="result-source"><span>${escapeHtml(skill.r)}</span><code>${escapeHtml(skill.p)}</code></span>
      <span class="result-open">Inspect source ↗</span>
    </a>`).join("");
  results.insertAdjacentHTML("beforeend", markup);
  shown += next.length;
  count.textContent = `${filtered.length.toLocaleString()} results`;
  empty.hidden = filtered.length !== 0;
  more.hidden = shown >= filtered.length;
  results.setAttribute("aria-busy", "false");
}

function search() {
  const query = input.value.trim().toLocaleLowerCase();
  filtered = query
    ? catalog.filter((skill) => `${skill.n} ${skill.r} ${skill.p}`.toLocaleLowerCase().includes(query))
    : catalog;
  render();
}

input.addEventListener("input", search);
more.addEventListener("click", () => render(false));

fetch("catalog.json")
  .then((response) => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  })
  .then((data) => {
    catalog = data;
    filtered = data;
    render();
    input.disabled = false;
  })
  .catch(() => {
    results.setAttribute("aria-busy", "false");
    count.textContent = "Catalog unavailable";
    error.hidden = false;
  });

