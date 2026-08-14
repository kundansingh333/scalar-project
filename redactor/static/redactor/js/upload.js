// upload.js — handles the loading state when the redaction form is submitted
(function () {
    "use strict";

    var form    = document.getElementById("redaction-form");
    var input   = form && form.querySelector('input[name="document"]');
    var loading = document.getElementById("loading");
    var estimate = document.getElementById("estimate");

    if (!form || !input || !loading || !estimate) { return; }

    form.addEventListener("submit", function () {
        var fileSizeMb = input.files[0] ? input.files[0].size / (1024 * 1024) : 1;
        var seconds    = Math.max(15, Math.ceil(10 + fileSizeMb * 3));
        estimate.textContent = "Estimated time: about " + seconds + " seconds";
        loading.classList.remove("hidden");
        var btn = form.querySelector("button[type=submit]");
        if (btn) { btn.disabled = true; }
    });
}());
