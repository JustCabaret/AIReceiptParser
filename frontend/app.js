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
    const formData = new FormData();
    formData.append("file", document.getElementById("fileInput").files[0]);
    formData.append("api_key", getCookie("api_key"));

    try {
        const response = await fetch(`${API_BASE_URL}/process_receipt`, { method: "POST", body: formData });
        if (!response.ok) throw new Error("Upload failed.");
        alert("Receipt uploaded successfully!");
        bootstrap.Modal.getInstance(document.getElementById("receiptModal")).hide();
        loadReceipts();
    } catch (error) {
        alert(error.message);
    }
}

async function showReceiptDetails(receiptId) {
    const detailsTableBody = document.getElementById("detailsTableBody");
    showModal("detailsModal");

    try {
        const response = await fetch(`${API_BASE_URL}/receipts/${receiptId}`);
        if (!response.ok) throw new Error("Failed to fetch details.");
        const data = await response.json();

        detailsTableBody.innerHTML = data.items
            .map(
                (item) => `
            <tr>
                <td>${item.product}</td>
                <td>${item.quantity}</td>
                <td>${(item.price / 100).toFixed(2)}</td>
                <td>${item.category}</td>
            </tr>`
            )
            .join("");
    } catch (error) {
        detailsTableBody.innerHTML = `<tr><td colspan="4" class="text-danger">${error.message}</td></tr>`;
    }
}

function showModal(id) {
    const modal = new bootstrap.Modal(document.getElementById(id));
    modal.show();
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    return value.split(`; ${name}=`).pop().split(";").shift();
}
