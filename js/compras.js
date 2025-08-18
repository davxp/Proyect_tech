requireAuth(["admin"]); document.getElementById("btnLogout").onclick = logout;

const URL = `${API}/purchases`;
const tabla = document.getElementById("tabla");
const msg = document.getElementById("msg");
const itemsDiv = document.getElementById("items");
const form = document.getElementById("formCompra");
const addItemBtn = document.getElementById("addItem");

function itemRow() {
  const wrap = document.createElement("div");
  wrap.className = "item";
  wrap.innerHTML = `
    <input type="number" class="product_id" placeholder="ID producto" required>
    <input type="number" class="quantity" placeholder="Cantidad" required>
    <input type="number" step="0.01" class="price" placeholder="Precio" required>
    <button type="button" class="del">X</button>
  `;
  wrap.querySelector(".del").onclick = () => wrap.remove();
  return wrap;
}

addItemBtn.onclick = () => itemsDiv.appendChild(itemRow());
itemsDiv.appendChild(itemRow()); // arranco con 1 fila

async function cargar() {
  const data = await jsonFetch(URL);
  tabla.innerHTML = data.map(p => `
    <tr>
      <td>${p.id}</td>
      <td>${p.client_id || "-"}</td>
      <td>${p.total}</td>
      <td>
        ${p.items.map(i => `#${i.product_id} x${i.quantity} ($${i.price})`).join("<br>")}
      </td>
      <td><button onclick="eliminar(${p.id})">Eliminar</button></td>
    </tr>
  `).join("");
}

form.addEventListener("submit", async (e)=>{
  e.preventDefault();
  msg.textContent = "";
  const items = [...document.querySelectorAll(".item")].map(r => ({
    product_id: parseInt(r.querySelector(".product_id").value),
    quantity: parseInt(r.querySelector(".quantity").value),
    price: parseFloat(r.querySelector(".price").value)
  })).filter(i => !isNaN(i.product_id) && !isNaN(i.quantity) && !isNaN(i.price));

  if (!items.length) { msg.textContent = "Agrega al menos un ítem"; return; }

  const payload = {
    client_id: client_id.value ? parseInt(client_id.value) : null,
    created_by: created_by.value ? parseInt(created_by.value) : null,
    items
  };

  try {
    await jsonFetch(URL, { method: "POST", body: JSON.stringify(payload) });
    form.reset(); itemsDiv.innerHTML = ""; itemsDiv.appendChild(itemRow());
    msg.textContent = "Compra registrada";
    cargar();
  } catch (err) {
    msg.textContent = "Error: " + err.message;
  }
});

async function eliminar(id) {
  if (!confirm("¿Eliminar compra?")) return;
  await jsonFetch(`${URL}/${id}`, { method:"DELETE" });
  cargar();
}

cargar();
