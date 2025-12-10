const inputBuscar = document.getElementById("buscarUsuario");
const listaResultados = document.getElementById("resultadosUsuarios");
const inputUsuarioId = document.getElementById("usuario_id");
let timeout = null;

inputBuscar.addEventListener("input", () => {
  const texto = inputBuscar.value.trim();

  listaResultados.innerHTML = "";
  inputUsuarioId.value = "";

  if (!texto) return;

  // Pequeño debounce para no disparar demasiadas peticiones
  clearTimeout(timeout);
  timeout = setTimeout(() => {
    fetch(`/api/users?search=${encodeURIComponent(texto)}`)
      .then((res) => 
        res.json())
      .then((data) => {
        listaResultados.innerHTML = "";

        const usuarios = Array.isArray(data)
          ? data
          : data.results || data.data || data.usuarios || [];

        if (!usuarios.length) return;

        usuarios.forEach((u) => {
          console.log(u);
          const item = document.createElement("button");
          item.type = "button";
          item.className = "list-group-item list-group-item-action";
          item.textContent = `${u.first_name} ${u.last_name}`;
          item.dataset.id = u.id;

          item.addEventListener("click", () => {
            inputBuscar.value = `${u.first_name} ${u.last_name}`;
            inputUsuarioId.value = u.id;
            listaResultados.innerHTML = "";
          });

          listaResultados.appendChild(item);
        });
      })
      .catch((err) => {
        console.error(err);
      });
  }, 300);
});

document.addEventListener("click", (e) => {
  if (
    !e.target.closest("#buscarUsuario") &&
    !e.target.closest("#resultadosUsuarios")
  ) {
    listaResultados.innerHTML = "";
  }
});
