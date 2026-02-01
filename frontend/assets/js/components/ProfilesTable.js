// frontend/assets/js/components/ProfilesTable.js
import { $ } from "../utils/dom.js";

export function renderProfilesTable(students) {
  const body = $("profilesTableBody");
  const noProfiles = $("noProfiles");

  if (!body) return;

  body.innerHTML = "";

  if (!students || students.length === 0) {
    if (noProfiles) noProfiles.style.display = "block";
    return;
  }

  if (noProfiles) noProfiles.style.display = "none";

  students.forEach((s) => {
    const tr = document.createElement("tr");
    tr.className = "border-b";

    tr.innerHTML = `
      <td class="px-3 py-2">${s.id}</td>

      <td class="px-3 py-2">
        <a href="/profiles/${s.id}" data-link class="text-blue-600 hover:underline font-medium">
          ${s.name}
        </a>
      </td>

      <td class="px-3 py-2">${s.email}</td>
      <td class="px-3 py-2">${s.phone || ""}</td>
      <td class="px-3 py-2">${s.doctor_name || ""}</td>

      <td class="px-3 py-2 flex gap-2">
        <a href="/profiles/${s.id}" data-link
          class="inline-flex items-center justify-center px-3 py-1 rounded bg-brand-1 text-white hover:bg-brand-2">
          View
        </a>
        <button class="inline-flex items-center justify-center px-3 py-1 rounded btn-danger" data-delete="${s.id}">Delete</button>
      </td>
    `;

    // Add delete handler
    tr.querySelector('[data-delete]')?.addEventListener('click', async () => {
      const res = await import('../services/patientService.js').then(m => m.apiDelete(s.id));
      if (res.ok) {
        tr.remove();
        const alert = await import('../components/Alert.js');
        alert.showAlert('Patient deleted!');
      } else {
        const alert = await import('../components/Alert.js');
        alert.showAlert('Failed to delete patient', 'error');
      }
    });
    body.appendChild(tr);
  });
}
