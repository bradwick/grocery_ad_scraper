// Function to handle hiding a deal
function hideDeal(dealId) {
    // Implement hiding logic here
    const dealElement = document.getElementById(dealId);
    dealElement.style.display = 'none';
    fetch("/hide", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: dealId }),
    });
}

// Function to handle pinning a deal
function pinDeal(dealId) {
    // Implement pinning logic here
    const dealElement = document.getElementById(dealId);
    dealElement.classList.toggle('pinned');
    fetch("/favorite", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: dealId }),
    });
    const pin = dealElement.querySelector(".pin img")
    if (dealElement.classList.contains("pinned")){
        pin.src='/static/img/unpin.png'
    }else{
        pin.src='/static/img/pin.png'
    }
}

// Function to handle saving a deal
function saveDeal(dealId) {
    // Implement saving logic here
    const dealElement = document.getElementById(dealId);
    dealElement.classList.toggle('saved');
    fetch("/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: dealId }),
    });
    const save = dealElement.querySelector(".save img")
    if (dealElement.classList.contains("saved")){
        save.src='/static/img/remove.png'
    }else{
        save.src='/static/img/save.png'
    }
}

// Function to handle initializing the actions for each deal
function initializeDealActions() {
    // Get all action buttons
    const actionButtons = document.querySelectorAll('.action-button');

    // Add click event listeners to each button
    actionButtons.forEach((button) => {
        const dealId = button.getAttribute('data-id');

        button.addEventListener('click', (event) => {
            const buttonType = button.classList[1];

            switch (buttonType) {
                case 'hide':
                    hideDeal(dealId);
                    break;
                case 'pin':
                    pinDeal(dealId);
                    break;
                case 'save':
                    saveDeal(dealId);
                    break;
                default:
                    break;
            }
        });
    });
}

// Initialize deal actions when the DOM is loaded
document.addEventListener('DOMContentLoaded', initializeDealActions);

