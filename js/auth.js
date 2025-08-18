// Manejo de login simple (sin JWT, usando respuesta del backend)
const form = document.getElementById("loginForm");
const msg = document.getElementById("msg");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  msg.textContent = "Validando...";
  try {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const data = await jsonFetch(`${API}/users/login?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`, { method: "POST" });
    // La API devuelve { message, user: { id, name, role } }
    saveUserSession(data.user);
    location.href = data.user.role === "admin" ? "./admin.html" : "./user.html";
  } catch (err) {
    msg.textContent = "Credenciales inválidas";
  }
});
