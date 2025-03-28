document.addEventListener('DOMContentLoaded', () => {
    try {
        initInvitationSwitching();
        updateMeetingTimes();
        groupDynamicMeetings();
    } catch (error) {
        console.error("Error during initialisation:", error);
    }
});

function initInvitationSwitching() {
    const invitationForms = document.querySelectorAll('.invitation_form');
    invitationForms.forEach(form => {
        form.addEventListener('change', handleInvitationChange);

        if (!form.dataset.inviteId) {
            const inviteIdField = form.querySelector('[name="invitation_id"]');
            if (inviteIdField) {
                form.dataset.inviteId = inviteIdField.value;
            }
        }
    });
}

function updateMeetingTimes() {
    const meetings = document.querySelectorAll('.meeting');
    meetings.forEach(meetingEl => {
        const unixStart = Number(meetingEl.dataset.start);
        const unixEnd = Number(meetingEl.dataset.end);
        if (isNaN(unixStart) || isNaN(unixEnd)) return;
        const formattedTime = formatEventTime(unixStart, unixEnd);
        const timeInfo = meetingEl.querySelector('.time-info');
        if (timeInfo) {
            timeInfo.textContent = formattedTime;
        }
    });
}

async function handleInvitationChange(event) {
    const form = event.target.closest('form');
    if (!form) return;

    const inviteIdField = form.querySelector('[name="invitation_id"]');
    if (!inviteIdField) {
        console.error("Invitation ID not found in form");
        return;
    }
    const inviteId = inviteIdField.value;
    const newStatus = event.target.value;

    setLoadingState(form, true);

    try {
        const response = await fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const result = await response.json();

        if (result.success) {
            if (newStatus === "True") {
            } else if (newStatus === "False") {
            }
        } else {
            console.error("Error updating status:", result.message);
        }
    } catch (error) {
        console.error("AJAX error:", error);
        // flashElement(form, 'error');
    } finally {
        setLoadingState(form, false);
    }
}

function setLoadingState(element, isLoading) {
    requestAnimationFrame(() => {
        if (isLoading) {
            element.classList.add('opacity-50');
            element.setAttribute('aria-busy', 'true');
        } else {
            element.classList.remove('opacity-50');
            element.removeAttribute('aria-busy');
        }
    });
}

function formatEventTime(unixStart, unixEnd) {
    const startDate = new Date(unixStart * 1000);
    const endDate = new Date(unixEnd * 1000);
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const tomorrow = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1);
    const eventDay = new Date(startDate.getFullYear(), startDate.getMonth(), startDate.getDate());

    let dateStr;
    if (eventDay.getTime() === today.getTime()) {
        dateStr = "Today";
    } else if (eventDay.getTime() === tomorrow.getTime()) {
        dateStr = "Tomorrow";
    } else {
        const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        const eventDayOfWeek = startDate.getDay();
        const todayDayOfWeek = today.getDay();
        
        const daysToNext = (eventDayOfWeek - todayDayOfWeek + 7) % 7;
        const nextOccurrence = new Date(today);
        nextOccurrence.setDate(today.getDate() + (daysToNext === 0 ? 7 : daysToNext));
        
        if (eventDay.getTime() === nextOccurrence.getTime()) {
            dateStr = days[eventDayOfWeek]
        } else {
            const dayAbbrev = days[eventDayOfWeek].substring(0, 3);
            const dateNumber = startDate.getDate();
            const monthAbbrev = startDate.toLocaleString('en-GB', { month: 'short', timeZone: 'Europe/London' });
            dateStr = `${dayAbbrev} ${dateNumber} ${monthAbbrev}`;
            if (startDate.getFullYear() !== now.getFullYear()) {
                dateStr += ` ${startDate.getFullYear()}`;
            }
        }
    }
    
    const timeOptions = { hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'Europe/London' };
    const startTimeStr = startDate.toLocaleTimeString('en-GB', timeOptions);
    const endTimeStr = endDate.toLocaleTimeString('en-GB', timeOptions);
    return `${dateStr} - ${startTimeStr} - ${endTimeStr}`;
}

