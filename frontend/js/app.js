const API_BASE_URL = "";
let cuentasCache = [], telefonosCache = [], notasCache = [], recordatoriosCache = [];
let filtroActual = "todas", accionConfirmada = null;
let cuentaEditandoId = null, telefonoEditandoId = null, notaEditandoId = null, recordatorioEditandoId = null;

function guardarToken(t) { localStorage.setItem("notaapp_token", t); }
function obtenerToken() { return localStorage.getItem("notaapp_token"); }
function guardarUsuario(u) { localStorage.setItem("notaapp_user", JSON.stringify(u)); }
function obtenerUsuario() { try { return JSON.parse(localStorage.getItem("notaapp_user") || "null"); } catch { return null; } }
function cerrarSesion() { localStorage.removeItem("notaapp_token"); localStorage.removeItem("notaapp_user"); mostrarPantalla("screen-login"); }

function mostrarPantalla(id) { document.querySelectorAll(".screen").forEach(s => s.classList.remove("active")); document.getElementById(id).classList.add("active"); window.scrollTo(0, 0); }
function mostrarMensaje(id, texto, tipo) { const el = document.getElementById(id); if (el) { el.textContent = texto; el.className = "mensaje " + (tipo || ""); } }
function abrirModal(id) { document.getElementById(id).classList.add("active"); }
function cerrarModal(id) { document.getElementById(id).classList.remove("active"); }
function pedirConfirmacion(mensaje, callback) { document.getElementById("confirmar-mensaje").textContent = mensaje; accionConfirmada = callback; abrirModal("modal-confirmar"); }
function escaparHTML(texto) { const div = document.createElement("div"); div.textContent = texto == null ? "" : texto; return div.innerHTML; }
function activarBoton(btn, texto = "Cargando...") { btn.dataset.textoOriginal = btn.innerHTML; btn.innerHTML = `<span class="spinner"></span> ${texto}`; btn.disabled = true; }
function desactivarBoton(btn) { btn.innerHTML = btn.dataset.textoOriginal; btn.disabled = false; }
function mostrarSpinnerLista(id) { const c = document.getElementById(id); if (c) c.innerHTML = `<div class="cargando-box"><span class="spinner grande"></span></div>`; }

async function apiFetch(ruta, opciones = {}) {
    const token = obtenerToken(); const headers = { "Content-Type": "application/json" };
    if (token) headers["Authorization"] = `Bearer ${token}`;
    const r = await fetch(`${API_BASE_URL}${ruta}`, { ...opciones, headers: { ...headers, ...(opciones.headers || {}) } });
    if (r.status === 401) { cerrarSesion(); throw new Error("Sesión vencida"); }
    if (!r.ok) { const d = await r.json().catch(() => ({})); throw new Error(d.detail || `Error ${r.status}`); }
    return await r.json();
}

async function iniciarSesion(e) {
    e.preventDefault(); const btn = e.target.querySelector("button");
    const email = document.getElementById("login-email").value.trim(); const password = document.getElementById("login-password").value;
    activarBoton(btn, "Ingresando..."); mostrarMensaje("login-mensaje", "", "");
    try {
        const r = await fetch(`${API_BASE_URL}/auth/login`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, password }) });
        const data = await r.json(); if (!r.ok) throw new Error(data.detail || "Credenciales inválidas");
        guardarToken(data.access_token); guardarUsuario(data.user);
        document.getElementById("saludo-nombre").textContent = data.user.nombre || "Titular"; mostrarPantalla("screen-main");
    } catch (e) { mostrarMensaje("login-mensaje", e.message, "error"); } finally { desactivarBoton(btn); }
}

async function registrar(e) {
    e.preventDefault(); const btn = e.target.querySelector("button");
    const nombre = document.getElementById("reg-nombre").value.trim(); const email = document.getElementById("reg-email").value.trim();
    const password = document.getElementById("reg-password").value; const rol = document.getElementById("reg-rol").value;
    activarBoton(btn, "Registrando...");
    try {
        const r = await fetch(`${API_BASE_URL}/auth/register`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ nombre, email, password, rol }) });
        if (!r.ok) { const d = await r.json(); throw new Error(d.detail || "Error"); }
        mostrarMensaje("register-mensaje", "¡Registrado! Ingresá.", "ok"); setTimeout(() => mostrarPantalla("screen-login"), 1500);
    } catch (e) { mostrarMensaje("register-mensaje", e.message, "error"); } finally { desactivarBoton(btn); }
}

