// frontend/assets/js/router/viewRouter.js

async function loadView(path) {
  const res = await fetch(path);

  // If the view file is missing, show 404 view
  if (!res.ok) {
    const fallback = await fetch("/frontend/pages/404.html").then((r) => r.text());
    document.querySelector("#app").innerHTML = fallback;
    return;
  }

  const html = await res.text();
  document.querySelector("#app").innerHTML = html;

  // If Mermaid is available, re-render diagrams after HTML injection
  if (window.mermaid) {
    try {
      await window.mermaid.run({ querySelector: "#app .mermaid" });
    } catch (e) {
      console.warn("Mermaid render skipped:", e);
    }
  }
}

export async function router() {
  // Normalize path: remove trailing slash (except "/")
  let path = window.location.pathname;
  if (path.length > 1) path = path.replace(/\/$/, "");

  // --------------------
  // HOME
  // --------------------
  if (path === "/" || path === "/home") {
    await loadView("/frontend/pages/home.html");
    return;
  }


  // --------------------
  // PATIENTS (CRUD)
  // --------------------
  if (path === "/patients") {
    await loadView("/frontend/pages/patients.html");
    const mod = await import("../controllers/patientController.js");
    mod.initPatientController();
    return;
  }

  // --------------------
  // DOCTORS (CRUD)
  // --------------------
  if (path === "/doctors") {
    await loadView("/frontend/pages/doctors.html");
    const mod = await import("../controllers/doctorController.js");
    mod.initDoctorController();
    return;
  }

  // --------------------
  // BILLING (CRUD)
  // --------------------
  if (path === "/billing") {
    await loadView("/frontend/pages/billing.html");
    const mod = await import("../controllers/billingController.js");
    mod.initBillingController();
    return;
  }

  // Redirect old appointments route to billing
  if (path === "/appointments") {
    history.replaceState(null, "", "/billing");
    await loadView("/frontend/pages/billing.html");
    const mod = await import("../controllers/billingController.js");
    mod.initBillingController();
    return;
  }


  // --------------------
  // DOCS FLOW
  // --------------------
  if (path === "/docs/flow") {
    await loadView("/frontend/pages/flow.html");
    return;
  }

  // --------------------
  // PROFILES DIRECTORY (list)
  // --------------------
  if (path === "/profiles") {
    await loadView("/frontend/pages/profiles.html");
    const mod = await import("../controllers/profilesController.js");
    mod.initProfilesController();
    return;
  }

  // --------------------
  // PROFILE PAGE (dynamic): /profiles/:id
  // --------------------
  if (path.startsWith("/profiles/")) {
    const idStr = path.split("/")[2]; // "/profiles/1" -> "1"
    const id = Number(idStr);

    // If invalid id, show 404
    if (!Number.isInteger(id)) {
      await loadView("/frontend/pages/404.html");
      return;
    }

    await loadView("/frontend/pages/profile.html");
    const mod = await import("../controllers/profileController.js");
    mod.initProfileController(id);
    return;
  }

  // --------------------
  // DEFAULT
  // --------------------
  await loadView("/frontend/pages/404.html");
}

export function initRouterEvents() {
  document.addEventListener("click", (e) => {
    const link = e.target.closest("[data-link]");
    if (!link) return;

    e.preventDefault();
    history.pushState(null, "", link.getAttribute("href"));
    router();
  });

  window.addEventListener("popstate", router);
}