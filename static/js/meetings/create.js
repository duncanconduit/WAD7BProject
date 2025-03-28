document.addEventListener('DOMContentLoaded', function () {
    const meetingForm = document.getElementById('meeting_form');
    const errorMessageContainer = document.getElementById('error-message');
    const errorMessageText = errorMessageContainer.querySelector('p');
    const descriptionInput = document.getElementById('description');
    const startTimeInput = document.getElementById('start_time');
    const endTimeInput = document.getElementById('end_time');
    const placeInput = document.getElementById('place');
    const submitButton = meetingForm.querySelector('button[type="submit"]');
    const placeContainer = document.getElementById('place-container');
    const isVirtualInput = document.getElementById('is_virtual');
    const inPersonRadio = document.getElementById('in_person');
    const virtualRadio = document.getElementById('virtual');
    const addInviteButton = document.getElementById('add-invite');
    const invitesContainer = document.getElementById('invites-container');
    const inviteError = document.getElementById('invite-error');

    // Disable submit button by default
    submitButton.disabled = true;

    // Track if a field has been interacted with
    const touchedFields = {
        description: false,
        start_time: false,
        end_time: false,
        place: false
    };

    // Use a single global markAsTouched function
    window.markAsTouched = function(fieldName) {
        touchedFields[fieldName] = true;
        console.log(`Field "${fieldName}" marked as touched.`, touchedFields);
        validateForm(); // Immediately validate after marking as touched
    };

    // Handle meeting type selection change
    function handleMeetingTypeChange() {
        const isVirtual = virtualRadio.checked;
        isVirtualInput.value = isVirtual ? 'True' : 'False';
        
        if (isVirtual) {
            placeContainer.classList.add('hidden');
            placeInput.value = '';
            placeInput.required = false;
            const placeErrorLabel = document.getElementById('place-error-label');
            if (placeErrorLabel) {
                placeErrorLabel.classList.add('hidden');
            }
            placeInput.classList.remove('error');
            touchedFields.place = false;
        } else {
            placeContainer.classList.remove('hidden');
            placeInput.required = true;
        }
        
        validateForm();
    }
    
    inPersonRadio.addEventListener('change', handleMeetingTypeChange);
    virtualRadio.addEventListener('change', handleMeetingTypeChange);
    handleMeetingTypeChange();

    function validateForm() {
        let isValid = true;
        const descriptionValue = descriptionInput.value.trim();
        const startTimeValue = startTimeInput.value;
        const endTimeValue = endTimeInput.value;
        const placeValue = placeInput.value;
        const isVirtual = virtualRadio.checked;

        console.log("Validating form:", {
            description: descriptionValue,
            startTime: startTimeValue,
            endTime: endTimeValue,
            place: placeValue,
            isVirtual: isVirtual,
            touched: { ...touchedFields }
        });

        resetErrors();

        if (!descriptionValue) {
            isValid = false;
            if (touchedFields.description) {
                showError(descriptionInput, 'description-error-label', 'Please provide a meeting description.');
            }
        }

        if (!startTimeValue) {
            isValid = false;
            if (touchedFields.start_time) {
                showError(startTimeInput, 'start-time-error-label', 'Please select a start time.');
            }
        }

        if (!endTimeValue) {
            isValid = false;
            if (touchedFields.end_time) {
                showError(endTimeInput, 'end-time-error-label', 'Please select an end time.');
            }
        }

        if (startTimeValue && endTimeValue) {
            const startDate = new Date(startTimeValue);
            const endDate = new Date(endTimeValue);
            if (endDate <= startDate) {
                isValid = false;
                if (touchedFields.end_time) {
                    showError(endTimeInput, 'end-time-error-label', 'End time must be after start time.');
                }
            }
        }

        if (!isVirtual && !placeValue) {
            isValid = false;
            if (touchedFields.place) {
                showError(placeInput, 'place-error-label', 'Please select a place for the meeting.');
            }
        }

        const inviteInputs = document.querySelectorAll('.invite-input');
        inviteInputs.forEach(input => {
            const email = input.value.trim();
            if (email && !isValidEmail(email)) {
                inviteError.textContent = 'Please enter valid email addresses.';
                inviteError.classList.remove('hidden');
                isValid = false;
            }
        });

        submitButton.disabled = !isValid;
        console.log("Form valid:", isValid);
        return isValid;
    }

    function isValidEmail(email) {
        const regEx = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regEx.test(email);
    }

    function showError(inputElement, errorLabelId, message) {
        inputElement.classList.add('error');
        const errorLabel = document.getElementById(errorLabelId);
        if (errorLabel) {
            errorLabel.textContent = message;
            errorLabel.classList.remove('hidden');
        }
    }

    function resetErrors() {
        const inputs = [descriptionInput, startTimeInput, endTimeInput];
        inputs.forEach(input => {
            input.classList.remove('error');
        });

        document.querySelectorAll('.field-error').forEach(el => {
            el.classList.add('hidden');
        });

        inviteError.classList.add('hidden');
        errorMessageContainer.classList.add('hidden');

        document.querySelectorAll('.invite-input').forEach(input => {
            input.classList.remove('error');
        });
    }

    const inputFields = [
        { el: descriptionInput, name: 'description' },
        { el: startTimeInput, name: 'start_time' },
        { el: endTimeInput, name: 'end_time' }
    ];
    
    inputFields.forEach(field => {
        if (!field.el) return;
        
        field.el.addEventListener('focus', function() {
            this.classList.remove('error');
            const fieldId = this.id;
            const errorLabel = document.getElementById(`${fieldId}-error-label`) || 
                               document.getElementById(`${fieldId.replace('_', '-')}-error-label`);
            if (errorLabel) {
                errorLabel.classList.add('hidden');
            }
        });

        field.el.addEventListener('blur', function() {
            window.markAsTouched(field.name);
        });
        
        field.el.addEventListener('input', function() {
            validateForm();
        });
    });
    
    addInviteButton.addEventListener('click', function() {
        const newInviteGroup = document.createElement('div');
        newInviteGroup.className = 'invite-input-group mb-2 flex items-center';
        
        newInviteGroup.innerHTML = `
            <input type="email" name="invitees" 
                class="invite-input flex-1 px-3 py-2 border border-inputborder rounded-md focus:outline-none focus:ring-1 focus:ring-brand-primary focus:border-brand-primary dark:border-transparent dark:bg-darktextbox dark:text-white text-sm" 
                placeholder="Enter email address">
            <button type="button" class="remove-invite ml-2 text-gray-400 hover:text-red-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 011.414 1.414L11.414 10l4.293 4.293a1 1 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
            </button>
        `;
        
        invitesContainer.appendChild(newInviteGroup);
        
        const removeButton = newInviteGroup.querySelector('.remove-invite');
        removeButton.addEventListener('click', function() {
            invitesContainer.removeChild(newInviteGroup);
            validateForm();
        });
        
        const newInput = newInviteGroup.querySelector('input');
        newInput.focus();
        
        newInput.addEventListener('input', validateForm);
        newInput.addEventListener('blur', validateForm);
    });

    resetErrors();
    validateForm();

    meetingForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        Object.keys(touchedFields).forEach(field => {
            touchedFields[field] = true;
        });
        
        if (!validateForm()) {
            return;
        }

        resetErrors();
        
        const formData = new FormData(meetingForm);
        
        fetch(meetingForm.action, {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect || '/';
            } else {
                if (data.error && data.error.includes('Invalid invitee(s) selected')) {
                    inviteError.textContent = 'Invalid invitee(s) selected.';
                    inviteError.classList.remove('hidden');
                    
                    document.querySelectorAll('.invite-input').forEach(input => {
                        input.classList.add('error');
                    });
                } else {
                    errorMessageText.textContent = data.error || 'An error occurred while creating the meeting.';
                    errorMessageContainer.classList.remove('hidden');
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            errorMessageText.textContent = 'Network error occurred. Please try again.';
            errorMessageContainer.classList.remove('hidden');
        });
    });
});

// Toggle dropdown menu
function toggleDropdown() {
    const dropdown = document.getElementById('dropdown-menu');
    const arrowIcon = document.getElementById("arrow-icon");
    dropdown.classList.toggle('hidden');
    arrowIcon.classList.toggle("rotate-180");
}

// Select a place from the dropdown and trigger validation
function selectPlace(placeId, placeName) {
    console.log("selectPlace called:", { placeId, placeName });
    if (!placeId) {
        console.warn("No valid place id provided for", placeName);
    }
    const placeInput = document.getElementById('place');
    placeInput.value = placeId;
    
    const selectedOption = document.getElementById('selected-option');
    selectedOption.textContent = placeName;
    
    toggleDropdown();
    
    placeInput.dispatchEvent(new Event('input', { bubbles: true }));
    window.markAsTouched('place');
}

// Close dropdown when clicking outside
window.addEventListener('click', function(e) {
    const dropdown = document.getElementById('dropdown-menu');
    const button = document.getElementById('menu-button');
    if (dropdown && button && !button.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.add('hidden');
        const arrowIcon = document.getElementById('arrow-icon');
        if (arrowIcon) {
            arrowIcon.classList.remove('rotate-180');
        }
    }
});