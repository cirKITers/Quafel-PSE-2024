

//hwps_sims containing all hardware profiles and simulators
let hwps_sims;

// Variables to store the selected values of the dropdowns, needed for selectCombinations
let selectedHwp = "";
let selectedSim = "";
let selectedSimVersion = "";

// Check if hardwareprofile list is matching with configuration form
let hwps_uptodate = false;

// Add event listener when the document is loaded
document.addEventListener("DOMContentLoaded", function () {
	stripeTable();

	// Submit button sends checked entries
	document.getElementById("btn_submit").addEventListener("click", sentCheckedEntries);

	// Master Checkbox switches all other
	document.querySelector('#table_header input[type="checkbox"]').addEventListener("change", function () {
		var slaveCheckboxes = document.querySelectorAll('#computed_overview tr input[type="checkbox"]');

		// Toggle the state of the slave checkboxes
		var isChecked = this.checked;
		slaveCheckboxes.forEach(function (checkbox) {
			checkbox.checked = isChecked;
		});
	});

	document.querySelectorAll(".conf_selection input").forEach(function(input) {
		input.addEventListener("change", function () {
			hwps_uptodate = false;
			document.getElementById("simulation_conf_submit").innerText = "Please Update Hardwareprofiles";
		});
	});

	document.getElementById("simulation_conf_submit").addEventListener("click", function () {
		hwps_uptodate = true;
		// this.innerText = "Hardware Profiles List is up to date";
	});

	hwps_sims = JSON.parse(document.getElementById("add-hardwareprofile").getAttribute("data-hwps-sims"));

	// Add event listener to the "Add Hardware Profile" button
	document.getElementById("add-hardwareprofile").addEventListener("click", function () {
		console.log(hwps_sims);
		const hwpsOptions = hwps_sims.hwps
			.map((profile) => `<option value="${profile.name}">${profile.name}-${profile.description}</option>`)
			.join("");

		// Extract unique simulation profiles based on name
		const uniqueSims = Array.from(new Set(hwps_sims.sims.map((profile) => profile.name))).map((name) => {
			return hwps_sims.sims.find((profile) => profile.name === name);
		});
		// Generate options for simulation profiles, ensuring each name is only added once
		const simsOptions = uniqueSims.map((profile) => `<option value="${profile.name}">${profile.name}</option>`).join("");

		var tbody = document.querySelector("#computed_overview tbody");
		// var newRow = tbody.rows[tbody.rows.length - 1].cloneNode(true);
		var newRow = document.createElement("tr");
		for (let i = 0; i < 5; i++) {
			newRow.appendChild(document.createElement("td"));
		}
		newRow.id = "newRow";
		// newRow.cells[0].querySelector("input").checked = true;
		// newRow.cells[0].innerHTML = `<button class="apply" onclick="insertNewCombi(this)" disabled>Apply</button>`;
		newRow.cells[0].innerHTML = `<div class="buttons">
									<button class="apply" onclick="insertNewCombi(this)" disabled>
										<img src="/static/valid.svg" width="12" height="12" alt="Delete">
									</button>
									<button class="delete" onclick="deleteNewCombi(this)">
										<img src="/static/delete.svg" width="12" height="12" alt="Delete">
									</button>
									</div>
									`;

		newRow.cells[1].innerHTML = `<select name="hardwareprofile">
									<option value="" selected disabled hidden>Choose Hardware Profile</option>
									${hwpsOptions}
									</select>`;
		newRow.cells[2].innerHTML = `<select name="simulatorprofile">
									<option value="" selected disabled hidden>Choose Simulator</option>
									${simsOptions}
									</select>`;
		newRow.cells[3].innerHTML = `<select name="simulatorversion">
									<option value="" selected disabled hidden>Choose Version</option>
									</select>`;
		newRow.cells[4].innerText = "0/" + this.getAttribute("data-n-runs");

		tbody.appendChild(newRow);
		stripeTable();
		document.querySelector('select[name="hardwareprofile"]').addEventListener("change", function () {
			selectCombinations(this, this.value);
		});
		document.querySelector('select[name="simulatorprofile"]').addEventListener("change", function () {
			selectCombinations(this, undefined, this.value);
		});
		document.querySelector('select[name="simulatorversion"]').addEventListener("change", function () {
			selectCombinations(this, undefined, undefined, this.value);
		});
		// disbale the button after it is clicked, till the new row is applied
		this.disabled = true;
	});

	// Makes sure that only combinations can be chosen that are not already present in the table
	function selectCombinations(select, hwp = null, sim = null, simVersion = null) {
		let somethingChanged = false;
		console.log("before", selectedHwp, selectedSim, selectedSimVersion);

		if (hwp != null && hwp !== selectedHwp) {
			selectedHwp = hwp;
			somethingChanged = true;
		}
		if (sim != null && sim !== selectedSim) {
			selectedSim = sim;
			selectedSimVersion = "";
			document.querySelector('select[name="simulatorversion"]').innerHTML = "";
			document.querySelector(
				'select[name="simulatorversion"]'
			).innerHTML = `<option value="" selected disabled hidden>Choose Version</option>`;
			for (const filteredSim of hwps_sims.sims.filter((sim) => sim.name === selectedSim)) {
				document.querySelector(
					'select[name="simulatorversion"]'
				).innerHTML += `<option value="${filteredSim.version}">${filteredSim.version}</option>`;
			}
			somethingChanged = true;
		}
		if (simVersion != null && simVersion !== selectedSimVersion) {
			selectedSimVersion = simVersion;
			somethingChanged = true;
		}

		let n_selected = 0;
		if (selectedHwp !== "") {
			n_selected++;
		}
		if (selectedSim !== "") {
			n_selected++;
		}
		if (selectedSimVersion !== "") {
			n_selected++;
		}

		console.log(selectedHwp, selectedSim, selectedSimVersion);

		if (n_selected >= 2 && somethingChanged) {
			// Get already chosen combinations
			const usedCombinations = [];
			document.querySelectorAll(".run-checkbox").forEach((checkbox) => {
				usedCombinations.push([
					checkbox.getAttribute("data-hwp-name"),
					checkbox.getAttribute("data-simulator"),
					checkbox.getAttribute("data-simulator-version"),
				]);
			});
			console.log(usedCombinations);
			const matchingCombinations = usedCombinations.filter(([hwpName, simulator, simulatorVersion]) => {
				if (selectedHwp === "" && selectedSim !== "" && selectedSimVersion !== "") {
					return simulator === selectedSim && simulatorVersion === selectedSimVersion;
				} else if (selectedHwp !== "" && selectedSim !== "" && selectedSimVersion === "") {
					return hwpName === selectedHwp && simulator === selectedSim;
				} else if (selectedHwp !== "" && selectedSim !== "" && selectedSimVersion !== "") {
					return hwpName === selectedHwp && simulator === selectedSim && simulatorVersion === selectedSimVersion;
				}
			});
			document.querySelectorAll("#newRow select option").forEach((option) => {
				option.disabled = false;
			});
			if (selectedHwp === "" && selectedSim !== "" && selectedSimVersion !== "") {
				const matchingCombinations = usedCombinations.filter(([hwpName, simulator, simulatorVersion]) => {
					return simulator === selectedSim && simulatorVersion === selectedSimVersion;
				});

				for (const [hwpName, simulator, simulatorVersion] of matchingCombinations) {
					document.querySelector(`select[name="hardwareprofile"] option[value="${hwpName}"]`).disabled = true;
				}
			} else if (selectedHwp !== "" && selectedSim !== "" && selectedSimVersion === "") {
				const matchingCombinations = usedCombinations.filter(([hwpName, simulator, simulatorVersion]) => {
					return hwpName === selectedHwp && simulator === selectedSim;
				});
				for (const [hwpName, simulator, simulatorVersion] of matchingCombinations) {
					document.querySelector(`select[name="simulatorversion"] option[value="${simulatorVersion}"]`).disabled = true;
				}
			} else if (selectedHwp !== "" && selectedSim !== "" && selectedSimVersion !== "") {
				const matchingCombinations1 = usedCombinations.filter(([hwpName, simulator, simulatorVersion]) => {
					return simulator === selectedSim && simulatorVersion === selectedSimVersion;
				});

				for (const [hwpName, simulator, simulatorVersion] of matchingCombinations1) {
					document.querySelector(`select[name="hardwareprofile"] option[value="${hwpName}"]`).disabled = true;
				}

				const matchingCombinations2 = usedCombinations.filter(([hwpName, simulator, simulatorVersion]) => {
					return hwpName === selectedHwp && simulator === selectedSim;
				});
				for (const [hwpName, simulator, simulatorVersion] of matchingCombinations2) {
					document.querySelector(`select[name="simulatorversion"] option[value="${simulatorVersion}"]`).disabled = true;
				}
			}
			//enable the apply button if all three values are selected
			if (selectedHwp !== "" && selectedSim !== "" && selectedSimVersion !== "") {
				select.closest("tr").querySelector("button.apply").disabled = false;
			}
		}
	}
});

