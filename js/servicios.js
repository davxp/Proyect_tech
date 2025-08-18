requireAuth(["admin"]); document.getElementById("btnLogout").onclick = logout;

const URL = `${API}/services`;
const tabla = document.getElementById("tabla");
const form = document.getElementById("form");

async function cargar() {
  const data = await jsonFetch(URL);
  tabla.innerHTML = data.map(s => `
    <tr>
      <td>${s.id}</td>
      <td>${s.title}</td>
      <td>${s.cost}</td>
      <td>${s.estimated_time_minutes} min</td>
      <td>
        <button onclick='edit(${JSON.stringify(s).replace(/'/g,"&#39;")})'>Editar</button>
        <button onclick='delS(${s.id})'>Eliminar</button>
      </td>
    </tr>
  `).join("");
}

function edit(s){
  id.value = s.id;
  title.value = s.title;
  description.value = s.description || "";
  cost.value = s.cost;
  estimated_time_minutes.value = s.estimated_time_minutes;
  assigned_technician_id.value = s.assigned_technician_id || "";
}

form.addEventListener("submit", async (e)=>{
  e.preventDefault();
  const payload = {
    title: title.value.trim(),
    description: description.value.trim() || null,
    cost: parseFloat(cost.value),
    estimated_time_minutes: parseInt(estimated_time_minutes.value),
    assigned_technician_id: assigned_technician_id.value ? parseInt(assigned_technician_id.value) : null
  };
  if (id.value) await jsonFetch(`${URL}/${id.value}`, { method:"PUT", body: JSON.stringify(payload) });
  else await jsonFetch(URL, { method:"POST", body: JSON.stringify(payload) });
  form.reset(); cargar();
});

async function delS(idv){
  if(!confirm("¿Eliminar servicio?")) return;
  await jsonFetch(`${URL}/${idv}`, { method:"DELETE" });
  cargar();
}

cargar();
