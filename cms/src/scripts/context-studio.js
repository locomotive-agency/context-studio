// @ts-nocheck
import { ArrowLeft, Badge, Box, Braces, Brackets, Building2, ChevronLeft, ChevronRight, CircleAlert, CircleCheck, Database, FilePlus2, FileSearch, FileText, Files, Folder, FolderCog, FolderPlus, GitBranch, GripVertical, History, Menu, Network, PanelRight, Pencil, Plus, RefreshCw, RotateCcw, Save, Search, ShieldCheck, TestTube2, Trash2, Upload, UserPlus, Users, X, createIcons } from "lucide";
import DOMPurify from "dompurify";
import yaml from "js-yaml";
import { marked } from "marked";

const API = "";
const state = { user: null, auth: {mode: "local", repository: null}, documents: [], folders: [], scopes: [], collections: [], collectionDocuments: [], selectedCollection: "", revisions: [], current: null, selectedRevision: null, schemaPath: "", drawerMode: "", drawerData: null, deleteArmed: false, documentDeleteArmed: false, folderDeleteArmed: false, dirty: false, folder: "", page: 1, pageSize: 50, draggedScopeId: null, draggedDocumentPath: "", draggedFolderPath: "", editorMode: "raw", historyMode: "repository", okfImportScan: null, okfImportFiles: [], okfImportFolderName: "", okfImportPayload: null, benchCollections: new Set(), benchSources: new Map() };
const viewLabels = { documents: "Documents", collections: "Collections", "test-bench": "MCP Test Tool", validation: "Validation", history: "History", scopes: "Scopes", schemas: "Schemas", users: "Users" };
const byId = (id) => document.getElementById(id);
const api = async (path, options = {}) => {
  const response = await fetch(`${API}${path}`, { credentials: "include", headers: { "Content-Type": "application/json", ...(options.headers || {}) }, ...options });
  if (!response.ok) { const data = await response.json().catch(() => ({})); throw new Error(data.detail || `Request failed (${response.status})`); }
  return response.status === 204 ? null : response.json();
};
const escapeHtml = (value = "") => value.replace(/[&<>'"]/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" })[char]);
const toast = (message, error = false) => { const el = byId("toast"); el.textContent = message; el.className = `toast${error ? " error" : ""}`; setTimeout(() => el.classList.add("hidden"), 2600); };
const iconSet = { ArrowLeft, Badge, Box, Braces, Brackets, Building2, ChevronLeft, ChevronRight, CircleAlert, CircleCheck, Database, FilePlus2, FileSearch, FileText, Files, Folder, FolderCog, FolderPlus, GitBranch, GripVertical, History, Menu, Network, PanelRight, Pencil, Plus, RefreshCw, RotateCcw, Save, Search, ShieldCheck, TestTube2, Trash2, Upload, UserPlus, Users, X };
const canEdit = () => Boolean(state.user?.can_edit ?? state.user?.role !== "viewer");
const canManage = () => state.user?.role === "admin";
const refreshIcons = () => createIcons({ icons: iconSet });
const typeOptions = [["audience-profile","Audience Profile"],["brand-messaging","Brand Messaging"],["business-goals","Business Goals"],["case-study","Case Study"],["communication-preferences","Communication Preferences"],["competitive-landscape","Competitive Landscape"],["customer-journey","Customer Journey"],["how-we-look","How We Look"],["how-we-sound","How We Sound"],["how-we-write","How We Write"],["legal-and-compliance","Legal and Compliance"],["measurement-and-kpis","Measurement and KPIs"],["playbook","Playbook"],["product-and-offering","Product and Offering"],["proof-points","Proof Points"],["reference","Reference"],["sub-product","Sub-product"],["tech-stack","Tech Stack"],["use-cases-and-solutions","Use Cases and Solutions"],["value-proposition","Value Proposition"]];
const metadataGroups = [
  {title:"Classification", fields:[
    {key:"type", label:"Type", type:"select", options:typeOptions},
    {key:"scope_id", label:"Scope", type:"scope"},
    {key:"durability", label:"Durability", type:"select", options:[["ephemeral","Ephemeral"],["time_bound","Time-bound"],["persistent","Persistent"]]},
    {key:"criticality", label:"Criticality", type:"select", options:[["flexible","Flexible"],["hybrid","Hybrid"],["controlled","Controlled"]]},
  ]},
  {title:"Governance and access", fields:[
    {key:"status", label:"Status", type:"select", options:[["draft","Draft"],["proposed","Proposed"],["approved","Approved"],["archived","Archived"]]},
  ]},
  {title:"Sources and freshness", fields:[
    {key:"provenance", label:"Provenance", type:"text", placeholder:"Source URL, URI, or document name"},
    {key:"valid_until", label:"Good until", type:"date", temporal:true},
  ]},
  {title:"Supporting sources", hideWhenCriticality:"controlled", fields:[
    {key:"supporting_sources.collections", label:"Collections", type:"list", placeholder:"collection-1, collection-2"},
    {key:"supporting_sources.web", label:"Web", type:"list", placeholder:"https://example.com/page"},
    {key:"supporting_sources.mcp", label:"MCP servers", type:"list", placeholder:"sales-calls, https://example.com/mcp"},
  ]},
];
const allMetadataFields = metadataGroups.flatMap((group) => group.fields);
const metadataFieldByKey = new Map(allMetadataFields.map((field) => [field.key, field]));
const metadataKeys = allMetadataFields.map((field) => field.key);

const mcpTools = [
  ["list_context_scopes", "List context scopes"],
  ["list_context_types", "List context types"],
  ["list_context_folders", "List context folders"],
  ["read_context_index", "Read context index"],
  ["read_context_log", "Read context log"],
  ["list_context_documents", "List context documents"],
  ["read_context_document", "Read context document"],
  ["search_collection", "Search collection"],
  ["read_collection_source", "Read collection source"],
  ["validate_context", "Validate context"],
];

const benchFieldsByTool = {
  list_context_scopes: [],
  list_context_types: [{key:"scope_id", label:"Scope", type:"scope"}],
  list_context_folders: [{key:"type", label:"Type", type:"context-type", optional:true}, {key:"scope_id", label:"Scope", type:"scope"}],
  read_context_index: [{key:"folder", label:"Folder", placeholder:"competitors"}, {key:"scope_id", label:"Scope", type:"scope"}],
  read_context_log: [{key:"folder", label:"Folder", placeholder:"competitors"}, {key:"scope_id", label:"Scope", type:"scope"}],
  list_context_documents: [{key:"type", label:"Type", type:"context-type"}, {key:"scope_id", label:"Scope", type:"scope"}, {key:"folder", label:"Folder", placeholder:"competitors/sub-products"}, {key:"limit", label:"Limit", type:"number", value:"100"}],
  read_context_document: [{key:"path", label:"Path", placeholder:"competitors/sub-products/apollo-b2b-data.md"}, {key:"scope_id", label:"Scope", type:"scope"}],
  search_collection: [{key:"collection", label:"Collection", type:"bench-collection"}, {key:"query", label:"Query", placeholder:"renewal risk"}, {key:"limit", label:"Limit", type:"number", value:"10"}],
  read_collection_source: [{key:"collection", label:"Collection", type:"bench-collection"}, {key:"source_id", label:"Source", type:"bench-source"}],
  validate_context: [],
};

function renderMetadataFields(prefix, own = {}, inherited = {}, disabled = false) {
  const container = byId(`${prefix}-metadata-fields`);
  container.innerHTML = visibleMetadataGroups(own, inherited).map((group) => `<section class="metadata-section"><div class="metadata-section-heading"><strong>${group.title}</strong></div><div class="metadata-grid">${group.fields.map((field) => metadataFieldMarkup(prefix, field, own, inherited, disabled)).join("")}</div></section>`).join("");
  const durability = byId(`${prefix}-meta-durability`);
  const updateTemporal = () => {
    const show = (durability.value || inherited.durability) === "time_bound" || Boolean(own.valid_until);
    container.querySelectorAll("[data-temporal]").forEach((element) => element.classList.toggle("hidden", !show));
  };
  durability.addEventListener("change", updateTemporal); updateTemporal();
  const criticality = byId(`${prefix}-meta-criticality`);
  criticality.addEventListener("change", () => {
    const draft = collectMetadataFields(prefix, structuredClone(own), {pruneControlled:false});
    renderMetadataFields(prefix, draft, inherited, disabled);
    if (prefix === "document") markDocumentDirty();
  });
  if (prefix === "document") container.querySelectorAll("input, select").forEach((element) => element.addEventListener("input", markDocumentDirty));
}

function visibleMetadataGroups(own = {}, inherited = {}) {
  const effectiveCriticality = own.criticality || inherited.criticality || "";
  return metadataGroups.filter((group) => group.hideWhenCriticality !== effectiveCriticality);
}

function metadataFieldMarkup(prefix, field, own, inherited, disabled) {
  const ownValue = getPathValue(own, field.key);
  const inheritedValue = getPathValue(inherited, field.key);
  const hasOwn = ownValue !== undefined && ownValue !== null;
  const value = hasOwn ? metadataInputValue(ownValue, field.type) : "";
  const inheritedText = inheritedValue === undefined || inheritedValue === null ? "Not set" : `Inherited: ${metadataDisplayValue(field.key, inheritedValue)}`;
  const id = metadataElementId(prefix, field.key);
  let control;
  if (field.type === "select" || field.type === "boolean") {
    const options = field.type === "boolean" ? [["true","Yes"],["false","No"]] : field.options;
    const known = options.some(([option]) => option === value);
    control = `<select id="${id}" class="select" ${disabled ? "disabled" : ""}><option value="">${escapeHtml(inheritedText)}</option>${!known && value ? `<option value="${escapeHtml(value)}" selected>${escapeHtml(value)}</option>` : ""}${options.map(([option,label]) => `<option value="${option}" ${value === option ? "selected" : ""}>${label}</option>`).join("")}</select>`;
  } else if (field.type === "scope") {
    control = `<select id="${id}" class="select" ${disabled ? "disabled" : ""}><option value="">${escapeHtml(inheritedText)}</option>${orderedScopes().map(({scope,depth}) => `<option value="${escapeHtml(scope.id)}" ${value === scope.id ? "selected" : ""}>${"— ".repeat(depth)}${escapeHtml(scope.name)} (${escapeHtml(scope.level)})</option>`).join("")}</select>`;
  } else {
    control = `<input id="${id}" class="input" type="${field.type === "list" ? "text" : field.type}" value="${escapeHtml(value)}" placeholder="${escapeHtml(hasOwn ? field.placeholder || "" : inheritedText)}" ${field.type === "number" ? "min=\"1\"" : ""} ${disabled ? "readonly" : ""} />`;
  }
  const ownLabel = prefix === "schema" ? "Set for this folder" : "Overrides folder default";
  return `<div class="field metadata-field" ${field.temporal ? "data-temporal" : ""}><label for="${id}">${field.label}</label>${control}${hasOwn ? `<small class="override-label">${ownLabel}</small>` : inheritedValue !== undefined && inheritedValue !== null ? `<small class="inherited-label">${escapeHtml(inheritedText)}</small>` : ""}</div>`;
}

function metadataInputValue(value, type) {
  if (type === "list") return Array.isArray(value) ? value.join(", ") : String(value || "");
  if (type === "boolean") return value === true ? "true" : value === false ? "false" : "";
  if (type === "date" && value instanceof Date) return value.toISOString().slice(0, 10);
  return String(value ?? "");
}

function metadataDisplayValue(key, value) {
  if (key === "scope_id") { const scope = state.scopes.find((item) => item.id === value); return scope ? `${scope.name} (${scope.level})` : String(value); }
  if (Array.isArray(value)) return value.join(", ");
  if (value === true) return "Yes";
  if (value === false) return "No";
  return String(value).replaceAll("_", " ");
}

function collectMetadataFields(prefix, target, options = {}) {
  const {pruneControlled = true} = options;
  for (const key of metadataKeys) {
    const field = metadataFieldByKey.get(key);
    const element = byId(metadataElementId(prefix, key));
    if (!element) { deletePathValue(target, key); continue; }
    const value = element.value.trim();
    if (!value) { deletePathValue(target, key); continue; }
    if (field.type === "list") setPathValue(target, key, value.split(",").map((item) => item.trim()).filter(Boolean));
    else if (field.type === "boolean") setPathValue(target, key, value === "true");
    else if (field.type === "number") setPathValue(target, key, Number(value));
    else setPathValue(target, key, value);
  }
  if (pruneControlled) pruneControlledSupportingSources(prefix, target);
  if (target.supporting_sources && !Object.values(target.supporting_sources).some((value) => Array.isArray(value) && value.length)) delete target.supporting_sources;
  return target;
}

function pruneControlledSupportingSources(prefix, target) {
  const criticality = target.criticality || byId(`${prefix}-meta-criticality`)?.value || "";
  if (criticality === "controlled") delete target.supporting_sources;
}

function metadataElementId(prefix, key) {
  return `${prefix}-meta-${key.replaceAll("_", "-").replaceAll(".", "-")}`;
}

function getPathValue(source, path) {
  return path.split(".").reduce((current, part) => current?.[part], source);
}

function setPathValue(target, path, value) {
  const parts = path.split(".");
  let current = target;
  parts.slice(0, -1).forEach((part) => { current[part] = current[part] || {}; current = current[part]; });
  current[parts.at(-1)] = value;
}

function deletePathValue(target, path) {
  const parts = path.split(".");
  let current = target;
  parts.slice(0, -1).forEach((part) => { current = current?.[part]; });
  if (current) delete current[parts.at(-1)];
}

function markDocumentDirty() {
  if (!state.current) return;
  state.dirty = true; byId("save-state").textContent = "Unsaved changes";
}

async function start() {
  refreshIcons();
  state.auth = await api("/api/auth/config");
  configureLogin();
  const error = new URLSearchParams(window.location.search).get("auth_error");
  if (error) { byId("login-error").textContent = error; byId("login-error").classList.remove("hidden"); }
  try { state.user = await api("/api/auth/me"); await enterWorkspace(); } catch { byId("login").classList.remove("hidden"); }
}

function configureLogin() {
  const githubMode = state.auth.mode === "github";
  byId("login-copy").textContent = githubMode && state.auth.repository ? `Sign in with access to ${state.auth.repository}` : "Documentation workspace";
  document.querySelectorAll(".local-login-field").forEach((element) => element.classList.toggle("hidden", githubMode));
  byId("local-login-button").classList.toggle("hidden", githubMode);
  byId("github-login-button").classList.toggle("hidden", !githubMode);
  refreshIcons();
}

byId("github-login-button").addEventListener("click", () => { window.location.href = `${API}/api/auth/github/login`; });

byId("login-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    state.user = await api("/api/auth/login", { method: "POST", body: JSON.stringify({ username: byId("username").value, password: byId("password").value }) });
    byId("login-error").classList.add("hidden");
    await enterWorkspace();
  } catch (error) { byId("login-error").textContent = error.message; byId("login-error").classList.remove("hidden"); }
});

