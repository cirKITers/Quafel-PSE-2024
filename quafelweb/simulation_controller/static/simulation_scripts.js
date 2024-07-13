function sentCheckedEntries() {
	// Stores tuples of (hwp_id, simulator_id) for checked checkboxes
	const checkedEntries = [];
	document.querySelectorAll(".run-checkbox").forEach((checkbox) => {
		if (checkbox.checked) {
			checkedEntries.push([checkbox.getAttribute("data-hwp-name"), checkbox.getAttribute("data-simulator-id")]);
		}
	});
	console.log(checkedEntries);
	// Example: Sending 'checkedEntries' as JSON
	fetch("/simulation/select_environments/", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"X-CSRFToken": getCookie("csrftoken"), // Ensure CSRF token is sent; see note below
		},
		body: JSON.stringify({ checkedEntries: checkedEntries }),
	})
		// .then((response) => response.json())
		// .then((data) => console.log(data))
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

//hwps_sims containing all hardware profiles and simulators
let hwps_sims;

// Variables to store the selected values of the dropdowns, needed for selectCombinations
let selectedHwp = "";
let selectedSim = "";
let selectedSimVersion = "";

// Add event listener when the document is loaded
document.addEventListener("DOMContentLoaded", function () {
	stripeTable();

	// Submit button sends checked entries
	document.getElementById("btn_submit").addEventListener("click", sentCheckedEntries);

	// Master Checkbox switches all other
	document.querySelector('#table_header input[type="checkbox"]').addEventListener("change", function () {
		var slaveCheckboxes = document.querySelectorAll('#computed_overview tr input[type="checkbox"]');

		// Step 4: Toggle the state of the slave checkboxes
		var isChecked = this.checked;
		slaveCheckboxes.forEach(function (checkbox) {
			checkbox.checked = isChecked;
		});
	});

	hwps_sims = JSON.parse(document.getElementById("add-hardwareprofile").getAttribute("data-hwps-sims"));

	// Add event listener to the "Add Hardware Profile" button
	document.getElementById("add-hardwareprofile").addEventListener("click", function () {
		//TODO: Maybe not doing it with fetch, instead getting the information from the html, where it is stored in data-* form django context.
		console.log(hwps_sims);
		//TODO: Add logic so already present combinations are not added again
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
		var newRow = tbody.rows[tbody.rows.length - 1].cloneNode(true);
		newRow.id = "newRow";
		// newRow.cells[0].querySelector("input").checked = true;
		newRow.cells[0].innerHTML = `<button class="apply" onclick="insertNewCombi(this)" disabled>Apply</button>`;

		newRow.cells[1].innerHTML = `<select name="hardwareprofile">
									<option value="" selected disabled hidden>Choose Hardware Profile</option>
									${hwpsOptions}
									</select>`;
		newRow.cells[2].innerHTML = `<select name="simulatorprofile">
									<option value="" selected disabled hidden>Choose Simulator</option>
									${simsOptions}
									</select>`;
		newRow.cells[3].innerHTML = `<select name="simulatorversion">
									<option value="" selected disabled hidden>Choose Sim Version</option>
									</select>`;
		newRow.cells[4].innerText = newRow.cells[4].innerText.replace(/\d+/, "0");
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
			somethingChanged = true;
		}
		if (simVersion != null && simVersion !== selectedSimVersion) {
			selectedSimVersion = simVersion;
			somethingChanged = true;
		}

		console.log(selectedHwp, selectedSim, selectedSimVersion);

		if (somethingChanged) {
			// Get already chosen combinations
			const usedCombinations = [];
			document.querySelectorAll(".run-checkbox").forEach((checkbox) => {
				usedCombinations.push([
					checkbox.getAttribute("data-hwp-name"),
					checkbox.getAttribute("data-simulator"),
					checkbox.getAttribute("data-simulator-version"),
				]);
			});
			const matchingCombinations = usedCombinations.filter(([hwpName, simulator, simulatorVersion]) => {
				if (selectedHwp === "") {
					if (selectedSim !== "" && selectedSimVersion !== "") {
						console.log("Schwanz");
						return simulator === selectedSim && simulatorVersion === selectedSimVersion;
					} else if (selectedSim !== "") {
						// && selectedSimVersion === ""
					}
				} else if (selectedSim !== "") {
					// && selectedSimVersion === ""
					return hwpName === selectedHwp && simulator === selectedSim;
				}
			});
			console.log(matchingCombinations);

			// Enable all options
			document.querySelectorAll("#newRow select option").forEach((option) => {
				option.disabled = false;
			});

			if (selectedHwp === "") {
				// if already a sim and sim version is selected, then disable all combinations with this sim and sim version and hwps which already are in the table
				if (selectedSim !== "" && selectedSimVersion !== "") {
					for (const [hwpName, simulator, simulatorVersion] of matchingCombinations) {
						document.querySelector(`select[name="hardwareprofile"] option[value="${hwpName}"]`).disabled = true;
					}
				}
				// only sim is selected, then list the versions of the selected sim
				else if (selectedSim !== "") {
					//selectedSimVersion === ""
					document.querySelector(
						'select[name="simulatorversion"]'
					).innerHTML = `<option value="" selected disabled hidden>Choose Version</option>`;
					for (const filteredSim of hwps_sims.sims.filter((sim) => sim.name === selectedSim)) {
						document.querySelector(
							'select[name="simulatorversion"]'
						).innerHTML += `<option value="${filteredSim.version}">${filteredSim.version}</option>`;
					}
				}
			}
			// hwp and sim are selected, then list the versions of the selected sim, disable all combinations with this sim and sim version and hwps which already are in the table
			else if (selectedSim !== "") {
				//&& selectedHwp !== ""
				if (selectedSimVersion === "") {
					document.querySelector(
						'select[name="simulatorversion"]'
					).innerHTML = `<option value="" selected disabled hidden>Choose Version</option>`;
					for (const filteredSim of hwps_sims.sims.filter((sim) => sim.name === selectedSim)) {
						document.querySelector(
							'select[name="simulatorversion"]'
						).innerHTML += `<option value="${filteredSim.version}">${filteredSim.version}</option>`;
					}
					for (const [hwpName, simulator, simulatorVersion] of matchingCombinations) {
						document.querySelector(`select[name="simulatorversion"] option[value="${simulatorVersion}"]`).disabled = true;
					}
				}
				else{

				}
			}

			//enable the apply button if all three values are selected
			if ((selectedHwp !== "", selectedSim !== "", selectedSimVersion !== "")) {
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

function stripeTable() {
	const rows = document.querySelectorAll("#computed_overview table tr");
	rows.forEach((row, index) => {
		row.classList.remove("even", "odd");
		row.classList.add(index % 2 === 0 ? "odd" : "even");
	});
}
