document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('login_form');
    const errorMessageContainer = document.getElementById('error-message');
    const errorMessageText = errorMessageContainer.querySelector('p');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const submitButton = loginForm.querySelector('button[type="submit"]');
    const emailErrorLabel = document.getElementById('error-label');

    function isValidEmail(email) {
        const regEx = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regEx.test(email);
    }

    function validateInputs() {
        const emailValue = emailInput.value.trim();
        const passwordValue = passwordInput.value.trim();

        errorMessageContainer.classList.add('hidden');
        errorMessageText.textContent = '';

        let isFormValid = true;

        if (emailValue === '' || passwordValue === '') {
            isFormValid = false;
        }

        if (emailValue && !isValidEmail(emailValue)) {
            isFormValid = false;
        }
        submitButton.disabled = !isFormValid;
    }

    submitButton.disabled = true;

    emailInput.addEventListener('input', validateInputs);
    passwordInput.addEventListener('input', validateInputs);

    loginForm.addEventListener('submit', function (e) {
        e.preventDefault();
        validateInputs();

        if (submitButton.disabled) {
            return;
        }

        errorMessageContainer.classList.add('hidden');
        const formData = new FormData(loginForm);

        fetch(loginForm.action, {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = data.redirect;
                } else {
                    errorMessageText.textContent = data.message;
                    errorMessageContainer.classList.remove('hidden');
                }
            })
            .catch(() => {
                errorMessageText.textContent = 'Network error occurred. Please try again.';
                errorMessageContainer.classList.remove('hidden');
            });
    });
});