async function enterWorkspace() {
  byId("login").classList.add("hidden"); byId("workspace").classList.remove("hidden");
  byId("user-initial").textContent = state.user.username.slice(0, 1).toUpperCase();
  byId("user-name").textContent = state.user.username;
  byId("user-role").textContent = state.user.auth_mode === "github" ? `${state.user.role} via GitHub` : state.user.role;
  document.querySelectorAll(".admin-only").forEach((el) => el.classList.toggle("hidden", !canManage()));
  document.querySelectorAll(".editor-only").forEach((el) => el.classList.toggle("hidden", !canEdit()));
  document.querySelector('[data-view="users"]')?.classList.toggle("hidden", state.user.auth_mode === "github" || !canManage());
  byId("save-document").classList.add("hidden");
  byId("move-document").classList.add("hidden");
  await Promise.all([loadDocuments(), loadValidation(), loadScopes(), loadCollections()]);
  renderToolBenchOptions();
}

async function loadDocuments() {
  const [documents, stats, folders] = await Promise.all([api("/api/documents"), api("/api/stats"), api("/api/folders")]);
  state.documents = documents; state.folders = folders; byId("git-sha").textContent = `Git ${stats.git_sha}`; byId("document-count").textContent = `${documents.length.toLocaleString()} documents`; renderBrowser();
}

async function loadCollections() {
  state.collections = await api("/api/collections");
  if (!state.selectedCollection && state.collections.length) state.selectedCollection = state.collections[0].id;
  if (state.selectedCollection && !state.collections.some((collection) => collection.id === state.selectedCollection)) state.selectedCollection = state.collections[0]?.id || "";
  if (state.selectedCollection) state.collectionDocuments = await api(`/api/collections/${encodeURIComponent(state.selectedCollection)}/documents`);
  else state.collectionDocuments = [];
  renderCollections();
}

