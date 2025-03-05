// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    console.log('Sistema de Gestión de Selección de Personal - Inicializado');
    
    // Inicializar componentes
    initializeComponents();
    
    // Configurar manejadores de eventos
    setupEventHandlers();
    
    // Cargar datos del dashboard
    loadDashboardData();
});

// Inicializar componentes de la aplicación
function initializeComponents() {
    // Verificar estado de los servicios
    checkServicesStatus();
    
    // Inicializar tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Inicializar popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Configurar manejadores de eventos para los botones
function setupEventHandlers() {
    // Requisiciones
    addEventListenerIfElementExists('nuevaRequisicion', 'click', function() {
        showModal('Crear Nueva Requisición', createRequisitionForm());
    });
    
    addEventListenerIfElementExists('listarRequisiciones', 'click', function() {
        fetchAndDisplayRequisitions();
    });
    
    // Vacantes
    addEventListenerIfElementExists('publicarVacante', 'click', function() {
        showModal('Publicar Vacante', createVacancyForm());
    });
    
    addEventListenerIfElementExists('listarVacantes', 'click', function() {
        fetchAndDisplayVacancies();
    });
    
    // Candidatos
    addEventListenerIfElementExists('registrarCandidato', 'click', function() {
        showModal('Registrar Candidato', createCandidateForm());
    });
    
    addEventListenerIfElementExists('listarCandidatos', 'click', function() {
        showModal('Seleccionar Vacante', selectVacancyForm('listarCandidatos'));
    });
    
    addEventListenerIfElementExists('filtrarCandidatos', 'click', function() {
        showModal('Filtrar Candidatos', createCandidateFilterForm());
    });
    
    // Evaluaciones
    addEventListenerIfElementExists('asignarEvaluacion', 'click', function() {
        showModal('Asignar Evaluación', createEvaluationForm());
    });
    
    addEventListenerIfElementExists('registrarResultado', 'click', function() {
        showModal('Registrar Resultado de Prueba', createTestResultForm());
    });
    
    addEventListenerIfElementExists('descargarReporte', 'click', function() {
        showModal('Descargar Reporte', createReportDownloadForm());
    });
    
    // Entrevistas
    addEventListenerIfElementExists('programarEntrevista', 'click', function() {
        showModal('Programar Entrevista', createInterviewForm());
    });
    
    addEventListenerIfElementExists('registrarFeedback', 'click', function() {
        showModal('Registrar Feedback', createFeedbackForm());
    });
    
    // Selección
    addEventListenerIfElementExists('generarReporte', 'click', function() {
        showModal('Generar Reporte Final', createFinalReportForm());
    });
    
    addEventListenerIfElementExists('tomarDecision', 'click', function() {
        showModal('Tomar Decisión de Contratación', createDecisionForm());
    });
    
    // Botón de actualizar dashboard
    addEventListenerIfElementExists('btnActualizarDashboard', 'click', function() {
        loadDashboardData();
    });
}

// Función auxiliar para agregar eventos solo si el elemento existe
function addEventListenerIfElementExists(id, eventType, callback) {
    const element = document.getElementById(id);
    if (element) {
        element.addEventListener(eventType, callback);
    }
}

// Verificar el estado de los servicios
function checkServicesStatus() {
    fetch('/metrics')
        .then(response => response.json())
        .then(data => {
            console.log('Estado de los servicios:', data);
            // Mostrar estado en la interfaz si existe un elemento para ello
            const statusElement = document.getElementById('systemStatus');
            if (statusElement) {
                let statusHtml = '<div class="d-flex align-items-center">';
                
                if (data.all_services_healthy) {
                    statusHtml += '<span class="badge bg-success me-2">Todos los servicios operativos</span>';
                } else {
                    statusHtml += '<span class="badge bg-warning me-2">Algunos servicios con problemas</span>';
                }
                
                statusHtml += '<a href="#" data-bs-toggle="modal" data-bs-target="#serviceDetailsModal">Ver detalles</a></div>';
                statusElement.innerHTML = statusHtml;
            }
        })
        .catch(error => {
            console.error('Error al verificar el estado de los servicios:', error);
            // Mostrar error en la interfaz
            const statusElement = document.getElementById('systemStatus');
            if (statusElement) {
                statusElement.innerHTML = '<span class="badge bg-danger">Error al conectar con los servicios</span>';
            }
        });
}

// Cargar datos para el dashboard
function loadDashboardData() {
    // Mostrar spinner de carga
    document.querySelectorAll('.dashboard-counter').forEach(element => {
        element.innerHTML = '<div class="spinner-border spinner-border-sm text-primary" role="status"><span class="visually-hidden">Cargando...</span></div>';
    });
    
    // Simular carga de datos (ya que solo estamos trabajando en el frontend)
    setTimeout(() => {
        // Datos de ejemplo para el dashboard
        const dashboardData = {
            requisitions: { count: 15 },
            vacancies: { count: 8 },
            candidates: { count: 42 },
            evaluations: { count: 28 },
            interviews: { count: 12 },
            selected: { count: 5 }
        };
        
        // Actualizar los contadores en el dashboard
        updateDashboardCounter('requisicionesCounter', dashboardData.requisitions.count);
        updateDashboardCounter('vacantesCounter', dashboardData.vacancies.count);
        updateDashboardCounter('candidatosCounter', dashboardData.candidates.count);
        updateDashboardCounter('evaluacionesCounter', dashboardData.evaluations.count);
        updateDashboardCounter('entrevistasCounter', dashboardData.interviews.count);
        updateDashboardCounter('seleccionadosCounter', dashboardData.selected.count);
        
        // Mostrar notificación de éxito
        showAlert('success', 'Dashboard actualizado correctamente', 2000);
    }, 1500);
}

// Actualizar un contador en el dashboard
function updateDashboardCounter(elementId, count) {
    const element = document.getElementById(elementId);
    if (element) {
        // Efecto de contador animado
        let currentCount = 0;
        const targetCount = count;
        const duration = 1000; // duración en ms
        const framesPerSecond = 60;
        const totalFrames = duration * framesPerSecond / 1000;
        const increment = targetCount / totalFrames;
        
        const timer = setInterval(() => {
            currentCount += increment;
            if (currentCount >= targetCount) {
                clearInterval(timer);
                currentCount = targetCount;
            }
            element.textContent = Math.round(currentCount);
        }, 1000 / framesPerSecond);
    }
}

// Mostrar un modal con contenido dinámico
function showModal(title, content) {
    // Verificar si ya existe un modal
    let modalElement = document.getElementById('dynamicModal');
    
    if (!modalElement) {
        // Crear el modal si no existe
        modalElement = document.createElement('div');
        modalElement.id = 'dynamicModal';
        modalElement.className = 'modal fade';
        modalElement.setAttribute('tabindex', '-1');
        modalElement.setAttribute('aria-hidden', 'true');
        
        modalElement.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        ${content}
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modalElement);
    } else {
        // Actualizar el contenido si ya existe
        modalElement.querySelector('.modal-title').textContent = title;
        modalElement.querySelector('.modal-body').innerHTML = content;
    }
    
    // Mostrar el modal
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
}

