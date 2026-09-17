/* PV Solution — interaksi minimal untuk mockup statis.
   Hanya untuk mendemokan state yang ada di Figma (modal, toggle password).
   Tidak ada logika bisnis di sini. */
(function () {
  "use strict";

  /* ---- Modal: [data-modal-open="id"] / [data-modal-close] / klik overlay ---- */
  function openModal(id) {
    var el = document.getElementById(id);
    if (el) { el.classList.add("is-open"); document.body.style.overflow = "hidden"; }
  }

  function closeModal(el) {
    if (el) { el.classList.remove("is-open"); document.body.style.overflow = ""; }
  }

  document.addEventListener("click", function (e) {
    var opener = e.target.closest("[data-modal-open]");
    if (opener) {
      e.preventDefault();
      openModal(opener.getAttribute("data-modal-open"));
      return;
    }

    var closer = e.target.closest("[data-modal-close]");
    if (closer) {
      e.preventDefault();
      closeModal(closer.closest(".modal-overlay"));
      return;
    }

    if (e.target.classList.contains("modal-overlay")) closeModal(e.target);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      var open = document.querySelector(".modal-overlay.is-open");
      if (open) closeModal(open);
    }
  });

  /* ---- Toggle visibility password ---- */
  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-toggle-password]");
    if (!btn) return;
    var input = btn.parentElement.querySelector("input");
    if (!input) return;
    var hidden = input.type === "password";
    input.type = hidden ? "text" : "password";
    btn.querySelectorAll("svg").forEach(function (svg, i) {
      svg.style.display = (i === 0) === hidden ? "none" : "block";
    });
  });

  /* ---- Select: warna teks mengikuti ada/tidaknya pilihan ---- */
  document.querySelectorAll("select.select").forEach(function (sel) {
    function sync() {
      sel.style.color = sel.value === "" ? "var(--gray-400)" : "var(--gray-900)";
    }
    sel.addEventListener("change", sync);
    sync();
  });
})();
