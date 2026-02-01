const API_URL = window.ENV.API_BASE_URL; // usually /api/students (for studentService)
const REPORT_URL = "/api/reports/enrollments";

async function safeJson(res) {
  try { return await res.json(); } catch { return null; }
}

export async function apiGetEnrollmentReport() {
  const res = await fetch(REPORT_URL);
  if (!res.ok) return [];
  return safeJson(res);
}