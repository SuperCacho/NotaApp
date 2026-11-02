let token = localStorage.getItem('notaapp_token');
const API = ''; // Relativo

// LOGIN
function moveToNext(current, index) {
    if (current.value.length === 1) {
        const inputs = document.querySelectorAll('.pin-inputs input');
        if (index < 5) inputs[index + 1].focus();
    }
}

async function login() {
    const btn = document.querySelector('#login-view .btn');
    btn.innerText = "Cargando...";
    try {
        const res = await fetch('/auth/login', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: 'lucio@test.com', password: '123456' })
        });
        const data = await res.json();
        if (res.ok) {
            token = data.access_token;
            localStorage.setItem('notaapp_token', token);
            document.getElementById('login-view').style.display = 'none';
            document.getElementById('app').classList.add('active');
            cargarTodo();
        } else { alert("Error"); btn.innerText = "Desbloquear"; }
    } catch (e) { alert("Error de conexión"); btn.innerText = "Desbloquear"; }
}

// NAVEGACION
function showView(viewId) {
    document.querySelectorAll('#app > div').forEach(d => d.style.display = 'none');
    document.getElementById(viewId).style.display = 'block';
    if (viewId === 'main-view') cargarTodo();
    if (viewId === 'view-cuentas') cargarCuentas();
    if (viewId === 'view-telefonos') cargarTelefonos();
    if (viewId === 'view-notas') cargarNotas();
    if (viewId === 'view-recordatorios') cargarRecordatorios();
}

function openModal(id) { document.getElementById(id).classList.add('active'); }
function closeModal(id) { document.getElementById(id).classList.remove('active'); }

// FETCH HELPERS
const authHeaders = () => ({ 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` });

// CUENTAS
async function cargarCuentas() {
    const c = document.getElementById('lista-cuentas');
    c.innerHTML = '<p style="text-align:center; color:#999;">Cargando...</p>';
    const res = await fetch('/cuentas', { headers: authHeaders() });
    const data = await res.json();
    c.innerHTML = data.length ? '' : '<p style="text-align:center; color:#999;">No hay cuentas.</p>';
    data.forEach(item => {
        c.innerHTML += `
            <div class="item-card">
                <div class="item-info">
                    <h3>${item.sitio}</h3><p>${item.login}</p>
                    <div style="color:#ccc; letter-spacing:2px;">••••••••</div>
                </div>
                <div class="item-actions"><span>📋</span><span>✏️</span><span onclick="borrar('cuentas','${item.id}')">🗑️</span></div>
            </div>`;
    });
}
async function guardarCuenta() {
    const data = { sitio: document.getElementById('c-sitio').value, login: document.getElementById('c-login').value, tipo: document.getElementById('c-tipo').value, password_ciphertext: document.getElementById('c-pass').value };
    if (!data.sitio) return alert("Falta el sitio");
    await fetch('/cuentas', { method: 'POST', headers: authHeaders(), body: JSON.stringify(data) });
    closeModal('modal-cuenta'); cargarCuentas();
}

// TELEFONOS
async function cargarTelefonos() {
    const c = document.getElementById('lista-telefonos');
    c.innerHTML = 'Cargando...';
    const res = await fetch('/telefonos', { headers: authHeaders() });
    const data = await res.json();
    c.innerHTML = data.length ? '' : '<p style="text-align:center;">No hay teléfonos.</p>';
    data.forEach(item => {
        c.innerHTML += `
            <div class="item-card">
                <div class="item-info">
                    <h3>${item.nombre}</h3><p>📱 ${item.numero}</p>
                    <span class="item-tag">${item.tipo}</span>
                </div>
                <div class="item-actions"><span>📋</span><span>✏️</span><span onclick="borrar('telefonos','${item.id}')">🗑️</span></div>
            </div>`;
    });
}
async function guardarTelefono() {
    const data = { nombre: document.getElementById('t-nombre').value, numero: document.getElementById('t-numero').value, tipo: document.getElementById('t-tipo').value, descripcion: document.getElementById('t-desc').value };
    await fetch('/telefonos', { method: 'POST', headers: authHeaders(), body: JSON.stringify(data) });
    closeModal('modal-telefono'); cargarTelefonos();
}

// NOTAS
async function cargarNotas() {
    const c = document.getElementById('lista-notas');
    c.innerHTML = 'Cargando...';
    const res = await fetch('/notas', { headers: authHeaders() });
    const data = await res.json();
    c.innerHTML = data.length ? '' : '<p style="text-align:center;">No hay notas.</p>';
    data.forEach(item => {
        c.innerHTML += `
            <div class="item-card">
                <div class="item-info">
                    <h3>${item.titulo}</h3><p>${item.contenido}</p>
                    <span class="item-tag">${item.categoria}</span>
                </div>
                <div class="item-actions"><span>✏️</span><span onclick="borrar('notas','${item.id}')">🗑️</span></div>
            </div>`;
    });
}
async function guardarNota() {
    const data = { titulo: document.getElementById('n-titulo').value, contenido: document.getElementById('n-contenido').value, categoria: document.getElementById('n-categoria').value };
    await fetch('/notas', { method: 'POST', headers: authHeaders(), body: JSON.stringify(data) });
    closeModal('modal-nota'); cargarNotas();
}

// RECORDATORIOS
async function cargarRecordatorios() {
    const c = document.getElementById('lista-recordatorios');
    c.innerHTML = 'Cargando...';
    const res = await fetch('/recordatorios', { headers: authHeaders() });
    const data = await res.json();
    c.innerHTML = data.length ? '' : '<p style="text-align:center;">No hay recordatorios.</p>';

    // También actualizamos el Home
    const home = document.getElementById('home-recordatorios');
    home.innerHTML = '';

    data.forEach(item => {
        const html = `
            <div class="item-card">
                <div class="item-info">
                    <h3>${item.motivo}</h3><p>📅 ${item.fecha} ${item.hora}</p>
                </div>
                <span class="badge">${item.estado}</span>
            </div>`;
        c.innerHTML += html;
        home.innerHTML += `<div class="reminder-card"><div class="reminder-time">${item.hora}</div><div class="reminder-text">${item.motivo}</div><div class="badge">${item.estado}</div></div>`;
    });
}
async function guardarRecordatorio() {
    const data = { motivo: document.getElementById('r-motivo').value, fecha: document.getElementById('r-fecha').value, hora: document.getElementById('r-hora').value, estado: document.getElementById('r-estado').value };
    await fetch('/recordatorios', { method: 'POST', headers: authHeaders(), body: JSON.stringify(data) });
    closeModal('modal-recordatorio'); cargarRecordatorios();
}

// BORRAR GENERICO
async function borrar(endpoint, id) {
    if (!confirm("¿Seguro que querés eliminarlo?")) return;
    await fetch(`/${endpoint}/${id}`, { method: 'DELETE', headers: authHeaders() });
    cargarTodo();
}

function cargarTodo() {
    cargarCuentas(); cargarTelefonos(); cargarNotas(); cargarRecordatorios();
}

if (token) {
    document.getElementById('login-view').style.display = 'none';
    document.getElementById('app').classList.add('active');
    cargarTodo();
}