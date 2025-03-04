document.addEventListener('DOMContentLoaded', function() {
    const searchType = document.querySelector('#search_type');
    const exampleSpan = document.querySelector('#search-example');

    const examples = {
        'rs': 'Example: rs7903146',
        'coordinates': 'Example: chr3:185785668 or chr10:94478355-94485763',
        'gene': 'Example: TCF7L2'
    };

    function updateExample() {
        exampleSpan.textContent = examples[searchType.value] || '';
    }

    searchType.addEventListener('change', updateExample);
    updateExample(); // show initial example
});