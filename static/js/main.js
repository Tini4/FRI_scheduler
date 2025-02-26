// Add the event listener to the document or a parent element
document.addEventListener('click', function (event) {
    // Check if the clicked element (or its parent) is a <div> with the class "grid-entry"
    const gridEntry = event.target.closest('div.grid-entry');

    if (gridEntry) {
        // Remove the closest <div> with class "grid-entry"
        gridEntry.remove();
    }
});