function renderCollections() {
  const selected = state.collections.find((collection) => collection.id === state.selectedCollection);
  byId("collection-list").innerHTML = state.collections.map((collection) => `<button class="list-row ${collection.id === state.selectedCollection ? "active" : ""}" data-collection-id="${escapeHtml(collection.id)}"><i data-lucide="database"></i><span><strong>${escapeHtml(collection.name)}</strong><small>${escapeHtml(collection.id)}</small></span></button>`).join("") || `<div class="empty">No collections</div>`;
  byId("collection-list").querySelectorAll("[data-collection-id]").forEach((row) => row.addEventListener("click", async () => { state.selectedCollection = row.dataset.collectionId; await loadCollections(); }));
  byId("collection-title").textContent = selected ? selected.name : "No collection selected";
  byId("collection-description").textContent = selected?.description || (selected ? selected.id : "");
  byId("upload-collection-files").disabled = !selected;
  byId("collection-documents").innerHTML = state.collectionDocuments.map((doc) => `<div class="file-row"><span class="file-name"><i data-lucide="file-text"></i><span><strong>${escapeHtml(doc.source_title)}</strong><small>${escapeHtml(doc.source_path)}</small></span></span><span class="file-type">${escapeHtml(doc.mime_type || "file")}</span><span><span class="status-pill ${doc.index_status === "indexed" ? "valid" : "invalid"}"><i data-lucide="${doc.index_status === "indexed" ? "circle-check" : "circle-alert"}"></i>${escapeHtml(doc.index_status)}</span></span><span class="row-action"></span></div>`).join("") || `<div class="table-empty"><i data-lucide="file-search"></i><strong>No source files</strong></div>`;
  refreshIcons();
}

function renderToolBenchOptions() {
  const tool = byId("bench-tool");
  const current = tool.value || "list_context_documents";
  tool.innerHTML = mcpTools.map(([value, label]) => `<option value="${value}" ${value === current ? "selected" : ""}>${label}</option>`).join("");
  renderBenchFields();
}

function renderBenchFields() {
  const tool = byId("bench-tool").value;
  const fields = benchFieldsByTool[tool] || [];
  byId("bench-fields").innerHTML = fields.map(benchFieldMarkup).join("") || `<div class="empty compact">No inputs required</div>`;
  refreshIcons();
}

function benchFieldMarkup(field) {
  const id = `bench-${field.key.replaceAll("_", "-")}`;
  if (field.type === "scope") return `<div class="field"><label for="${id}">${field.label}</label><select id="${id}" class="select" data-bench-key="${field.key}">${scopeOptions("", true)}</select></div>`;
  if (field.type === "context-type") return `<div class="field"><label for="${id}">${field.label}</label><select id="${id}" class="select" data-bench-key="${field.key}">${field.optional ? `<option value="">Any type</option>` : ""}${typeOptions.map(([value, label]) => `<option value="${value}">${label}</option>`).join("")}</select></div>`;
  if (field.type === "bench-collection") {
    const collections = [...state.benchCollections].sort();
    return `<div class="field"><label for="${id}">${field.label}</label><select id="${id}" class="select" data-bench-key="${field.key}" ${collections.length ? "" : "disabled"}>${collections.map((value) => `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`).join("") || `<option value="">Run a scoped context tool first</option>`}</select></div>`;
  }
  if (field.type === "bench-source") {
    const sources = [...state.benchSources.entries()].sort(([left], [right]) => left.localeCompare(right));
    return `<div class="field"><label for="${id}">${field.label}</label><select id="${id}" class="select" data-bench-key="${field.key}" ${sources.length ? "" : "disabled"}>${sources.map(([value, label]) => `<option value="${escapeHtml(value)}">${escapeHtml(label)}</option>`).join("") || `<option value="">Run search_collection first</option>`}</select></div>`;
  }
  return `<div class="field"><label for="${id}">${field.label}</label><input id="${id}" class="input" data-bench-key="${field.key}" type="${field.type || "text"}" value="${escapeHtml(field.value || "")}" placeholder="${escapeHtml(field.placeholder || "")}" /></div>`;
}

byId("bench-tool").addEventListener("change", renderBenchFields);

function collectBenchPayload() {
  const payload = {};
  byId("bench-fields").querySelectorAll("[data-bench-key]").forEach((field) => {
    if (field.disabled) return;
    const key = field.dataset.benchKey;
    const value = field.value.trim();
    if (!value) return;
    payload[key] = field.type === "number" ? Number(value) : value;
  });
  return payload;
}

function renderBrowser() {
  const query = byId("document-search").value.toLowerCase();
  const folderCounts = new Map((state.folders.length ? state.folders : [{path: ""}]).map((folder) => [folder.path, 0]));
  folderCounts.set("", state.documents.length);
  state.documents.forEach((doc) => {
    const parts = doc.folder ? doc.folder.split("/") : [];
    parts.forEach((_part, index) => {
      const folder = parts.slice(0, index + 1).join("/");
      folderCounts.set(folder, (folderCounts.get(folder) || 0) + 1);
    });
  });
  const folders = [...folderCounts.entries()].sort(([left], [right]) => left.localeCompare(right));
  byId("folder-list").innerHTML = folders.map(([folder, count]) => {
    const depth = folder ? folder.split("/").length - 1 : 0;
    const name = folder ? folder.split("/").at(-1) : "All documents";
    return `<button class="folder-row ${state.folder === folder ? "active" : ""}" data-folder="${escapeHtml(folder)}" draggable="${canEdit() && folder ? "true" : "false"}" style="--depth:${depth}"><i data-lucide="${folder ? "folder" : "files"}"></i><span>${escapeHtml(name)}</span><small>${count.toLocaleString()}</small></button>`;
  }).join("");
  byId("folder-list").querySelectorAll("[data-folder]").forEach((button) => {
    button.addEventListener("click", () => { state.folder = button.dataset.folder; state.folderDeleteArmed = false; state.page = 1; renderBrowser(); });
    button.addEventListener("dragstart", (event) => {
      if (!canEdit() || !button.dataset.folder) return;
      state.draggedFolderPath = button.dataset.folder;
      button.classList.add("dragging");
      event.dataTransfer.effectAllowed = "move";
      event.dataTransfer.setData("text/plain", button.dataset.folder);
    });
    button.addEventListener("dragover", (event) => {
      if (!canEdit() || (!state.draggedDocumentPath && !state.draggedFolderPath)) return;
      if (state.draggedFolderPath && folderMoveWouldCycle(state.draggedFolderPath, button.dataset.folder)) return;
      event.preventDefault();
      event.dataTransfer.dropEffect = "move";
      byId("folder-list").querySelectorAll(".folder-row").forEach((row) => row.classList.remove("drop-inside"));
      button.classList.add("drop-inside");
    });
    button.addEventListener("drop", async (event) => {
      event.preventDefault();
      const targetFolder = button.dataset.folder;
      try {
        if (state.draggedDocumentPath) {
          const moved = await moveDocumentToFolder(state.draggedDocumentPath, targetFolder);
          state.folder = moved.folder;
          toast("Document moved");
        } else if (state.draggedFolderPath && !folderMoveWouldCycle(state.draggedFolderPath, targetFolder)) {
          const moved = await api("/api/folders/move", {method:"POST", body:JSON.stringify({path:state.draggedFolderPath, target_parent:targetFolder})});
          state.folder = moved.path;
          await Promise.all([loadDocuments(), loadSchemas()]);
          toast("Folder moved");
        }
      } catch (error) { toast(error.message, true); }
      clearDocumentDragState();
    });
    button.addEventListener("dragend", clearDocumentDragState);
  });

  const filtered = state.documents.filter((doc) => {
    const inFolder = !state.folder || doc.folder === state.folder || doc.folder.startsWith(`${state.folder}/`);
    const matchesQuery = `${doc.path} ${doc.frontmatter.title || ""} ${doc.frontmatter.type || ""}`.toLowerCase().includes(query);
    return inFolder && matchesQuery;
  });
  const pages = Math.max(1, Math.ceil(filtered.length / state.pageSize));
  state.page = Math.min(state.page, pages);
  const start = (state.page - 1) * state.pageSize;
  const visible = filtered.slice(start, start + state.pageSize);
  byId("document-list").innerHTML = visible.map((doc) => `<button class="file-row" data-path="${escapeHtml(doc.path)}" draggable="${canEdit() ? "true" : "false"}"><span class="file-name"><i data-lucide="${doc.format === "json" ? "braces" : "file-text"}"></i><span><strong>${escapeHtml(doc.frontmatter.title || doc.name)}</strong><small>${escapeHtml(doc.path)}</small></span></span><span class="file-type">${escapeHtml(doc.format === "json" ? "JSON" : doc.frontmatter.type || "Context Document")}</span><span><span class="status-pill ${doc.validation.valid ? "valid" : "invalid"}"><i data-lucide="${doc.validation.valid ? "circle-check" : "circle-alert"}"></i>${doc.validation.valid ? (doc.format === "json" ? "Valid JSON" : "Valid OKF") : "Invalid"}</span></span><span class="row-action"><i data-lucide="chevron-right"></i></span></button>`).join("") || `<div class="table-empty"><i data-lucide="file-search"></i><strong>No documents found</strong></div>`;
  byId("document-list").querySelectorAll("[data-path]").forEach((button) => {
    button.addEventListener("click", () => openDocument(button.dataset.path));
    button.addEventListener("dragstart", (event) => {
      if (!canEdit()) return;
      state.draggedDocumentPath = button.dataset.path;
      button.classList.add("dragging");
      event.dataTransfer.effectAllowed = "move";
      event.dataTransfer.setData("text/plain", button.dataset.path);
    });
    button.addEventListener("dragend", clearDocumentDragState);
  });
  byId("result-count").textContent = `${filtered.length.toLocaleString()} ${filtered.length === 1 ? "document" : "documents"}`;
  byId("page-status").textContent = `Page ${state.page} of ${pages}`;
  byId("previous-page").disabled = state.page === 1;
  byId("next-page").disabled = state.page === pages;
  byId("browser-summary").textContent = state.folder ? state.folder : "Browse context files by folder.";
  updateFolderDeleteButton();
  refreshIcons();
}

