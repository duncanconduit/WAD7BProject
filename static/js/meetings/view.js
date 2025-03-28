document.addEventListener('DOMContentLoaded', () => {
    try {
        updateMeetingTimes();
        initAttendeeInteractions();
        checkMeetingStatus();
    } catch (error) {
        console.error("Error during meeting view initialization:", error);
    }
});

function updateMeetingTimes() {
    const startTimeEl = document.getElementById('meeting-start-time');
    const endTimeEl = document.getElementById('meeting-end-time');
    const dateEl = document.getElementById('meeting-date');
    const durationEl = document.getElementById('meeting-duration');
    
    if (!startTimeEl || !endTimeEl || !dateEl || !durationEl) return;
    
    const unixStart = Number(startTimeEl.dataset.timestamp);
    const unixEnd = Number(endTimeEl.dataset.timestamp);
    
    if (isNaN(unixStart) || isNaN(unixEnd)) return;
    
    const dateStr = formatEventDate(unixStart);
    dateEl.textContent = dateStr;
    
    const duration = calculateDuration(unixStart, unixEnd);
    durationEl.textContent = `Duration: ${duration}`;
    
    const statusBadge = document.getElementById('meeting-status-badge');
    if (statusBadge && statusBadge.dataset.status === 'upcoming') {
        startCountdown(unixStart);
    }
}

function formatEventDate(unixTimestamp) {
    const date = new Date(unixTimestamp * 1000);
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const tomorrow = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1);
    const eventDay = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    
    let dateStr;
    if (eventDay.getTime() === today.getTime()) {
        dateStr = "Today";
    } else if (eventDay.getTime() === tomorrow.getTime()) {
        dateStr = "Tomorrow";
    } else {
        const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        const eventDayOfWeek = date.getDay();
        const todayDayOfWeek = today.getDay();
        
        const daysToNext = (eventDayOfWeek - todayDayOfWeek + 7) % 7;
        const nextOccurrence = new Date(today);
        nextOccurrence.setDate(today.getDate() + (daysToNext === 0 ? 7 : daysToNext));
        
        if (eventDay.getTime() === nextOccurrence.getTime()) {
            dateStr = days[eventDayOfWeek];
        } else {
            const dayAbbrev = days[eventDayOfWeek].substring(0, 3);
            const dateNumber = date.getDate();
            const monthAbbrev = date.toLocaleString('en-GB', { month: 'short', timeZone: 'Europe/London' });
            dateStr = `${dayAbbrev} ${dateNumber} ${monthAbbrev}`;
            if (date.getFullYear() !== now.getFullYear()) {
                dateStr += ` ${date.getFullYear()}`;
            }
        }
    }
    
    return dateStr;
}

function calculateDuration(unixStart, unixEnd) {
    const durationSeconds = unixEnd - unixStart;
    const hours = Math.floor(durationSeconds / 3600);
    const minutes = Math.floor((durationSeconds % 3600) / 60);
    
    let durationStr = '';
    if (hours > 0) {
        durationStr += `${hours} hour${hours !== 1 ? 's' : ''}`;
    }
    if (minutes > 0) {
        if (hours > 0) durationStr += ' and ';
        durationStr += `${minutes} minute${minutes !== 1 ? 's' : ''}`;
    }
    if (durationStr === '') {
        durationStr = 'Less than a minute';
    }
    
    return durationStr;
}

function initAttendeeInteractions() {
    const attendeeCards = document.querySelectorAll('.attendee-card');
    attendeeCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.classList.add('scale-102', 'shadow-md');
        });
        card.addEventListener('mouseleave', () => {
            card.classList.remove('scale-102', 'shadow-md');
        });
    });
}

function startCountdown(unixStart) {
    const countdownEl = document.getElementById('meeting-countdown');
    if (!countdownEl) return;
    
    const updateCountdown = () => {
        const now = Math.floor(Date.now() / 1000);
        const timeLeft = unixStart - now;
        
        if (timeLeft <= 0) {
            countdownEl.textContent = 'Starting now!';
            countdownEl.classList.remove('hidden');
            countdownEl.classList.add('animate-pulse', 'text-green-600', 'dark:text-green-400');
            setTimeout(() => {
                window.location.reload();
            }, 60000); // Reload page after a minute
            return;
        }
        
        const days = Math.floor(timeLeft / 86400);
        const hours = Math.floor((timeLeft % 86400) / 3600);
        const minutes = Math.floor((timeLeft % 3600) / 60);
        
        let countdownText = '';
        if (days > 0) {
            countdownText = `Starts in ${days}d ${hours}h ${minutes}m`;
        } else if (hours > 0) {
            countdownText = `Starts in ${hours}h ${minutes}m`;
        } else if (minutes > 0) {
            countdownText = `Starts in ${minutes}m`;
        } else {
            countdownText = 'Starting in less than a minute';
        }
        
        countdownEl.textContent = countdownText;
        countdownEl.classList.remove('hidden');
    };
    
    updateCountdown();
    
    setInterval(updateCountdown, 60000);
}

function checkMeetingStatus() {
    const now = Math.floor(Date.now() / 1000);
    const startTimeEl = document.getElementById('meeting-start-time');
    const endTimeEl = document.getElementById('meeting-end-time');
    
    if (!startTimeEl || !endTimeEl) return;
    
    const unixStart = Number(startTimeEl.dataset.timestamp);
    const unixEnd = Number(endTimeEl.dataset.timestamp);
    
    if (now > unixEnd && document.getElementById('status-badge-completed') === null) {
        const statusContainer = document.querySelector('.meeting-status');
        if (statusContainer) {
            const notification = document.createElement('div');
            notification.className = 'text-xs text-gray-500 mt-2 italic animate-fade-in';
            notification.textContent = 'Meeting status has changed. Refresh for latest status.';
            statusContainer.appendChild(notification);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const style = document.createElement('style');
    style.textContent = `
        .scale-102 {
            transform: scale(1.02);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .animate-fade-in {
            animation: fadeIn 0.5s ease-in;
        }
        .animate-pulse {
            animation: pulse 1.5s infinite;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }
    `;
    document.head.appendChild(style);
});