// Mostrar una alerta en la parte superior de la página
function showAlert(type, message, duration = 5000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3 shadow`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Insertar en el body para que aparezca por encima de todo
    document.body.appendChild(alertDiv);
    
    // Eliminar automáticamente después del tiempo especificado
    setTimeout(() => {
        if (alertDiv && alertDiv.parentNode) {
            alertDiv.classList.remove('show');
            setTimeout(() => alertDiv.remove(), 150);
        }
    }, duration);
}

// Función para obtener y mostrar requisiciones
function fetchAndDisplayRequisitions() {
    fetch('/requisitions/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener las requisiciones');
            }
            return response.json();
        })
        .then(data => {
            let content = `
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Cargo</th>
                                <th>Estado</th>
                                <th>Fecha de Creación</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            if (data.length === 0) {
                content += `
                    <tr>
                        <td colspan="5" class="text-center">No hay requisiciones disponibles</td>
                    </tr>
                `;
            } else {
                data.forEach(req => {
                    content += `
                        <tr>
                            <td>${req.id}</td>
                            <td>${req.positionName || req.position_name}</td>
                            <td>${req.status}</td>
                            <td>${req.createdAt || req.created_at}</td>
                            <td>
                                <button class="btn btn-sm btn-info" onclick="viewRequisition(${req.id})">Ver</button>
                            </td>
                        </tr>
                    `;
                });
            }
            
            content += `
                        </tbody>
                    </table>
                </div>
            `;
            
            showModal('Requisiciones de Personal', content);
        })
        .catch(error => {
            showAlert('danger', error.message);
        });
}

// Función para actualizar el contenido de un modal existente
function updateModalContent(title, content) {
    const modalElement = document.getElementById('dynamicModal');
    if (modalElement) {
        modalElement.querySelector('.modal-title').textContent = title;
        modalElement.querySelector('.modal-body').innerHTML = content;
    }
}

// Funciones para crear formularios dinámicos

// Formulario de requisición
function createRequisitionForm() {
    return `
        <form id="requisitionForm" class="needs-validation" novalidate>
            <div class="mb-3">
                <label for="positionName" class="form-label">Nombre del Cargo *</label>
                <input type="text" class="form-control" id="positionName" required>
                <div class="invalid-feedback">
                    Por favor ingrese el nombre del cargo.
                </div>
            </div>
            <div class="mb-3">
                <label for="functions" class="form-label">Funciones *</label>
                <textarea class="form-control" id="functions" rows="3" placeholder="Ingrese una función por línea" required></textarea>
                <div class="invalid-feedback">
                    Por favor ingrese al menos una función.
                </div>
            </div>
            <div class="mb-3">
                <label for="salaryCategory" class="form-label">Categoría Salarial *</label>
                <select class="form-select" id="salaryCategory" required>
                    <option value="">Seleccione una categoría</option>
                    <option value="Junior">Junior</option>
                    <option value="Semi-Senior">Semi-Senior</option>
                    <option value="Senior">Senior</option>
                    <option value="Lead">Lead</option>
                </select>
                <div class="invalid-feedback">
                    Por favor seleccione una categoría salarial.
                </div>
            </div>
            <div class="mb-3">
                <label for="profile" class="form-label">Perfil del Candidato *</label>
                <textarea class="form-control" id="profile" rows="3" required></textarea>
                <div class="invalid-feedback">
                    Por favor ingrese el perfil del candidato.
                </div>
            </div>
            <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary">Crear Requisición</button>
            </div>
        </form>
    `;
}

// Función para enviar la requisición
function submitRequisition() {
    const form = document.getElementById('requisitionForm');
    
    if (!validateForm(form)) {
        return;
    }
    
    const positionName = document.getElementById('positionName').value;
    const functionsText = document.getElementById('functions').value;
    const functions = functionsText.split('\n').filter(line => line.trim() !== '');
    const salaryCategory = document.getElementById('salaryCategory').value;
    const profile = document.getElementById('profile').value;
    
    // Mostrar indicador de carga
    const submitButton = form.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.innerHTML;
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Procesando...';
    
    const requisitionData = {
        position_name: positionName,
        functions: functions,
        salary_category: salaryCategory,
        profile: profile
    };
    
    fetch('/requisitions/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requisitionData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al crear la requisición');
        }
        return response.json();
    })
    .then(data => {
        // Actualizar el contador del dashboard
        loadDashboardData();
        
        showAlert('success', 'Requisición creada exitosamente');
        // Cerrar el modal
        const modalElement = document.getElementById('dynamicModal');
        const modal = bootstrap.Modal.getInstance(modalElement);
        modal.hide();
    })
    .catch(error => {
        showAlert('danger', error.message);
    })
    .finally(() => {
        // Restaurar el botón
        submitButton.disabled = false;
        submitButton.innerHTML = originalButtonText;
    });
}

// Formulario para crear vacante
function createVacancyForm() { 
    return `
        <form id="vacancyForm" class="needs-validation" novalidate>
            <div class="mb-3">
                <label for="requisitionId" class="form-label">ID de Requisición *</label>
                <div class="input-group">
                    <input type="number" class="form-control" id="requisitionId" required>
                    <button class="btn btn-outline-secondary" type="button" onclick="showRequisitionSelector()">
                        <i class="bi bi-search"></i> Buscar
                    </button>
                </div>
                <div class="invalid-feedback">
                    Por favor ingrese un ID de requisición válido.
                </div>
            </div>
            <div class="mb-3">
                <label for="platforms" class="form-label">Plataformas de Publicación *</label>
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" name="platforms" value="INTERNAL" id="platformInternal">
                    <label class="form-check-label" for="platformInternal">Interna</label>
                </div>
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" name="platforms" value="LINKEDIN" id="platformLinkedIn">
                    <label class="form-check-label" for="platformLinkedIn">LinkedIn</label>
                </div>
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" name="platforms" value="INDEED" id="platformIndeed">
                    <label class="form-check-label" for="platformIndeed">Indeed</label>
                </div>
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" name="platforms" value="JOBSITE" id="platformJobsite">
                    <label class="form-check-label" for="platformJobsite">Jobsite</label>
                </div>
                <div class="invalid-feedback" id="platformsInvalidFeedback">
                    Por favor seleccione al menos una plataforma.
                </div>
            </div>
            <div class="d-grid gap-2">
                <button type="submit" class="btn btn-success">Publicar Vacante</button>
            </div>
        </form>
    `;
}

