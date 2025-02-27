let deleted = [];

// Listen for clicks on entries
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('div.grid-entry').forEach((entry) => {
        entry.addEventListener('click', (event) => {
            const div = event.currentTarget;

            deleted.push(div);
            div.style.display = 'none';
        });
    });
});

// Listen for Ctrl+Z (Undo)
document.addEventListener('keydown', (event) => {
    if (event.ctrlKey && event.key === 'z') {
        event.preventDefault();

        const div = deleted.pop();

        if (div) {
            div.style.display = '';
        }
    }
});

/* TODO: Export to calendar
// Generate .ical
function downloadFile(filename, content) {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');

    a.href = url;
    a.download = filename;

    document.body.appendChild(a);
    a.click();

    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Listen for Ctrl+E (Export)
document.addEventListener('keydown', (event) => {
    if (event.ctrlKey && event.key === 'e') {
        event.preventDefault();

        let file =
            "BEGIN:VCALENDAR\n" +
            "VERSION:2.0\n" +
            "PRODID:-//Urnik FRI//urnik.fri.uni-lj.si//\n";

        document.querySelectorAll('div.grid-entry').forEach((entry) => {
            const parent = entry.closest('div.grid-day-column');

            file += "BEGIN:VEVENT\n";

            console.log(entry.style["grid-row"]);

            file += "SUMMARY:" + entry.querySelector('a.link-subject').innerText.trim() + " " +
                entry.querySelector('a.entry-type').innerText.trim() + "\n";
            file += "DTSTART;TZID=Europe/Ljubljana;VALUE=DATE-TIME:200001??T" + entry.style.grid.trim();
                "DTSTART;TZID=Europe/Ljubljana;VALUE=DATE-TIME:20250218T080000\n" +
                "DTEND;TZID=Europe/Ljubljana;VALUE=DATE-TIME:20250218T100000\n" +
                "DTSTAMP;VALUE=DATE-TIME:20250226T205034Z\n" +
                "UID:urnikfri-186038\n" +
                "RRULE:FREQ=WEEKLY;UNTIL=20250606T235959;BYDAY=TU\n" +
                "DESCRIPTION:Algoritmi in podatkovne strukture 2 LV @ PR06\\nLuka Fürst\n" +
                "LOCATION:PR06\n";

            file += "END:VEVENT\n";
        });

        file += "END:VCALENDAR\n";

        // downloadFile('schedule.txt', file);
    }
});
*/
