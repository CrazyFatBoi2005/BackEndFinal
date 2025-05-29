document.addEventListener('DOMContentLoaded', function() {
    // Функция для показа уведомлений
    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.innerHTML = `
            <i class="fas fa-${type === 'danger' ? 'exclamation-circle' : 'check-circle'}"></i>
            ${message}
        `;

        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);

        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }

    // Обработчик формы генерации изображений
    // const generateForm = document.getElementById('generateForm');
    // if (generateForm) {
    //     generateForm.addEventListener('submit', async function(e) {
    //         e.preventDefault();
    //         const prompt = document.getElementById('prompt').value;
    //         const button = this.querySelector('button[type="submit"]');
    //         const originalButtonText = button.innerHTML;
    //
    //         button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Генерация...';
    //         button.disabled = true;
    //
    //         try {
    //             const response = await fetch('/generate', {
    //                 method: 'POST',
    //                 headers: {
    //                     'Content-Type': 'application/json',
    //                     'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
    //                 },
    //                 body: JSON.stringify({ prompt })
    //             });
    //
    //             const data = await response.json();
    //             if (data.image_url) {
    //                 document.getElementById('result').innerHTML = `
    //                     <div class="alert alert-success">
    //                         <i class="fas fa-check-circle"></i> Изображение успешно сгенерировано!
    //                     </div>
    //                     <img src="${data.image_url}" class="generated-image" alt="Generated image">
    //                     <div class="mt-3">
    //                         <button class="btn btn-download" onclick="downloadImage('${data.image_url}')">
    //                             <i class="fas fa-download"></i> Скачать
    //                         </button>
    //                     </div>
    //                 `;
    //             } else if (data.error) {
    //                 showAlert(data.error, 'danger');
    //             }
    //         } catch (error) {
    //             console.error('Error:', error);
    //             showAlert('Произошла ошибка при генерации изображения', 'danger');
    //         } finally {
    //             button.innerHTML = originalButtonText;
    //             button.disabled = false;
    //         }
    //     });
    // }

    // Проверка сложности пароля
    function checkPasswordStrength(password) {
        const strengthBar = document.getElementById('passwordStrength');
        if (!strengthBar) return;

        let strength = 0;
        if (password.length >= 8) strength += 1;
        if (password.match(/[a-z]+/)) strength += 1;
        if (password.match(/[A-Z]+/)) strength += 1;
        if (password.match(/[0-9]+/)) strength += 1;
        if (password.match(/[$@#&!]+/)) strength += 1;

        const width = (strength / 5) * 100;
        strengthBar.style.width = `${width}%`;

        if (strength < 2) {
            strengthBar.style.background = '#dc3545';
        } else if (strength < 4) {
            strengthBar.style.background = '#fd7e14';
        } else {
            strengthBar.style.background = '#28a745';
        }
    }

    // Валидация формы регистрации
    const registerForm = document.querySelector('form[data-action="register"]');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const password = document.getElementById('password');
            const confirmPassword = document.getElementById('confirm_password');

            if (password && confirmPassword && password.value !== confirmPassword.value) {
                e.preventDefault();
                showAlert('Пароли не совпадают', 'danger');
                return;
            }

            if (password && password.value.length < 8) {
                e.preventDefault();
                showAlert('Пароль должен содержать не менее 8 символов', 'danger');
                return;
            }
        });

        // Динамическая проверка пароля при вводе
        const passwordInput = document.getElementById('password');
        if (passwordInput) {
            passwordInput.addEventListener('input', function() {
                checkPasswordStrength(this.value);
            });
        }
    }

    // Функция для скачивания изображения (глобальная)
    window.downloadImage = function(url) {
        const link = document.createElement('a');
        link.href = url;
        link.download = `generated-image-${new Date().getTime()}.png`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    // Анимация для всех форм
    const forms = document.querySelectorAll('.form-container');
    forms.forEach((form, index) => {
        form.style.animationDelay = `${index * 0.1}s`;
    });
});