function insertNewCombi(button) {
	// Find the parent row of the clicked button
	const row = button.closest("tr");
	row.removeAttribute("id");

	// Extract selected values and text from the dropdowns in this row
	const hardwareSelect = row.querySelector('select[name="hardwareprofile"]');
	const simulatorSelect = row.querySelector('select[name="simulatorprofile"]');
	const simulatorVersionSelect = row.querySelector('select[name="simulatorversion"]');
	const hardwareProfile = hardwareSelect.options[hardwareSelect.selectedIndex];
	const simulatorProfile = simulatorSelect.options[simulatorSelect.selectedIndex];
	const simulatorVersion = simulatorVersionSelect.options[simulatorVersionSelect.selectedIndex];

	console.log(hardwareProfile.value, simulatorProfile.value, simulatorVersion.value);
	// Replace the dropdowns with the selected values
	row.cells[0].innerHTML =
		`<input type="checkbox" class="run-checkbox"` +
		`data-hwp-name="${hardwareProfile.value}"` +
		`data-simulator="${simulatorProfile.value}"` +
		`data-simulator-version="${simulatorVersion.value}"` +
		`data-simulator-id="${simulatorProfile.getAttribute("data-simulator-id")}">`;
	row.cells[0].querySelector("input").checked = true;
	row.cells[1].innerText = hardwareProfile.value;
	row.cells[1].classList.add("hardware_profile_name");
	row.cells[2].innerText = simulatorProfile.value;
	row.cells[2].classList.add("simulator_name");
	row.cells[3].innerText = simulatorVersion.value;
	row.cells[3].classList.add("simulator_version");

	document.getElementById("add-hardwareprofile").disabled = false;
	selectedHwp = "";
	selectedSim = "";
	selectedSimVersion = "";
}

