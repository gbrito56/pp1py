const apiUrl = "http://localhost:8000";

const MENSAJE = document.getElementById("mensaje");
const TABLA = document.getElementById("tablaArticulos");
const INICIO = document.getElementById("inicio");
const BOTON_EXPLORAR = document.getElementById("boton_explorar");
const BOTON_REVISAR = document.getElementById("boton_revisar");
const CHECK_EDITAR = document.getElementById("editar");
const CHECK_BORRAR = document.getElementById("borrar");
const ID_EDITAR = document.getElementById("idEditar");
const ACTIVO_EDITAR = document.getElementById("activoEditar");
const NOMBRE_EDITAR = document.getElementById("nombreEditar");
const PRECIO_EDITAR = document.getElementById("precioEditar");
const NOMBRE_NUEVO = document.getElementById("nombreNuevo");
const PRECIO_NUEVO = document.getElementById("precioNuevo");
const ACTIVO_NUEVO = document.getElementById("activoNuevo");

let listaExplorada = false;

CHECK_EDITAR.addEventListener("change", () => {
    const isChecked = CHECK_EDITAR.checked;
    if (CHECK_BORRAR.checked && isChecked) {
        CHECK_BORRAR.checked = false;
    }
    ID_EDITAR.disabled = !isChecked;
    NOMBRE_EDITAR.disabled = !isChecked;
    PRECIO_EDITAR.disabled = !isChecked;
    ACTIVO_EDITAR.disabled = !isChecked;
    if (isChecked) {
        ACTIVO_EDITAR.checked = true;
    } else {
        ACTIVO_EDITAR.checked = false;
    }
    document.getElementById("boton_editar").disabled = !isChecked;
});

CHECK_BORRAR.addEventListener("change", () => {
    const isChecked = CHECK_BORRAR.checked;
    NOMBRE_EDITAR.disabled = true;
    PRECIO_EDITAR.disabled = true;
    if (CHECK_EDITAR.checked && isChecked) {
        CHECK_EDITAR.checked = false;
    }
    if (ACTIVO_EDITAR.checked) {
        ACTIVO_EDITAR.checked = false;
    }
    ID_EDITAR.disabled = !isChecked;
    ACTIVO_EDITAR.disabled = !isChecked;
    document.getElementById("boton_borrar").disabled = !isChecked;
    if (isChecked) {
        alert("Al borrar un artículo, se eliminará de la lista de selección automáticamente. \nMarcar la casilla 'Activo' para cambiar el estado del artículo a 'No Disponible' en lugar de eliminarlo completamente.");
    }
});

BOTON_REVISAR.addEventListener("click", () => {
    BOTON_REVISAR.className = "text-sm font-medium transition-colors duration-300 text-stone-600 border-b-2 border-stone-300 px-2 py-1";
    BOTON_EXPLORAR.className = "text-sm font-medium transition-colors duration-300 px-2 py-1";
    INICIO.classList.replace("block", "hidden");
    MENSAJE.innerText = "";
    if (!TABLA.classList.contains("hidden")) {
        TABLA.classList.add("hidden");
    }
    mostrarSeleccion();
});

BOTON_EXPLORAR.addEventListener("click", () => {
    BOTON_EXPLORAR.className = "text-sm font-medium transition-colors duration-300 text-stone-600 border-b-2 border-stone-300 px-2 py-1";
    BOTON_REVISAR.className = "text-sm font-medium transition-colors duration-300 px-2 py-1";
    INICIO.classList.replace("hidden", "block");
    if (listaExplorada) {
        listarArticulos();
    } else {
        TABLA.classList.add("hidden");
        MENSAJE.innerText = "Click en 'Mostrar Artículos' para ver el listado. Los cambios realizados se mostraran en el listado automaticamente.";
    }
});

function verSeleccion() {
    const seleccion = localStorage.getItem('lista_seleccion');
    return seleccion ? JSON.parse(seleccion) : [];
}

function cambiarSeleccion(id) {
    let seleccion = verSeleccion()
    const idStr = String(id)

    if (seleccion.includes(idStr)) {
        seleccion = seleccion.filter(item => item !== idStr);
    } else {
        seleccion.push(idStr);
    }

    localStorage.setItem('lista_seleccion', JSON.stringify(seleccion))
}

async function mostrarSeleccion() {
    MENSAJE.innerText = "";
    MENSAJE.innerText = "Cargando...";
    const seleccion = verSeleccion();
    if (seleccion.length === 0) {
        MENSAJE.innerText = "No hay artículos seleccionados.";
        return;
    }

    try {
        const articulos = await obtenerArticulos();
        const articulosSeleccionados = articulos.filter(articulo =>
            seleccion.includes(String(articulo.id)));
        generarTabla(articulosSeleccionados);
        MENSAJE.innerText = "Selección obtenida correctamente.";
    } catch (error) {
        MENSAJE.innerText = "Error: " + error.message;
    }
}

async function obtenerArticulos() {

    try {
        const response = await fetch(`${apiUrl}/articulos`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error("Error en la respuesta del servidor");
        }

        const articulos = await response.json();
        return articulos;
    } catch (error) {
        MENSAJE.innerText = "Error: " + error.message;
        return [];
    }
}

async function filtrarArticulos() {
    try {
        const articulos = await obtenerArticulos();
        const seleccion = verSeleccion();
        const articulosFiltrados = articulos.filter(articulo =>
            seleccion.includes(String(articulo.id)));
        return articulosFiltrados;
    } catch (error) {
        MENSAJE.innerText = "Error: " + error.message;
        return [];
    }
}

