// frontend/assets/js/utils/exportTools.js

function downloadBlob(filename, blob) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

function escHtml(v) {
  return String(v ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function safeCsv(v) {
  const s = String(v ?? "");
  const escaped = s.replaceAll('"', '""');
  return /[",\n]/.test(escaped) ? `"${escaped}"` : escaped;
}

// -------------------------
// Existing: CSV (table only)
// -------------------------
export function exportToCSV(filename, rows, columns) {
  const header = columns.map((c) => safeCsv(c.label)).join(",");
  const body = (rows || [])
    .map((r) => columns.map((c) => safeCsv(r?.[c.key])).join(","))
    .join("\n");

  const csv = header + "\n" + body;
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
  downloadBlob(filename, blob);
}

// -------------------------
// Existing: PDF (print HTML)
// -------------------------
export function exportToPDF(title, htmlContent) {
  const w = window.open("", "_blank");
  if (!w) return;

  w.document.open();
  w.document.write(`
    <html>
      <head>
        <title>${escHtml(title)}</title>
        <meta charset="utf-8" />
        <style>
          body { font-family: Arial, sans-serif; padding: 16px; color: #111827; }
          h1 { font-size: 18px; margin: 0 0 12px; }
          h2 { font-size: 14px; margin: 16px 0 8px; }
          .meta { font-size: 12px; color: #6b7280; margin-bottom: 12px; }
          .kv { width: 100%; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden; }
          .kv-row { display: flex; gap: 12px; padding: 10px 12px; border-top: 1px solid #e5e7eb; }
          .kv-row:first-child { border-top: 0; }
          .k { width: 180px; font-size: 12px; color: #6b7280; }
          .v { font-size: 12px; font-weight: 600; color: #111827; }
          table { width: 100%; border-collapse: collapse; margin-top: 8px; }
          th, td { border: 1px solid #e5e7eb; padding: 8px; text-align: left; font-size: 12px; }
          th { background: #f3f4f6; }
          .muted { color: #6b7280; font-size: 12px; }
        </style>
      </head>
      <body>
        ${htmlContent}
      </body>
    </html>
  `);
  w.document.close();
  w.focus();
  w.print();
}

// ============================================================
// NEW: Generic “Profile export” that includes STUDENT + TABLE
// ============================================================

function buildProfileHTML(title, student, studentFields, rows, rowColumns) {
  const metaLine = `Generated on: ${new Date().toLocaleString()}`;

  const studentBlock = `
    <h2>Student Details</h2>
    <div class="kv">
      ${(studentFields || [])
        .map(
          (f) => `
        <div class="kv-row">
          <div class="k">${escHtml(f.label)}</div>
          <div class="v">${escHtml(student?.[f.key])}</div>
        </div>
      `
        )
        .join("")}
    </div>
  `;

  const tableBlock = `
    <h2>Enrollments</h2>
    ${
      rows?.length
        ? `
      <table>
        <thead>
          <tr>
            ${(rowColumns || []).map((c) => `<th>${escHtml(c.label)}</th>`).join("")}
          </tr>
        </thead>
        <tbody>
          ${(rows || [])
            .map(
              (r) => `
            <tr>
              ${(rowColumns || [])
                .map((c) => `<td>${escHtml(r?.[c.key])}</td>`)
                .join("")}
            </tr>
          `
            )
            .join("")}
        </tbody>
      </table>
    `
        : `<div class="muted">No enrollments found.</div>`
    }
  `;

  return `
    <h1>${escHtml(title)}</h1>
    <div class="meta">${escHtml(metaLine)}</div>
    ${studentBlock}
    ${tableBlock}
  `;
}

// One CSV that contains:
// - Student block (key,value)
// - blank line
// - Enrollments table
function buildProfileCSV(student, studentFields, rows, rowColumns) {
  const studentLines = (studentFields || []).map(
    (f) => `${safeCsv(f.label)},${safeCsv(student?.[f.key])}`
  );

  const tableHeader = (rowColumns || []).map((c) => safeCsv(c.label)).join(",");
  const tableBody = (rows || [])
    .map((r) => (rowColumns || []).map((c) => safeCsv(r?.[c.key])).join(","))
    .join("\n");

  return [
    "Student Details",
    "Field,Value",
    ...studentLines,
    "",
    "Enrollments",
    tableHeader,
    tableBody,
  ]
    .filter((x) => x !== undefined)
    .join("\n");
}

/**
 * Export profile data to CSV (student details + enrollments)
 *
 * @param {string} filename
 * @param {object} student
 * @param {Array<object>} rows
 * @param {object} config
 *  - studentFields: [{key,label}]
 *  - rowColumns: [{key,label}]
 */
export function exportProfileToCSV(filename, student, rows, config) {
  const csv = buildProfileCSV(
    student,
    config?.studentFields || [],
    rows || [],
    config?.rowColumns || []
  );
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
  downloadBlob(filename, blob);
}

/**
 * Export profile data to PDF (student details + enrollments)
 *
 * @param {string} title
 * @param {object} student
 * @param {Array<object>} rows
 * @param {object} config
 *  - studentFields: [{key,label}]
 *  - rowColumns: [{key,label}]
 */
export function exportProfileToPDF(title, student, rows, config) {
  const html = buildProfileHTML(
    title,
    student,
    config?.studentFields || [],
    rows || [],
    config?.rowColumns || []
  );
  exportToPDF(title, html);
}