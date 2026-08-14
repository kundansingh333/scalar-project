// upload.js — handles drag-drop display, loading overlay, and progress simulation
(function () {
  "use strict";

  var dropZone   = document.getElementById("drop-zone");
  var fileInput  = document.getElementById("file-input");
  var fileInfo   = document.getElementById("file-info");
  var fileLabel  = document.getElementById("file-name-display");
  var form       = document.getElementById("upload-form");
  var submitBtn  = document.getElementById("submit-btn");
  var overlay    = document.getElementById("loading-overlay");
  var etaText    = document.getElementById("eta-text");
  var progressBar = document.getElementById("progress-bar");

  if (!form) { return; }

  // Drag-and-drop visual feedback
  if (dropZone) {
    dropZone.addEventListener("dragover", function (e) {
      e.preventDefault();
      dropZone.classList.add("drag-over");
    });
    dropZone.addEventListener("dragleave", function () {
      dropZone.classList.remove("drag-over");
    });
    dropZone.addEventListener("drop", function (e) {
      e.preventDefault();
      dropZone.classList.remove("drag-over");
      if (e.dataTransfer && e.dataTransfer.files.length) {
        fileInput.files = e.dataTransfer.files;
        showFileInfo(fileInput.files[0]);
      }
    });
  }

  // Show selected file name
  if (fileInput) {
    fileInput.addEventListener("change", function () {
      if (fileInput.files.length) {
        showFileInfo(fileInput.files[0]);
      }
    });
  }

  function showFileInfo(file) {
    if (!fileInfo || !fileLabel) { return; }
    fileLabel.textContent = file.name + " (" + (file.size / (1024 * 1024)).toFixed(1) + " MB)";
    fileInfo.classList.add("visible");
  }

  // Form submit → show loading overlay + progress bar
  form.addEventListener("submit", function () {
    if (!fileInput.files.length) { return; }

    var sizeMb = fileInput.files[0].size / (1024 * 1024);
    var estimatedSec = Math.max(20, Math.ceil(15 + sizeMb * 4));

    if (etaText) {
      etaText.textContent = "Estimated time: about " + estimatedSec + " seconds";
    }

    if (submitBtn) { submitBtn.disabled = true; }
    if (overlay)   { overlay.classList.add("visible"); }

    // Simulate progress bar filling up to 90% over estimated time
    if (progressBar) {
      var startTime = Date.now();
      var totalMs = estimatedSec * 1000;
      var rafId;

      function tick() {
        var elapsed = Date.now() - startTime;
        var pct = Math.min(90, (elapsed / totalMs) * 90);
        progressBar.style.width = pct + "%";
        if (pct < 90) {
          rafId = requestAnimationFrame(tick);
        }
      }

      rafId = requestAnimationFrame(tick);
    }
  });

}());
