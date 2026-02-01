// Load an HTML file into a target element
export async function loadComponent(selector, url) {
  const target = document.querySelector(selector);
  if (!target) return;

  const html = await fetch(url).then(res => res.text());
  target.innerHTML = html;
}
