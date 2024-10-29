$(document).ready(function () {
    $(document).on('click', '#add-form-btn', function () {
        const formsetContainer = $('.timesheet-formset-container');
        const totalForms = $('#id_form-TOTAL_FORMS');
        const formCount = parseInt(totalForms.val());

        const newForm = formsetContainer.find('.timesheet-form:first').clone(true);

        newForm.find(':input').each(function () {
            const name = $(this).attr('name');
            if (name) {
                const newName = name.replace(/-\d+-/, `-${formCount}-`);
                $(this).attr('name', newName);

                const id = $(this).attr('id');
                if (id) {
                    const newId = id.replace(/-\d+-/, `-${formCount}-`);
                    $(this).attr('id', newId);
                }

                if (name.includes('hours')) {
                    $(this).val('');
                }
            }
        });

        totalForms.val(formCount + 1);
        formsetContainer.append(newForm);
    });

    // Totals Calculation
    const weekdayMap = ["monday_hours", "tuesday_hours", "wednesday_hours", "thursday_hours", "friday_hours", "saturday_hours", "sunday_hours"];

    function updateTotals() {
        let weekTotal = 0;
        let dayTotals = { 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0 };

        document.querySelectorAll('[id^="id_form-"]').forEach(input => {
            weekdayMap.forEach((day, index) => {
                if (input.id.endsWith(day)) {
                    const hours = parseFloat(input.value) || 0;
                    weekTotal += hours;
                    dayTotals[index] += hours;
                }
            });
        });

        const weekTotalElement = document.getElementById("week-total");
        if (weekTotalElement) {
            weekTotalElement.innerText = weekTotal.toFixed(2);
            weekTotalElement.style.color = weekTotal >= 24 ? "red" : "black";
        }

        weekdayMap.forEach((day, index) => {
            const dayTotalElement = document.getElementById(`${day.split('_')[0]}-total`);
            if (dayTotalElement) {
                dayTotalElement.innerText = dayTotals[index].toFixed(2);
                dayTotalElement.style.color = dayTotals[index] >= 24 ? "red" : "black";
            }
        });
    }

    document.querySelectorAll('[id^="id_form-"]').forEach(input => {
        if (weekdayMap.some(day => input.id.endsWith(day))) {
            input.addEventListener('input', updateTotals);
        }
    });

    updateTotals();
});
