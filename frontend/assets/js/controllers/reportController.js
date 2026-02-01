import { apiGetEnrollmentReport } from "../services/reportService.js";
import { renderEnrollmentReportTable } from "../components/EnrollmentReportTable.js";
import { $ } from "../utils/dom.js";

export function initEnrollmentReportController() {
  loadReport();
}

async function loadReport() {
  const spinner = $("loadingSpinner");
  const table = $("reportTableContainer");

  spinner.style.display = "block";
  table.style.display = "none";

  const rows = await apiGetEnrollmentReport();
  renderEnrollmentReportTable(rows);

  spinner.style.display = "none";
  table.style.display = "block";
}