function groupDynamicMeetings() {
    const tileContainer = document.getElementById('meeting-tiles');
    if (!tileContainer) return;

    const originalMeetingTiles = Array.from(tileContainer.querySelectorAll('.meeting-tile'));

    const meetingsDynamic = document.getElementById('meetings-dynamic');
    if (!meetingsDynamic) return;
    meetingsDynamic.innerHTML = '';

    const now = new Date();

    const day = now.getDay();
    const diffToMonday = (day === 0 ? 1 : (8 - day));
    const nextMonday = new Date(now);
    nextMonday.setDate(now.getDate() + diffToMonday);
    // Set to beginning of the day
    nextMonday.setHours(0, 0, 0, 0);
    
    // Create end of this week (Sunday at 23:59:59.999)
    const endOfThisWeek = new Date(nextMonday);
    endOfThisWeek.setDate(endOfThisWeek.getDate() - 1);
    endOfThisWeek.setHours(23, 59, 59, 999);
    
    const endNextWeek = new Date(nextMonday);
    endNextWeek.setDate(nextMonday.getDate() + 6);
    endNextWeek.setHours(23, 59, 59, 999);

    const groups = {
        "Rest of This Week": [],
        "Early Next Week": [],
        "Later Next Week": [],
        "Later This Month": [],
        "Next Month": []
    };

    originalMeetingTiles.forEach(tile => {
        const meetingUnix = tile.getAttribute('data-start');
        if (!meetingUnix) return;
        const meetingTime = new Date(Number(meetingUnix) * 1000);
        if (meetingTime <= now) return;

        if (meetingTime <= endOfThisWeek) {
            groups["Rest of This Week"].push(tile);
        } else if (meetingTime <= endNextWeek) {
            const weekday = meetingTime.getDay();
            if (weekday >= 1 && weekday <= 3) {
                groups["Early Next Week"].push(tile);
            } else if (weekday >= 4 && weekday <= 6) {
                groups["Later Next Week"].push(tile);
            } else {
                groups["Later Next Week"].push(tile);
            }
        } else if (meetingTime.getMonth() === now.getMonth()) {
            groups["Later This Month"].push(tile);
        } else {
            const nextMonth = (now.getMonth() + 1) % 12;
            const nextMonthYear = (now.getMonth() === 11 ? now.getFullYear() + 1 : now.getFullYear());
            if (meetingTime.getMonth() === nextMonth && meetingTime.getFullYear() === nextMonthYear) {
                groups["Next Month"].push(tile);
            }
        }
    });

    const order = [
        "Rest of This Week",
        "Early Next Week",
        "Later Next Week",
        "Later This Month",
        "Next Month"
    ];

    const nonEmptyGroups = {};
    order.forEach(key => {
        if (groups[key].length > 0) {
            nonEmptyGroups[key] = groups[key];
        }
    });

    const primaryOrder = order.slice(0, 3);
    let finalGroups = [];
    primaryOrder.forEach(key => {
        if (nonEmptyGroups[key]) {
            finalGroups.push({ name: key, tiles: nonEmptyGroups[key] });
        }
    });

    if (finalGroups.length < 2) {
        order.slice(3).forEach(key => {
            if (nonEmptyGroups[key] && finalGroups.length < 3) {
                finalGroups.push({ name: key, tiles: nonEmptyGroups[key] });
            }
        });
    }
    if (finalGroups.length > 3) {
        finalGroups = finalGroups.slice(0, 3);
    }

    function addSection(title, tiles) {
        const section = document.createElement('section');
        section.className = "mt-4";

        const header = document.createElement('h3');
        header.textContent = title;
        header.className = "text-lg font-semibold text-gray-950 dark:text-white mb-2";
        section.appendChild(header);

        const div = document.createElement('div');
        div.className = "mt-4 flex flex-col gap-5";
        section.appendChild(div);

        tiles.forEach(tile => {
            const clonedTile = tile.cloneNode(true);
            clonedTile.classList.remove('hidden');
            div.appendChild(clonedTile);
        });

        meetingsDynamic.appendChild(section);
    }

    if (finalGroups.length === 0) {
        meetingsDynamic.innerHTML = "<p>No upcoming meetings to show.</p>";
    } else {
        finalGroups.forEach(group => addSection(group.name, group.tiles));
    }
}

Date.prototype.getWeek = function () {
    const date = new Date(this.getTime());
    date.setHours(0, 0, 0, 0);
    date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
    const week1 = new Date(date.getFullYear(), 0, 4);
    return 1 + Math.round(((date.getTime() - week1.getTime()) / 86400000 - 3 + (week1.getDay() + 6) % 7) / 7);
};
