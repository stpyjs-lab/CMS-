// frontend/assets/js/services/profileService.js
// Only data fetching / shaping (no DOM here)

export async function fetchStudentById(studentId) {
  const res = await fetch(`/api/students/${studentId}`);
  if (!res.ok) return null;
  return res.json();
}

export async function fetchEnrollmentsForStudent(studentId) {
  const res = await fetch(`/api/reports/enrollments`);
  if (!res.ok) return [];

  const all = await res.json();
  return (all || []).filter((r) => Number(r.student_id) === Number(studentId));
}
