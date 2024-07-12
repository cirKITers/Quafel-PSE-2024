function sentCheckedEntries() {
	// Stores tuples of (hwp_id, simulator_id) for checked checkboxes
	const checkedEntries = [];
	document.querySelectorAll(".run-checkbox").forEach((checkbox) => {
		if (checkbox.checked) {
			checkedEntries.push([
				checkbox.getAttribute("data-hwp-id"),
				checkbox.getAttribute("data-simulator-id"),
			]);
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
				cookieValue = decodeURIComponent(
					cookie.substring(name.length + 1)
				);
				break;
			}
		}
	}
	return cookieValue;
}

// Add event listener when the document is loaded
document.addEventListener("DOMContentLoaded", function () {
    stripeTable()



	// Master Checkbox switches all other
	document
		.querySelector('#table_header input[type="checkbox"]')
		.addEventListener("change", function () {
			var slaveCheckboxes = document.querySelectorAll(
				'#computed_overview tr:not(:first-child) input[type="checkbox"]'
			);

			// Step 4: Toggle the state of the slave checkboxes
			var isChecked = this.checked;
			slaveCheckboxes.forEach(function (checkbox) {
				checkbox.checked = isChecked;
			});
		});

    // Add event listener to the "Add Hardware Profile" button
	document
		.getElementById("add-hardwareprofile")
		.addEventListener("click", function () {

            //TODO: Maybe not doing it with fetch, instead getting the information from the html, where it is stored in data-* form django context.
			fetch("/simulation/get_hardwareprofiles_simulators/", {
				method: "GET",
				headers: {
					"Content-Type": "application/json",
					// "X-CSRFToken": getCookie("csrftoken"), // Typically not needed for GET requests
				},
			})
				.then((response) => {
					if (!response.ok) {
						throw new Error("Network response was not ok");
					}
					return response.json();
				})
				.then((data) => {
					console.log(data);
                    //TODO: Add logic so already present combinations are not added again
					const hwpsOptions = data.hwps
						.map(
							(profile) =>
								`<option value="${profile.name}">${profile.name} - ${profile.description}</option>`
						)
						.join("");
					const simsOptions = data.sims
						.map(
							(profile) =>
								`<option data-simulator-id="${profile.id}" data-simulator-name="${profile.name}" data-simulator-version=${profile.version}>${profile.name} - ${profile.version}</option>`
						)
						.join("");

					var tbody = document.querySelector(
						"#computed_overview tbody"
					);
                    var newRow = tbody.rows[tbody.rows.length - 1].cloneNode(true);
					// newRow.cells[0].querySelector("input").checked = true;
					newRow.cells[0].innerHTML = `<button class="apply" onclick="insertNewCombi(this)">Apply</button>`;

					newRow.cells[1].innerHTML = `<select name="hardwareprofile">
                                                ${hwpsOptions}
                                                </select>`;
					newRow.cells[2].innerHTML = `<select name="simulatorprofile">
                                                ${simsOptions}
                                                </select>`;
					newRow.cells[3].innerHTML = "";
                    newRow.cells[4].innerText = newRow.cells[4].innerText.replace(/\d+/, "0");
					tbody.appendChild(newRow);
                    stripeTable()
				})
				.catch((error) => console.error("Error:", error));
		});
});


function insertNewCombi(button) {
    // Find the parent row of the clicked button
    const row = button.closest('tr');

    // Extract selected values and text from the dropdowns in this row
    const hardwareSelect = row.querySelector('select[name="hardwareprofile"]');
    const simulatorSelect = row.querySelector('select[name="simulatorprofile"]');
    const hardwareProfile = hardwareSelect.options[hardwareSelect.selectedIndex];
    const simulatorProfile = simulatorSelect.options[simulatorSelect.selectedIndex];

    

    // Replace the dropdowns with the selected values
    row.cells[0].innerHTML = `<input type="checkbox" class="run-checkbox" data-hwp-id="${hardwareProfile.value}" data-simulator-id="${simulatorProfile.getAttribute('data-simulator-id')}">`;
    row.cells[0].querySelector('input').checked = true;
    row.cells[1].innerText = hardwareProfile.value;
    row.cells[1].classList.add("hardware_profile_name");
    row.cells[2].innerText = simulatorProfile.getAttribute('data-simulator-name');
    row.cells[2].classList.add("simulator_name");
    row.cells[3].innerText = simulatorProfile.getAttribute('data-simulator-version');
    row.cells[3].classList.add("simulator_version");

}



function stripeTable() {
    const rows = document.querySelectorAll("#computed_overview table tr");
    rows.forEach((row, index) => {
    row.classList.remove('even', 'odd');
    row.classList.add(index % 2 === 0 ? 'odd' : 'even');
    });
}