/* ---------- CUENTAS ---------- */
function renderCuentas() {
    const c = document.getElementById("lista-cuentas"); let l = cuentasCache;
    if (filtroActual !== "todas") l = l.filter(x => x.tipo === filtroActual);
    if (l.length === 0) { c.innerHTML = `<p class="vacio">No hay cuentas.</p>`; return; }
    c.innerHTML = ""; l.forEach(x => {
        const d = document.createElement("div"); d.className = "cuenta-card";
        d.innerHTML = `<div class="cuenta-info"><h3>${escaparHTML(x.sitio)}</h3><p>${escaparHTML(x.login)}</p><p class="puntos">●●●●●●●●</p><span class="cuenta-estado estado-${x.estado}">${x.estado.charAt(0).toUpperCase() + x.estado.slice(1)}</span></div>
        <div class="acciones"><button class="btn-accion" data-accion="editar-cuenta" data-id="${x.id}" type="button">✏️</button><button class="btn-accion peligro" data-accion="eliminar-cuenta" data-id="${x.id}" type="button">🗑️</button></div>`;
        c.appendChild(d);
    });
}
async function cargarCuentas() { mostrarSpinnerLista("lista-cuentas"); try { cuentasCache = await apiFetch("/cuentas/"); renderCuentas(); } catch (e) { document.getElementById("lista-cuentas").innerHTML = `<p class="vacio error">${e.message}</p>`; } }
function abrirModalNuevaCuenta() { cuentaEditandoId = null; document.getElementById("modal-titulo-cuenta").textContent = "Nueva cuenta"; document.getElementById("form-cuenta").reset(); document.getElementById("cuenta-password").required = true; mostrarMensaje("cuenta-mensaje", "", ""); abrirModal("modal-cuenta"); }
function editarCuenta(id) { const x = cuentasCache.find(c => c.id === id); if (!x) return; cuentaEditandoId = id; document.getElementById("modal-titulo-cuenta").textContent = "Editar cuenta"; document.getElementById("cuenta-sitio").value = x.sitio; document.getElementById("cuenta-login").value = x.login; document.getElementById("cuenta-password").value = ""; document.getElementById("cuenta-password").required = false; document.getElementById("cuenta-tipo").value = x.tipo; document.getElementById("cuenta-estado").value = x.estado; abrirModal("modal-cuenta"); }
async function guardarCuenta(e) {
    e.preventDefault(); const btn = document.getElementById("btn-guardar-cuenta");
    const data = { sitio: document.getElementById("cuenta-sitio").value.trim(), login: document.getElementById("cuenta-login").value.trim(), password: document.getElementById("cuenta-password").value, tipo: document.getElementById("cuenta-tipo").value, estado: document.getElementById("cuenta-estado").value };
    activarBoton(btn, cuentaEditandoId ? "Actualizando..." : "Guardando...");
    try {
        if (cuentaEditandoId) { const cam = { ...data }; if (!cam.password) delete cam.password; await apiFetch(`/cuentas/${cuentaEditandoId}`, { method: "PUT", body: JSON.stringify(cam) }); }
        else { await apiFetch("/cuentas/", { method: "POST", body: JSON.stringify(data) }); }
        mostrarMensaje("cuenta-mensaje", "¡Guardado!", "ok"); setTimeout(() => { cerrarModal("modal-cuenta"); cargarCuentas(); }, 800);
    } catch (e) { mostrarMensaje("cuenta-mensaje", e.message, "error"); } finally { desactivarBoton(btn); }
}