function updateFolderDeleteButton() {
  const button = byId("delete-folder");
  const count = state.folder ? documentsInFolder(state.folder) : 0;
  button.classList.toggle("hidden", !state.folder || !canEdit());
  button.disabled = !state.folder || count > 0;
  button.title = !state.folder ? "Select a folder to delete" : count > 0 ? "Folder must be empty before it can be deleted" : `Delete ${state.folder}`;
  button.innerHTML = `<i data-lucide="trash-2"></i>${state.folderDeleteArmed ? "Confirm delete" : "Delete folder"}`;
}

async function openDocument(path) {
  if (state.dirty && state.current?.path !== path && !window.confirm("Discard unsaved changes?")) return;
  state.current = await api(`/api/documents/${path}`);
  byId("library").classList.remove("open");
  byId("document-browser").classList.add("hidden"); byId("document-editor").classList.remove("hidden");
  byId("save-document").classList.toggle("hidden", !canEdit());
  byId("move-document").classList.toggle("hidden", !canEdit());
  byId("toggle-inspector").classList.toggle("hidden", state.current.format === "json");
  byId("document-history").classList.remove("hidden"); byId("editor-mode-bar").classList.remove("hidden");
  setInspectorOpen(false);
  byId("current-location").textContent = state.current.frontmatter.title || state.current.name;
  byId("document-title").value = state.current.frontmatter.title || state.current.name;
  byId("document-title").readOnly = !canEdit() || state.current.format === "json";
  byId("document-path").textContent = state.current.path;
  byId("document-body").value = state.current.body; byId("document-body").readOnly = !canEdit();
  byId("frontmatter-editor").value = state.current.format === "markdown" ? yaml.dump(state.current.frontmatter, { lineWidth: -1, noRefs: true }) : "";
  byId("frontmatter-editor").readOnly = !canEdit();
  byId("meta-description").value = state.current.frontmatter.description || "";
  byId("meta-tags").value = (state.current.frontmatter.tags || []).join(", ");
  renderMetadataFields("document", state.current.frontmatter, state.current.inherited_frontmatter, !canEdit());
  ["meta-description", "meta-tags"].forEach((id) => byId(id).readOnly = !canEdit());
  renderGovernance(state.current.effective_frontmatter);
  state.documentDeleteArmed = false;
  byId("delete-document").innerHTML = `<i data-lucide="trash-2"></i>Delete document`;
  byId("delete-document").classList.toggle("hidden", !canEdit());
  setEditorMode("preview");
  state.dirty = false;
  byId("save-state").textContent = "";
  renderDocumentValidation(state.current.validation); showView("documents");
}

function renderGovernance(metadata) {
  const keys = ["type", "scope_id", "durability", "criticality", "status", "provenance", "valid_until"];
  byId("resolved-metadata").innerHTML = keys.filter((key) => metadata[key] !== undefined).map((key) => {
    const value = Array.isArray(metadata[key]) ? metadata[key].join(", ") : String(metadata[key]);
    return `<div><dt>${escapeHtml(key.replaceAll("_", " "))}</dt><dd>${escapeHtml(value)}</dd></div>`;
  }).join("");
}

function renderDocumentValidation(validation) {
  const status = byId("document-status"); const kind = state.current?.format === "json" ? "JSON" : "OKF"; const label = validation.valid ? `${kind} valid` : `${kind} issue`;
  status.className = `badge certification-badge ${validation.valid ? "valid" : "invalid"}`;
  status.title = validation.valid ? `${kind} validation passed` : `${kind} validation needs attention`;
  status.innerHTML = `<i data-lucide="${validation.valid ? "shield-check" : "circle-alert"}"></i><span>${label}</span>`;
  const errors = byId("validation-errors"); errors.innerHTML = validation.errors.map((error) => `<div><i data-lucide="circle-alert"></i>${escapeHtml(error)}</div>`).join(""); errors.classList.toggle("hidden", validation.valid); refreshIcons();
}

byId("save-document").addEventListener("click", async () => {
  if (!state.current) return;
  try {
    const frontmatter = state.current.format === "json" ? {} : yaml.load(byId("frontmatter-editor").value) || {};
    if (state.current.format === "markdown") { frontmatter.title = byId("document-title").value; frontmatter.description = byId("meta-description").value.trim(); frontmatter.tags = byId("meta-tags").value.split(",").map((tag) => tag.trim()).filter(Boolean); collectMetadataFields("document", frontmatter); }
    state.current = await api(`/api/documents/${state.current.path}`, { method: "PUT", body: JSON.stringify({ frontmatter, body: byId("document-body").value }) });
    state.dirty = false; byId("save-state").textContent = "Saved"; await Promise.all([loadDocuments(), loadValidation()]); openDocument(state.current.path); toast("Document saved");
  } catch (error) { toast(error.message, true); }
});

byId("delete-document").addEventListener("click", async () => {
  if (!state.current || !canEdit()) return;
  if (!state.documentDeleteArmed) {
    state.documentDeleteArmed = true;
    byId("delete-document").innerHTML = `<i data-lucide="trash-2"></i>Confirm delete`;
    refreshIcons();
    return;
  }
  try {
    const path = state.current.path;
    await api(`/api/documents/${path}`, { method: "DELETE" });
    state.current = null;
    state.dirty = false;
    setInspectorOpen(false);
    byId("document-editor").classList.add("hidden");
    byId("document-browser").classList.remove("hidden");
    byId("document-history").classList.add("hidden");
    byId("editor-mode-bar").classList.add("hidden");
    byId("toggle-inspector").classList.add("hidden");
    byId("save-document").classList.add("hidden");
    byId("move-document").classList.add("hidden");
    byId("save-state").textContent = "";
    byId("current-location").textContent = "Documents";
    await Promise.all([loadDocuments(), loadValidation()]);
    toast("Document deleted");
  } catch (error) {
    state.documentDeleteArmed = false;
    byId("delete-document").innerHTML = `<i data-lucide="trash-2"></i>Delete document`;
    refreshIcons();
    toast(error.message, true);
  }
});

document.querySelectorAll(".rail-button[data-view]").forEach((button) => button.addEventListener("click", async () => {
  showView(button.dataset.view);
  byId("library").classList.remove("open");
  if (button.dataset.view === "documents") showDocumentBrowser();
  if (button.dataset.view === "collections") await loadCollections();
  if (button.dataset.view === "test-bench") renderToolBenchOptions();
  if (button.dataset.view === "validation") await loadValidation();
  if (button.dataset.view === "history") { state.historyMode = "repository"; await loadHistory(); }
  if (button.dataset.view === "scopes") await loadScopes();
  if (button.dataset.view === "schemas") await loadSchemas();
  if (button.dataset.view === "users") await loadUsers();
}));

function showView(name) {
  document.querySelectorAll(".view").forEach((view) => view.classList.remove("active")); byId(`view-${name}`).classList.add("active");
  document.querySelectorAll(".rail-button").forEach((button) => button.classList.toggle("active", button.dataset.view === name));
  if (name !== "documents") {
    byId("editor-mode-bar").classList.add("hidden");
    byId("document-history").classList.add("hidden");
    byId("toggle-inspector").classList.add("hidden");
    byId("save-document").classList.add("hidden");
    byId("move-document").classList.add("hidden");
    byId("save-state").textContent = "";
  }
  byId("current-location").textContent = name === "documents" && state.current ? state.current.frontmatter.title : viewLabels[name] || name;
}

function showDocumentBrowser() {
  if (state.dirty && !window.confirm("Discard unsaved changes?")) return;
  state.dirty = false;
  byId("document-editor").classList.add("hidden");
  byId("document-browser").classList.remove("hidden");
  byId("toggle-inspector").classList.add("hidden");
  byId("document-history").classList.add("hidden"); byId("editor-mode-bar").classList.add("hidden");
  byId("save-document").classList.add("hidden");
  byId("move-document").classList.add("hidden");
  byId("save-state").textContent = "";
  byId("current-location").textContent = "Documents";
  renderBrowser();
}