async function generarTabla(articulos) {

    MENSAJE.innerText = "Cargando...";
    if (!TABLA.classList.contains("hidden")) {
        TABLA.classList.add("hidden");
    }
    const tbody = TABLA.querySelector("tbody");
    tbody.innerHTML = "";

    if (articulos.length === 0) {
        MENSAJE.innerText = "No hay artículos disponibles.";
        return;
    }

    const seleccion = verSeleccion();

    articulos.forEach(articulo => {
        const fila = document.createElement("tr");
        
        const tdId = document.createElement("td");
        tdId.innerText = articulo.id;
        tdId.className = "border-2 border-gray-600 px-2 py-1";
        fila.appendChild(tdId);
        
        const tdNombre = document.createElement("td");
        tdNombre.innerText = articulo.nombre;
        tdNombre.className = "border-2 border-gray-600 px-2 py-1";
        fila.appendChild(tdNombre);
        
        const tdPrecio = document.createElement("td");
        tdPrecio.innerText = "$" + articulo.precio;
        tdPrecio.className = "border-2 border-gray-600 px-2 py-1";
        fila.appendChild(tdPrecio);
        
        const tdEstado = document.createElement("td");
        tdEstado.innerText = articulo.activo ? "Disponible" : "No Disponible";
        tdEstado.className = "border-2 border-gray-600 px-2 py-1";
        fila.appendChild(tdEstado);

        const tdSelect = document.createElement("td");
        tdSelect.className = "border-2 border-gray-600 px-2 py-1 justify-center items-center";
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.className = "appearance-none w-6 h-6 border-2 border-gray-700 rounded transition-colors duration-300";

        if (seleccion.includes(String(articulo.id))) {
            checkbox.checked = true;
        }

        if (checkbox.checked) {
            checkbox.classList.add("bg-green-500");
        } else {
            checkbox.classList.remove("bg-green-500");
        }

        checkbox.addEventListener("change", () => {
            if (checkbox.checked) {
                checkbox.classList.add("bg-green-500");
            } else {
                checkbox.classList.remove("bg-green-500");
            }
            cambiarSeleccion(articulo.id);
            if (INICIO.classList.contains("hidden")) {
                mostrarSeleccion();
            }
        });

        tdSelect.appendChild(checkbox);
        fila.appendChild(tdSelect);
        tbody.appendChild(fila);
    });
    TABLA.classList.remove("hidden");
    MENSAJE.innerText = "Resultados obtenidos correctamente.";
}

async function listarArticulos() {
    try {
        const articulos = await obtenerArticulos();
        generarTabla(articulos);
        listaExplorada = true;
    }   catch (error) {
        MENSAJE.innerText = "Error: " + error.message;
    }
}

async function crearArticulo() {

    const nombre = NOMBRE_NUEVO.value;
    const precio = parseInt(PRECIO_NUEVO.value);
    const activo = ACTIVO_NUEVO.checked;
    const mensaje = document.getElementById("mensaje");

    if (!nombre || isNaN(precio) || precio < 500) {
        alert("Complete todos los datos correctamente (Precio mayor a 500)");
        return;
    }

    if (!activo) {
        const confirmacion = confirm("El artículo se creará como 'No Disponible'. ¿Desea continuar?");
        if (!confirmacion) {
            return;
        }
    }

    try {
    const response = await fetch(`${apiUrl}/articulos`, {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({ nombre, precio, activo })
    });

    if (!response.ok) {
        throw new Error("Error al crear el artículo");
    }

    listarArticulos();

    NOMBRE_NUEVO.value = "";
    PRECIO_NUEVO.value = "";
    ACTIVO_NUEVO.checked = true;

    } catch (error) {
        MENSAJE.innerText = "Error: " + error.message;
    }
}

async function borrarArticulo() {
    const id = parseInt(ID_EDITAR.value);
    const logico = ACTIVO_EDITAR.checked;
    const mensaje = document.getElementById("mensaje");

    if (isNaN(id)) {
        alert("Ingrese un ID válido");
        return;
    }

    try {
    const response = await fetch(`${apiUrl}/articulos/${id}?logico=${logico}`, {
        method: "DELETE",
        headers: {
        "Content-Type": "application/json"
        }
    });

    if (!response.ok) {
        throw new Error("Error al borrar el artículo");
    }

    const data = await response.json();

    listarArticulos();

    } catch (error) {
        MENSAJE.innerText = "Error: " + error.message;
    }
}

async function editarArticulo() {
    const id = parseInt(ID_EDITAR.value);
    const nombre = document.getElementById("nombreEditar").value;
    const precio = parseInt(document.getElementById("precioEditar").value);
    const activo = ACTIVO_EDITAR.checked;

    if (isNaN(id) || id <= 0 || !nombre || isNaN(precio) || precio < 500) {
        alert("Complete todos los datos correctamente (Precio mayor o igual a 500)");
        return;
    }

    try {
    const response = await fetch(`${apiUrl}/articulos/${id}`, {
        method: "PUT",
        headers: {
        "Content-Type": "application/json"
        },
        body: JSON.stringify({ nombre, precio, activo })
    });

    if (!response.ok) {
        throw new Error("Error al editar el artículo");
    }

    const data = await response.json();

    listarArticulos();

    } catch (error) {
        MENSAJE.innerText = "Error: " + error.message;
    }
}
