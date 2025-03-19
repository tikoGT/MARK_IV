// app/static/js/main.js

// Función para verificar el estado de autenticación
function checkAuth() {
    const token = localStorage.getItem('token');
    const publicPaths = ['/', '/login'];
    
    if (!token && !publicPaths.includes(window.location.pathname)) {
        window.location.href = '/login';
    }
}

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} fade-in`;
    notification.innerText = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 500);
    }, 3000);
}

// Función para realizar peticiones a la API con el token
async function apiRequest(url, method = 'GET', data = null) {
    const token = localStorage.getItem('token');
    
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (token) {
        options.headers['Authorization'] = `Bearer ${token}`;
    }
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        
        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
            return null;
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error en la petición:', error);
        showNotification('Error en la conexión con el servidor', 'error');
        return null;
    }
}

// Función para cerrar sesión
function logout() {
    localStorage.removeItem('token');
    window.location.href = '/login';
}

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    // Verificar autenticación en páginas protegidas
    checkAuth();
    
    // Configurar drag and drop para subida de archivos
    const dropzones = document.querySelectorAll('.dropzone');
    
    dropzones.forEach(dropzone => {
        dropzone.addEventListener('dragover', e => {
            e.preventDefault();
            dropzone.classList.add('active');
        });
        
        dropzone.addEventListener('dragleave', () => {
            dropzone.classList.remove('active');
        });
        
        dropzone.addEventListener('drop', e => {
            e.preventDefault();
            dropzone.classList.remove('active');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                // Si hay un input file asociado, actualizar su valor
                const fileInput = dropzone.querySelector('input[type="file"]');
                if (fileInput) {
                    fileInput.files = files;
                    // Disparar evento change para activar handlers
                    const event = new Event('change');
                    fileInput.dispatchEvent(event);
                }
            }
        });
    });
});