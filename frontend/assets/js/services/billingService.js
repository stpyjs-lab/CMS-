const API_URL = "/api/billing";

async function safeJson(res) {
  try {
    return await res.json();
  } catch (_) {
    return null;
  }
}

export async function apiGetAll() {
  const res = await fetch(API_URL);
  if (!res.ok) return [];
  return safeJson(res);
}

export async function apiGetOne(id) {
  const res = await fetch(`${API_URL}/${id}`);
  if (!res.ok) return null;
  return safeJson(res);
}

export function apiCreate(data) {
  return fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}

export function apiUpdate(id, data) {
  return fetch(`${API_URL}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}

export function apiDelete(id) {
  return fetch(`${API_URL}/${id}`, { method: "DELETE" });
}