async function loadValidation() {
  const report = await api("/api/validation"); byId("validation-dot").classList.toggle("hidden", report.invalid === 0);
  byId("validation-summary").innerHTML = `<div><strong>${report.total}</strong><span>Documents</span></div><div><strong>${report.total - report.invalid}</strong><span>Valid</span></div><div class="${report.invalid ? "danger" : ""}"><strong>${report.invalid}</strong><span>Invalid</span></div>`;
  byId("validation-list").innerHTML = report.invalid ? report.documents.map((doc) => `<button class="list-row" data-invalid-path="${escapeHtml(doc.path)}"><i data-lucide="circle-alert"></i><span><strong>${escapeHtml(doc.path)}</strong><small>${escapeHtml(doc.validation.errors.join("; "))}</small></span><i data-lucide="chevron-right"></i></button>`).join("") : `<div class="empty"><div><i class="icon" data-lucide="shield-check"></i><div>All documents are valid OKF</div></div></div>`;
  byId("validation-list").querySelectorAll("[data-invalid-path]").forEach((row) => row.addEventListener("click", () => openDocument(row.dataset.invalidPath))); refreshIcons();
}
byId("refresh-validation").addEventListener("click", loadValidation);

async function loadHistory() {
  const documentMode = state.historyMode === "document" && state.current;
  const history = await api(`/api/history${documentMode ? `?path=${encodeURIComponent(state.current.path)}` : ""}`);
  state.revisions = history; state.selectedRevision = null;
  byId("history-context").textContent = documentMode ? state.current.path : "Repository and structural changes";
  byId("history-list").innerHTML = history.map((item, index) => `<button class="list-row history-row" data-revision-index="${index}"><span class="commit">${item.short_hash}</span><span><strong>${escapeHtml(item.subject)}</strong><small>${escapeHtml(item.author)} · ${new Date(item.timestamp).toLocaleString()}</small></span></button>`).join("") || `<div class="empty">No revisions</div>`;
  byId("history-list").querySelectorAll("[data-revision-index]").forEach((row) => row.addEventListener("click", () => showRevision(Number(row.dataset.revisionIndex), !!documentMode)));
  byId("revision-empty").classList.toggle("hidden", history.length > 0); byId("revision-detail").classList.add("hidden");
  if (history.length) await showRevision(0, !!documentMode);
}

async function showRevision(index, documentMode) {
  const revision = state.revisions[index];
  if (!revision) return;
  state.selectedRevision = {...revision, index, documentMode};
  byId("history-list").querySelectorAll("[data-revision-index]").forEach((row) => row.classList.toggle("active", Number(row.dataset.revisionIndex) === index));
  byId("revision-empty").classList.add("hidden"); byId("revision-detail").classList.remove("hidden");
  byId("revision-hash").textContent = revision.short_hash; byId("revision-title").textContent = revision.subject; byId("revision-meta").textContent = `${revision.author} · ${new Date(revision.timestamp).toLocaleString()}`;
  byId("diff-view").innerHTML = `<div class="diff-loading">Loading changes…</div>`;
  byId("diff-label").textContent = documentMode ? "Changes from the previous document revision" : "Changes in this repository revision";
  const restore = byId("restore-revision"); const currentRevision = index === 0;
  restore.classList.toggle("hidden", !documentMode || !canEdit()); restore.disabled = currentRevision;
  restore.innerHTML = currentRevision ? `<i data-lucide="circle-check"></i>Current version` : `<i data-lucide="rotate-ccw"></i>Restore this version`;
  refreshIcons();
  try {
    const query = documentMode ? `?path=${encodeURIComponent(state.current.path)}` : "";
    const data = await api(`/api/history/${revision.hash}/diff${query}`);
    renderRevisionDiff(data.diff);
  } catch (error) { byId("diff-view").innerHTML = `<div class="diff-loading error">${escapeHtml(error.message)}</div>`; }
}

function renderRevisionDiff(diff) {
  const rows = [];
  for (const line of (diff || "").split("\n")) {
    if (line.startsWith("diff --git ")) { rows.push(`<div class="diff-file">${escapeHtml(line.split(" b/").at(-1))}</div>`); continue; }
    if (line.startsWith("index ") || line.startsWith("--- ") || line.startsWith("+++ ") || !line) continue;
    if (line.startsWith("@@")) { rows.push(`<div class="diff-line hunk"><span></span><code>${escapeHtml(line)}</code></div>`); continue; }
    const kind = line.startsWith("+") ? "added" : line.startsWith("-") ? "removed" : "context";
    const marker = kind === "added" ? "+" : kind === "removed" ? "−" : "";
    rows.push(`<div class="diff-line ${kind}"><span>${marker}</span><code>${escapeHtml(line.slice(kind === "context" && !line.startsWith(" ") ? 0 : 1))}</code></div>`);
  }
  byId("diff-view").innerHTML = rows.join("") || `<div class="diff-loading">No content changes in this revision</div>`;
}

async function loadSchemas() {
  state.folders = await api("/api/folders");
  byId("schema-list").innerHTML = state.folders.map((folder) => {
    const count = documentsInFolder(folder.path);
    return `<button class="list-row" data-schema-path="${escapeHtml(folder.path)}"><i data-lucide="folder-cog"></i><span><strong>${escapeHtml(folder.path || "Root")}</strong><small>${count.toLocaleString()} ${count === 1 ? "document" : "documents"}</small></span></button>`;
  }).join("");
  byId("schema-list").querySelectorAll("[data-schema-path]").forEach((row) => row.addEventListener("click", () => selectSchema(row.dataset.schemaPath)));
  refreshIcons();
  if (state.folders.length) selectSchema(state.folders.some((folder) => folder.path === state.schemaPath) ? state.schemaPath : state.folders[0].path);
}

function documentsInFolder(folder) {
  return state.documents.filter((doc) => !folder || doc.folder === folder || doc.folder.startsWith(`${folder}/`)).length;
}

function selectSchema(path) {
  const folder = state.folders.find((item) => item.path === path);
  if (!folder) return;
  state.schemaPath = folder.path;
  byId("schema-label").textContent = folder.path || "Root";
  byId("schema-body").value = yaml.dump(folder.schema, { lineWidth: -1, noRefs: true });
  renderMetadataFields("schema", folder.schema, folder.inherited_schema);
  byId("schema-list").querySelectorAll("[data-schema-path]").forEach((row) => row.classList.toggle("active", row.dataset.schemaPath === path));
}

byId("schema-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    const schema = yaml.load(byId("schema-body").value) || {};
    collectMetadataFields("schema", schema);
    await api("/api/schemas", { method: "PUT", body: JSON.stringify({ path: state.schemaPath, schema }) });
    await Promise.all([loadSchemas(), loadDocuments(), loadValidation()]); toast("Folder metadata saved");
  } catch (error) { toast(error.message, true); }
});

async function loadScopes() {
  state.scopes = await api("/api/scopes");
  if (!byId("view-scopes").classList.contains("active")) return;
  const ordered = orderedScopes();
  byId("scope-list").innerHTML = ordered.map(({scope, depth}) => `<div class="scope-row" style="--depth:${depth}" data-scope-id="${escapeHtml(scope.id)}" data-parent-id="${escapeHtml(scope.parent_id || "")}" ${canManage() ? "draggable=\"true\"" : ""}><span class="scope-branch"></span><span class="drag-handle" title="Reorder or change nesting"><i data-lucide="grip-vertical"></i></span><span class="scope-icon"><i data-lucide="${scope.level === "company" ? "building-2" : scope.level === "brand" ? "badge" : "box"}"></i></span><span class="scope-name"><strong>${escapeHtml(scope.name)}</strong><small>${escapeHtml(scope.id)}${scope.parent_id ? ` · inherits from ${escapeHtml(scope.parent_id)}` : ""}</small></span><span class="level-pill">${escapeHtml(scope.level)}</span>${canManage() ? `<button class="icon-button" data-edit-scope="${escapeHtml(scope.id)}" title="Edit scope"><i data-lucide="pencil"></i></button>` : ""}</div>`).join("") || `<div class="empty">No scopes</div>`;
  byId("scope-list").querySelectorAll("[data-edit-scope]").forEach((button) => button.addEventListener("click", () => openDrawer("scope-edit", state.scopes.find((scope) => scope.id === button.dataset.editScope))));
  bindScopeDragging();
  refreshIcons();
}

