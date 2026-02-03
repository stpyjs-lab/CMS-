// Feature: patient form component — handles form reset/fill for patient data. Connects: patientController and DOM utils.
import { $, createElement } from "../utils/dom.js";

export function resetForm() {
  $("patientForm").reset();
  $("submitBtn").textContent = "Add Patient";
  $("cancelBtn").style.display = "none";
}

export function fillForm(patient) {
  $("first_name").value = patient.first_name || "";
  $("last_name").value = patient.last_name || "";
  $("age").value = patient.age != null ? patient.age : "";
  $("gender").value = patient.gender || "";
  $("phone").value = patient.phone || "";

  $("submitBtn").textContent = "Update Patient";
  $("cancelBtn").style.display = "inline-block";
} 