/* ---------- TELÉFONOS ---------- */
async function cargarTelefonos() {
    mostrarSpinnerLista("lista-telefonos");
    try {
        telefonosCache = await apiFetch("/telefonos/"); const c = document.getElementById("lista-telefonos");
        if (telefonosCache.length === 0) { c.innerHTML = `<p class="vacio">No hay teléfonos.</p>`; return; }
        c.innerHTML = ""; telefonosCache.forEach(x => {
            const d = document.createElement("div"); d.className = "cuenta-card";
            d.innerHTML = `<div class="cuenta-info"><h3>${escaparHTML(x.nombre)}</h3><p>📱 ${escaparHTML(x.numero)}</p><span class="cuenta-estado estado-normal">${escaparHTML(x.tipo)}</span></div><div class="acciones"><button class="btn-accion" data-accion="editar-tel" data-id="${x.id}" type="button">✏️</button><button class="btn-accion peligro" data-accion="eliminar-tel" data-id="${x.id}" type="button">🗑️</button></div>`;
            c.appendChild(d);
        });
    } catch (e) { document.getElementById("lista-telefonos").innerHTML = `<p class="vacio error">${e.message}</p>`; }
}
function editarTelefono(id) { const x = telefonosCache.find(c => c.id === id); if (!x) return; telefonoEditandoId = id; document.getElementById("modal-titulo-tel").textContent = "Editar teléfono"; document.getElementById("tel-nombre").value = x.nombre; document.getElementById("tel-numero").value = x.numero; document.getElementById("tel-tipo").value = x.tipo; document.getElementById("tel-desc").value = x.descripcion || ""; abrirModal("modal-telefono"); }
async function guardarTelefono(e) {
    e.preventDefault(); const btn = document.getElementById("btn-guardar-telefono");
    const data = { nombre: document.getElementById("tel-nombre").value.trim(), numero: document.getElementById("tel-numero").value.trim(), tipo: document.getElementById("tel-tipo").value, descripcion: document.getElementById("tel-desc").value.trim() };
    activarBoton(btn, telefonoEditandoId ? "Actualizando..." : "Guardando...");
    try {
        if (telefonoEditandoId) { await apiFetch(`/telefonos/${telefonoEditandoId}`, { method: "PUT", body: JSON.stringify(data) }); }
        else { await apiFetch("/telefonos/", { method: "POST", body: JSON.stringify(data) }); }
        mostrarMensaje("telefono-mensaje", "¡Guardado!", "ok"); setTimeout(() => { cerrarModal("modal-telefono"); cargarTelefonos(); }, 800);
    } catch (e) { mostrarMensaje("telefono-mensaje", e.message, "error"); } finally { desactivarBoton(btn); }
}

/* ---------- NOTAS ---------- */
async function cargarNotas() {
    mostrarSpinnerLista("lista-notas");
    try {
        notasCache = await apiFetch("/notas/"); const c = document.getElementById("lista-notas");
        if (notasCache.length === 0) { c.innerHTML = `<p class="vacio">No hay notas.</p>`; return; }
        c.innerHTML = ""; notasCache.forEach(x => {
            const d = document.createElement("div"); d.className = "cuenta-card";
            d.innerHTML = `<div class="cuenta-info"><h3>${escaparHTML(x.titulo)}</h3><p>${escaparHTML(x.contenido)}</p><span class="cuenta-estado estado-normal">${escaparHTML(x.categoria)}</span></div><div class="acciones"><button class="btn-accion" data-accion="editar-nota" data-id="${x.id}" type="button">✏️</button><button class="btn-accion peligro" data-accion="eliminar-nota" data-id="${x.id}" type="button">🗑️</button></div>`;
            c.appendChild(d);
        });
    } catch (e) { document.getElementById("lista-notas").innerHTML = `<p class="vacio error">${e.message}</p>`; }
}
function editarNota(id) { const x = notasCache.find(c => c.id === id); if (!x) return; notaEditandoId = id; document.getElementById("modal-titulo-nota").textContent = "Editar nota"; document.getElementById("nota-titulo").value = x.titulo; document.getElementById("nota-contenido").value = x.contenido; document.getElementById("nota-categoria").value = x.categoria; abrirModal("modal-nota"); }
async function guardarNota(e) {
    e.preventDefault(); const btn = document.getElementById("btn-guardar-nota");
    const data = { titulo: document.getElementById("nota-titulo").value.trim(), contenido: document.getElementById("nota-contenido").value.trim(), categoria: document.getElementById("nota-categoria").value };
    activarBoton(btn, notaEditandoId ? "Actualizando..." : "Guardando...");
    try {
        if (notaEditandoId) { await apiFetch(`/notas/${notaEditandoId}`, { method: "PUT", body: JSON.stringify(data) }); }
        else { await apiFetch("/notas/", { method: "POST", body: JSON.stringify(data) }); }
        mostrarMensaje("nota-mensaje", "¡Guardado!", "ok"); setTimeout(() => { cerrarModal("modal-nota"); cargarNotas(); }, 800);
    } catch (e) { mostrarMensaje("nota-mensaje", e.message, "error"); } finally { desactivarBoton(btn); }
}