// Función para mostrar selector de requisiciones
function showRequisitionSelector() {
    fetch('/requisitions/?status=APPROVED')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener las requisiciones');
            }
            return response.json();
        })
        .then(data => {
            let content = `
                <div class="mb-3">
                    <input type="text" class="form-control" id="searchRequisition" placeholder="Buscar por cargo...">
                </div>
                <div class="table-responsive" style="max-height: 400px; overflow-y: auto;">
                    <table class="table table-hover table-striped">
                        <thead class="table-light sticky-top">
                            <tr>
                                <th>ID</th>
                                <th>Cargo</th>
                                <th>Estado</th>
                                <th>Acción</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            if (data.length === 0) {
                content += `
                    <tr>
                        <td colspan="4" class="text-center">No hay requisiciones aprobadas disponibles</td>
                    </tr>
                `;
            } else {
                data.forEach(req => {
                    content += `
                        <tr>
                            <td>${req.id}</td>
                            <td>${req.positionName || req.position_name}</td>
                            <td><span class="badge bg-success">Aprobada</span></td>
                            <td>
                                <button class="btn btn-sm btn-primary" onclick="selectRequisition(${req.id}, '${req.positionName || req.position_name}')">Seleccionar</button>
                            </td>
                        </tr>
                    `;
                });
            }
            
            content += `
                        </tbody>
                    </table>
                </div>
            `;
            
            showModal('Seleccionar Requisición', content);
            
            // Agregar búsqueda en tiempo real
            document.getElementById('searchRequisition').addEventListener('keyup', function() {
                const searchTerm = this.value.toLowerCase();
                const rows = document.querySelectorAll('tbody tr');
                
                rows.forEach(row => {
                    const cargo = row.querySelector('td:nth-child(2)').textContent.toLowerCase();
                    if (cargo.includes(searchTerm)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            });
        })
        .catch(error => {
            showAlert('danger', error.message);
        });
}

// Función para seleccionar una requisición
function selectRequisition(id, name) {
    document.getElementById('requisitionId').value = id;
    
    // Cerrar el modal selector
    const modalElement = document.getElementById('dynamicModal');
    const modal = bootstrap.Modal.getInstance(modalElement);
    modal.hide();
    
    // Mostrar confirmación
    showAlert('info', `Requisición seleccionada: ${name} (ID: ${id})`, 2000);
    
    // Volver a mostrar el formulario de vacante
    setTimeout(() => {
        showModal('Publicar Vacante', createVacancyForm());
        document.getElementById('requisitionId').value = id;
    }, 500);
}

// Formulario para registrar candidato
function createCandidateForm() { 
    return `
        <form id="candidateForm" class="needs-validation" novalidate>
            <div class="mb-3">
                <label for="candidateName" class="form-label">Nombre Completo *</label>
                <input type="text" class="form-control" id="candidateName" required>
                <div class="invalid-feedback">
                    Por favor ingrese el nombre completo.
                </div>
            </div>
            <div class="mb-3">
                <label for="candidateEmail" class="form-label">Correo Electrónico *</label>
                <input type="email" class="form-control" id="candidateEmail" required>
                <div class="invalid-feedback">
                    Por favor ingrese un correo electrónico válido.
                </div>
            </div>
            <div class="mb-3">
                <label for="resumeUrl" class="form-label">URL del CV *</label>
                <input type="url" class="form-control" id="resumeUrl" required>
                <div class="invalid-feedback">
                    Por favor ingrese la URL del CV.
                </div>
            </div>
            <div class="mb-3">
                <label for="vacancyId" class="form-label">ID de Vacante *</label>
                <input type="number" class="form-control" id="vacancyId" required>
                <div class="invalid-feedback">
                    Por favor ingrese un ID de vacante válido.
                </div>
            </div>
            <div class="mb-3">
                <label for="skills" class="form-label">Habilidades *</label>
                <input type="text" class="form-control" id="skills" placeholder="Separadas por coma: Python, JavaScript, SQL..." required>
                <div class="invalid-feedback">
                    Por favor ingrese al menos una habilidad.
                </div>
            </div>
            <div class="mb-3">
                <label for="experienceYears" class="form-label">Años de Experiencia *</label>
                <input type="number" class="form-control" id="experienceYears" min="0" required>
                <div class="invalid-feedback">
                    Por favor ingrese los años de experiencia.
                </div>
            </div>
            <button type="submit" class="btn btn-info">Registrar Candidato</button>
        </form>
    `;
}

// Función para registrar candidato
function submitCandidate() {
    const candidateName = document.getElementById('candidateName').value;
    const candidateEmail = document.getElementById('candidateEmail').value;
    const resumeUrl = document.getElementById('resumeUrl').value;
    const vacancyId = document.getElementById('vacancyId').value;
    const skills = document.getElementById('skills').value.split(',').map(skill => skill.trim());
    const experienceYears = document.getElementById('experienceYears').value;
    
    // Mostrar indicador de carga
    const submitButton = document.querySelector('#candidateForm button[type="submit"]');
    const originalButtonText = submitButton.innerHTML;
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Procesando...';
    
    const candidateData = {
        name: candidateName,
        email: candidateEmail,
        resume_url: resumeUrl,
        vacancy_id: parseInt(vacancyId),
        skills: skills,
        experience_years: parseInt(experienceYears)
    };
    
    fetch('/candidates/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(candidateData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al registrar el candidato');
        }
        return response.json();
    })
    .then(data => {
        // Actualizar el contador del dashboard
        loadDashboardData();
        
        showAlert('success', 'Candidato registrado exitosamente');
        // Cerrar el modal
        const modalElement = document.getElementById('dynamicModal');
        const modal = bootstrap.Modal.getInstance(modalElement);
        modal.hide();
    })
    .catch(error => {
        showAlert('danger', error.message);
    })
    .finally(() => {
        // Restaurar el botón
        submitButton.disabled = false;
        submitButton.innerHTML = originalButtonText;
    });
}

// Formulario para filtrar candidatos
function createCandidateFilterForm() { 
    return `
        <form id="filterCandidatesForm" class="needs-validation" novalidate>
            <div class="mb-3">
                <label for="filterVacancyId" class="form-label">ID de Vacante *</label>
                <input type="number" class="form-control" id="filterVacancyId" required>
                <div class="invalid-feedback">
                    Por favor ingrese un ID de vacante válido.
                </div>
            </div>
            <div class="mb-3">
                <label for="filterStatus" class="form-label">Estado</label>
                <select class="form-select" id="filterStatus">
                    <option value="">Todos</option>
                    <option value="REGISTERED">Registrado</option>
                    <option value="IN_EVALUATION">En Evaluación</option>
                    <option value="EVALUATED">Evaluado</option>
                    <option value="INTERVIEWING">En Entrevista</option>
                    <option value="REJECTED">Rechazado</option>
                    <option value="SELECTED">Seleccionado</option>
                </select>
            </div>
            <div class="mb-3">
                <label for="requiredSkills" class="form-label">Habilidades Requeridas</label>
                <input type="text" class="form-control" id="requiredSkills" placeholder="Separadas por coma: Python, JavaScript, SQL...">
            </div>
            <div class="mb-3">
                <label for="minExperience" class="form-label">Experiencia Mínima (años)</label>
                <input type="number" class="form-control" id="minExperience" min="0">
            </div>
            <button type="submit" class="btn btn-secondary">Filtrar Candidatos</button>
        </form>
    `;
}

// Función para filtrar candidatos
function submitCandidateFilter() {
    const form = document.getElementById('filterCandidatesForm');
    
    if (!validateForm(form)) {
        return;
    }
    
    const vacancyId = document.getElementById('filterVacancyId').value;
    const status = document.getElementById('filterStatus').value;
    const requiredSkills = document.getElementById('requiredSkills').value;
    const minExperience = document.getElementById('minExperience').value;
    
    // Mostrar indicador de carga
    const submitButton = form.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.innerHTML;
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Buscando...';
    
    // Construir los parámetros de consulta
    let queryParams = `vacancy_id=${vacancyId}`;
    if (status) queryParams += `&status=${status}`;
    if (requiredSkills) {
        const skills = requiredSkills.split(',').map(skill => skill.trim()).join(',');
        queryParams += `&skills=${skills}`;
    }
    if (minExperience) queryParams += `&min_experience=${minExperience}`;
    
    // Hacer la petición
    fetch(`/candidates/filter?${queryParams}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al filtrar candidatos');
            }
            return response.json();
        })
        .then(data => {
            displayFilteredCandidates(data);
        })
        .catch(error => {
            showAlert('danger', error.message);
        })
        .finally(() => {
            // Restaurar el botón
            submitButton.disabled = false;
            submitButton.innerHTML = originalButtonText;
        });
}