function orderedScopes() {
  const children = new Map();
  state.scopes.forEach((scope) => { const parent = scope.parent_id || ""; children.set(parent, [...(children.get(parent) || []), scope]); });
  const ordered = [];
  const visit = (parent, depth) => (children.get(parent) || []).sort((a, b) => (a.order ?? 0) - (b.order ?? 0) || a.name.localeCompare(b.name)).forEach((scope) => { ordered.push({scope, depth}); visit(scope.id, depth + 1); });
  visit("", 0);
  return ordered;
}

function bindScopeDragging() {
  if (!canManage()) return;
  const rows = byId("scope-list").querySelectorAll("[data-scope-id]");
  rows.forEach((row) => {
    row.addEventListener("dragstart", (event) => { state.draggedScopeId = row.dataset.scopeId; row.classList.add("dragging"); event.dataTransfer.effectAllowed = "move"; event.dataTransfer.setData("text/plain", row.dataset.scopeId); });
    row.addEventListener("dragover", (event) => {
      const source = byId("scope-list").querySelector(`[data-scope-id="${state.draggedScopeId}"]`);
      if (!source || source === row) return;
      const bounds = row.getBoundingClientRect(); const ratio = (event.clientY - bounds.top) / bounds.height;
      const target = state.scopes.find((scope) => scope.id === row.dataset.scopeId);
      const newParentId = ratio > .25 && ratio < .75 ? target.id : target.parent_id;
      if (scopeMoveWouldCycle(state.draggedScopeId, newParentId)) return;
      event.preventDefault();
      event.dataTransfer.dropEffect = "move";
      rows.forEach((item) => item.classList.remove("drop-before", "drop-after", "drop-inside"));
      row.classList.add(ratio <= .25 ? "drop-before" : ratio >= .75 ? "drop-after" : "drop-inside");
    });
    row.addEventListener("drop", async (event) => {
      event.preventDefault();
      const sourceId = state.draggedScopeId; const targetId = row.dataset.scopeId;
      const source = state.scopes.find((scope) => scope.id === sourceId); const target = state.scopes.find((scope) => scope.id === targetId);
      if (!source || !target) return;
      const nestInside = row.classList.contains("drop-inside"); const after = row.classList.contains("drop-after");
      const parentId = nestInside ? target.id : target.parent_id;
      if (scopeMoveWouldCycle(sourceId, parentId)) return;
      const siblings = state.scopes.filter((scope) => scope.parent_id === parentId && scope.id !== sourceId).sort((a, b) => (a.order ?? 0) - (b.order ?? 0) || a.name.localeCompare(b.name));
      const targetIndex = nestInside ? siblings.length : siblings.findIndex((scope) => scope.id === targetId) + (after ? 1 : 0);
      try { await api("/api/scopes/move", {method:"POST", body:JSON.stringify({scope_id:sourceId, parent_id:parentId || null, index:Math.max(0, targetIndex)})}); await loadScopes(); toast(nestInside ? "Scope nesting saved" : "Scope order saved"); } catch (error) { toast(error.message, true); }
    });
    row.addEventListener("dragend", () => { state.draggedScopeId = null; rows.forEach((item) => item.classList.remove("dragging", "drop-before", "drop-after", "drop-inside")); });
  });
}

function scopeMoveWouldCycle(scopeId, parentId) {
  let current = parentId;
  while (current) {
    if (current === scopeId) return true;
    current = state.scopes.find((scope) => scope.id === current)?.parent_id || null;
  }
  return false;
}

function scopeOptions(selected = "", allowGlobal = false) {
  const options = allowGlobal ? `<option value="">Global / unscoped</option>` : `<option value="">No parent</option>`;
  return options + orderedScopes().map(({scope, depth}) => `<option value="${escapeHtml(scope.id)}" ${scope.id === selected ? "selected" : ""}>${"— ".repeat(depth)}${escapeHtml(scope.name)} (${escapeHtml(scope.level)})</option>`).join("");
}

function folderOptions(selected = "") {
  const folders = state.folders.length ? state.folders : [{path: ""}];
  return folders
    .slice()
    .sort((left, right) => left.path.localeCompare(right.path))
    .map((folder) => {
      const depth = folder.path ? folder.path.split("/").length - 1 : 0;
      const label = folder.path ? `${"— ".repeat(depth)}${folder.path}` : "Root";
      return `<option value="${escapeHtml(folder.path)}" ${folder.path === selected ? "selected" : ""}>${escapeHtml(label)}</option>`;
    })
    .join("");
}

function folderMoveWouldCycle(source, target) {
  return Boolean(source && (source === target || target.startsWith(`${source}/`)));
}

function clearDocumentDragState() {
  state.draggedDocumentPath = "";
  state.draggedFolderPath = "";
  document.querySelectorAll(".folder-row, .file-row").forEach((row) => row.classList.remove("dragging", "drop-inside"));
}

async function moveDocumentToFolder(path, targetFolder) {
  const moved = await api("/api/documents/move", {method:"POST", body:JSON.stringify({path, target_folder:targetFolder})});
  await Promise.all([loadDocuments(), loadValidation()]);
  return moved;
}

async function loadUsers() {
  const users = await api("/api/users");
  byId("user-list").innerHTML = users.map((user) => `<div class="list-row"><div class="avatar">${user.username.slice(0,1).toUpperCase()}</div><span><strong>${escapeHtml(user.username)}</strong><small>Local account</small></span><span class="role-pill">${escapeHtml(user.role)}</span><button class="icon-button" data-edit-user="${escapeHtml(user.username)}" title="Edit user"><i data-lucide="pencil"></i></button></div>`).join("");
  byId("user-list").querySelectorAll("[data-edit-user]").forEach((button) => button.addEventListener("click", () => openDrawer("user-edit", users.find((user) => user.username === button.dataset.editUser))));
  refreshIcons();
}

function openDrawer(mode, data = null) {
  state.drawerMode = mode; state.drawerData = data; state.deleteArmed = false;
  const editing = mode.endsWith("-edit");
  const kind = mode.split("-")[0];
  const restoring = kind === "revision";
  const titles = {document: "New document", folder: "New folder", collection: "New collection", user: editing ? "Edit user" : "Add user", scope: editing ? "Edit scope" : "Add scope", revision: "Restore document", move: "Move document"};
  byId("drawer-eyebrow").textContent = kind === "move" ? "Organize" : restoring ? "History" : editing ? "Edit" : "Create"; byId("drawer-title").textContent = titles[kind]; byId("save-drawer").textContent = kind === "move" ? "Move" : restoring ? "Restore version" : editing ? "Save changes" : "Create";
  byId("delete-drawer-item").classList.toggle("hidden", !editing || !["user", "scope"].includes(kind));
  if (kind === "document") byId("drawer-fields").innerHTML = `<div class="field"><label for="drawer-format">Format</label><select id="drawer-format" class="select"><option value="markdown">Markdown / OKF</option><option value="json">JSON</option></select></div><div class="field"><label for="drawer-folder">Folder</label><select id="drawer-folder" class="select">${folderOptions(state.folder)}</select></div><div class="field"><label for="drawer-filename">Filename</label><input id="drawer-filename" class="input" placeholder="document-name" pattern="[^/\\\\]+" required /></div><div class="field"><label for="drawer-document-title">Title</label><input id="drawer-document-title" class="input" required /></div><div class="field markdown-option"><label for="drawer-type">Type</label><select id="drawer-type" class="select" required>${typeOptions.map(([value,label]) => `<option value="${value}" ${value === "reference" ? "selected" : ""}>${label}</option>`).join("")}</select></div><div class="field markdown-option"><label for="drawer-scope">Scope</label><select id="drawer-scope" class="select">${scopeOptions("", true)}</select></div>`;
  if (kind === "folder") byId("drawer-fields").innerHTML = `<div class="field"><label for="drawer-path">Folder path</label><input id="drawer-path" class="input" placeholder="products/platform" required /></div>`;
  if (kind === "collection") byId("drawer-fields").innerHTML = `<div class="field"><label for="drawer-collection-id">Collection ID</label><input id="drawer-collection-id" class="input" placeholder="sales-calls" required /></div><div class="field"><label for="drawer-collection-name">Name</label><input id="drawer-collection-name" class="input" placeholder="Sales calls" required /></div><div class="field"><label for="drawer-collection-description">Description</label><textarea id="drawer-collection-description" class="textarea" rows="3"></textarea></div>`;
  if (kind === "user") byId("drawer-fields").innerHTML = `<div class="field"><label for="drawer-username">Username</label><input id="drawer-username" class="input" value="${escapeHtml(data?.username || "")}" ${editing ? "readonly" : "required"} /></div><div class="field"><label for="drawer-password">${editing ? "New password" : "Password"}</label><input id="drawer-password" class="input" type="password" ${editing ? "" : "required"} /></div><div class="field"><label for="drawer-role">Role</label><select id="drawer-role" class="select"><option ${data?.role === "viewer" ? "selected" : ""}>viewer</option><option ${data?.role === "editor" ? "selected" : ""}>editor</option><option ${data?.role === "admin" ? "selected" : ""}>admin</option></select></div>`;
  if (kind === "scope") byId("drawer-fields").innerHTML = `<div class="field"><label for="drawer-scope-id">Scope ID</label><input id="drawer-scope-id" class="input" value="${escapeHtml(data?.id || "")}" ${editing ? "readonly" : "required"} placeholder="product-a" /></div><div class="field"><label for="drawer-scope-name">Name</label><input id="drawer-scope-name" class="input" value="${escapeHtml(data?.name || "")}" required /></div><div class="field"><label for="drawer-scope-level">Level</label><select id="drawer-scope-level" class="select">${["company","brand","product","market","campaign","audience","channel","custom"].map((level) => `<option ${data?.level === level ? "selected" : ""}>${level}</option>`).join("")}</select></div><div class="field"><label for="drawer-parent">Parent</label><select id="drawer-parent" class="select">${scopeOptions(data?.parent_id || "")}</select></div>`;
  if (kind === "revision") byId("drawer-fields").innerHTML = `<div class="restore-summary"><span class="commit">${escapeHtml(data.short_hash)}</span><strong>${escapeHtml(data.subject)}</strong><small>${escapeHtml(state.current.path)}</small><p>The selected version will replace the current document and be saved as a new Git revision. Existing history will remain available.</p></div>`;
  if (kind === "move") byId("drawer-fields").innerHTML = `<div class="field"><label for="drawer-target-folder">Folder</label><select id="drawer-target-folder" class="select">${folderOptions(data?.folder || "")}</select></div>`;
  byId("drawer-scrim").classList.remove("hidden"); refreshIcons();
}

