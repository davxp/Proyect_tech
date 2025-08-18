// Base de la API y helpers para sesión/navegación
const BASE = "http://127.0.0.1:8000";
const API = BASE + "/api";

function saveUserSession(user) { localStorage.setItem("user", JSON.stringify(user)); }
function getUserSession() { const u = localStorage.getItem("user"); return u ? JSON.parse(u) : null; }
function logout() { localStorage.removeItem("user"); location.href = "./index.html"; }

function requireAuth(roles = []) {
  const u = getUserSession();
  if (!u) { location.href = "./index.html"; return null; }
  if (roles.length && !roles.includes(u.role)) {
    // si el rol no cuadra, lo mando a su panel
    location.href = u.role === "admin" ? "./admin.html" : "./user.html";
    return null;
  }
  return u;
}

async function jsonFetch(url, options = {}) {
  const o = Object.assign({ headers: { "Content-Type": "application/json" } }, options);
  const res = await fetch(url, o);
  if (!res.ok) throw new Error((await res.text()) || res.statusText);
  return res.headers.get("content-type")?.includes("application/json") ? res.json() : res.text();
}
