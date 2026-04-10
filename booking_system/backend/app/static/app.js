(function () {
  // Preference picker logic (group page)
  const picker = document.getElementById("slot-picker");
  if (picker) {
    const maxDays = parseInt(picker.dataset.maxDays || "1", 10);
    const maxPerDay = parseInt(picker.dataset.maxPerDay || "1", 10);
    const maxTotal = parseInt(picker.dataset.maxTotal || String(maxDays * maxPerDay), 10);

    const list = document.getElementById("ranked-list");
    const hiddenInput = document.getElementById("slot_ids_input");
    const clearBtn = document.getElementById("clear-rank");

    const buttons = Array.from(document.querySelectorAll(".slot-btn"));
    const slotMeta = new Map();
    buttons.forEach((btn) => {
      const sid = Number(btn.dataset.slotId);
      slotMeta.set(sid, {
        id: sid,
        day: btn.dataset.day,
        time: btn.dataset.time,
      });
    });

    let ranked = [];

    function countsByDay(ids) {
      const map = new Map();
      ids.forEach((id) => {
        const m = slotMeta.get(id);
        if (!m) return;
        map.set(m.day, (map.get(m.day) || 0) + 1);
      });
      return map;
    }

    function canAdd(id) {
      if (ranked.includes(id)) return [false, "Already added"];
      if (ranked.length >= maxTotal) return [false, `Max total is ${maxTotal}`];

      const m = slotMeta.get(id);
      if (!m) return [false, "Invalid slot"];

      const after = ranked.concat([id]);
      const dayCount = countsByDay(after);
      if (dayCount.size > maxDays) return [false, `Max days is ${maxDays}`];
      if ((dayCount.get(m.day) || 0) > maxPerDay) return [false, `Per-day max is ${maxPerDay}`];
      return [true, ""];
    }

    function syncInput() {
      hiddenInput.value = ranked.join(",");
      buttons.forEach((btn) => {
        const sid = Number(btn.dataset.slotId);
        btn.classList.toggle("added", ranked.includes(sid));
      });
    }

    function moveItem(index, delta) {
      const target = index + delta;
      if (target < 0 || target >= ranked.length) return;
      const item = ranked[index];
      ranked[index] = ranked[target];
      ranked[target] = item;
      render();
    }

    function removeItem(index) {
      ranked.splice(index, 1);
      render();
    }

    function render() {
      list.innerHTML = "";
      ranked.forEach((sid, index) => {
        const m = slotMeta.get(sid);
        if (!m) return;

        const li = document.createElement("li");
        li.className = "rank-item";

        const rank = document.createElement("span");
        rank.className = "rank-index";
        rank.textContent = String(index + 1);

        const text = document.createElement("div");
        text.textContent = `${m.day} | ${m.time} (#${m.id})`;

        const controls = document.createElement("div");

        const up = document.createElement("button");
        up.type = "button";
        up.className = "icon-btn";
        up.textContent = "↑";
        up.addEventListener("click", () => moveItem(index, -1));

        const down = document.createElement("button");
        down.type = "button";
        down.className = "icon-btn";
        down.textContent = "↓";
        down.addEventListener("click", () => moveItem(index, 1));

        const del = document.createElement("button");
        del.type = "button";
        del.className = "icon-btn";
        del.textContent = "×";
        del.addEventListener("click", () => removeItem(index));

        controls.appendChild(up);
        controls.appendChild(down);
        controls.appendChild(del);

        li.appendChild(rank);
        li.appendChild(text);
        li.appendChild(controls);
        list.appendChild(li);
      });

      syncInput();
    }

    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const sid = Number(btn.dataset.slotId);
        const [ok, err] = canAdd(sid);
        if (!ok) {
          alert(err);
          return;
        }
        ranked.push(sid);
        render();
      });
    });

    if (clearBtn) {
      clearBtn.addEventListener("click", () => {
        ranked = [];
        render();
      });
    }

    const initial = (hiddenInput.value || "")
      .split(",")
      .map((x) => parseInt(x.trim(), 10))
      .filter((x) => Number.isInteger(x) && slotMeta.has(x));

    ranked = initial.slice(0, maxTotal);
    render();
  }

  // Teacher dashboard filters
  const groupInput = document.getElementById("filter-group");
  const roundSelect = document.getElementById("filter-round");
  const statusSelect = document.getElementById("filter-status");
  const resetBtn = document.getElementById("filter-reset");

  if (groupInput && roundSelect && statusSelect) {
    const resultRows = Array.from(document.querySelectorAll("#results-table tbody tr[data-group]"));
    const groupRows = Array.from(document.querySelectorAll("#groups-table tbody tr[data-group]"));

    function applyFilter() {
      const kw = (groupInput.value || "").trim().toLowerCase();
      const round = roundSelect.value;
      const status = statusSelect.value;

      resultRows.forEach((tr) => {
        const groupText = tr.dataset.group || "";
        const rowRound = tr.dataset.round || "";
        const rowStatus = tr.dataset.status || "";

        const okGroup = !kw || groupText.includes(kw);
        const okRound = !round || rowRound === round;
        const okStatus = !status || rowStatus === status;
        tr.style.display = okGroup && okRound && okStatus ? "" : "none";
      });

      groupRows.forEach((tr) => {
        const groupText = tr.dataset.group || "";
        const rowStatus = tr.dataset.status || "";
        const okGroup = !kw || groupText.includes(kw);
        const okStatus = !status || rowStatus === status;
        tr.style.display = okGroup && okStatus ? "" : "none";
      });
    }

    groupInput.addEventListener("input", applyFilter);
    roundSelect.addEventListener("change", applyFilter);
    statusSelect.addEventListener("change", applyFilter);

    if (resetBtn) {
      resetBtn.addEventListener("click", () => {
        groupInput.value = "";
        roundSelect.value = "";
        statusSelect.value = "";
        applyFilter();
      });
    }
  }
})();
