const input = document.querySelector("#search");
const results = document.querySelector("#results");
const count = document.querySelector("#result-count");
const compatibility = document.querySelector("#compatibility");
const category = document.querySelector("#category");
const security = document.querySelector("#security");
const sourceContext = document.querySelector("#source-context");
const sort = document.querySelector("#sort");
const unique = document.querySelector("#unique");
const minScore = document.querySelector("#min-score");
const packageStatus = document.querySelector("#package-status");
const highSignal = document.querySelector("#high-signal");
const resetFilters = document.querySelector("#reset-filters");
const emptyReset = document.querySelector("#empty-reset");
const copyLink = document.querySelector("#copy-link");
const copyStatus = document.querySelector("#copy-status");
const searchExamples = [...document.querySelectorAll(".search-example")];
const empty = document.querySelector("#empty");
const externalSearch = document.querySelector("#external-search");
const error = document.querySelector("#error");
const retryLoad = document.querySelector("#retry-load");
const more = document.querySelector("#more");
const languageLink = document.querySelector("#language-link");
const metricRecords = document.querySelector("#metric-records");
const metricShas = document.querySelector("#metric-shas");
const metricRepositories = document.querySelector("#metric-repositories");
const snapshotNote = document.querySelector("#snapshot-note");
const snapshotFingerprint = document.querySelector("#snapshot-fingerprint");
const curatedNote = document.querySelector("#curated-note");
const curatedCountText = document.querySelector("#curated-count-text");
const heroCount = document.querySelector("#hero-count");
const isChinese = document.documentElement.lang.startsWith("zh");

let catalog = [];
let packagesByDownload = new Map();
let filtered = [];
let shown = 0;
const PAGE_SIZE = 40;
const DEFAULT_CHECKSUM_URL = "https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/SHA256SUMS";
let checksumUrl = DEFAULT_CHECKSUM_URL;
const FILTERS = {
  category: new Set([...category.options].map((option) => option.value)),
  compatibility: new Set([...compatibility.options].map((option) => option.value)),
  security: new Set([...security.options].map((option) => option.value)),
  source: new Set([...sourceContext.options].map((option) => option.value)),
  sort: new Set([...sort.options].map((option) => option.value)),
  minScore: new Set([...minScore.options].map((option) => option.value)),
  packageStatus: new Set([...packageStatus.options].map((option) => option.value)),
};

function syncLanguageLink() {
  languageLink.href = `${languageLink.dataset.target}${location.search}${location.hash}`;
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>'"]/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
  })[character]);
}

function catalogId(skill) {
  return `github:${skill.r}:${skill.p}`;
}

function packageAsset(skill) {
  if (!skill.a) return "";
  try {
    const asset = new URL(skill.a).pathname.split("/").pop();
    return asset && asset.endsWith(".zip") ? asset : "";
  } catch {
    return "";
  }
}

function packageInstallCommand(skill) {
  const indexedCommand = packagesByDownload.get(skill.a)?.download_command;
  if (indexedCommand) return indexedCommand;
  const asset = packageAsset(skill);
  return asset
    ? `gh release download --repo sandbaseai/workbuddy-skill --pattern '${asset}' --pattern SHA256SUMS --dir workbuddy-download --clobber`
    : "";
}

function restoreUrlState() {
  const params = new URLSearchParams(location.search);
  input.value = params.get("q") || "";
  for (const [name, control] of Object.entries({ category, compatibility, security, source: sourceContext, sort, minScore, packageStatus })) {
    control.value = control.options[0].value;
    const value = params.get(name);
    if (value && FILTERS[name].has(value)) control.value = value;
  }
  unique.checked = params.get("duplicates") !== "all";
}

function syncUrlState(historyMode = "replace") {
  const params = new URLSearchParams();
  if (input.value.trim()) params.set("q", input.value.trim());
  for (const [name, control] of Object.entries({ category, compatibility, security, source: sourceContext, packageStatus })) {
    if (control.value !== "all") params.set(name, control.value);
  }
  if (sort.value !== "score") params.set("sort", sort.value);
  if (minScore.value !== "all") params.set("minScore", minScore.value);
  if (!unique.checked) params.set("duplicates", "all");
  const query = params.toString();
  history[`${historyMode}State`](null, "", `${location.pathname}${query ? `?${query}` : ""}${location.hash}`);
  syncLanguageLink();
}