function deleteNewCombi(button) {
	const row = button.closest("tr");
	// Enable the "Add Hardware Profile" button
	document.getElementById("add-hardwareprofile").disabled = false;
	row.remove();
}

function stripeTable() {
	const rows = document.querySelectorAll("#computed_overview table tr");
	rows.forEach((row, index) => {
		row.classList.remove("even", "odd");
		row.classList.add(index % 2 === 0 ? "odd" : "even");
	});
}

function sentCheckedEntries(e) {
	e.preventDefault()
	if (!hwps_uptodate) {
		alert("Hardwareprofiles List is not up to date. Make sure you know what your doing!");
		return;
	}

	const qubitsMin = document.querySelector('input[name="qubits_range_min"]').value;
    const qubitsMax = document.querySelector('input[name="qubits_range_max"]').value;
    const depthMin = document.querySelector('input[name="depth_range_min"]').value;
    const depthMax = document.querySelector('input[name="depth_range_max"]').value;
    const shotsMin = document.querySelector('input[name="shots_range_min"]').value;
    const shotsMax = document.querySelector('input[name="shots_range_max"]').value;
    const evalMin = document.querySelector('input[name="eval_range_min"]').value;
    const evalMax = document.querySelector('input[name="eval_range_max"]').value;

	if (qubitsMin > qubitsMax) {
		alert("Minimum qubits is bigger than maximum qubits");
		return;
	}
	if (depthMin > depthMax) {
		alert("Minimum depth is bigger than maximum depth");
		return;
	}
	if (shotsMin > shotsMax) {
		alert("Minimum shots is bigger than maximum shots");
		return;
	}
	if (evalMin > evalMax) {
		alert("Minimum eval is bigger than maximum eval");
		return;
	}

	// Stores tuples of (hwp_id, simulator_id) for checked checkboxes
	const checkedEntries = [];
	const hwps = [];
	document.querySelectorAll(".run-checkbox").forEach((checkbox) => {
		if (checkbox.checked) {
			const hwp_name = checkbox.getAttribute("data-hwp-name");
			checkedEntries.push([hwp_name, checkbox.getAttribute("data-simulator"). checkbox.getAttribute("data-simulator-version"), checkbox.getAttribute("data-simulator-data-simulator-id")]);
			hwps.push(hwp_name);
		}
	});

	if (checkedEntries.length === 0) {
		alert("No Hardwareprofiles selected");
		return;
	}

	console.log(checkedEntries);

	fetch("/simulation/select_environments/", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"X-CSRFToken": getCookie("csrftoken"), // Ensure CSRF token is sent; see note below
		},
		body: JSON.stringify({ hwps: hwps}),
	})
		.then((response) => response.json())
		.then((data) => {
			
			// TODO: Popup window with password, totp prompt 

			fetch("/simulation/submit_request/", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFToken": getCookie("csrftoken"), // Ensure CSRF token is sent; see note below
				},
				body: JSON.stringify({ checkedEntries: checkedEntries,
					qubitsMin: qubitsMin,
					qubitsMax: qubitsMax,
					depthMin: depthMin,
					depthMax: depthMax,
					shotsMin: shotsMin,
					shotsMax: shotsMax,
					evalMin: evalMin,
					evalMax: evalMax,
					recalculate: document.querySelector('input[name="recalculate"]').checked,
				}),
			})

		})
		.then(response => {
			if (response) {
				return response.json();
			}
		})
		.then(data => {
			if (data) {
				console.log("Success");
			}
		})
		.catch((error) => console.error("Error:", error));
}

function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== "") {
		const cookies = document.cookie.split(";");
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === name + "=") {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}