document.addEventListener("DOMContentLoaded", function() {
    const btnEliminar = document.getElementById('btnEliminarCuenta');
    if (btnEliminar) {
        btnEliminar.onclick = async function() {
            const { value: password } = await Swal.fire({
                title: 'Verificación de Identidad',
                text: 'Por motivos de seguridad, debe introducir su contraseña para continuar con el proceso.',
                input: 'password',
                inputPlaceholder: 'Contraseña',
                showCancelButton: true,
                confirmButtonColor: '#2c3e50',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Continuar',
                cancelButtonText: 'Cancelar',
                heightAuto: false
            });

            if (password) {
                const { value: confirmWord } = await Swal.fire({
                    title: 'Confirmación Final',
                    html: 'Esta acción es <strong>irreversible</strong>. Para confirmar la eliminación permanente de todos sus datos, escriba la palabra <strong>CONFIRMAR</strong> a continuación:',
                    input: 'text',
                    inputPlaceholder: 'CONFIRMAR',
                    showCancelButton: true,
                    confirmButtonColor: '#d33',
                    confirmButtonText: 'Eliminar cuenta definitivamente',
                    cancelButtonText: 'Cancelar',
                    heightAuto: false,
                    inputValidator: (value) => {
                        if (value !== 'CONFIRMAR') {
                            return 'La palabra introducida es incorrecta.';
                        }
                    }
                });

                if (confirmWord === 'CONFIRMAR') {
                    document.getElementById('inputPasswordHidden').value = password;
                    document.getElementById('formEliminarUsuario').submit();
                }
            }
        };
    }
});