function syncExternalSearchLink() {
  const query = input.value.trim();
  const search = query ? `${query} filename:SKILL.md` : "filename:SKILL.md";
  externalSearch.href = `https://github.com/search?${new URLSearchParams({ q: search, type: "code" })}`;
}

function announceCopy(message) {
  copyStatus.textContent = message;
}

async function copyText(value) {
  try {
    await navigator.clipboard.writeText(value);
    return;
  } catch {}
  const helper = document.createElement("textarea");
  helper.value = value;
  helper.setAttribute("readonly", "");
  helper.style.position = "fixed";
  helper.style.opacity = "0";
  document.body.append(helper);
  try {
    helper.select();
    if (!document.execCommand("copy")) throw new Error("copy failed");
  } finally {
    helper.remove();
  }
}

async function copyCatalogId(button) {
  const value = button.dataset.catalogId;
  try {
    await copyText(value);
  } catch {
    announceCopy(isChinese ? "复制目录 ID 失败" : "Could not copy catalog ID");
    return;
  }
  const original = button.textContent;
  button.textContent = isChinese ? "已复制" : "Copied";
  announceCopy(isChinese ? "目录 ID 已复制" : "Catalog ID copied");
  setTimeout(() => { button.textContent = original; }, 1600);
}

async function copySearchLink() {
  const value = location.href;
  try {
    await copyText(value);
  } catch {
    announceCopy(isChinese ? "复制结果链接失败" : "Could not copy result link");
    return;
  }
  const original = copyLink.textContent;
  copyLink.textContent = isChinese ? "链接已复制" : "Link copied";
  announceCopy(isChinese ? "结果链接已复制" : "Result link copied");
  setTimeout(() => { copyLink.textContent = original; }, 1600);
}

async function copyInstallCommand(button) {
  try {
    await copyText(button.dataset.installCommand);
  } catch {
    announceCopy(isChinese ? "复制安装命令失败" : "Could not copy install command");
    return;
  }
  const original = button.textContent;
  button.textContent = isChinese ? "命令已复制" : "Command copied";
  announceCopy(isChinese ? "安装命令已复制" : "Install command copied");
  setTimeout(() => { button.textContent = original; }, 1600);
}

function render(reset = true) {
  if (reset) {
    shown = 0;
    results.replaceChildren();
  }
  const next = filtered.slice(shown, shown + PAGE_SIZE);
  const markup = next.map((skill) => {
    const installCommand = packageInstallCommand(skill);
    return `
    <article class="result">
      <h3 class="result-name">${escapeHtml(skill.n)}</h3>
      <span class="result-source"><span>${escapeHtml(skill.r)}</span><code>${escapeHtml(skill.p)}</code></span>
      <span class="result-meta">
        <span class="badge">${skill.q ?? "—"}/100</span>
        <span class="badge">${escapeHtml(skill.g)}</span>
        ${skill.c > 1 ? `<span class="badge">${isChinese ? `${skill.c} 个副本` : `${skill.c} copies`}</span>` : ""}
        <span class="badge ${skill.k === "flagged" ? "flagged" : ""}">${escapeHtml(skill.k)}</span>
        ${skill.o === "review-source" ? `<span class="badge source-review" title="${escapeHtml((skill.x || []).join(", "))}">${isChinese ? "来源待审" : "source review"}</span>` : ""}
        ${skill.a ? `<span class="badge package-review">${isChinese ? "精选包" : "reviewed package"}</span>` : ""}
        <button class="copy-id" type="button" aria-label="${isChinese ? `复制 ${escapeHtml(skill.n)} 的目录 ID` : `Copy catalog ID for ${escapeHtml(skill.n)}`}" data-catalog-id="${escapeHtml(catalogId(skill))}">${isChinese ? "复制 ID" : "Copy ID"}</button>
        ${skill.a ? `<a class="result-install" href="${escapeHtml(skill.a)}" aria-label="${isChinese ? `下载 ${escapeHtml(skill.n)} 安装包` : `Download install ZIP for ${escapeHtml(skill.n)}`}">${isChinese ? "安装 ZIP" : "Install ZIP"} ↓</a>` : ""}
        ${skill.a ? `<a class="result-verify" href="${escapeHtml(checksumUrl)}" target="_blank" rel="noreferrer" aria-label="${isChinese ? `校验 ${escapeHtml(skill.n)} 的 SHA256` : `Verify SHA256 for ${escapeHtml(skill.n)}`}">${isChinese ? "校验 SHA256" : "Verify SHA256"} ↗</a>` : ""}
        ${installCommand ? `<button class="copy-install" type="button" aria-label="${isChinese ? `复制 ${escapeHtml(skill.n)} 的安装命令` : `Copy install command for ${escapeHtml(skill.n)}`}" data-install-command="${escapeHtml(installCommand)}">${isChinese ? "复制命令" : "Copy command"}</button>` : ""}
        <a class="result-open" href="${escapeHtml(skill.u)}" target="_blank" rel="noreferrer" aria-label="${isChinese ? `查看 ${escapeHtml(skill.n)} 的来源` : `Inspect source for ${escapeHtml(skill.n)}`}">${isChinese ? "查看来源" : "Inspect"} ↗</a>
      </span>
    </article>`;
  }).join("");
  results.insertAdjacentHTML("beforeend", markup);
  shown += next.length;
  count.textContent = isChinese
    ? `显示 ${shown.toLocaleString()} / ${filtered.length.toLocaleString()} 个结果`
    : `Showing ${shown.toLocaleString()} of ${filtered.length.toLocaleString()} results`;
  empty.hidden = filtered.length !== 0;
  more.hidden = shown >= filtered.length;
  results.setAttribute("aria-busy", "false");
}

