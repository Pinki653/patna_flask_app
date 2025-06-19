// static/script.js

console.log("JS Loaded ✅");

document.addEventListener("DOMContentLoaded", function () {
    const welcome = document.querySelector("h2");
    if (welcome) {
        welcome.classList.add("text-success");
        welcome.innerHTML += " 👋";
    }
});
