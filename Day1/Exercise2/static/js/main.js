// Main JavaScript file

// Global variables
let currentPage = 1;
let totalPages = 1;
let toast;

document.addEventListener('DOMContentLoaded', function () {
    // Initialize toast
    toast = document.getElementById('toast');

    // Initialize form submission
    const form = document.getElementById('addRecordForm');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }

    // Initialize filter inputs with debounce
    const nameFilter = document.getElementById('nameFilter');
    const minAgeFilter = document.getElementById('minAgeFilter');
    const maxAgeFilter = document.getElementById('maxAgeFilter');

    const debouncedLoadRecords = debounce(() => loadRecords(1), 300);

    [nameFilter, minAgeFilter, maxAgeFilter].forEach(filter => {
        if (filter) {
            filter.addEventListener('input', debouncedLoadRecords);
        }
    });

    // Load initial records
    loadRecords(1);

    // Health check
    const checkHealth = async () => {
        try {
            const response = await fetch('/health');
            const data = await response.json();

            const statusElement = document.getElementById('health-status');
            if (statusElement) {
                statusElement.textContent = data.status;
                statusElement.className = data.status === 'healthy' ? 'status-healthy' : 'status-unhealthy';
            }
        } catch (error) {
            console.error('Health check failed:', error);
        }
    };

    // Run health check every 30 seconds
    checkHealth();
    setInterval(checkHealth, 30000);

    // Add pagination button listeners
    const prevButton = document.getElementById('prevPage');
    const nextButton = document.getElementById('nextPage');
    const itemsPerPage = document.getElementById('itemsPerPage');

    if (prevButton) {
        prevButton.addEventListener('click', () => {
            if (currentPage > 1) {
                loadRecords(currentPage - 1);
            }
        });
    }

    if (nextButton) {
        nextButton.addEventListener('click', () => {
            if (currentPage < totalPages) {
                loadRecords(currentPage + 1);
            }
        });
    }

    if (itemsPerPage) {
        itemsPerPage.addEventListener('change', () => {
            loadRecords(1); // Reset to first page when changing items per page
        });
    }
});

// Debounce function to limit API calls
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Handle form submission
async function handleFormSubmit(event) {
    event.preventDefault();

    try {
        const form = document.getElementById('addRecordForm');
        if (!form) {
            throw new Error('Form not found');
        }

        const formData = {
            full_name: document.getElementById('fullName')?.value,
            age: parseInt(document.getElementById('age')?.value),
            api_key: document.getElementById('apiKey')?.value
        };

        // Validate form data
        if (!formData.full_name) {
            showToast('Full name is required', 'error');
            return;
        }
        if (isNaN(formData.age) || formData.age < 0) {
            showToast('Age must be a valid positive number', 'error');
            return;
        }
        if (!formData.api_key) {
            showToast('API key is required', 'error');
            return;
        }

        const response = await fetch('/insert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
            showToast('Record inserted successfully', 'success');
            form.reset();
            loadRecords(1); // Reload first page after insertion
        } else {
            showToast(data.message || 'Failed to insert record', 'error');
        }
    } catch (error) {
        console.error('Form submission error:', error);
        showToast('Error submitting form: ' + error.message, 'error');
    }
}

// Load records with pagination and filters
async function loadRecords(page = 1) {
    try {
        const nameFilter = document.getElementById('nameFilter')?.value || '';
        const minAge = document.getElementById('minAgeFilter')?.value || '';
        const maxAge = document.getElementById('maxAgeFilter')?.value || '';
        const itemsPerPage = document.getElementById('itemsPerPage')?.value || 10;

        const params = new URLSearchParams({
            page: page,
            per_page: itemsPerPage
        });

        if (nameFilter) params.append('name', nameFilter);
        if (minAge) params.append('min_age', minAge);
        if (maxAge) params.append('max_age', maxAge);

        const response = await fetch(`/records?${params.toString()}`);
        const data = await response.json();

        if (response.ok && data.status === 'success') {
            // Update pagination state
            currentPage = data.pagination.current_page;
            totalPages = data.pagination.total_pages;

            // Update records table
            updateRecordsTable(data.records);

            // Update records count
            const recordsCount = document.getElementById('recordsCount');
            if (recordsCount) {
                recordsCount.textContent = `Total Records: ${data.pagination.total_records}`;
            }

            // Update pagination UI
            updatePagination();

            // Update filters info if there are active filters
            if (nameFilter || minAge || maxAge) {
                updateActiveFilters(data.pagination.total_records);
            }
        } else {
            showToast(data.message || 'Failed to load records', 'error');
            // Clear table on error
            updateRecordsTable([]);
        }
    } catch (error) {
        console.error('Error loading records:', error);
        showToast('Error loading records: ' + error.message, 'error');
        // Clear table on error
        updateRecordsTable([]);
    }
}

