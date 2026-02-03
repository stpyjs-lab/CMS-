// Feature: profiles data client — fetch all profiles for listings. Connects: profiles page and backend API.
// frontend/assets/js/services/profilesService.js
// Only responsible for fetching data (no DOM / UI here)

const API_URL = window.ENV.API_BASE_URL; // /api/students

export async function fetchAllProfiles() {
  const res = await fetch(API_URL);
  return res.ok ? await res.json() : [];
}