// Función para mostrar candidatos filtrados
function displayFilteredCandidates(candidates) {
    let content = `
        <div class="mb-3">
            <div class="d-flex justify-content-between align-items-center">
                <h5>Se encontraron ${candidates.length} candidatos</h5>
                <div>
                    <button class="btn btn-sm btn-outline-primary" onclick="exportCandidateList()" title="Exportar a Excel">
                        <i class="bi bi-file-earmark-excel"></i> Exportar
                    </button>
                </div>
            </div>
        </div>
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead class="table-light">
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>Email</th>
                        <th>Experiencia</th>
                        <th>Habilidades</th>
                        <th>Estado</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    if (candidates.length === 0) {
        content += `
            <tr>
                <td colspan="7" class="text-center">No se encontraron candidatos con los filtros aplicados</td>
            </tr>
        `;
    } else {
        candidates.forEach(candidate => {
            content += `
                <tr>
                    <td>${candidate.id}</td>
                    <td>${candidate.name}</td>
                    <td>${candidate.email}</td>
                    <td>${candidate.experience_years} años</td>
                    <td>
                        ${candidate.skills.map(skill => `<span class="badge bg-info me-1">${skill}</span>`).join('')}
                    </td>
                    <td><span class="badge bg-${getStatusBadgeColor(candidate.status)}">${getStatusLabel(candidate.status)}</span></td>
                    <td>
                        <div class="btn-group">
                            <button class="btn btn-sm btn-outline-primary" onclick="viewCandidate(${candidate.id})">
                                <i class="bi bi-eye"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-warning" onclick="showModal('Asignar Evaluación', createEvaluationForm(${candidate.id}))">
                                <i class="bi bi-clipboard-check"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        });
    }
    
    content += `
                </tbody>
            </table>
        </div>
    `;
    
    updateModalContent('Candidatos Filtrados', content);
}

// Simulación de función para exportar lista de candidatos
function exportCandidateList() {
    showAlert('info', 'Preparando exportación de candidatos...', 2000);
    
    setTimeout(() => {
        showAlert('success', 'Lista de candidatos exportada exitosamente');
    }, 2000);
}

// Obtener color de badge para estado
function getStatusBadgeColor(status) {
    const statusColors = {
        'REGISTERED': 'primary',
        'IN_EVALUATION': 'info',
        'EVALUATED': 'success',
        'INTERVIEWING': 'warning',
        'REJECTED': 'danger',
        'SELECTED': 'success'
    };
    return statusColors[status] || 'secondary';
}

// Obtener etiqueta en español para estado
function getStatusLabel(status) {
    const statusLabels = {
        'REGISTERED': 'Registrado',
        'IN_EVALUATION': 'En Evaluación',
        'EVALUATED': 'Evaluado',
        'INTERVIEWING': 'En Entrevista',
        'REJECTED': 'Rechazado',
        'SELECTED': 'Seleccionado'
    };
    return statusLabels[status] || status;
}

// Formulario para asignar evaluación
function createEvaluationForm() { 
    return `
        <form id="evaluationForm" class="needs-validation" novalidate>
            <div class="mb-3">
                <label for="evalCandidateId" class="form-label">ID de Candidato *</label>
                <input type="number" class="form-control" id="evalCandidateId" required>
                <div class="invalid-feedback">
                    Por favor ingrese un ID de candidato válido.
                </div>
            </div>
            <div class="mb-3">
                <label for="evalVacancyId" class="form-label">ID de Vacante *</label>
                <input type="number" class="form-control" id="evalVacancyId" required>
                <div class="invalid-feedback">
                    Por favor ingrese un ID de vacante válido.
                </div>
            </div>
            <div class="mb-3">
                <label class="form-label">Pruebas a Asignar *</label>
                <div id="testsList">
                    <div class="test-item card mb-2 p-3">
                        <div class="mb-2">
                            <label class="form-label">Nombre de la Prueba *</label>
                            <input type="text" class="form-control test-name" required>
                        </div>
                        <div class="mb-2">
                            <label class="form-label">Tipo de Prueba *</label>
                            <select class="form-select test-type" required>
                                <option value="">Seleccione...</option>
                                <option value="TECHNICAL">Técnica</option>
                                <option value="LANGUAGE">Idioma</option>
                                <option value="PSYCHOMETRIC">Psicométrica</option>
                            </select>
                        </div>
                        <div class="mb-2">
                            <label class="form-label">Duración (minutos) *</label>
                            <input type="number" class="form-control test-duration" min="1" required>
                        </div>
                        <div class="mb-2">
                            <label class="form-label">Puntuación Mínima Requerida *</label>
                            <input type="number" class="form-control test-min-score" min="0" max="100" required>
                        </div>
                    </div>
                </div>
                <div class="mt-2">
                    <button type="button" class="btn btn-sm btn-outline-primary" id="addTestBtn">
                        Agregar Otra Prueba
                    </button>
                </div>
            </div>
            <button type="submit" class="btn btn-warning">Asignar Evaluación</button>
        </form>
    `;
}

// Función para enviar evaluación
function submitEvaluation() {
    const candidateId = document.getElementById('evalCandidateId').value;
    const vacancyId = document.getElementById('evalVacancyId').value;
    
    // Recopilar información de las pruebas
    const testItems = document.querySelectorAll('.test-item');
    const tests = Array.from(testItems).map(item => {
        return {
            name: item.querySelector('.test-name').value,
            type: item.querySelector('.test-type').value,
            duration_minutes: parseInt(item.querySelector('.test-duration').value),
            min_score_required: parseInt(item.querySelector('.test-min-score').value)
        };
    });
    
    const evaluationData = {
        candidate_id: parseInt(candidateId),
        vacancy_id: parseInt(vacancyId),
        tests: tests
    };
    
    fetch('/evaluations/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(evaluationData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al asignar la evaluación');
        }
        return response.json();
    })
    .then(data => {
        showAlert('success', 'Evaluación asignada exitosamente');
        // Cerrar el modal
        const modalElement = document.getElementById('dynamicModal');
        const modal = bootstrap.Modal.getInstance(modalElement);
        modal.hide();
    })
    .catch(error => {
        showAlert('danger', error.message);
    });
}

// Formulario para registrar resultado de prueba
function createTestResultForm() { 
    return `
        <form id="testResultForm" class="needs-validation" novalidate>
            <div class="mb-3">
                <label for="evaluationId" class="form-label">ID de Evaluación *</label>
                <input type="number" class="form-control" id="evaluationId" required>
                <div class="invalid-feedback">
                    Por favor ingrese un ID de evaluación válido.
                </div>
            </div>
            <div class="mb-3">
                <label for="testName" class="form-label">Nombre de la Prueba *</label>
                <input type="text" class="form-control" id="testName" required>
                <div class="invalid-feedback">
                    Por favor ingrese el nombre de la prueba.
                </div>
            </div>
            <div class="mb-3">
                <label for="testScore" class="form-label">Puntuación (0-100) *</label>
                <input type="number" class="form-control" id="testScore" min="0" max="100" required>
                <div class="invalid-feedback">
                    Por favor ingrese una puntuación válida (0-100).
                </div>
            </div>
            <div class="mb-3">
                <label for="testComments" class="form-label">Comentarios</label>
                <textarea class="form-control" id="testComments" rows="3"></textarea>
            </div>
            <button type="submit" class="btn btn-warning">Registrar Resultado</button>
        </form>
    `;
}

