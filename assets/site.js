document.getElementById("year").textContent = new Date().getFullYear();

const form = document.getElementById("contact-form");
if (form) {
  const status = form.querySelector(".form-status");
  const button = form.querySelector("button[type=submit]");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = Object.fromEntries(new FormData(form));
    if (data.botcheck) return;
    const label = button.textContent;
    button.disabled = true;
    button.textContent = form.dataset.sending;
    status.textContent = "";
    status.className = "form-status";
    try {
      if (!form.dataset.key) throw new Error("Form key missing");
      const response = await fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ ...data, access_key: form.dataset.key, from_name: "lerouxconsultancy.com" }),
      });
      const result = await response.json();
      if (!response.ok || !result.success) throw new Error(result.message || "Send failed");
      form.reset();
      status.textContent = form.dataset.ok;
      status.classList.add("ok");
    } catch {
      status.textContent = form.dataset.error;
      status.classList.add("error");
    } finally {
      button.disabled = false;
      button.textContent = label;
    }
  });
}