/* ---------- RECORDATORIOS ---------- */
async function cargarRecordatorios() {
    mostrarSpinnerLista("lista-recordatorios");
    try {
        recordatoriosCache = await apiFetch("/recordatorios/"); const c = document.getElementById("lista-recordatorios");
        if (recordatoriosCache.length === 0) { c.innerHTML = `<p class="vacio">No hay recordatorios.</p>`; return; }
        c.innerHTML = ""; recordatoriosCache.forEach(x => {
            const d = document.createElement("div"); d.className = "cuenta-card";
            d.innerHTML = `<div class="cuenta-info"><h3>${escaparHTML(x.motivo)}</h3><p>📅 ${x.fecha} - ⏰ ${x.hora}</p><span class="cuenta-estado estado-${x.estado.toLowerCase()}">${escaparHTML(x.estado)}</span></div><div class="acciones"><button class="btn-accion" data-accion="editar-rec" data-id="${x.id}" type="button">✏️</button><button class="btn-accion peligro" data-accion="eliminar-rec" data-id="${x.id}" type="button">🗑️</button></div>`;
            c.appendChild(d);
        });
    } catch (e) { document.getElementById("lista-recordatorios").innerHTML = `<p class="vacio error">${e.message}</p>`; }
}
function editarRecordatorio(id) { const x = recordatoriosCache.find(c => c.id === id); if (!x) return; recordatorioEditandoId = id; document.getElementById("modal-titulo-rec").textContent = "Editar recordatorio"; document.getElementById("rec-motivo").value = x.motivo; document.getElementById("rec-fecha").value = x.fecha; document.getElementById("rec-hora").value = x.hora; document.getElementById("rec-estado").value = x.estado; abrirModal("modal-recordatorio"); }
async function guardarRecordatorio(e) {
    e.preventDefault(); const btn = document.getElementById("btn-guardar-rec");
    const data = { motivo: document.getElementById("rec-motivo").value.trim(), fecha: document.getElementById("rec-fecha").value, hora: document.getElementById("rec-hora").value, estado: document.getElementById("rec-estado").value };
    activarBoton(btn, recordatorioEditandoId ? "Actualizando..." : "Guardando...");
    try {
        if (recordatorioEditandoId) { await apiFetch(`/recordatorios/${recordatorioEditandoId}`, { method: "PUT", body: JSON.stringify(data) }); }
        else { await apiFetch("/recordatorios/", { method: "POST", body: JSON.stringify(data) }); }
        mostrarMensaje("rec-mensaje", "¡Guardado!", "ok"); setTimeout(() => { cerrarModal("modal-recordatorio"); cargarRecordatorios(); }, 800);
    } catch (e) { mostrarMensaje("rec-mensaje", e.message, "error"); } finally { desactivarBoton(btn); }
}