// Función para registrar resultado de prueba
function submitTestResult() {
    const evaluationId = document.getElementById('evaluationId').value;
    const testName = document.getElementById('testName').value;
    const testScore = document.getElementById('testScore').value;
    const testComments = document.getElementById('testComments').value;
    
    const resultData = {
        evaluation_id: parseInt(evaluationId),
        test_name: testName,
        score: parseInt(testScore),
        comments: testComments
    };
    
    fetch('/evaluations/results', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(resultData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al registrar el resultado');
        }
        return response.json();
    })
    .then(data => {
        showAlert('success', 'Resultado registrado exitosamente');
        // Cerrar el modal
        const modalElement = document.getElementById('dynamicModal');
        const modal = bootstrap.Modal.getInstance(modalElement);
        modal.hide();
    })
    .catch(error => {
        showAlert('danger', error.message);
    });
}

// Formulario para descargar reportes
function createReportDownloadForm() { 
    return `
        <form id="reportDownloadForm" class="needs-validation" novalidate>
            <div class="mb-3">
                <label for="reportCandidateId" class="form-label">ID de Candidato *</label>
                <input type="number" class="form-control" id="reportCandidateId" required>
                <div class="invalid-feedback">
                    Por favor ingrese un ID de candidato válido.
                </div>
            </div>
            <div class="mb-3">
                <label class="form-label">Formato de Reporte *</label>
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="reportFormat" value="excel" id="formatExcel" checked>
                    <label class="form-check-label" for="formatExcel">Excel</label>
                </div>
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="reportFormat" value="pdf" id="formatPdf">
                    <label class="form-check-label" for="formatPdf">PDF</label>
                </div>
            </div>
            <button type="submit" class="btn btn-warning">Descargar Reporte</button>
        </form>
    `;
}

// Función para descargar reporte
function submitReportDownload() {
    const candidateId = document.getElementById('reportCandidateId').value;
    const format = document.querySelector('input[name="reportFormat"]:checked').value;
    
    // Construir URL para descargar el reporte
    const downloadUrl = `/reports/candidate/${candidateId}?format=${format}`;
    
    // Abrir en una nueva ventana para descargar
    window.open(downloadUrl, '_blank');
    
    // Cerrar el modal
    const modalElement = document.getElementById('dynamicModal');
    const modal = bootstrap.Modal.getInstance(modalElement);
    modal.hide();
}

// Formulario para programar entrevista
function createInterviewForm() { 
    return `
        <form id="interviewForm" class="needs-validation" novalidate>
            <div class="mb-3">
                <label for="intCandidateId" class="form-label">ID de Candidato *</label>
                <input type="number" class="form-control" id="intCandidateId" required>
                <div class="invalid-feedback">
                    Por favor ingrese un ID de candidato válido.
                </div>
            </div>
            <div class="mb-3">
                <label for="interviewerId" class="form-label">ID de Entrevistador *</label>
                <input type="number" class="form-control" id="interviewerId" required>
                <div class="invalid-feedback">
                    Por favor ingrese un ID de entrevistador válido.
                </div>
            </div>
            <div class="mb-3">
                <label for="intVacancyId" class="form-label">ID de Vacante *</label>
                <input type="number" class="form-control" id="intVacancyId" required>
                <div class="invalid-feedback">
                    Por favor ingrese un ID de vacante válido.
                </div>
            </div>
            <div class="mb-3">
                <label for="interviewType" class="form-label">Tipo de Entrevista *</label>
                <select class="form-select" id="interviewType" required>
                    <option value="">Seleccione...</option>
                    <option value="TECHNICAL">Técnica</option>
                    <option value="HR">Recursos Humanos</option>
                    <option value="CULTURAL">Cultural</option>
                </select>
                <div class="invalid-feedback">
                    Por favor seleccione un tipo de entrevista.
                </div>
            </div>
            <div class="mb-3">
                <label for="scheduledTime" class="form-label">Fecha y Hora *</label>
                <input type="datetime-local" class="form-control" id="scheduledTime" required>
                <div class="invalid-feedback">
                    Por favor seleccione fecha y hora.
                </div>
            </div>
            <div class="mb-3">
                <label for="durationMinutes" class="form-label">Duración (minutos) *</label>
                <input type="number" class="form-control" id="durationMinutes" min="15" required>
                <div class="invalid-feedback">
                    Por favor ingrese la duración en minutos.
                </div>
            </div>
            <div class="mb-3">
                <label for="location" class="form-label">Ubicación *</label>
                <input type="text" class="form-control" id="location" placeholder="Sala de reuniones, Zoom, etc." required>
                <div class="invalid-feedback">
                    Por favor ingrese la ubicación.
                </div>
            </div>
            <button type="submit" class="btn btn-danger">Programar Entrevista</button>
        </form>
    `;
}

// Función para programar entrevista
function submitInterview() {
    const candidateId = document.getElementById('intCandidateId').value;
    const interviewerId = document.getElementById('interviewerId').value;
    const vacancyId = document.getElementById('intVacancyId').value;
    const interviewType = document.getElementById('interviewType').value;
    const scheduledTime = document.getElementById('scheduledTime').value;
    const durationMinutes = document.getElementById('durationMinutes').value;
    const location = document.getElementById('location').value;
    
    const interviewData = {
        candidate_id: parseInt(candidateId),
        interviewer_id: parseInt(interviewerId),
        vacancy_id: parseInt(vacancyId),
        interview_type: interviewType,
        scheduled_time: scheduledTime,
        duration_minutes: parseInt(durationMinutes),
        location: location
    };
    
    fetch('/interviews/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(interviewData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al programar la entrevista');
        }
        return response.json();
    })
    .then(data => {
        showAlert('success', 'Entrevista programada exitosamente');
        // Cerrar el modal
        const modalElement = document.getElementById('dynamicModal');
        const modal = bootstrap.Modal.getInstance(modalElement);
        modal.hide();
    })
    .catch(error => {
        showAlert('danger', error.message);
    });
}

