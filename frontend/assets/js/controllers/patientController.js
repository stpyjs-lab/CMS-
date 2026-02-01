import { apiGetAll, apiGetOne, apiCreate, apiUpdate, apiDelete } from "../services/patientService.js";
import { showAlert } from "../components/Alert.js";
import { renderPatientTable } from "../components/PatientTable.js";
import { resetForm, fillForm } from "../components/PatientForm.js";
import { setState, getState } from "../state/store.js";
import { $, createElement } from "../utils/dom.js";

export function initPatientController() {
  loadPatients();

  $("patientForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
      first_name: $("first_name").value.trim(),
      last_name: $("last_name").value.trim(),
      dob: $("dob").value || null,
      phone: $("phone").value.trim(),
      email: $("email").value.trim(),
      address: $("address").value.trim(),
    };

    const { editingId } = getState();
    editingId ? await updatePatient(editingId, data) : await createNewPatient(data);
  });

  $("cancelBtn").addEventListener("click", () => {
    setState({ editingId: null });
    resetForm();
  });
}

export async function loadPatients() {
  const spinner = $("loadingSpinner");
  const table = $("patientsTableContainer");
  spinner.style.display = "block";
  table.style.display = "none";

  const patients = await apiGetAll();
  setState({ patients });
  renderPatientTable(patients);

  spinner.style.display = "none";
  table.style.display = "block";
}

export async function createNewPatient(data) {
  const res = await apiCreate(data);
  if (res.ok) {
    showAlert("Patient added!");
    resetForm();
    loadPatients();
  }
}

export async function editPatient(id) {
  const patient = await apiGetOne(id);
  setState({ editingId: id });
  fillForm(patient);
  window.scrollTo({ top: 0, behavior: "smooth" });
}

export async function updatePatient(id, data) {
  const res = await apiUpdate(id, data);
  if (res.ok) {
    showAlert("Updated!");
    resetForm();
    setState({ editingId: null });
    loadPatients();
  }
}

export async function deletePatientAction(id) {
  const res = await apiDelete(id);
  if (res.ok) {
    showAlert("Deleted!");
    loadPatients();
  }
}
