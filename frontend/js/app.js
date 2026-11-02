const API_BASE_URL = "";

let cuentaEditandoId = null;
let cuentasCache = [];
let filtroActual = "todas";

/* ---------- TOKEN ---------- */
function guardarToken(t) { localStorage.setItem("notaapp_token", t); }
function obtenerToken() { return localStorage.getItem("notaapp_token"); }
function guardarUsuario(u) { localStorage.setItem("notaapp_user", JSON.stringify(u)); }
function obtenerUsuario() {
    try { return JSON.parse(localStorage.getItem("notaapp_user") || "null"); }
    catch { return null; }
}
function cerrarSesion() {
    localStorage.removeItem("notaapp_token");
    localStorage.removeItem("notaapp_user");
    mostrarPantalla("screen-login");
    mostrarMensaje("login-mensaje", "Sesión cerrada correctamente", "ok");
}

/* ---------- API ---------- */
async function apiFetch(ruta, opciones = {}) {
    const token = obtenerToken();
    const headers = { "Content-Type": "application/json" };
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const respuesta = await fetch(`${API_BASE_URL}${ruta}`, {
        ...opciones,
        headers: { ...headers, ...(opciones.headers || {}) }
    });

    if (respuesta.status === 401) {
        cerrarSesion();
        mostrarMensaje("login-mensaje", "Tu sesión venció; ingresá nuevamente.", "error");
        throw new Error("401");
    }

    if (!respuesta.ok) {
        const data = await respuesta.json().catch(() => ({}));
        let detalle = data.detail;
        if (Array.isArray(detalle)) {
            detalle = detalle.map(e => e.msg || JSON.stringify(e)).join(", ");
        }
        throw new Error(detalle || `Error ${respuesta.status}`);
    }

    return await respuesta.json();
}

/* ---------- UI ---------- */
function mostrarPantalla(id) {
    document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
    document.getElementById(id).classList.add("active");
    window.scrollTo(0, 0);
}
function mostrarMensaje(elementId, texto, tipo) {
    const el = document.getElementById(elementId);
    if (!el) return;
    el.textContent = texto;
    el.className = "mensaje " + (tipo || "");
}
function abrirModal(id) { document.getElementById(id).classList.add("active"); }
function cerrarModal(id) { document.getElementById(id).classList.remove("active"); }

function escaparHTML(texto) {
    const div = document.createElement("div");
    div.textContent = texto == null ? "" : texto;
    return div.innerHTML;
}

/* ---------- AUTH ---------- */
async function registrar() {
    const nombre = document.getElementById("reg-nombre").value.trim();
    const email = document.getElementById("reg-email").value.trim();
    const password = document.getElementById("reg-password").value;
    const rol = document.getElementById("reg-rol").value;

    mostrarMensaje("register-mensaje", "Registrando...", "");

    try {
        const r = await fetch(`${API_BASE_URL}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nombre, email, password, rol })
        });
        const data = await r.json();
        if (!r.ok) throw new Error(data.detail || "Error en el registro");

        mostrarMensaje("register-mensaje", "¡Registro exitoso! Ya podés iniciar sesión.", "ok");
        setTimeout(() => mostrarPantalla("screen-login"), 1200);
    } catch (e) {
        mostrarMensaje("register-mensaje", e.message, "error");
    }
}

async function iniciarSesion() {
    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-password").value;

    mostrarMensaje("login-mensaje", "Ingresando...", "");

    try {
        const r = await fetch(`${API_BASE_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });
        const data = await r.json();
        if (!r.ok) throw new Error(data.detail || "Credenciales inválidas");

        guardarToken(data.access_token);
        guardarUsuario(data.user);

        document.getElementById("saludo-nombre").textContent = data.user.nombre || "Titular";
        mostrarPantalla("screen-main");
    } catch (e) {
        mostrarMensaje("login-mensaje", e.message, "error");
    }
}

async function cargarPerfil() {
    const u = obtenerUsuario();
    if (u) document.getElementById("saludo-nombre").textContent = u.nombre || "Titular";
    try {
        const perfil = await apiFetch("/auth/me");
        guardarUsuario(perfil);
        document.getElementById("saludo-nombre").textContent = perfil.nombre || "Titular";
    } catch (e) {
        console.error(e);
    }
}

/* ---------- CUENTAS ---------- */
function renderCuentas() {
    const contenedor = document.getElementById("lista-cuentas");

    let lista = cuentasCache;
    if (filtroActual !== "todas") {
        lista = lista.filter(c => c.tipo === filtroActual);
    }

    if (lista.length === 0) {
        contenedor.innerHTML = `<p class="vacio">No hay cuentas ${filtroActual === "todas" ? "guardadas todavía" : "en esta categoría"}.</p>`;
        return;
    }

    contenedor.innerHTML = "";
    lista.forEach(c => {
        const div = document.createElement("div");
        div.className = "cuenta-card";

        const estadoTexto = c.estado.charAt(0).toUpperCase() + c.estado.slice(1);

        div.innerHTML = `
            <div class="cuenta-info">
                <h3>${escaparHTML(c.sitio)}</h3>
                <p>${escaparHTML(c.login)}</p>
                <p class="puntos">●●●●●●●●</p>
                <span class="cuenta-estado estado-${c.estado}">${estadoTexto}</span>
            </div>
            <div class="acciones">
                <button class="btn-accion" data-accion="editar" data-id="${c.id}" title="Editar" type="button">✏️</button>
                <button class="btn-accion peligro" data-accion="eliminar" data-id="${c.id}" title="Eliminar" type="button">🗑️</button>
            </div>
        `;
        contenedor.appendChild(div);
    });
}

