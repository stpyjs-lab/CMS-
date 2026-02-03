// Feature: billing form component — populate selects and manage form state for invoices. Connects: billingController and services.
import { $ } from "../utils/dom.js";
import { apiGetAll as apiGetAllPatients } from "../services/patientService.js";
import { apiGetAll as apiGetAllDoctors } from "../services/doctorService.js";

export async function populateSelects() {
  const patients = await apiGetAllPatients();
  const pSelect = $("patient_id");
  pSelect.innerHTML = "<option value=''>Select patient</option>";
  (patients || []).forEach((p) => {
    const opt = document.createElement("option");
    opt.value = p.id;
    opt.textContent = `${p.first_name} ${p.last_name}`;
    pSelect.appendChild(opt);
  });

  const doctors = await apiGetAllDoctors();
  const dSelect = $("doctor_id");
  dSelect.innerHTML = "<option value=''>Select doctor</option>";
  (doctors || []).forEach((d) => {
    const opt = document.createElement("option");
    opt.value = d.id;
    opt.textContent = d.name || `${d.first_name || ""} ${d.last_name || ""}`.trim();
    dSelect.appendChild(opt);
  });
}

export function resetForm() {
  $("billingForm").reset();
  $("submitBtn").textContent = "Create Invoice";
  $("cancelBtn").style.display = "none";
  $("doctor_id").value = "";
}

export function fillForm(inv) {
  $("patient_id").value = inv.patient_id;
  $("doctor_id").value = inv.doctor_id || "";
  $("amount").value = inv.amount;
  $("issued_on").value = inv.issued_on || "";
  $("description").value = inv.description || "";

  $("submitBtn").textContent = "Update Invoice";
  $("cancelBtn").style.display = "inline-block";
}
