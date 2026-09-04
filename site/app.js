const input = document.querySelector("#search");
const results = document.querySelector("#results");
const count = document.querySelector("#result-count");
const compatibility = document.querySelector("#compatibility");
const category = document.querySelector("#category");
const security = document.querySelector("#security");
const sort = document.querySelector("#sort");
const unique = document.querySelector("#unique");
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
const FILTERS = {
  category: new Set([...category.options].map((option) => option.value)),
  compatibility: new Set([...compatibility.options].map((option) => option.value)),
  security: new Set([...security.options].map((option) => option.value)),
  sort: new Set([...sort.options].map((option) => option.value)),
};

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
  })[character]);
}

function catalogId(skill) {
  return `github:${skill.r}:${skill.p}`;
}

function restoreUrlState() {
  const params = new URLSearchParams(location.search);
  input.value = params.get("q") || "";
  for (const [name, control] of Object.entries({ category, compatibility, security, sort })) {
    const value = params.get(name);
    if (value && FILTERS[name].has(value)) control.value = value;
  }
  unique.checked = params.get("duplicates") !== "all";
}

function syncUrlState() {
  const params = new URLSearchParams();
  if (input.value.trim()) params.set("q", input.value.trim());
  for (const [name, control] of Object.entries({ category, compatibility, security })) {
    if (control.value !== "all") params.set(name, control.value);
  }
  if (sort.value !== "score") params.set("sort", sort.value);
  if (!unique.checked) params.set("duplicates", "all");
  const query = params.toString();
  history.replaceState(null, "", `${location.pathname}${query ? `?${query}` : ""}${location.hash}`);
}

async function copyCatalogId(button) {
  const value = button.dataset.catalogId;
  try {
    await navigator.clipboard.writeText(value);
  } catch {
    const helper = document.createElement("textarea");
    helper.value = value;
    helper.setAttribute("readonly", "");
    helper.style.position = "fixed";
    helper.style.opacity = "0";
    document.body.append(helper);
    helper.select();
    document.execCommand("copy");
    helper.remove();
  }
  const original = button.textContent;
  button.textContent = isChinese ? "已复制" : "Copied";
  setTimeout(() => { button.textContent = original; }, 1600);
}

function render(reset = true) {
  if (reset) {
    shown = 0;
    results.replaceChildren();
  }
  const next = filtered.slice(shown, shown + PAGE_SIZE);
  const markup = next.map((skill) => `
    <article class="result">
      <span class="result-name">${escapeHtml(skill.n)}</span>
      <span class="result-source"><span>${escapeHtml(skill.r)}</span><code>${escapeHtml(skill.p)}</code></span>
      <span class="result-meta">
        <span class="badge">${skill.q ?? "—"}/100</span>
        <span class="badge">${escapeHtml(skill.g)}</span>
        ${skill.c > 1 ? `<span class="badge">${skill.c} copies</span>` : ""}
        <span class="badge ${skill.k === "flagged" ? "flagged" : ""}">${escapeHtml(skill.k)}</span>
        <button class="copy-id" type="button" data-catalog-id="${escapeHtml(catalogId(skill))}">${isChinese ? "复制 ID" : "Copy ID"}</button>
        <a class="result-open" href="${escapeHtml(skill.u)}" target="_blank" rel="noreferrer">${isChinese ? "查看来源" : "Inspect"} ↗</a>
      </span>
    </article>`).join("");
  results.insertAdjacentHTML("beforeend", markup);
  shown += next.length;
  count.textContent = isChinese ? `${filtered.length.toLocaleString()} 个结果` : `${filtered.length.toLocaleString()} results`;
  empty.hidden = filtered.length !== 0;
  more.hidden = shown >= filtered.length;
  results.setAttribute("aria-busy", "false");
}

function search() {
  const terms = input.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  filtered = catalog.filter((skill) => {
    const searchable = `${skill.n} ${skill.r} ${skill.p}`.toLocaleLowerCase();
    const textMatch = terms.every((term) => searchable.includes(term));
    const categoryMatch = category.value === "all" || skill.g === category.value;
    const compatibilityMatch = compatibility.value === "all" || skill.w === compatibility.value;
    const securityMatch = security.value === "all" || skill.k === security.value;
    return textMatch && categoryMatch && compatibilityMatch && securityMatch;
  });
  if (unique.checked) {
    const seen = new Set();
    filtered = filtered.filter((skill) => {
      if (seen.has(skill.s)) return false;
      seen.add(skill.s);
      return true;
    });
  }
  const byName = (left, right) => left.n.localeCompare(right.n) || left.r.localeCompare(right.r);
  if (sort.value === "score") {
    filtered.sort((left, right) => (right.q ?? -1) - (left.q ?? -1) || right.c - left.c || byName(left, right));
  } else if (sort.value === "copies") {
    filtered.sort((left, right) => right.c - left.c || (right.q ?? -1) - (left.q ?? -1) || byName(left, right));
  } else if (sort.value === "name") {
    filtered.sort(byName);
  }
  syncUrlState();
  render();
}

input.addEventListener("input", search);
category.addEventListener("change", search);
compatibility.addEventListener("change", search);
security.addEventListener("change", search);
sort.addEventListener("change", search);
unique.addEventListener("change", search);
more.addEventListener("click", () => render(false));
results.addEventListener("click", (event) => {
  const button = event.target.closest(".copy-id");
  if (button) copyCatalogId(button);
});

restoreUrlState();

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
    search();
    input.disabled = false;
  })
  .catch(() => {
    results.setAttribute("aria-busy", "false");
    count.textContent = isChinese ? "目录暂时不可用" : "Catalog unavailable";
    error.hidden = false;
  });