async function cargarCuentas() {
    const contenedor = document.getElementById("lista-cuentas");
    contenedor.innerHTML = `<p class="vacio">Cargando...</p>`;
    try {
        cuentasCache = await apiFetch("/cuentas/");
        renderCuentas();
    } catch (e) {
        contenedor.innerHTML = `<p class="vacio error">Error: ${escaparHTML(e.message)}</p>`;
    }
}

function abrirModalNueva() {
    cuentaEditandoId = null;
    document.getElementById("modal-titulo").textContent = "Nueva cuenta";
    document.getElementById("form-cuenta").reset();
    document.getElementById("cuenta-password").required = true;
    mostrarMensaje("cuenta-mensaje", "", "");
    abrirModal("modal-cuenta");
}

function abrirModalEditar(id) {
    const c = cuentasCache.find(x => x.id === id);
    if (!c) return;

    cuentaEditandoId = id;
    document.getElementById("modal-titulo").textContent = "Editar cuenta";
    document.getElementById("cuenta-sitio").value = c.sitio;
    document.getElementById("cuenta-login").value = c.login;
    document.getElementById("cuenta-password").value = "";
    document.getElementById("cuenta-password").required = false;
    document.getElementById("cuenta-tipo").value = c.tipo;
    document.getElementById("cuenta-estado").value = c.estado;
    mostrarMensaje("cuenta-mensaje", "", "");
    abrirModal("modal-cuenta");
}

async function guardarCuenta() {
    const sitio = document.getElementById("cuenta-sitio").value.trim();
    const login = document.getElementById("cuenta-login").value.trim();
    const password = document.getElementById("cuenta-password").value;
    const tipo = document.getElementById("cuenta-tipo").value;
    const estado = document.getElementById("cuenta-estado").value;

    mostrarMensaje("cuenta-mensaje", "Guardando...", "");

    try {
        if (cuentaEditandoId) {
            const cambios = { sitio, login, tipo, estado };
            if (password) cambios.password = password;
            await apiFetch(`/cuentas/${cuentaEditandoId}`, {
                method: "PUT",
                body: JSON.stringify(cambios)
            });
            mostrarMensaje("cuenta-mensaje", "¡Cuenta actualizada!", "ok");
        } else {
            await apiFetch("/cuentas/", {
                method: "POST",
                body: JSON.stringify({ sitio, login, password, tipo, estado })
            });
            mostrarMensaje("cuenta-mensaje", "¡Cuenta creada!", "ok");
        }

        setTimeout(() => {
            cerrarModal("modal-cuenta");
            cargarCuentas();
        }, 700);
    } catch (e) {
        mostrarMensaje("cuenta-mensaje", e.message, "error");
    }
}

async function eliminarCuenta(id) {
    const c = cuentasCache.find(x => x.id === id);
    if (!c) return;
    if (!confirm(`¿Eliminar "${c.sitio}"?`)) return;
    try {
        await apiFetch(`/cuentas/${id}`, { method: "DELETE" });
        cargarCuentas();
    } catch (e) {
        alert("Error al eliminar: " + e.message);
    }
}

/* ---------- INIT ---------- */
document.addEventListener("DOMContentLoaded", () => {
    // Links auth
    document.getElementById("link-register").addEventListener("click", e => {
        e.preventDefault(); mostrarPantalla("screen-register");
    });
    document.getElementById("link-login").addEventListener("click", e => {
        e.preventDefault(); mostrarPantalla("screen-login");
    });

    // Forms
    document.getElementById("form-login").addEventListener("submit", e => {
        e.preventDefault(); iniciarSesion();
    });
    document.getElementById("form-register").addEventListener("submit", e => {
        e.preventDefault(); registrar();
    });

    // Logout
    document.getElementById("btn-logout").addEventListener("click", cerrarSesion);

    // Navegación
    document.getElementById("btn-cuentas").addEventListener("click", () => {
        mostrarPantalla("screen-cuentas");
        cargarCuentas();
    });
    document.getElementById("btn-back-main").addEventListener("click", () => {
        mostrarPantalla("screen-main");
    });

    // Modal
    document.getElementById("btn-nueva-cuenta").addEventListener("click", abrirModalNueva);
    document.getElementById("btn-cancelar-cuenta").addEventListener("click", () => {
        cerrarModal("modal-cuenta");
        mostrarMensaje("cuenta-mensaje", "", "");
    });
    document.getElementById("form-cuenta").addEventListener("submit", e => {
        e.preventDefault(); guardarCuenta();
    });

    // Acciones en tarjetas
    document.getElementById("lista-cuentas").addEventListener("click", e => {
        const btn = e.target.closest("button[data-accion]");
        if (!btn) return;
        const id = btn.dataset.id;
        if (btn.dataset.accion === "editar") abrirModalEditar(id);
        else if (btn.dataset.accion === "eliminar") eliminarCuenta(id);
    });

    // Filtros
    document.querySelectorAll(".filtro").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".filtro").forEach(b => b.classList.remove("activo"));
            btn.classList.add("activo");
            filtroActual = btn.dataset.tipo;
            renderCuentas();
        });
    });

    // Restaurar sesión
    const token = obtenerToken();
    if (token) {
        mostrarPantalla("screen-main");
        cargarPerfil();
    } else {
        mostrarPantalla("screen-login");
    }
});