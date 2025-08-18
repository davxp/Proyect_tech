requireAuth(["admin"]); document.getElementById("btnLogout").onclick = logout;

const URL = `${API}/providers`;
const tabla = document.getElementById("tabla");
const form = document.getElementById("form");

async function cargar() {
  const data = await jsonFetch(URL);
  tabla.innerHTML = data.map(p => `
    <tr>
      <td>${p.id}</td>
      <td>${p.company_name}</td>
      <td>${p.contact_name || "-"}</td>
      <td>${p.phone || "-"}</td>
      <td>
        <button onclick='edit(${JSON.stringify(p).replace(/'/g,"&#39;")})'>Editar</button>
        <button onclick='delP(${p.id})'>Eliminar</button>
      </td>
    </tr>
  `).join("");
}

function edit(p){
  id.value = p.id;
  company_name.value = p.company_name;
  contact_name.value = p.contact_name || "";
  phone.value = p.phone || "";
  email.value = p.email || "";
}

form.addEventListener("submit", async (e)=>{
  e.preventDefault();
  const payload = {
    company_name: company_name.value.trim(),
    contact_name: contact_name.value.trim() || null,
    phone: phone.value.trim() || null,
    email: email.value.trim() || null
  };
  if (id.value) await jsonFetch(`${URL}/${id.value}`, { method:"PUT", body: JSON.stringify(payload) });
  else await jsonFetch(URL, { method:"POST", body: JSON.stringify(payload) });
  form.reset(); cargar();
});

async function delP(pid){
  if(!confirm("¿Eliminar proveedor?")) return;
  await jsonFetch(`${URL}/${pid}`, { method:"DELETE" });
  cargar();
}

cargar();