// Formulario para registrar feedback de entrevista
function createFeedbackForm() { 
    return `
        <form id="feedbackForm" class="needs-validation" novalidate>
            <div class="mb-3">
                <label for="interviewId" class="form-label">ID de Entrevista *</label>
                <input type="number" class="form-control" id="interviewId" required>
                <div class="invalid-feedback">
                    Por favor ingrese un ID de entrevista válido.
                </div>
            </div>
            <div class="mb-3">
                <label for="strengths" class="form-label">Fortalezas *</label>
                <textarea class="form-control" id="strengths" rows="3" required placeholder="Ingrese cada fortaleza en una línea"></textarea>
                <div class="invalid-feedback">
                    Por favor ingrese al menos una fortaleza.
                </div>
            </div>
            <div class="mb-3">
                <label for="weaknesses" class="form-label">Áreas de Mejora *</label>
                <textarea class="form-control" id="weaknesses" rows="3" required placeholder="Ingrese cada área de mejora en una línea"></textarea>
                <div class="invalid-feedback">
                    Por favor ingrese al menos un área de mejora.
                </div>
            </div>
            <div class="mb-3">
                <label for="technicalScore" class="form-label">Puntuación Técnica (1-10) *</label>
                <input type="number" class="form-control" id="technicalScore" min="1" max="10" required>
                <div class="invalid-feedback">
                    Por favor ingrese una puntuación entre 1 y 10.
                </div>
            </div>
            <div class="mb-3">
                <label for="communicationScore" class="form-label">Puntuación de Comunicación (1-10) *</label>
                <input type="number" class="form-control" id="communicationScore" min="1" max="10" required>
                <div class="invalid-feedback">
                    Por favor ingrese una puntuación entre 1 y 10.
                </div>
            </div>
            <div class="mb-3">
                <label for="cultureFitScore" class="form-label">Puntuación de Ajuste Cultural (1-10) *</label>
                <input type="number" class="form-control" id="cultureFitScore" min="1" max="10" required>
                <div class="invalid-feedback">
                    Por favor ingrese una puntuación entre 1 y 10.
                </div>
            </div>
            <div class="mb-3">
                <label for="recommendation" class="form-label">Recomendación *</label>
                <select class="form-select" id="recommendation" required>
                    <option value="">Seleccione...</option>
                    <option value="HIRE">Contratar</option>
                    <option value="CONSIDER">Considerar</option>
                    <option value="REJECT">Rechazar</option>
                </select>
                <div class="invalid-feedback">
                    Por favor seleccione una recomendación.
                </div>
            </div>
            <div class="mb-3">
                <label for="feedbackNotes" class="form-label">Notas Adicionales</label>
                <textarea class="form-control" id="feedbackNotes" rows="3"></textarea>
            </div>
            <button type="submit" class="btn btn-danger">Registrar Feedback</button>
        </form>
    `;
}

// Función para registrar feedback de entrevista
function submitFeedback() {
    const interviewId = document.getElementById('interviewId').value;
    const strengths = document.getElementById('strengths').value.split('\n').filter(item => item.trim() !== '');
    const weaknesses = document.getElementById('weaknesses').value.split('\n').filter(item => item.trim() !== '');
    const technicalScore = document.getElementById('technicalScore').value;
    const communicationScore = document.getElementById('communicationScore').value;
    const cultureFitScore = document.getElementById('cultureFitScore').value;
    const recommendation = document.getElementById('recommendation').value;
    const feedbackNotes = document.getElementById('feedbackNotes').value;
    
    const feedbackData = {
        interview_id: parseInt(interviewId),
        strengths: strengths,
        weaknesses: weaknesses,
        technical_score: parseInt(technicalScore),
        communication_score: parseInt(communicationScore),
        culture_fit_score: parseInt(cultureFitScore),
        recommendation: recommendation,
        notes: feedbackNotes
    };
    
    fetch('/interviews/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(feedbackData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al registrar el feedback');
        }
        return response.json();
    })
    .then(data => {
        showAlert('success', 'Feedback registrado exitosamente');
        // Cerrar el modal
        const modalElement = document.getElementById('dynamicModal');
        const modal = bootstrap.Modal.getInstance(modalElement);
        modal.hide();
    })
    .catch(error => {
        showAlert('danger', error.message);
    });
}

// Formulario para generar reporte final
function createFinalReportForm() { 
    return `
        <form id="finalReportForm" class="needs-validation" novalidate>
            <div class="mb-3">
                <label for="selectionId" class="form-label">ID del Proceso de Selección *</label>
                <input type="number" class="form-control" id="selectionId" required>
                <div class="invalid-feedback">
                    Por favor ingrese un ID de proceso de selección válido.
                </div>
            </div>
            <div class="card mb-3">
                <div class="card-header bg-light">Evaluación Técnica</div>
                <div class="card-body">
                    <div class="mb-3">
                        <label for="technicalEvalScore" class="form-label">Puntuación (0-100) *</label>
                        <input type="number" class="form-control" id="technicalEvalScore" min="0" max="100" required>
                        <div class="invalid-feedback">
                            Por favor ingrese una puntuación válida.
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="technicalEvalFeedback" class="form-label">Retroalimentación *</label>
                        <textarea class="form-control" id="technicalEvalFeedback" rows="3" required></textarea>
                        <div class="invalid-feedback">
                            Por favor ingrese la retroalimentación.
                        </div>
                    </div>
                </div>
            </div>
            <div class="card mb-3">
                <div class="card-header bg-light">Evaluación de RRHH</div>
                <div class="card-body">
                    <div class="mb-3">
                        <label for="hrEvalScore" class="form-label">Puntuación (0-100) *</label>
                        <input type="number" class="form-control" id="hrEvalScore" min="0" max="100" required>
                        <div class="invalid-feedback">
                            Por favor ingrese una puntuación válida.
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="hrEvalFeedback" class="form-label">Retroalimentación *</label>
                        <textarea class="form-control" id="hrEvalFeedback" rows="3" required></textarea>
                        <div class="invalid-feedback">
                            Por favor ingrese la retroalimentación.
                        </div>
                    </div>
                </div>
            </div>
            <div class="mb-3">
                <label for="additionalNotes" class="form-label">Notas Adicionales</label>
                <textarea class="form-control" id="additionalNotes" rows="3"></textarea>
            </div>
            <button type="submit" class="btn btn-dark">Generar Reporte Final</button>
        </form>
    `;
}

// Función para generar reporte final
function submitFinalReport() {
    const selectionId = document.getElementById('selectionId').value;
    const technicalEvalScore = document.getElementById('technicalEvalScore').value;
    const technicalEvalFeedback = document.getElementById('technicalEvalFeedback').value;
    const hrEvalScore = document.getElementById('hrEvalScore').value;
    const hrEvalFeedback = document.getElementById('hrEvalFeedback').value;
    const additionalNotes = document.getElementById('additionalNotes').value;
    
    const reportData = {
        selection_id: parseInt(selectionId),
        technical_evaluation: {
            score: parseInt(technicalEvalScore),
            feedback: technicalEvalFeedback
        },
        hr_evaluation: {
            score: parseInt(hrEvalScore),
            feedback: hrEvalFeedback
        },
        additional_notes: additionalNotes
    };
    
    fetch('/selections/reports', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(reportData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al generar el reporte final');
        }
        return response.json();
    })
    .then(data => {
        showAlert('success', 'Reporte final generado exitosamente');
        // Cerrar el modal
        const modalElement = document.getElementById('dynamicModal');
        const modal = bootstrap.Modal.getInstance(modalElement);
        modal.hide();
    })
    .catch(error => {
        showAlert('danger', error.message);
    });
}

