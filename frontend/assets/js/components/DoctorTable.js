import { $ } from "../utils/dom.js";
import { editDoctor, deleteDoctorAction } from "../controllers/doctorController.js";

export function renderDoctorTable(doctors) {
  const body = $("doctorsTableBody");
  const noDoctors = $("noDoctors");

  body.innerHTML = "";

  if (!doctors || doctors.length === 0) {
    noDoctors.style.display = "block";
    return;
  }

  noDoctors.style.display = "none";

  doctors.forEach((d) => {
    const row = document.createElement("tr");
    row.className = "border-b";

    row.innerHTML = `
      <td class="px-3 py-2">${d.id}</td>
      <td class="px-3 py-2 font-medium text-gray-900">${d.name}</td>
      <td class="px-3 py-2">${d.specialty || ""}</td>
      <td class="px-3 py-2">${d.phone || ""}</td>
      <td class="px-3 py-2 flex space-x-2">
        <button class="bg-yellow-400 hover:bg-yellow-500 text-black py-1 px-3 rounded" data-edit="${d.id}">Edit</button>
        <button class="btn-danger text-white py-1 px-3 rounded" data-delete="${d.id}">Delete</button>
      </td>
    `;

    row.querySelector("[data-edit]").onclick = () => editDoctor(d.id);
    row.querySelector("[data-delete]").onclick = () => deleteDoctorAction(d.id);

    body.appendChild(row);
  });
}
