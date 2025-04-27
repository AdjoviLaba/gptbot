// Main JavaScript file for Product Review AI

// Enable tooltips globally
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-dismiss alerts
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-important)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Preview image upload
    const imageInput = document.getElementById('product_image');
    if (imageInput) {
        imageInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                // You could add image preview functionality here
                console.log('File selected:', this.files[0].name);
            }
        });
    }
    
    // This function allows adding follow-up questions after receiving a review
    window.addFollowUpQuestion = function(question) {
        // This function would be called when the user clicks a "follow-up" button
        const formData = new FormData();
        formData.append('product_info', document.getElementById('product_info').value);
        formData.append('follow_up_question', question);
        
        // You would implement this functionality in a future version
        console.log('Follow-up question:', question);
        
        // Example alert for demo purposes
        alert('Follow-up question feature will be implemented in the next version.');
    };
});