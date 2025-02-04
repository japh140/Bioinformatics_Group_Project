document.addEventListener('DOMContentLoaded', function() {
    const searchType = document.querySelector('#search_type');
    const exampleSpan = document.querySelector('#search-example');

    const examples = {
        'rs': 'Example: rs2028299',
        'coordinates': 'Example: chr15:89831025 or chr15:89831025-89831030',
        'gene': 'Example: TCF7L2'
    };

    function updateExample() {
        exampleSpan.textContent = examples[searchType.value] || '';
    }

    searchType.addEventListener('change', updateExample);
    updateExample(); // show initial example
});