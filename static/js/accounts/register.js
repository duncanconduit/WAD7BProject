document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.getElementById('register_form');
    const errorMessageContainer = document.getElementById('error-message');
    const errorMessageText = errorMessageContainer.querySelector('p');

    const firstNameInput = document.getElementById('first-name');
    const lastNameInput = document.getElementById('last-name');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    const organisationInput = document.getElementById('organisation');
    const submitButton = registerForm.querySelector('button[type="submit"]');

    const emailErrorLabel = document.getElementById('email-error-label');
    const passwordErrorLabel = document.getElementById('password-error-label');
    const confirmPasswordErrorLabel = document.getElementById('confirm-password-error-label');
    const organisationErrorLabel = document.getElementById('organisation-error-label');

    function isValidEmail(email) {
        const regEx = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regEx.test(email);
    }

    function isValidPassword(password) {
        if (password.length < 8) return false;
        const hasLetter = /[A-Za-z]/.test(password);
        const hasNumber = /\d/.test(password);
        const hasSpecialChar = /[^A-Za-z0-9]/.test(password);
    
        return hasLetter && hasNumber && hasSpecialChar;
    }

    function toggleSubmitButton() {
        const allValid =
            firstNameInput.value.trim() !== '' &&
            lastNameInput.value.trim() !== '' &&
            isValidEmail(emailInput.value.trim()) &&
            isValidPassword(passwordInput.value.trim()) &&
            passwordInput.value.trim() === confirmPasswordInput.value.trim() &&
            organisationInput.value.trim() !== '';

        submitButton.disabled = !allValid;
    }

    // Email validation
    emailInput.addEventListener('blur', function () {
        const val = emailInput.value.trim();
        if (val !== '' && !isValidEmail(val)) {
            emailErrorLabel.textContent = "Please enter a valid email address.";
            emailErrorLabel.classList.remove('hidden');
            emailInput.classList.add('error');
        }
        toggleSubmitButton();
    });

    emailInput.addEventListener('focus', function () {
        emailErrorLabel.classList.add('hidden');
        emailInput.classList.remove('error');
    });

    // Password validations
    passwordInput.addEventListener('blur', function () {
        const pwd = passwordInput.value.trim();
        if (pwd !== '' && !isValidPassword(pwd)) {
            passwordErrorLabel.textContent = "Password must be 8+ characters with one letter and number.";
            passwordErrorLabel.classList.remove('hidden');
            passwordInput.classList.add('error');
        }
        toggleSubmitButton();
    });

    passwordInput.addEventListener('focus', function () {
        passwordErrorLabel.classList.add('hidden');
        passwordInput.classList.remove('error');
    });

    // Confirm Password
    confirmPasswordInput.addEventListener('blur', function () {
        const pwd = passwordInput.value.trim();
        const confirm = confirmPasswordInput.value.trim();
        if (confirm !== '' && confirm !== pwd) {
            confirmPasswordErrorLabel.textContent = "Passwords do not match.";
            confirmPasswordErrorLabel.classList.remove('hidden');
            confirmPasswordInput.classList.add('error');
        }
        toggleSubmitButton();
    });

    confirmPasswordInput.addEventListener('focus', function () {
        confirmPasswordErrorLabel.classList.remove('hidden');
        confirmPasswordInput.classList.remove('error');
    });

    organisationInput.addEventListener('change', function() {
        toggleSubmitButton();
    });

    // ========== FORM SUBMIT ==========
    registerForm.addEventListener('submit', function (e) {
        e.preventDefault();

        toggleSubmitButton();
        if (submitButton.disabled) {
            return;
        }

        const formData = new FormData(registerForm);

        fetch(registerForm.action, {
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

    submitButton.disabled = true;
});

function toggleDropdown() {
    const dropdown = document.getElementById('dropdown-menu');
    const arrowIcon = document.getElementById("arrow-icon");
    dropdown.classList.toggle('hidden');
    arrowIcon.classList.toggle("rotate-180");
}

function selectOrganisation(orgId, orgName) {
    document.getElementById('organisation').value = orgId;
    document.getElementById('selected-option').textContent = orgName;
    toggleDropdown();
    document.getElementById('organisation').dispatchEvent(new Event('change'));
}

window.addEventListener('click', function(e) {
    const dropdown = document.getElementById('dropdown-menu');
    const button = document.getElementById('menu-button');
    if (!button.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.classList.add('hidden');
      document.getElementById('arrow-icon').classList.remove('rotate-180');
    }
});