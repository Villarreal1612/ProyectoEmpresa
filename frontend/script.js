const API_URL = "https://gestion-trabajadores-backend.onrender.com";

document.addEventListener("DOMContentLoaded", cargarTrabajadores);

document.getElementById("formulario").addEventListener("submit", async (event) => {
    event.preventDefault();
    
    const nombre = document.getElementById("nombre").value;
    const edad = document.getElementById("edad").value;
    const puesto = document.getElementById("puesto").value;
    const salario = document.getElementById("salario").value;

    const response = await fetch(`${API_URL}/trabajadores/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre, edad, puesto, salario })
    });

    if (response.ok) {
        cargarTrabajadores();
        document.getElementById("formulario").reset();
    }
});

async function cargarTrabajadores() {
    const response = await fetch(`${API_URL}/trabajadores/`);
    const trabajadores = await response.json();

    const tabla = document.getElementById("tablaTrabajadores");
    tabla.innerHTML = "";

    trabajadores.forEach(trabajador => {
        const fila = document.createElement("tr");
        fila.innerHTML = `
            <td>${trabajador.nombre}</td>
            <td>${trabajador.edad}</td>
            <td>${trabajador.puesto}</td>
            <td>${trabajador.salario}</td>
            <td>
                <button class="editar" onclick="editarTrabajador('${trabajador._id}', '${trabajador.nombre}', ${trabajador.edad}, '${trabajador.puesto}', ${trabajador.salario})">Editar</button>
                <button class="eliminar" onclick="eliminarTrabajador('${trabajador._id}')">Eliminar</button>
            </td>
        `;
        tabla.appendChild(fila);
    });
}

async function eliminarTrabajador(id) {
    await fetch(`${API_URL}/trabajadores/${id}`, { method: "DELETE" });
    cargarTrabajadores();
}

function editarTrabajador(id, nombre, edad, puesto, salario) {
    document.getElementById("nombre").value = nombre;
    document.getElementById("edad").value = edad;
    document.getElementById("puesto").value = puesto;
    document.getElementById("salario").value = salario;

    const formulario = document.getElementById("formulario");
    formulario.onsubmit = async (event) => {
        event.preventDefault();
        const nuevoNombre = document.getElementById("nombre").value;
        const nuevaEdad = document.getElementById("edad").value;
        const nuevoPuesto = document.getElementById("puesto").value;
        const nuevoSalario = document.getElementById("salario").value;

        await fetch(`${API_URL}/trabajadores/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nombre: nuevoNombre, edad: nuevaEdad, puesto: nuevoPuesto, salario: nuevoSalario })
        });

        formulario.onsubmit = agregarTrabajador;
        formulario.reset();
        cargarTrabajadores();
    };
}

document.getElementById("descargarExcel").addEventListener("click", () => {
    window.location.href = `${API_URL}/trabajadores/exportar/`;
});
