import { $, createElement } from "../utils/dom.js";

export function resetForm() {
  $("doctorForm").reset();
  $("submitBtn").textContent = "Add Doctor";
  $("cancelBtn").style.display = "none";
}

export function fillForm(doctor) {
  $("name").value = doctor.name || "";
  $("specialty").value = doctor.specialty || "";
  $("phone").value = doctor.phone || "";
  $("email").value = doctor.email || "";

  $("submitBtn").textContent = "Update Doctor";
  $("cancelBtn").style.display = "inline-block";
}
