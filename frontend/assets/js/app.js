// Feature: frontend app bootstrap — initializes SPA router and UI. Connects: router and page assets.
// Main entrypoint for frontend
// import { initStudentController } from "./controllers/studentController.js";
import { router } from "./router/viewRouter.js";

// Initialize app on page load
window.addEventListener("DOMContentLoaded", async () => {
  router();
  // Auto-enable background image if it exists at the expected path
  try {
    const res = await fetch('/assets/images/clinic-bg.jpg', { method: 'HEAD' });
    if (res.ok) document.body.classList.add('bg-image');
  } catch (e) {
    // network or file not present - fall back to gradient
  }
  // initStudentController();
});