/* ---------- INIT ---------- */
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("link-register").addEventListener("click", e => { e.preventDefault(); mostrarPantalla("screen-register"); });
    document.getElementById("link-login").addEventListener("click", e => { e.preventDefault(); mostrarPantalla("screen-login"); });
    document.getElementById("form-login").addEventListener("submit", iniciarSesion);
    document.getElementById("form-register").addEventListener("submit", registrar);
    document.getElementById("btn-logout").addEventListener("click", cerrarSesion);

    document.getElementById("btn-cuentas").addEventListener("click", () => { mostrarPantalla("screen-cuentas"); cargarCuentas(); });
    document.getElementById("btn-telefonos").addEventListener("click", () => { mostrarPantalla("screen-telefonos"); cargarTelefonos(); });
    document.getElementById("btn-notas").addEventListener("click", () => { mostrarPantalla("screen-notas"); cargarNotas(); });
    document.getElementById("btn-recordatorios").addEventListener("click", () => { mostrarPantalla("screen-recordatorios"); cargarRecordatorios(); });

    document.getElementById("btn-back-main").addEventListener("click", () => mostrarPantalla("screen-main"));
    document.getElementById("btn-back-main-tel").addEventListener("click", () => mostrarPantalla("screen-main"));
    document.getElementById("btn-back-main-notas").addEventListener("click", () => mostrarPantalla("screen-main"));
    document.getElementById("btn-back-main-rec").addEventListener("click", () => mostrarPantalla("screen-main"));

    document.getElementById("btn-nueva-cuenta").addEventListener("click", abrirModalNuevaCuenta);
    document.getElementById("btn-cancelar-cuenta").addEventListener("click", () => cerrarModal("modal-cuenta"));
    document.getElementById("form-cuenta").addEventListener("submit", guardarCuenta);

    document.getElementById("btn-nuevo-telefono").addEventListener("click", () => { telefonoEditandoId = null; document.getElementById("modal-titulo-tel").textContent = "Nuevo teléfono"; document.getElementById("form-telefono").reset(); abrirModal("modal-telefono"); });
    document.getElementById("btn-cancelar-telefono").addEventListener("click", () => cerrarModal("modal-telefono"));
    document.getElementById("form-telefono").addEventListener("submit", guardarTelefono);

    document.getElementById("btn-nueva-nota").addEventListener("click", () => { notaEditandoId = null; document.getElementById("modal-titulo-nota").textContent = "Nueva nota"; document.getElementById("form-nota").reset(); abrirModal("modal-nota"); });
    document.getElementById("btn-cancelar-nota").addEventListener("click", () => cerrarModal("modal-nota"));
    document.getElementById("form-nota").addEventListener("submit", guardarNota);

    document.getElementById("btn-nuevo-recordatorio").addEventListener("click", () => { recordatorioEditandoId = null; document.getElementById("modal-titulo-rec").textContent = "Nuevo recordatorio"; document.getElementById("form-recordatorio").reset(); abrirModal("modal-recordatorio"); });
    document.getElementById("btn-cancelar-rec").addEventListener("click", () => cerrarModal("modal-recordatorio"));
    document.getElementById("form-recordatorio").addEventListener("submit", guardarRecordatorio);

    // Delegación de eventos para editar y eliminar
    document.getElementById("lista-cuentas").addEventListener("click", e => {
        const btn = e.target.closest("button[data-accion]"); if (!btn) return;
        if (btn.dataset.accion === "editar-cuenta") editarCuenta(btn.dataset.id);
        else if (btn.dataset.accion === "eliminar-cuenta") pedirConfirmacion("¿Eliminar cuenta?", async () => { activarBoton(btn, ""); await apiFetch(`/cuentas/${btn.dataset.id}`, { method: "DELETE" }); cargarCuentas(); });
    });
    document.getElementById("lista-telefonos").addEventListener("click", e => {
        const btn = e.target.closest("button[data-accion]"); if (!btn) return;
        if (btn.dataset.accion === "editar-tel") editarTelefono(btn.dataset.id);
        else if (btn.dataset.accion === "eliminar-tel") pedirConfirmacion("¿Eliminar teléfono?", async () => { activarBoton(btn, ""); await apiFetch(`/telefonos/${btn.dataset.id}`, { method: "DELETE" }); cargarTelefonos(); });
    });
    document.getElementById("lista-notas").addEventListener("click", e => {
        const btn = e.target.closest("button[data-accion]"); if (!btn) return;
        if (btn.dataset.accion === "editar-nota") editarNota(btn.dataset.id);
        else if (btn.dataset.accion === "eliminar-nota") pedirConfirmacion("¿Eliminar nota?", async () => { activarBoton(btn, ""); await apiFetch(`/notas/${btn.dataset.id}`, { method: "DELETE" }); cargarNotas(); });
    });
    document.getElementById("lista-recordatorios").addEventListener("click", e => {
        const btn = e.target.closest("button[data-accion]"); if (!btn) return;
        if (btn.dataset.accion === "editar-rec") editarRecordatorio(btn.dataset.id);
        else if (btn.dataset.accion === "eliminar-rec") pedirConfirmacion("¿Eliminar recordatorio?", async () => { activarBoton(btn, ""); await apiFetch(`/recordatorios/${btn.dataset.id}`, { method: "DELETE" }); cargarRecordatorios(); });
    });

    document.getElementById("btn-cancelar-confirmar").addEventListener("click", () => { cerrarModal("modal-confirmar"); accionConfirmada = null; });
    document.getElementById("btn-aceptar-confirmar").addEventListener("click", async () => { if (accionConfirmada) { cerrarModal("modal-confirmar"); await accionConfirmada(); accionConfirmada = null; } });

    document.querySelectorAll(".filtro").forEach(btn => {
        btn.addEventListener("click", () => { document.querySelectorAll(".filtro").forEach(b => b.classList.remove("activo")); btn.classList.add("activo"); filtroActual = btn.dataset.tipo; renderCuentas(); });
    });

    mostrarPantalla("screen-login");
});