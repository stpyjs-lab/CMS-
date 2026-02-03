// Feature: DOM utils — helper helpers for element selection and creation. Connects: components and controllers.
// Shortcut for selecting elements by ID
export const $ = (id) => document.getElementById(id);

// Converts an HTML string into a real DOM element
export function createElement(html) {
  const div = document.createElement("div");
  div.innerHTML = html.trim();
  return div.firstChild; // return the generated element
}
