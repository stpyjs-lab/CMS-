import { $ } from "../utils/dom.js";

// Displays a temporary alert message (success by default, or error if specified)
export function showAlert(message, type = "success") {
  // Get the designated container element in the HTML where alerts should appear
  const container = $("alertContainer");

  // Create a new div element dynamically to hold the alert message
  const el = document.createElement("div");

  // Apply CSS classes (likely Tailwind CSS) for styling based on the alert type
  el.className =
    `px-4 py-2 rounded shadow text-white ${ // Base styles
      type === "success" ? "bg-green-500" : "bg-red-500" // Conditional background color
    }`;
  
  // Set the actual text content of the alert element
  el.textContent = message;

  // Add the newly created alert element to the container in the DOM
  container.appendChild(el);
  
  // Set a timer to automatically remove the alert element after 3000 milliseconds (3 seconds)
  setTimeout(() => el.remove(), 3000);
}