// Update the records table
function updateRecordsTable(records) {
    const tbody = document.querySelector('#recordsTable');
    if (!tbody) {
        console.error('Table body element not found');
        return;
    }

    tbody.innerHTML = '';

    if (!records || records.length === 0) {
        const tr = document.createElement('tr');
        tr.innerHTML = '<td colspan="3" class="text-center">No records found</td>';
        tbody.appendChild(tr);
        return;
    }

    records.forEach(record => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${record.full_name || ''}</td>
            <td>${record.age || ''}</td>
            <td>${record.added_at || ''}</td>
        `;
        tbody.appendChild(tr);
    });
}

// Update pagination UI
function updatePagination() {
    const prevButton = document.getElementById('prevPage');
    const nextButton = document.getElementById('nextPage');
    const currentPageSpan = document.getElementById('currentPage');
    const totalPagesSpan = document.getElementById('totalPages');
    const paginationNumbers = document.getElementById('pagination');

    if (!prevButton || !nextButton || !currentPageSpan || !totalPagesSpan || !paginationNumbers) {
        console.error('Pagination elements not found');
        return;
    }

    // Update page numbers
    currentPageSpan.textContent = currentPage;
    totalPagesSpan.textContent = totalPages;

    // Enable/disable prev/next buttons
    prevButton.disabled = currentPage === 1;
    nextButton.disabled = currentPage === totalPages;

    // Generate pagination numbers
    paginationNumbers.innerHTML = '';

    // Calculate range of pages to show
    let startPage = Math.max(1, currentPage - 2);
    let endPage = Math.min(totalPages, currentPage + 2);

    // Always show first page
    if (startPage > 1) {
        addPageNumber(1);
        if (startPage > 2) {
            addEllipsis();
        }
    }

    // Add page numbers
    for (let i = startPage; i <= endPage; i++) {
        addPageNumber(i);
    }

    // Always show last page
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            addEllipsis();
        }
        addPageNumber(totalPages);
    }

    function addPageNumber(pageNum) {
        const button = document.createElement('button');
        button.className = `btn btn-sm ${pageNum === currentPage ? 'btn-primary' : 'btn-outline-secondary'}`;
        button.textContent = pageNum;
        button.style.margin = '0 2px';
        button.onclick = () => loadRecords(pageNum);
        paginationNumbers.appendChild(button);
    }

    function addEllipsis() {
        const span = document.createElement('span');
        span.className = 'mx-2';
        span.textContent = '...';
        paginationNumbers.appendChild(span);
    }
}

// Update active filters display
function updateActiveFilters(totalRecords) {
    const nameFilter = document.getElementById('nameFilter')?.value;
    const minAge = document.getElementById('minAgeFilter')?.value;
    const maxAge = document.getElementById('maxAgeFilter')?.value;

    let activeFilters = 0;
    if (nameFilter) activeFilters++;
    if (minAge) activeFilters++;
    if (maxAge) activeFilters++;

    if (activeFilters > 0) {
        showToast(
            `Found ${totalRecords} record${totalRecords !== 1 ? 's' : ''} with ${activeFilters} active filter${activeFilters !== 1 ? 's' : ''}`,
            'info'
        );
    }
}

// Clear all filters
function clearFilters() {
    const filters = ['nameFilter', 'minAgeFilter', 'maxAgeFilter'];
    filters.forEach(id => {
        const element = document.getElementById(id);
        if (element) element.value = '';
    });
    loadRecords(1);
}

// Show toast notification
function showToast(message, type = 'info') {
    if (!toast) return;

    // Remove existing classes
    toast.className = 'toast';

    // Add appropriate class based on type
    switch (type) {
        case 'success':
            toast.classList.add('toast-success');
            break;
        case 'error':
            toast.classList.add('toast-error');
            break;
        case 'info':
            toast.classList.add('toast-info');
            break;
    }

    toast.textContent = message;
    toast.style.display = 'block';

    // Hide after 3 seconds
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
} 