// Feature: list utilities — searching, filtering, sorting helpers. Connects: controllers and components.
// frontend/assets/js/utils/listTools.js

// Turn an object into a searchable lowercase string using selected fields
export function makeSearchHaystack(obj, fields) {
  return fields
    .map((f) => String(obj?.[f] ?? ""))
    .join(" ")
    .toLowerCase();
}

// Filter a list by query over selected fields
export function filterList(list, query, fields) {
  const q = (query ?? "").trim().toLowerCase();
  if (!q) return [...(list || [])];

  return (list || []).filter((item) => {
    const hay = makeSearchHaystack(item, fields);
    return hay.includes(q);
  });
}

// Sort list by key + direction (asc/desc)
// Supports numeric sort for keys like id, fees, duration_weeks if values are numeric-like.
export function sortList(list, sortKey, sortDir = "asc") {
  const dir = sortDir === "desc" ? -1 : 1;
  const arr = [...(list || [])];

  arr.sort((a, b) => {
    let av = a?.[sortKey];
    let bv = b?.[sortKey];

    // Try numeric compare first if both look like numbers
    const an = Number(av);
    const bn = Number(bv);
    const bothNumeric = !Number.isNaN(an) && !Number.isNaN(bn);

    if (bothNumeric) return (an - bn) * dir;

    // fallback string compare
    av = String(av ?? "");
    bv = String(bv ?? "");
    return av.localeCompare(bv) * dir;
  });

  return arr;
}