// frontend/assets/js/controllers/profilesController.js

import { $ } from "../utils/dom.js";
import { filterList, sortList } from "../utils/listTools.js";
import { exportToCSV, exportToPDF } from "../utils/exportTools.js";

import { renderProfilesTable } from "../components/ProfilesTable.js";
import { buildPrintableTableHTML } from "../utils/printTable.js";
import { apiGetAll as apiGetAllPatients } from "../services/patientService.js";
import { apiGetAll as apiGetAllInvoices } from "../services/billingService.js";
import { apiGetAll as apiGetAllDoctors } from "../services/doctorService.js";

const COLUMNS = [
  { key: "id", label: "ID" },
  { key: "patient_name", label: "Patient" },
  { key: "email", label: "Email" },
  { key: "phone", label: "Phone" },
  { key: "doctor_name", label: "Doctor" },
];

let allRows = [];

export function initProfilesController() {
  loadProfiles();

  $("searchInput")?.addEventListener("input", refresh);
  $("sortBy")?.addEventListener("change", refresh);
  $("sortDir")?.addEventListener("change", refresh);

  $("exportCsvBtn")?.addEventListener("click", () => {
    exportToCSV("clinic_report.csv", getRows(), COLUMNS);
  });

  $("exportPdfBtn")?.addEventListener("click", () => {
    const rows = getRows();
    const html = buildPrintableTableHTML("Clinic Report", rows, COLUMNS);
    exportToPDF("Clinic Report", html);
  });
}

async function loadProfiles() {
  const spinner = $("loadingSpinner");
  const container = $("profilesTableContainer");

  if (spinner) spinner.style.display = "block";
  if (container) container.style.display = "none";

  const [patients, invoices, doctors] = await Promise.all([
    apiGetAllPatients(),
    apiGetAllInvoices(),
    apiGetAllDoctors(),
  ]);

  const invByPatient = new Map();
  (invoices || []).slice().sort((a,b)=>b.id - a.id).forEach(inv => {
    if (!invByPatient.has(inv.patient_id)) invByPatient.set(inv.patient_id, inv);
  });

  const doctorMap = new Map((doctors||[]).map(d => [d.id, d.name]));

  allRows = (patients || []).map(p => ({
    id: p.id,
    name: `${p.first_name || ""} ${p.last_name || ""}`.trim(),
    email: p.email || "",
    phone: p.phone || "",
    doctor_name: (invByPatient.get(p.id) && invByPatient.get(p.id).doctor_name) || "",
  }));

  refresh();

  if (spinner) spinner.style.display = "none";
  if (container) container.style.display = "block";
}

function getRows() {
  const q = $("searchInput")?.value?.trim() ?? "";
  const sortKey = $("sortBy")?.value ?? "id";
  const sortDir = $("sortDir")?.value ?? "asc";

  const filtered = filterList(allRows, q, ["id", "patient_name", "email", "phone", "doctor_name"]);
  return sortList(filtered, sortKey, sortDir);
}

function refresh() {
  renderProfilesTable(getRows());
}
