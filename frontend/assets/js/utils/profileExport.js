// Feature: profile export helpers — build CSV/PDF fragments for profiles. Connects: profileController and export UI.
// frontend/assets/js/utils/profileExport.js
// Only export helpers for the profile page (no DOM events)

function esc(v) {
  return String(v ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

export const PROFILE_CSV_COLUMNS = [
  { key: "enrollment_id", label: "Enrollment ID" },
  { key: "course_title", label: "Course" },
  { key: "course_code", label: "Code" },
  { key: "teacher_name", label: "Teacher" },
  { key: "fees", label: "Fees" },
  { key: "duration_weeks", label: "Weeks" },
  { key: "enrolled_on", label: "Enrolled On" },
];

export function normalizeProfileRows(rows) {
  // keep it consistent even if backend keys vary slightly
  return (rows || []).map((r) => ({
    enrollment_id: r.enrollment_id ?? r.id ?? "",
    course_title: r.course_title ?? "",
    course_code: r.course_code ?? r.code ?? "",
    teacher_name: r.teacher_name ?? "",
    fees: r.fees ?? "",
    duration_weeks: r.duration_weeks ?? "",
    enrolled_on: r.enrolled_on ?? "",
  }));
}

export function buildProfilePDFHtml(student, rows) {
  const safeStudent = student || {};
  const safeRows = normalizeProfileRows(rows);

  return `
    <h1>Student Profile</h1>

    <h2>Basic Details</h2>
    <table>
      <tbody>
        <tr><th>ID</th><td>${esc(safeStudent.id)}</td></tr>
        <tr><th>Name</th><td>${esc(safeStudent.name)}</td></tr>
        <tr><th>Email</th><td>${esc(safeStudent.email)}</td></tr>
        <tr><th>Year</th><td>${esc(safeStudent.year)}</td></tr>
        <tr><th>Total Enrollments</th><td>${esc(safeRows.length)}</td></tr>
      </tbody>
    </table>

    <h2>Enrolled Courses</h2>
    <table>
      <thead>
        <tr>
          <th>Enroll ID</th>
          <th>Course</th>
          <th>Code</th>
          <th>Teacher</th>
          <th>Fees</th>
          <th>Weeks</th>
          <th>Enrolled On</th>
        </tr>
      </thead>
      <tbody>
        ${
          safeRows.length
            ? safeRows
                .map(
                  (r) => `
          <tr>
            <td>${esc(r.enrollment_id)}</td>
            <td>${esc(r.course_title)}</td>
            <td>${esc(r.course_code)}</td>
            <td>${esc(r.teacher_name)}</td>
            <td>${esc(r.fees)}</td>
            <td>${esc(r.duration_weeks)}</td>
            <td>${esc(r.enrolled_on)}</td>
          </tr>
        `
                )
                .join("")
            : `<tr><td colspan="7">No enrollments found.</td></tr>`
        }
      </tbody>
    </table>
  `;
}
