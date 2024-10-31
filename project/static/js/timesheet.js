document.addEventListener("DOMContentLoaded", function () {
    const formsetContainer = document.getElementById("tbody");
    const emptyFormTemplate = document.getElementById("empty-form");
    const addItemBtn = document.getElementById("#add-item-btn");
    const totalForms = document.querySelector("#id_form-TOTAL_FORMS");

    addItemBtn.addEventListener("click", function () {
        // Clone the empty form template
        const newForm = emptyFormTemplate.cloneNode(true);
        newForm.style.display = "block";

        // Get the current number of forms
        const formCount = parseInt(totalForms.value);

        // Update the new form's fields by replacing __prefix__ with formCount
        newForm.innerHTML = newForm.innerHTML.replace(/__prefix__/g, formCount);

        // Append the new form to the formset container
        formsetContainer.appendChild(newForm);

        // Increment the total form count
        totalForms.value = formCount + 1;
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
