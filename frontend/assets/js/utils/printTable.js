// frontend/assets/js/utils/printTable.js
// Only builds printable HTML (no export / no DOM events)

export function buildPrintableTableHTML(title, rows, columns) {
  const esc = (v) =>
    String(v ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;");

  return `
    <h1>${esc(title)}</h1>
    <table>
      <thead>
        <tr>
          ${columns.map((c) => `<th>${esc(c.label)}</th>`).join("")}
        </tr>
      </thead>
      <tbody>
        ${(rows || [])
          .map(
            (r) => `
          <tr>
            ${columns.map((c) => `<td>${esc(r?.[c.key])}</td>`).join("")}
          </tr>
        `
          )
          .join("")}
      </tbody>
    </table>
  `;
}