// Formulario para tomar decisión de contratación
function createDecisionForm() { 
    return `
        <form id="decisionForm" class="needs-validation" novalidate>
            <div class="mb-3">
                <label for="decisionSelectionId" class="form-label">ID del Proceso de Selección *</label>
                <input type="number" class="form-control" id="decisionSelectionId" required>
                <div class="invalid-feedback">
                    Por favor ingrese un ID de proceso de selección válido.
                </div>
            </div>
            <div class="mb-3">
                <label for="hiringDecision" class="form-label">Decisión *</label>
                <select class="form-select" id="hiringDecision" required>
                    <option value="">Seleccione...</option>
                    <option value="HIRE">Contratar</option>
                    <option value="REJECT">Rechazar</option>
                </select>
                <div class="invalid-feedback">
                    Por favor seleccione una decisión.
                </div>
            </div>
            <div class="mb-3">
                <label for="decisionReason" class="form-label">Motivo</label>
                <textarea class="form-control" id="decisionReason" rows="3"></textarea>
            </div>
            <button type="submit" class="btn btn-dark">Confirmar Decisión</button>
        </form>
    `;
}

// Función para tomar decisión de contratación
function submitDecision() {
    const selectionId = document.getElementById('decisionSelectionId').value;
    const hiringDecision = document.getElementById('hiringDecision').value;
    const decisionReason = document.getElementById('decisionReason').value;
    
    const decisionData = {
        selection_id: parseInt(selectionId),
        decision: hiringDecision,
        reason: decisionReason
    };
    
    fetch('/selections/decisions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(decisionData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al registrar la decisión');
        }
        return response.json();
    })
    .then(data => {
        showAlert('success', 'Decisión registrada exitosamente');
        // Cerrar el modal
        const modalElement = document.getElementById('dynamicModal');
        const modal = bootstrap.Modal.getInstance(modalElement);
        modal.hide();
    })
    .catch(error => {
        showAlert('danger', error.message);
    });
}

// Función para ver detalles de una requisición
function viewRequisition(id) { 
    // Implementar la visualización de requisición
    showModal('Detalles de Requisición', '<p>Cargando detalles de la requisición ' + id + '...</p>');
    
    // Aquí se llamaría a la API para obtener detalles
    // Por ahora, simularemos una respuesta
    setTimeout(() => {
        const requisitionDetails = `
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Desarrollador Full Stack</h5>
                    <p class="card-text"><strong>ID:</strong> ${id}</p>
                    <p class="card-text"><strong>Estado:</strong> <span class="badge bg-success">Aprobada</span></p>
                    <p class="card-text"><strong>Fecha de Creación:</strong> 2024-03-01</p>
                    <h6>Funciones:</h6>
                    <ul>
                        <li>Desarrollo de APIs RESTful</li>
                        <li>Desarrollo de interfaces de usuario</li>
                        <li>Pruebas unitarias y de integración</li>
                    </ul>
                    <h6>Perfil Requerido:</h6>
                    <p>Desarrollador con experiencia en Python, JavaScript y bases de datos relacionales.</p>
                </div>
                <div class="card-footer">
                    <button class="btn btn-primary btn-sm" onclick="showModal('Publicar Vacante', createVacancyForm())">Publicar Vacante</button>
                </div>
            </div>
        `;
        
        updateModalContent('Detalles de Requisición', requisitionDetails);
    }, 1000);
}

// Formulario para seleccionar vacante
function selectVacancyForm(action) {
    return `
        <form id="selectVacancyForm" class="needs-validation" novalidate>
            <div class="mb-3">
                <label for="selectVacancyId" class="form-label">ID de Vacante *</label>
                <input type="number" class="form-control" id="selectVacancyId" required>
                <div class="invalid-feedback">
                    Por favor ingrese un ID de vacante válido.
                </div>
            </div>
            <button type="button" class="btn btn-primary" onclick="handleVacancySelection('${action}')">Seleccionar</button>
        </form>
    `;
}

// Función para manejar la selección de vacante
function handleVacancySelection(action) {
    const vacancyId = document.getElementById('selectVacancyId').value;
    
    if (!vacancyId || isNaN(vacancyId) || vacancyId <= 0) {
        showAlert('danger', 'Por favor ingrese un ID de vacante válido');
        return;
    }
    
    switch(action) {
        case 'listarCandidatos':
            fetchCandidatesByVacancy(vacancyId);
            break;
        default:
            showAlert('warning', 'Acción no implementada');
    }
}

// Función para obtener candidatos por vacante
function fetchCandidatesByVacancy(vacancyId) {
    // Simulamos una llamada a la API
    showModal('Candidatos para Vacante ' + vacancyId, '<p>Cargando candidatos...</p>');
    
    setTimeout(() => {
        const candidatesTable = `
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Email</th>
                            <th>Experiencia</th>
                            <th>Estado</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>1</td>
                            <td>Juan Pérez</td>
                            <td>juan.perez@ejemplo.com</td>
                            <td>5 años</td>
                            <td><span class="badge bg-primary">Registrado</span></td>
                            <td>
                                <button class="btn btn-sm btn-outline-primary">Ver</button>
                                <button class="btn btn-sm btn-outline-warning">Evaluar</button>
                            </td>
                        </tr>
                        <tr>
                            <td>2</td>
                            <td>María Gómez</td>
                            <td>maria.gomez@ejemplo.com</td>
                            <td>3 años</td>
                            <td><span class="badge bg-info">En Evaluación</span></td>
                            <td>
                                <button class="btn btn-sm btn-outline-primary">Ver</button>
                                <button class="btn btn-sm btn-outline-danger">Entrevista</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        `;
        
        updateModalContent('Candidatos para Vacante ' + vacancyId, candidatesTable);
    }, 1000);
}

// Agregar manejador de eventos para el botón de agregar prueba
document.addEventListener('click', function(event) {
    if (event.target && event.target.id === 'addTestBtn') {
        const testsList = document.getElementById('testsList');
        if (testsList) {
            const newTest = document.createElement('div');
            newTest.className = 'test-item card mb-2 p-3';
            newTest.innerHTML = `
                <div class="d-flex justify-content-end mb-2">
                    <button type="button" class="btn btn-sm btn-outline-danger remove-test">
                        <i class="bi bi-x"></i> Eliminar
                    </button>
                </div>
                <div class="mb-2">
                    <label class="form-label">Nombre de la Prueba *</label>
                    <input type="text" class="form-control test-name" required>
                </div>
                <div class="mb-2">
                    <label class="form-label">Tipo de Prueba *</label>
                    <select class="form-select test-type" required>
                        <option value="">Seleccione...</option>
                        <option value="TECHNICAL">Técnica</option>
                        <option value="LANGUAGE">Idioma</option>
                        <option value="PSYCHOMETRIC">Psicométrica</option>
                    </select>
                </div>
                <div class="mb-2">
                    <label class="form-label">Duración (minutos) *</label>
                    <input type="number" class="form-control test-duration" min="1" required>
                </div>
                <div class="mb-2">
                    <label class="form-label">Puntuación Mínima Requerida *</label>
                    <input type="number" class="form-control test-min-score" min="0" max="100" required>
                </div>
            `;
            testsList.appendChild(newTest);
        }
    }
    
    // Manejar eliminación de prueba
    if (event.target && event.target.classList.contains('remove-test')) {
        const testItem = event.target.closest('.test-item');
        if (testItem && testItem.parentNode) {
            testItem.parentNode.removeChild(testItem);
        }
    }
});

