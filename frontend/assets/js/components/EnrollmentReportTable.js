// Feature: enrollment report table component — renders enrollment/join reports. Connects: reportController and DOM utils.
import { $ } from "../utils/dom.js";

export function renderEnrollmentReportTable(rows) {
  const body = $("reportTableBody");
  const empty = $("noRows");

  body.innerHTML = "";

  if (!rows || rows.length === 0) {
    empty.classList.remove("hidden");
    return;
  }
  empty.classList.add("hidden");

  rows.forEach(r => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td class="px-3 py-2 border">${r.enrollment_id ?? ""}</td>
      <td class="px-3 py-2 border">
        ${r.student_name ?? ""} <span class="text-xs text-gray-500">(ID: ${r.student_id ?? ""})</span>
      </td>
      <td class="px-3 py-2 border">
        ${r.course_title ?? ""} <span class="text-xs text-gray-500">(ID: ${r.course_id ?? ""})</span>
      </td>
      <td class="px-3 py-2 border">${r.enrolled_on ?? ""}</td>
    `;
    body.appendChild(tr);
  });
}