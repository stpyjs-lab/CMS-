import { $, createElement } from "../utils/dom.js";

export function resetForm() {
  $("patientForm").reset();
  $("submitBtn").textContent = "Add Patient";
  $("cancelBtn").style.display = "none";
}

export function fillForm(patient) {
  $("first_name").value = patient.first_name || "";
  $("last_name").value = patient.last_name || "";
  $("dob").value = patient.dob || "";
  $("phone").value = patient.phone || "";
  $("email").value = patient.email || "";
  $("address").value = patient.address || "";

  $("submitBtn").textContent = "Update Patient";
  $("cancelBtn").style.display = "inline-block";
}