function closeDrawer() { byId("drawer-scrim").classList.add("hidden"); state.drawerMode = ""; state.drawerData = null; }

byId("new-menu").addEventListener("click", () => openDrawer("document")); byId("new-folder-documents").addEventListener("click", () => openDrawer("folder")); byId("new-folder").addEventListener("click", () => openDrawer("folder")); byId("new-collection").addEventListener("click", () => openDrawer("collection")); byId("new-user").addEventListener("click", () => openDrawer("user")); byId("new-scope").addEventListener("click", () => openDrawer("scope")); byId("move-document").addEventListener("click", () => { if (state.current) openDrawer("move", state.current); }); byId("restore-revision").addEventListener("click", () => { if (state.selectedRevision?.documentMode && state.selectedRevision.index > 0) openDrawer("revision-restore", state.selectedRevision); });
byId("close-drawer").addEventListener("click", closeDrawer); byId("cancel-drawer").addEventListener("click", closeDrawer); byId("drawer-scrim").addEventListener("click", (event) => { if (event.target === byId("drawer-scrim")) closeDrawer(); });

byId("drawer-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    const kind = state.drawerMode.split("-")[0]; const editing = state.drawerMode.endsWith("-edit");
    if (kind === "document") { const format = byId("drawer-format").value; const folder = byId("drawer-folder").value; const filename = byId("drawer-filename").value.trim().replace(/\.(md|json)$/i, ""); if (!filename || filename.includes("/") || filename.includes("\\")) throw new Error("Filename cannot include folders"); const path = `${folder ? `${folder}/` : ""}${filename}.${format === "json" ? "json" : "md"}`; const title = byId("drawer-document-title").value.trim(); const frontmatter = format === "json" ? {} : {type:byId("drawer-type").value.trim(), title}; if (format !== "json" && byId("drawer-scope").value) frontmatter.scope_id = byId("drawer-scope").value; await api(`/api/documents/${path}`, {method:"PUT", body:JSON.stringify({frontmatter, body:format === "json" ? "{}" : `# ${title}`})}); closeDrawer(); await loadDocuments(); await openDocument(path); }
    if (kind === "folder") { const folder = await api("/api/folders", {method:"POST", body:JSON.stringify({path:byId("drawer-path").value.trim()})}); state.folder = folder.path; state.page = 1; closeDrawer(); await Promise.all([loadDocuments(), loadSchemas()]); }
    if (kind === "collection") { const created = await api("/api/collections", {method:"POST", body:JSON.stringify({id:byId("drawer-collection-id").value.trim(), name:byId("drawer-collection-name").value.trim(), description:byId("drawer-collection-description").value.trim()})}); state.selectedCollection = created.id; closeDrawer(); await loadCollections(); showView("collections"); }
    if (kind === "user") { const payload = {username:byId("drawer-username").value.trim(), password:byId("drawer-password").value, role:byId("drawer-role").value}; await api(editing ? `/api/users/${state.drawerData.username}` : "/api/users", {method:editing ? "PATCH" : "POST", body:JSON.stringify(payload)}); closeDrawer(); await loadUsers(); }
    if (kind === "scope") { const payload = {id:byId("drawer-scope-id").value.trim(), name:byId("drawer-scope-name").value.trim(), level:byId("drawer-scope-level").value, parent_id:byId("drawer-parent").value || null}; await api(editing ? `/api/scopes/${state.drawerData.id}` : "/api/scopes", {method:editing ? "PATCH" : "POST", body:JSON.stringify(payload)}); closeDrawer(); await loadScopes(); }
    if (kind === "revision") { const result = await api(`/api/history/${state.drawerData.hash}/restore`, {method:"POST", body:JSON.stringify({path:state.current.path})}); state.current = result.document; closeDrawer(); await Promise.all([loadDocuments(), loadValidation()]); await loadHistory(); toast("Document restored"); return; }
    if (kind === "move") { const moved = await moveDocumentToFolder(state.current.path, byId("drawer-target-folder").value); state.current = moved; closeDrawer(); await openDocument(moved.path); toast("Document moved"); return; }
    toast(editing ? "Changes saved" : "Created");
  } catch (error) { toast(error.message, true); }
});

byId("delete-drawer-item").addEventListener("click", async () => {
  if (!state.deleteArmed) { state.deleteArmed = true; byId("delete-drawer-item").textContent = "Confirm remove"; return; }
  try { const kind = state.drawerMode.split("-")[0]; await api(kind === "user" ? `/api/users/${state.drawerData.username}` : `/api/scopes/${state.drawerData.id}`, {method:"DELETE"}); closeDrawer(); if (kind === "user") await loadUsers(); else await loadScopes(); toast("Removed"); } catch (error) { state.deleteArmed = false; byId("delete-drawer-item").textContent = "Remove"; toast(error.message, true); }
});

byId("toggle-okf-import").addEventListener("click", () => {
  byId("okf-import-panel").classList.toggle("hidden");
});

byId("okf-import-folder").setAttribute("webkitdirectory", "");
byId("choose-okf-import").addEventListener("click", () => byId("okf-import-folder").click());
byId("okf-import-folder").addEventListener("change", (event) => {
  const files = [...event.target.files];
  state.okfImportFiles = files;
  state.okfImportPayload = null;
  state.okfImportScan = null;
  state.okfImportFolderName = okfImportFolderName(files);
  byId("okf-import-folder-label").value = files.length ? `${state.okfImportFolderName} (${files.length} files)` : "No folder selected";
  byId("okf-import-report").textContent = files.length ? "Ready to scan." : "No scan yet.";
  byId("apply-okf-import").disabled = true;
});

byId("scan-okf-import").addEventListener("click", async () => {
  try {
    const payload = await okfImportPayload();
    const scan = await api("/api/imports/okf-folder/scan-upload", {method:"POST", body:JSON.stringify(payload)});
    state.okfImportScan = scan;
    state.okfImportPayload = payload;
    renderOkfImportReport(scan);
    byId("apply-okf-import").disabled = Boolean(scan.blockers?.length);
  } catch (error) {
    byId("okf-import-report").textContent = error.message;
    byId("apply-okf-import").disabled = true;
    toast(error.message, true);
  }
});

byId("apply-okf-import").addEventListener("click", async () => {
  try {
    const payload = state.okfImportPayload || await okfImportPayload();
    const result = await api("/api/imports/okf-folder/apply-upload", {method:"POST", body:JSON.stringify(payload)});
    byId("okf-import-report").textContent = JSON.stringify(result, null, 2);
    byId("apply-okf-import").disabled = true;
    state.okfImportPayload = null;
    await Promise.all([loadDocuments(), loadValidation(), loadSchemas()]);
    toast("OKF folder imported");
  } catch (error) { toast(error.message, true); }
});

function okfImportFolderName(files) {
  const firstPath = files[0]?.webkitRelativePath || files[0]?.name || "";
  return firstPath.split("/").filter(Boolean)[0] || "uploaded-folder";
}

