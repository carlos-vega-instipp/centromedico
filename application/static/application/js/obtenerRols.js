const inputBuscarRol = document.getElementById("buscarRol");
const listaResultadosRoles = document.getElementById("resultadosRoles");
const inputRolId = document.getElementById("rol_id");
let timeoutRol = null;

inputBuscarRol.addEventListener("input", () => {
  const texto = inputBuscarRol.value.trim();

  listaResultadosRoles.innerHTML = "";
  inputRolId.value = "";

  if (!texto) return;

  // Pequeño debounce para no disparar demasiadas peticiones
  clearTimeout(timeoutRol);
  timeoutRol = setTimeout(() => {
    fetch(`/api/groups?search=${encodeURIComponent(texto)}`)
      .then((res) => res.json())
      .then((data) => {
        console.log("Respuesta del API: ", data);
        listaResultadosRoles.innerHTML = "";

        const roles = Array.isArray(data)
          ? data
          : data.results || data.data || data.roles || [];

        if (!roles.length) return;

        roles.forEach((r) => {
          const item = document.createElement("button");
          item.type = "button";
          item.className = "list-group-item list-group-item-action";
          item.textContent = `${r.name}`;
          item.dataset.id = r.id;

          item.addEventListener("click", () => {
            inputBuscarRol.value = `${r.name}`;
            inputRolId.value = r.id;
            listaResultadosRoles.innerHTML = "";
          });

          listaResultadosRoles.appendChild(item);
        });
      })
      .catch((err) => {
        console.error(err);
      });
  }, 300);
});

document.addEventListener("click", (e) => {
  if (
    !e.target.closest("#buscarRol") &&
    !e.target.closest("#resultadosRoles")
  ) {
    listaResultadosRoles.innerHTML = "";
  }
});
