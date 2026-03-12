const API_BASE_URL = "http://localhost:5000";
let currentPage = 1;
const rowsPerPage = 10;

document.addEventListener("DOMContentLoaded", () => {
    checkApiKey();
    loadReceipts();

    document.getElementById("addReceiptBtn").addEventListener("click", () => showModal("receiptModal"));
    document.getElementById("changeApiKeyBtn").addEventListener("click", () => showModal("apiKeyModal"));
    document.getElementById("saveApiKeyBtn").addEventListener("click", saveApiKey);
    document.getElementById("uploadForm").addEventListener("submit", processFile);
});

function checkApiKey() {
    const apiKey = getCookie("api_key");
    if (!apiKey) showModal("apiKeyModal");
}

function saveApiKey() {
    const apiKey = document.getElementById("apiKeyInput").value.trim();
    if (apiKey) {
        document.cookie = `api_key=${apiKey}; path=/; max-age=2592000`;
        bootstrap.Modal.getInstance(document.getElementById("apiKeyModal")).hide();
        alert("API Key saved successfully!");
        loadReceipts();
    } else {
        alert("Please enter a valid API Key.");
    }
}


async function loadReceipts() {
    try {
        const response = await fetch(`${API_BASE_URL}/receipts`);
        if (!response.ok) throw new Error("Failed to fetch receipts.");
        const receipts = await response.json();
        displayReceipts(receipts);
    } catch (error) {
        console.error(error);
    }
}

function displayReceipts(receipts) {
    const tableBody = document.querySelector("#receiptsTable tbody");
    const pagination = document.getElementById("pagination");
    const totalPages = Math.ceil(receipts.length / rowsPerPage);

    const paginatedReceipts = receipts.slice((currentPage - 1) * rowsPerPage, currentPage * rowsPerPage);

    tableBody.innerHTML = paginatedReceipts
        .map(
            (receipt) => `
            <tr onclick="showReceiptDetails(${receipt.id})">
                <td>${receipt.store}</td>
                <td>${(receipt.total / 100).toFixed(2)}</td>
            </tr>`
        )
        .join("");

    pagination.innerHTML = Array.from({ length: totalPages }, (_, i) => i + 1)
        .map(
            (page) => `
            <li class="page-item ${currentPage === page ? "active" : ""}">
                <button class="page-link" onclick="changePage(${page})">${page}</button>
            </li>`
        )
        .join("");
}

function changePage(page) {
    currentPage = page;
    loadReceipts();
}

async function processFile(e) {
    e.preventDefault();
    const btn = document.getElementById("uploadBtn");
    const spinner = document.getElementById("uploadSpinner");
    const btnText = document.getElementById("uploadBtnText");

    // Loading State
    btn.disabled = true;
    spinner.classList.remove("d-none");
    btnText.textContent = "Processing AI...";

    const formData = new FormData();
    formData.append("file", document.getElementById("fileInput").files[0]);
    formData.append("api_key", getCookie("api_key"));

    try {
        const response = await fetch(`${API_BASE_URL}/process_receipt`, { method: "POST", body: formData });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Upload failed due to a server error.");
        }
        
        alert("Receipt uploaded successfully!");
        bootstrap.Modal.getInstance(document.getElementById("receiptModal")).hide();
        loadReceipts();
    } catch (error) {
        alert("Error: " + error.message);
    } finally {
        // Reset State
        btn.disabled = false;
        spinner.classList.add("d-none");
        btnText.textContent = "Upload";
        document.getElementById("uploadForm").reset();
    }
}

async function showReceiptDetails(receiptId) {
    const detailsTableBody = document.getElementById("detailsTableBody");
    const exportBtn = document.getElementById("exportCsvBtn");
    
    // Reset export state
    exportBtn.style.display = "none";
    showModal("detailsModal");

    try {
        const response = await fetch(`${API_BASE_URL}/receipts/${receiptId}`);
        if (!response.ok) throw new Error("Failed to fetch details.");
        const data = await response.json();

        detailsTableBody.innerHTML = data.items
            .map(
                (item) => `
            <tr>
                <td class="fw-medium">${item.product}</td>
                <td class="text-center">${item.quantity}</td>
                <td class="text-end fw-semibold">${(item.price / 100).toFixed(2)}</td>
                <td><span class="category-badge">${item.category}</span></td>
            </tr>`
            )
            .join("");

        // Show Export button and attach event listener
        exportBtn.style.display = "block";
        exportBtn.onclick = () => downloadCSV(data.items);
    } catch (error) {
        detailsTableBody.innerHTML = `<tr><td colspan="4" class="text-danger">${error.message}</td></tr>`;
    }
}

function downloadCSV(items) {
    const headers = "Product,Quantity,Price,Category\n";
    const rows = items.map(item => `"${item.product}",${item.quantity},${(item.price / 100).toFixed(2)},"${item.category}"`).join("\n");
    const csvContent = headers + rows;
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", "receipt_export.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function showModal(id) {
    const modal = new bootstrap.Modal(document.getElementById(id));
    modal.show();
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    return value.split(`; ${name}=`).pop().split(";").shift();
}