async function okfImportPayload() {
  if (!state.okfImportFiles.length) throw new Error("Choose a folder first");
  const files = [];
  for (const file of state.okfImportFiles) {
    const relativePath = file.webkitRelativePath || file.name;
    const parts = relativePath.split("/").filter(Boolean);
    const path = parts.join("/");
    files.push({path, content_base64: await fileToBase64(file)});
  }
  return {folder_name: state.okfImportFolderName || okfImportFolderName(state.okfImportFiles), files};
}

function renderOkfImportReport(scan) {
  const report = {
    blockers: scan.blockers || [],
    warnings: scan.warnings || [],
    files: scan.files || [],
  };
  byId("okf-import-report").textContent = JSON.stringify(report, null, 2);
}

byId("upload-collection-files").addEventListener("click", () => byId("collection-files").click());
byId("collection-files").addEventListener("change", async (event) => {
  const files = [...event.target.files];
  if (!state.selectedCollection || !files.length) return;
  try {
    for (const file of files) {
      const content_base64 = await fileToBase64(file);
      await api(`/api/collections/${encodeURIComponent(state.selectedCollection)}/documents`, {method:"POST", body:JSON.stringify({filename:file.name, content_base64})});
    }
    event.target.value = "";
    await loadCollections();
    toast("Files indexed");
  } catch (error) { toast(error.message, true); }
});

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onerror = () => reject(new Error("Could not read file"));
    reader.onload = () => resolve(String(reader.result).split(",", 2)[1] || "");
    reader.readAsDataURL(file);
  });
}

byId("bench-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const tool = byId("bench-tool").value;
  const request = collectBenchPayload();
  byId("bench-request").textContent = JSON.stringify(request, null, 2);
  try {
    const response = await api(`/api/mcp-tools/${encodeURIComponent(tool)}`, {method:"POST", body:JSON.stringify(request)});
    byId("bench-response").textContent = JSON.stringify(response, null, 2);
    renderBenchResults(response);
  } catch (error) {
    byId("bench-response").textContent = error.message;
    byId("bench-results").innerHTML = "";
    toast(error.message, true);
  }
});

function renderBenchResults(response) {
  harvestBenchCollections(response.result);
  if (response.tool === "search_collection") harvestBenchSources(response.result);
  byId("bench-results").innerHTML = benchPreview(response.tool, response.result);
  renderBenchFields();
  refreshIcons();
}

function harvestBenchCollections(value) {
  const visit = (item) => {
    if (!item || typeof item !== "object") return;
    const collections = item.supporting_sources?.collections;
    if (Array.isArray(collections)) collections.forEach((collection) => state.benchCollections.add(collection));
    if (Array.isArray(item)) item.forEach(visit);
    else Object.values(item).forEach(visit);
  };
  visit(value);
}

function harvestBenchSources(results) {
  if (!Array.isArray(results)) return;
  results.forEach((item) => {
    if (!item.source_id) return;
    state.benchSources.set(item.source_id, `${item.source_title || item.source_id} (${item.source_id})`);
    if (item.collection_id) state.benchCollections.add(item.collection_id);
  });
}

function benchPreview(tool, result) {
  if (Array.isArray(result) && !result.length) return `<div class="empty">No results</div>`;
  if (tool === "list_context_documents") {
    return `<div class="result-section">${result.map((record) => `<article><strong>${escapeHtml(record.title)}</strong><small>${escapeHtml(record.path)}${record.scope_id ? ` &middot; ${escapeHtml(record.scope_id)}` : ""}</small><p>${escapeHtml(record.description || record.type)}</p>${record.supporting_sources?.collections?.length ? `<small>Collections: ${record.supporting_sources.collections.map(escapeHtml).join(", ")}</small>` : ""}</article>`).join("")}</div>`;
  }
  if (tool === "read_context_document") {
    return `<section class="bench-result"><div class="bench-result-header"><strong>${escapeHtml(result.title || result.name || result.path)}</strong><span>${escapeHtml(result.type || "document")}</span></div><pre class="text-preview">${escapeHtml((result.body || "").slice(0, 1200))}</pre></section>`;
  }
  if (tool === "search_collection") {
    return `<div class="result-section">${result.map((item) => `<article><strong>${escapeHtml(item.source_title)}</strong><small>${escapeHtml(item.collection_id)} &middot; ${escapeHtml(item.location)} &middot; ${escapeHtml(item.source_id)}</small><p>${escapeHtml(item.snippet)}</p></article>`).join("")}</div>`;
  }
  if (tool === "read_collection_source") {
    return `<section class="bench-result"><div class="bench-result-header"><strong>${escapeHtml(result.source_title || result.id)}</strong><span>${escapeHtml(result.collection_id)}</span></div><small class="source-path">${escapeHtml(result.source_path || "")}</small><pre class="text-preview">${escapeHtml((result.text || "").slice(0, 1600))}</pre></section>`;
  }
  if (Array.isArray(result)) return `<div class="result-section">${result.slice(0, 100).map((item) => `<article><strong>${escapeHtml(item.title || item.name || item.path || item.id || String(item))}</strong><small>${escapeHtml(item.path || item.id || item.type || "")}</small></article>`).join("")}</div>`;
  return `<pre class="json-output">${escapeHtml(JSON.stringify(result, null, 2))}</pre>`;
}

byId("document-search").addEventListener("input", () => { state.page = 1; renderBrowser(); });
byId("previous-page").addEventListener("click", () => { if (state.page > 1) { state.page -= 1; renderBrowser(); } });
byId("next-page").addEventListener("click", () => { state.page += 1; renderBrowser(); });
byId("delete-folder").addEventListener("click", async () => {
  if (!state.folder || documentsInFolder(state.folder) > 0 || !canEdit()) return;
  if (!state.folderDeleteArmed) {
    state.folderDeleteArmed = true;
    updateFolderDeleteButton();
    refreshIcons();
    return;
  }
  try {
    const folder = state.folder;
    await api(`/api/folders/${folder}`, { method: "DELETE" });
    state.folder = "";
    state.folderDeleteArmed = false;
    await Promise.all([loadDocuments(), loadSchemas(), loadValidation()]);
    toast("Folder deleted");
  } catch (error) {
    state.folderDeleteArmed = false;
    updateFolderDeleteButton();
    refreshIcons();
    toast(error.message, true);
  }
});
byId("back-to-documents").addEventListener("click", showDocumentBrowser);
byId("document-history").addEventListener("click", async () => { state.historyMode = "document"; showView("history"); await loadHistory(); });
byId("editor-modes").querySelectorAll("[data-editor-mode]").forEach((button) => button.addEventListener("click", () => setEditorMode(button.dataset.editorMode)));

function setEditorMode(mode) {
  state.editorMode = mode; byId("content-editor").className = `content-editor mode-${mode}`;
  byId("editor-modes").querySelectorAll("[data-editor-mode]").forEach((button) => button.classList.toggle("active", button.dataset.editorMode === mode));
  renderPreview();
}

function renderPreview() {
  if (!state.current || state.editorMode === "raw") return;
  const raw = byId("document-body").value;
  if (state.current.format === "json") {
    try { byId("document-preview").innerHTML = `<pre>${escapeHtml(JSON.stringify(JSON.parse(raw), null, 2))}</pre>`; }
    catch (error) { byId("document-preview").innerHTML = `<div class="preview-error">${escapeHtml(error.message)}</div>`; }
  } else {
    const preview = byId("document-preview");
    preview.innerHTML = DOMPurify.sanitize(marked.parse(raw));
    const title = preview.querySelector("h1");
    const metadataRows = [];
    let next = title?.nextElementSibling;
    while (next?.tagName === "P" && next.firstElementChild?.tagName === "STRONG") {
      metadataRows.push(next);
      next = next.nextElementSibling;
    }
    if (title && metadataRows.length) {
      const metadata = document.createElement("section");
      metadata.className = "preview-metadata";
      metadata.setAttribute("aria-label", "Document metadata");
      metadataRows.forEach((row) => metadata.append(row));
      title.after(metadata);
    }
  }
}
byId("mobile-library").addEventListener("click", () => byId("library").classList.toggle("open"));
const setInspectorOpen = (open) => { byId("document-editor").classList.toggle("inspector-open", open); byId("toggle-inspector").setAttribute("aria-expanded", String(open)); };
byId("toggle-inspector").addEventListener("click", () => setInspectorOpen(!byId("document-editor").classList.contains("inspector-open")));
byId("close-inspector").addEventListener("click", () => setInspectorOpen(false));
["document-title", "document-body", "meta-description", "meta-tags", "frontmatter-editor"].forEach((id) => byId(id).addEventListener("input", () => { markDocumentDirty(); if (id === "document-body") renderPreview(); }));
start();