function search({ historyMode = "replace" } = {}) {
  const terms = input.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  filtered = catalog.filter((skill) => {
    const searchable = [
      skill.n,
      skill.r,
      skill.p,
      catalogId(skill),
      skill.g,
      skill.w,
      skill.k,
      skill.o,
      ...(skill.x || []),
    ].join(" ").toLocaleLowerCase();
    const textMatch = terms.every((term) => searchable.includes(term));
    const categoryMatch = category.value === "all" || skill.g === category.value;
    const compatibilityMatch = compatibility.value === "all" || skill.w === compatibility.value;
    const securityMatch = security.value === "all" || skill.k === security.value;
    const sourceMatch = sourceContext.value === "all" || skill.o === sourceContext.value;
    const scoreMatch = minScore.value === "all" || (skill.q ?? -1) >= Number(minScore.value);
    const packageMatch = packageStatus.value === "all"
      || (packageStatus.value === "reviewed" ? Boolean(skill.a) : !skill.a);
    return textMatch && categoryMatch && compatibilityMatch && securityMatch && sourceMatch && scoreMatch && packageMatch;
  });
  if (unique.checked) {
    const seen = new Set();
    filtered = filtered.filter((skill) => {
      if (seen.has(skill.s)) return false;
      seen.add(skill.s);
      return true;
    });
  }
  const compareStable = (left, right) => {
    const a = left.toLowerCase();
    const b = right.toLowerCase();
    return a < b ? -1 : a > b ? 1 : 0;
  };
  const byName = (left, right) => compareStable(left.n, right.n) || compareStable(left.r, right.r);
  const bySource = (left, right) => compareStable(left.r, right.r) || compareStable(left.p, right.p);
  if (sort.value === "score") {
    filtered.sort((left, right) => (right.q ?? -1) - (left.q ?? -1) || right.c - left.c || byName(left, right));
  } else if (sort.value === "copies") {
    filtered.sort((left, right) => right.c - left.c || (right.q ?? -1) - (left.q ?? -1) || byName(left, right));
  } else if (sort.value === "name") {
    filtered.sort(byName);
  } else if (sort.value === "source") {
    filtered.sort(bySource);
  }
  syncExternalSearchLink();
  syncUrlState(historyMode);
  render();
}

