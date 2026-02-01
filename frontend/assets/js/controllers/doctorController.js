import { apiGetAll, apiGetOne, apiCreate, apiUpdate, apiDelete } from "../services/doctorService.js";
import { showAlert } from "../components/Alert.js";
import { renderDoctorTable } from "../components/DoctorTable.js";
import { resetForm, fillForm } from "../components/DoctorForm.js";
import { setState, getState } from "../state/store.js";
import { $, createElement } from "../utils/dom.js";

export function initDoctorController() {
  loadDoctors();

  $("doctorForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
      name: $("name").value.trim(),
      specialty: $("specialty").value.trim(),
      schedule: $("schedule").value || null,
      phone: $("phone").value.trim(),
    };

    const { editingId } = getState();
    editingId ? await updateDoctor(editingId, data) : await createNewDoctor(data);
  });

  $("cancelBtn").addEventListener("click", () => {
    setState({ editingId: null });
    resetForm();
  });
}

export async function loadDoctors() {
  const spinner = $("loadingSpinner");
  const table = $("doctorsTableContainer");
  spinner.style.display = "block";
  table.style.display = "none";

  const doctors = await apiGetAll();
  setState({ doctors });
  renderDoctorTable(doctors);

  spinner.style.display = "none";
  table.style.display = "block";
}

export async function createNewDoctor(data) {
  const res = await apiCreate(data);
  if (res.ok) {
    showAlert("Doctor added!");
    resetForm();
    loadDoctors();
  }
}

export async function editDoctor(id) {
  const doctor = await apiGetOne(id);
  setState({ editingId: id });
  fillForm(doctor);
  window.scrollTo({ top: 0, behavior: "smooth" });
}

export async function updateDoctor(id, data) {
  const res = await apiUpdate(id, data);
  if (res.ok) {
    showAlert("Updated!");
    resetForm();
    setState({ editingId: null });
    loadDoctors();
  }
}

export async function deleteDoctorAction(id) {
  const res = await apiDelete(id);
  if (res.ok) {
    showAlert("Deleted!");
    loadDoctors();
  }
}
