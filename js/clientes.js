requireAuth(["admin"]); document.getElementById("btnLogout").onclick = logout;

const URL = `${API}/clients`;
const tabla = document.getElementById("tabla");
const form = document.getElementById("form");

async function cargar() {
  const data = await jsonFetch(URL);
  tabla.innerHTML = data.map(c => `
    <tr>
      <td>${c.id}</td>
      <td>${c.first_name} ${c.last_name || ""}</td>
      <td>${c.email || "-"}</td>
      <td>${c.phone || "-"}</td>
      <td>
        <button onclick='edit(${JSON.stringify(c).replace(/'/g,"&#39;")})'>Editar</button>
        <button onclick='delC(${c.id})'>Eliminar</button>
      </td>
    </tr>
  `).join("");
}

function edit(c){
  id.value = c.id;
  first_name.value = c.first_name;
  last_name.value = c.last_name || "";
  email.value = c.email || "";
  phone.value = c.phone || "";
  address.value = c.address || "";
}

form.addEventListener("submit", async (e)=>{
  e.preventDefault();
  const payload = {
    first_name: first_name.value.trim(),
    last_name: last_name.value.trim(),
    email: email.value.trim() || null,
    phone: phone.value.trim() || null,
    address: address.value.trim() || null
  };
  if (id.value) await jsonFetch(`${URL}/${id.value}`, { method:"PUT", body: JSON.stringify(payload) });
  else await jsonFetch(URL, { method:"POST", body: JSON.stringify(payload) });
  form.reset(); cargar();
});

async function delC(cid){
  if(!confirm("¿Eliminar cliente?")) return;
  await jsonFetch(`${URL}/${cid}`, { method:"DELETE" });
  cargar();
}

cargar();
