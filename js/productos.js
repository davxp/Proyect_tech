const u = requireAuth(["admin"]);
document.getElementById("btnLogout").onclick = logout;

const URL = `${API}/products`;
const tabla = document.getElementById("tabla");
const form = document.getElementById("formProducto");
const imgForm = document.getElementById("formImagen");
const imgMsg = document.getElementById("imgMsg");

async function cargar() {
  const data = await jsonFetch(URL);
  tabla.innerHTML = data.map(p => `
    <tr>
      <td>${p.id}</td>
      <td>${p.sku}</td>
      <td>${p.name}</td>
      <td>${p.price}</td>
      <td>${p.stock}</td>
      <td>${p.image_path ? `<img src="${p.image_path}" alt="" style="height:40px">` : "-"}</td>
      <td>
        <button onclick='editar(${JSON.stringify(p).replace(/'/g,"&#39;")})'>Editar</button>
        <button onclick="eliminar(${p.id})">Eliminar</button>
      </td>
    </tr>
  `).join("");
}

function editar(p) {
  document.getElementById("pid").value = p.id;
  document.getElementById("sku").value = p.sku;
  document.getElementById("name").value = p.name;
  document.getElementById("description").value = p.description || "";
  document.getElementById("price").value = p.price;
  document.getElementById("stock").value = p.stock;
  document.getElementById("provider_id").value = p.provider_id || "";
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    sku: sku.value.trim(),
    name: name.value.trim(),
    description: description.value.trim(),
    price: parseFloat(price.value),
    stock: parseInt(stock.value),
    provider_id: provider_id.value ? parseInt(provider_id.value) : null
  };

  const id = document.getElementById("pid").value;
  if (id) {
    await jsonFetch(`${URL}/${id}`, { method: "PUT", body: JSON.stringify(payload) });
  } else {
    await jsonFetch(URL, { method: "POST", body: JSON.stringify(payload) });
  }
  form.reset();
  cargar();
});

async function eliminar(id) {
  if (!confirm("¿Eliminar producto?")) return;
  await jsonFetch(`${URL}/${id}`, { method: "DELETE" });
  cargar();
}

imgForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  imgMsg.textContent = "";
  const id = document.getElementById("pid").value;
  if (!id) { imgMsg.textContent = "Primero selecciona un producto (Editar)"; return; }
  const file = document.getElementById("imagen").files[0];
  if (!file) { imgMsg.textContent = "Selecciona una imagen"; return; }
  const fd = new FormData();
  fd.append("file", file);
  const res = await fetch(`${URL}/${id}/upload-image`, { method: "POST", body: fd });
  if (!res.ok) { imgMsg.textContent = "Error al subir"; return; }
  imgMsg.textContent = "Imagen subida";
  cargar();
});

cargar();