input.addEventListener("input", search);
document.addEventListener("keydown", (event) => {
  const target = event.target;
  const isFormControl = target instanceof HTMLElement
    && ["INPUT", "SELECT", "TEXTAREA", "BUTTON"].includes(target.tagName);
  if (event.key === "/" && !event.metaKey && !event.ctrlKey && !event.altKey && !isFormControl) {
    event.preventDefault();
    input.focus();
  } else if (event.key === "Escape" && document.activeElement === input && input.value) {
    input.value = "";
    search({ historyMode: "push" });
  }
});
for (const example of searchExamples) {
  example.addEventListener("click", () => {
    input.value = example.dataset.search || "";
    search({ historyMode: "push" });
    input.focus();
  });
}
for (const control of [category, compatibility, security, sourceContext, sort, unique, minScore, packageStatus]) {
  control.addEventListener("change", () => search({ historyMode: "push" }));
}
highSignal.addEventListener("click", () => {
  compatibility.value = "all";
  security.value = "no-static-flags";
  sourceContext.value = "primary-looking";
  minScore.value = "85";
  sort.value = "score";
  unique.checked = true;
  search({ historyMode: "push" });
});
resetFilters.addEventListener("click", () => {
  input.value = "";
  category.value = "all";
  compatibility.value = "all";
  security.value = "all";
  sourceContext.value = "all";
  minScore.value = "all";
  packageStatus.value = "all";
  sort.value = "score";
  unique.checked = true;
  search({ historyMode: "push" });
});
emptyReset.addEventListener("click", () => resetFilters.click());
copyLink.addEventListener("click", copySearchLink);
window.addEventListener("popstate", () => {
  restoreUrlState();
  if (catalog.length) search({ historyMode: "replace" });
});
more.addEventListener("click", () => render(false));
results.addEventListener("click", (event) => {
  const button = event.target.closest(".copy-id");
  if (button) copyCatalogId(button);
  const installButton = event.target.closest(".copy-install");
  if (installButton) copyInstallCommand(installButton);
});

restoreUrlState();
syncLanguageLink();

async function loadCatalog() {
  error.hidden = true;
  retryLoad.disabled = true;
  count.textContent = isChinese ? "正在加载目录…" : "Loading catalog…";
  results.setAttribute("aria-busy", "true");
  try {
    const requestOptions = { cache: "no-cache" };
    const [catalogResponse, metaResponse, packagesResponse] = await Promise.all([
      fetch("catalog.json", requestOptions),
      fetch("catalog-meta.json", requestOptions),
      fetch("packages.json", requestOptions),
    ]);
    if (!catalogResponse.ok || !metaResponse.ok || !packagesResponse.ok) throw new Error("catalog unavailable");
    const [data, meta, packages] = await Promise.all([catalogResponse.json(), metaResponse.json(), packagesResponse.json()]);
    if (meta.snapshot_frozen !== true) throw new Error("catalog snapshot is not frozen");
    catalog = data;
    packagesByDownload = new Map(packages.map((packageRecord) => [packageRecord.download_url, packageRecord]));
    if (typeof meta.release_checksum_url === "string" && meta.release_checksum_url.startsWith("https://")) {
      checksumUrl = meta.release_checksum_url;
    }
    filtered = data;
    metricRecords.textContent = meta.records.toLocaleString();
    heroCount.textContent = meta.records.toLocaleString();
    metricShas.textContent = meta.unique_content_shas.toLocaleString();
    metricRepositories.textContent = meta.repositories.toLocaleString();
    snapshotNote.textContent = isChinese
      ? `当前目录：${meta.records.toLocaleString()} 条 Skill，来自 ${meta.repositories.toLocaleString()} 个仓库和 ${meta.unique_content_shas.toLocaleString()} 个唯一来源内容。请通过来源链接查看上游更新。`
      : `Catalog: ${meta.records.toLocaleString()} indexed Skills from ${meta.repositories.toLocaleString()} repositories and ${meta.unique_content_shas.toLocaleString()} unique source blobs. Follow each source link for upstream updates.`;
    snapshotFingerprint.textContent = meta.catalog_sha256.slice(0, 12);
    snapshotFingerprint.title = meta.catalog_sha256;
    curatedCountText.textContent = isChinese
      ? `Release 中提供 ${meta.curated_adaptations.toLocaleString()} 个经过审阅的 WorkBuddy 包。`
      : `${meta.curated_adaptations.toLocaleString()} reviewed WorkBuddy packages are available from Releases.`;
    search();
    input.disabled = false;
    searchExamples.forEach((example) => { example.disabled = false; });
  } catch {
    results.setAttribute("aria-busy", "false");
    count.textContent = isChinese ? "目录暂时不可用" : "Catalog unavailable";
    error.hidden = false;
  } finally {
    retryLoad.disabled = false;
  }
}

retryLoad.addEventListener("click", loadCatalog);
loadCatalog();
