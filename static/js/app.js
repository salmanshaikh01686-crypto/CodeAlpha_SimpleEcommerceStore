document.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => {
        document.querySelectorAll(".message").forEach((el) => {
            el.style.transition = "opacity .4s";
            el.style.opacity = "0";
            setTimeout(() => el.remove(), 400);
        });
    }, 3500);
});
