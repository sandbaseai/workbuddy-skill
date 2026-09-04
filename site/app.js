const input = document.querySelector("#search");
const results = document.querySelector("#results");
const count = document.querySelector("#result-count");
const compatibility = document.querySelector("#compatibility");
const security = document.querySelector("#security");
const empty = document.querySelector("#empty");
const error = document.querySelector("#error");
const more = document.querySelector("#more");
const metricRecords = document.querySelector("#metric-records");
const metricShas = document.querySelector("#metric-shas");
const metricRepositories = document.querySelector("#metric-repositories");
const isChinese = document.documentElement.lang.startsWith("zh");

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
      <span class="result-meta">
        <span class="badge">${skill.q ?? "—"}/100</span>
        <span class="badge ${skill.k === "flagged" ? "flagged" : ""}">${escapeHtml(skill.k)}</span>
        <span class="result-open">${isChinese ? "查看来源" : "Inspect"} ↗</span>
      </span>
    </a>`).join("");
  results.insertAdjacentHTML("beforeend", markup);
  shown += next.length;
  count.textContent = isChinese ? `${filtered.length.toLocaleString()} 个结果` : `${filtered.length.toLocaleString()} results`;
  empty.hidden = filtered.length !== 0;
  more.hidden = shown >= filtered.length;
  results.setAttribute("aria-busy", "false");
}

function search() {
  const query = input.value.trim().toLocaleLowerCase();
  filtered = catalog.filter((skill) => {
    const textMatch = !query || `${skill.n} ${skill.r} ${skill.p}`.toLocaleLowerCase().includes(query);
    const compatibilityMatch = compatibility.value === "all" || skill.w === compatibility.value;
    const securityMatch = security.value === "all" || skill.k === security.value;
    return textMatch && compatibilityMatch && securityMatch;
  });
  render();
}

input.addEventListener("input", search);
compatibility.addEventListener("change", search);
security.addEventListener("change", search);
more.addEventListener("click", () => render(false));

Promise.all([fetch("catalog.json"), fetch("catalog-meta.json")])
  .then(async ([catalogResponse, metaResponse]) => {
    if (!catalogResponse.ok || !metaResponse.ok) throw new Error("catalog unavailable");
    return Promise.all([catalogResponse.json(), metaResponse.json()]);
  })
  .then(([data, meta]) => {
    catalog = data;
    filtered = data;
    metricRecords.textContent = meta.records.toLocaleString();
    metricShas.textContent = meta.unique_content_shas.toLocaleString();
    metricRepositories.textContent = meta.repositories.toLocaleString();
    render();
    input.disabled = false;
  })
  .catch(() => {
    results.setAttribute("aria-busy", "false");
    count.textContent = isChinese ? "目录暂时不可用" : "Catalog unavailable";
    error.hidden = false;
  });
