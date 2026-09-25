document.getElementById("claimForm").addEventListener("submit", async function(event) {

    event.preventDefault();

    const result = document.getElementById("result");

    const customerName = document.getElementById("customerName").value;
    const claimType = document.getElementById("claimType").value;
    const claimAmount = Number(document.getElementById("claimAmount").value);
    const policyFile = document.getElementById("policyFile").files[0];

    if (!policyFile) {
        result.textContent = "Please upload an insurance policy PDF.";
        return;
    }

    result.textContent = "Analysing your insurance policy...";

    const formData = new FormData();

    formData.append("customer_name", customerName);
    formData.append("claim_type", claimType);
    formData.append("claim_amount", claimAmount);
    formData.append("policy_file", policyFile);

    try {

        const response = await fetch("http://127.0.0.1:8000/claims", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Server error: " + response.status);
        }

        const data = await response.json();

        result.innerHTML = `
            <h2>Claim Assessment</h2>

            <p><strong>Customer:</strong> ${data.customer_name}</p>
            <p><strong>Claim Type:</strong> ${data.claim_type}</p>
            <p><strong>Claim Amount:</strong> £${data.claim_amount.toFixed(2)}</p>

            <hr>

            <p><strong>Result:</strong> ${data.status}</p>
        `;

    } catch (error) {

        console.error(error);

        result.textContent =
            "Something went wrong while processing the claim.";

    }

});