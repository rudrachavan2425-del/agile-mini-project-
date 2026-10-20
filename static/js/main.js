/**
 * CampusNexus - Placement System & DevOps Suite
 * Core Frontend Interactions & Telemetry
 */

document.addEventListener("DOMContentLoaded", () => {
    // 1. Mobile Menu Toggle
    const mobileBtn = document.getElementById("mobileMenuBtn");
    const navLinks = document.getElementById("navLinks");

    if (mobileBtn && navLinks) {
        mobileBtn.addEventListener("click", () => {
            const isVisible = navLinks.style.display === "flex";
            navLinks.style.display = isVisible ? "none" : "flex";
            navLinks.style.flexDirection = "column";
            navLinks.style.position = "absolute";
            navLinks.style.top = "72px";
            navLinks.style.left = "0";
            navLinks.style.width = "100%";
            navLinks.style.background = "#0b0f19";
            navLinks.style.padding = "1.5rem";
            navLinks.style.borderBottom = "1px solid rgba(255, 255, 255, 0.1)";
        });
    }

    // 2. Auto Dismiss Flash Messages after 6 seconds
    const toasts = document.querySelectorAll(".toast-alert");
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.transition = "opacity 0.4s ease, transform 0.4s ease";
            toast.style.opacity = "0";
            toast.style.transform = "translateY(-10px)";
            setTimeout(() => toast.remove(), 400);
        }, 6000);
    });

    // 3. Quick Telemetry Updater for Dashboard sidebar
    const quickCpu = document.getElementById("quickCpu");
    const quickMem = document.getElementById("quickMem");

    if (quickCpu && quickMem) {
        setInterval(() => {
            fetch("/api/stats")
                .then(res => res.json())
                .then(data => {
                    quickCpu.innerText = data.stats.cpu_percent + "%";
                    quickMem.innerText = data.stats.mem_percent + "%";
                })
                .catch(() => {});
        }, 4000);
    }
});
