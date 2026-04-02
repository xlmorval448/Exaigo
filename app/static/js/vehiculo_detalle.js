document.addEventListener("DOMContentLoaded", function() {
    const btnEliminar = document.getElementById('btnEliminarVehiculo');
    if (btnEliminar) {
        btnEliminar.onclick = function(e) {
            e.preventDefault();
            Swal.fire({
                title: '¿Eliminar vehículo?',
                text: "Al borrarlo dejarás de ser conductor activo y no podrás publicar viajes.",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#e74c3c',
                cancelButtonColor: '#95a5a6',
                confirmButtonText: '<i class="fa-solid fa-trash-can me-2"></i>Sí, eliminar',
                cancelButtonText: 'Cancelar',
                reverseButtons: true,
                customClass: {
                    confirmButton: 'rounded-pill px-4',
                    cancelButton: 'rounded-pill px-4'
                }
            }).then((result) => {
                if (result.isConfirmed) {
                    document.getElementById('formEliminar').submit();
                }
            });
        };
    }
});