// Agregar manejadores de eventos para los formularios mediante delegación de eventos
document.addEventListener('submit', function(event) {
    if (event.target && event.target.id) {
        event.preventDefault();
        
        // Validar el formulario
        if (!validateForm(event.target)) {
            return;
        }
        
        // Manejar diferentes tipos de formularios
        switch (event.target.id) {
            case 'requisitionForm':
                submitRequisition();
                break;
            case 'vacancyForm':
                submitVacancy();
                break;
            case 'candidateForm':
                submitCandidate();
                break;
            case 'filterCandidatesForm':
                submitCandidateFilter();
                break;
            case 'evaluationForm':
                submitEvaluation();
                break;
            case 'testResultForm':
                submitTestResult();
                break;
            case 'reportDownloadForm':
                submitReportDownload();
                break;
            case 'interviewForm':
                submitInterview();
                break;
            case 'feedbackForm':
                submitFeedback();
                break;
            case 'finalReportForm':
                submitFinalReport();
                break;
            case 'decisionForm':
                submitDecision();
                break;
        }
    }
});

// Función para validar formulario
function validateForm(form) {
    if (!form.checkValidity()) {
        // Mostrar los mensajes de validación
        form.classList.add('was-validated');
        return false;
    }
    return true;
}

// Inicializar validación de formularios de Bootstrap
document.addEventListener('DOMContentLoaded', function() {
    // Validación de formularios
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});

// Ver detalles de un candidato
function viewCandidate(id) {
    showModal('Detalles del Candidato', '<p>Cargando información del candidato ' + id + '...</p>');
    
    // Aquí se llamaría a la API para obtener detalles
    // Por ahora, simularemos una respuesta
    setTimeout(() => {
        const candidateDetails = `
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Juan Pérez</h5>
                    <p class="card-text"><strong>ID:</strong> ${id}</p>
                    <p class="card-text"><strong>Email:</strong> juan.perez@ejemplo.com</p>
                    <p class="card-text"><strong>Experiencia:</strong> 5 años</p>
                    <p class="card-text">
                        <strong>CV:</strong> 
                        <a href="#" target="_blank">Ver CV</a>
                    </p>
                    <h6>Habilidades:</h6>
                    <div class="mb-3">
                        <span class="badge bg-primary me-1">Python</span>
                        <span class="badge bg-primary me-1">JavaScript</span>
                        <span class="badge bg-primary me-1">React</span>
                        <span class="badge bg-primary me-1">SQL</span>
                    </div>
                    <h6>Estado Actual:</h6>
                    <p><span class="badge bg-info">En Evaluación</span></p>
                </div>
                <div class="card-footer">
                    <button class="btn btn-warning btn-sm" onclick="showModal('Asignar Evaluación', createEvaluationForm())">Asignar Evaluación</button>
                    <button class="btn btn-danger btn-sm" onclick="showModal('Programar Entrevista', createInterviewForm())">Programar Entrevista</button>
                </div>
            </div>
        `;
        
        updateModalContent('Detalles del Candidato', candidateDetails);
    }, 1000);
}

// Función para listar vacantes
function fetchAndDisplayVacancies() {
    fetch('/vacancies/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener las vacantes');
            }
            return response.json();
        })
        .then(data => {
            let content = `
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Cargo</th>
                                <th>Plataformas</th>
                                <th>Estado</th>
                                <th>Candidatos</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            if (data.length === 0) {
                content += `
                    <tr>
                        <td colspan="6" class="text-center">No hay vacantes disponibles</td>
                    </tr>
                `;
            } else {
                data.forEach(vacancy => {
                    content += `
                        <tr>
                            <td>${vacancy.id}</td>
                            <td>${vacancy.position_name || 'Sin especificar'}</td>
                            <td>${getPlatformsBadges(vacancy.platforms)}</td>
                            <td><span class="badge bg-${getVacancyStatusColor(vacancy.status)}">${getVacancyStatusLabel(vacancy.status)}</span></td>
                            <td>${vacancy.candidates_count || 0}</td>
                            <td>
                                <button class="btn btn-sm btn-info" onclick="viewVacancy(${vacancy.id})">Ver</button>
                            </td>
                        </tr>
                    `;
                });
            }
            
            content += `
                        </tbody>
                    </table>
                </div>
            `;
            
            showModal('Vacantes Publicadas', content);
        })
        .catch(error => {
            showAlert('danger', error.message);
        });
}

// Obtener badges para las plataformas
function getPlatformsBadges(platforms) {
    if (!platforms || !Array.isArray(platforms)) return '';
    
    const platformsMap = {
        'INTERNAL': '<span class="badge bg-secondary me-1">Interna</span>',
        'LINKEDIN': '<span class="badge bg-primary me-1">LinkedIn</span>',
        'INDEED': '<span class="badge bg-success me-1">Indeed</span>',
        'JOBSITE': '<span class="badge bg-info me-1">Jobsite</span>'
    };
    
    return platforms.map(p => platformsMap[p] || '').join('');
}

// Obtener color para estado de vacante
function getVacancyStatusColor(status) {
    const statusColors = {
        'OPEN': 'success',
        'PAUSED': 'warning',
        'CLOSED': 'danger'
    };
    return statusColors[status] || 'secondary';
}

// Obtener etiqueta para estado de vacante
function getVacancyStatusLabel(status) {
    const statusLabels = {
        'OPEN': 'Abierta',
        'PAUSED': 'Pausada',
        'CLOSED': 'Cerrada'
    };
    return statusLabels[status] || status;
}

// Ver detalles de una vacante
function viewVacancy(id) {
    showModal('Detalles de la Vacante', '<p>Cargando información de la vacante ' + id + '...</p>');
    
    // Aquí se llamaría a la API para obtener detalles
    // Por ahora, simularemos una respuesta
    setTimeout(() => {
        const vacancyDetails = `
            <div class="card mb-3">
                <div class="card-body">
                    <h5 class="card-title">Desarrollador Full Stack</h5>
                    <p class="card-text"><strong>ID:</strong> ${id}</p>
                    <p class="card-text"><strong>Estado:</strong> <span class="badge bg-success">Abierta</span></p>
                    <p class="card-text"><strong>Fecha de Publicación:</strong> 2024-03-01</p>
                    <h6>Plataformas:</h6>
                    <div>
                        <span class="badge bg-primary me-1">LinkedIn</span>
                        <span class="badge bg-success me-1">Indeed</span>
                    </div>
                </div>
                <div class="card-footer">
                    <button class="btn btn-success btn-sm" onclick="showModal('Registrar Candidato', createCandidateForm())">Registrar Candidato</button>
                    <button class="btn btn-secondary btn-sm" onclick="showModal('Filtrar Candidatos', createCandidateFilterForm())">Filtrar Candidatos</button>
                </div>
            </div>
            <h5>Candidatos (5):</h5>
            <div class="table-responsive">
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Estado</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>1</td>
                            <td>Juan Pérez</td>
                            <td><span class="badge bg-primary">Registrado</span></td>
                            <td><button class="btn btn-sm btn-outline-primary" onclick="viewCandidate(1)">Ver</button></td>
                        </tr>
                        <tr>
                            <td>2</td>
                            <td>María Gómez</td>
                            <td><span class="badge bg-info">En Evaluación</span></td>
                            <td><button class="btn btn-sm btn-outline-primary" onclick="viewCandidate(2)">Ver</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        `;
        
        updateModalContent('Detalles de la Vacante', vacancyDetails);
    }, 1000);
} 
