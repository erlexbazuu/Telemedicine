// Function to generate options for days
function generateDayOptions() {
    const daySelect = document.getElementById('day');
    for (let i = 1; i <= 31; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.text = String(i).padStart(2, '0');
        daySelect.add(option);
    }
}

// Function to generate options for months
function generateMonthOptions() {
    const monthSelect = document.getElementById('month');
    const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    for (let i = 0; i < months.length; i++) {
        const option = document.createElement('option');
        option.value = i + 1;
        option.text = months[i];
        monthSelect.add(option);
    }
}

// Function to generate options for years
function generateYearOptions() {
    const yearSelect = document.getElementById('year');
    const currentYear = new Date().getFullYear();
    for (let i = currentYear - 100; i <= currentYear; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.text = i;
        yearSelect.add(option);
    }
}
document.getElementById("phone-number").focus();

// Call the functions to generate options
generateDayOptions();
generateMonthOptions();
generateYearOptions();



// Added

