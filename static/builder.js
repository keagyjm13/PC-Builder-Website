document.addEventListener("DOMContentLoaded", function () {
    const selections = {}; // user selections


    // make only compatible parts able to be selected
    function fetchAndUpdateCompatibility() {
        const currentSelections = getSelections();

        fetch("/get_compatible_parts", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(currentSelections)
        })
        .then(response => response.json())
        .then(data => {
            // all parts available if no selections (edge)
            if (Object.keys(data).length === 0) {
                document.querySelectorAll(".part-selector").forEach(select => {
                    Array.from(select.options).forEach(option => {
                        option.hidden = false;
                    });
                });
                return;
            }

            // compatability filtering
            Object.keys(data).forEach(cat => {

                const dropdown = document.querySelector(`[data-category="${cat}"]`);
                const selected = dropdown.value;
                const compatibleParts = data[cat];

                Array.from(dropdown.options).forEach(option => {
                    if (option.value === "" || option.value === selected) {
                        option.hidden = false;
                    } else {
                        option.hidden = !compatibleParts.includes(option.value);
                    }
                });
            });


        });
    }

    // get current selections
    function getSelections() {
        return selections;
    }

    // display selected parts specs
    function updateSpecsDisplay(category, selectedValue) {
        const dropdown = document.querySelector(`[data-category="${category}"]`);
        const selectedOption = Array.from(dropdown.options).find(option => option.value === selectedValue);
    
        // make div id = category-specs for each category
        const specsContainer = document.querySelector(`#${category}-specs`);
        specsContainer.innerHTML = "";
    

        // edgecase
        if (!selectedOption) return;
    
        // all have price
        const price = selectedOption.getAttribute("data-price");
        const priceElement = document.createElement("p");
        priceElement.innerHTML = `<strong>Price:</strong> $${price}`;
        specsContainer.appendChild(priceElement);
    
        // core-count, clock-count, boost-clock are the first three attributes following price (different for each part)
        switch (category) {
            case "cpu":
                appendSpec(specsContainer, "Core Count", selectedOption.getAttribute("data-core-count") + " cores");
                appendSpec(specsContainer, "Base Clock", selectedOption.getAttribute("data-core-clock") + " MHz");
                appendSpec(specsContainer, "Boost Clock", selectedOption.getAttribute("data-boost-clock") + " MHz");
                break;

            case "cpu_cooler":
                appendSpec(specsContainer, "Fan RPM", selectedOption.getAttribute("data-core-count"));
                appendSpec(specsContainer, "Noise Level", selectedOption.getAttribute("data-core-clock") + " dBA");
                appendSpec(specsContainer, "Radiator Size", selectedOption.getAttribute("data-boost-clock") + " mm");
                break;

            case "motherboard":
                appendSpec(specsContainer, "CPU Socket", selectedOption.getAttribute("data-core-count"));
                appendSpec(specsContainer, "Max Memory", selectedOption.getAttribute("data-core-clock") + " GB");
                appendSpec(specsContainer, "Form Factor", selectedOption.getAttribute("data-boost-clock"));
                break;

            case "memory":
                appendSpec(specsContainer, "Speed", selectedOption.getAttribute("data-core-count") + " MHz");
                appendSpec(specsContainer, "Modules", selectedOption.getAttribute("data-core-clock"));
                appendSpec(specsContainer, "CAS Latency", selectedOption.getAttribute("data-boost-clock"));
                break;

            case "storage":
                appendSpec(specsContainer, "Capacity", selectedOption.getAttribute("data-core-count"));
                appendSpec(specsContainer, "Type", selectedOption.getAttribute("data-core-clock"));
                appendSpec(specsContainer, "Interface", selectedOption.getAttribute("data-boost-clock"));
                break;

            case "video_card":
                appendSpec(specsContainer, "Chipset", selectedOption.getAttribute("data-core-count"));
                appendSpec(specsContainer, "Memory", selectedOption.getAttribute("data-core-clock") + " GB");
                appendSpec(specsContainer, "Boost Clock", selectedOption.getAttribute("data-boost-clock") + " MHz");
                break;

            case "pc_case":
                appendSpec(specsContainer, "Type", selectedOption.getAttribute("data-core-count"));
                appendSpec(specsContainer, "Side Panel", selectedOption.getAttribute("data-core-clock"));
                appendSpec(specsContainer, "Volume", selectedOption.getAttribute("data-boost-clock") + " L");
                break;

            case "power_supply":
                appendSpec(specsContainer, "Wattage", selectedOption.getAttribute("data-core-count") + " W");
                appendSpec(specsContainer, "Efficiency", selectedOption.getAttribute("data-core-clock"));
                appendSpec(specsContainer, "Modular", selectedOption.getAttribute("data-boost-clock"));
                break;

            case "operating_system":
                appendSpec(specsContainer, "Mode", selectedOption.getAttribute("data-core-count"));
                appendSpec(specsContainer, "Max Memory", selectedOption.getAttribute("data-core-clock") + " " + selectedOption.getAttribute("data-boost-clock"));
                break;


        }
    
        // add new spec to category
        function appendSpec(container, label, value) {
            if (value && value !== "null" && value !== "undefined") {
                const el = document.createElement("p");
                el.innerHTML = `<strong>${label}:</strong> ${value}`;
                container.appendChild(el);

    
            }
        }
    }

    // update dropdowns with selections
    document.querySelectorAll(".part-selector").forEach(select => {
        select.addEventListener("change", function () {
            const category = this.dataset.category;
            const selectedValue = this.value;

            if (selectedValue === "") {
                // user reset drop
                delete selections[category];
            } else {
                selections[category] = selectedValue;
            }


        
            // update specs for selection
            updateSpecsDisplay(category, selectedValue);

            // update compatibility for selection
            fetchAndUpdateCompatibility();
        });
    });

        // get total price ffrom build
    function calculateTotalPrice(selectedParts) {
        let totalPrice = 0;

        // sum part prices
        Object.keys(selectedParts).forEach(category => {
            const priceKey = `${category}_price`;
            if (selectedParts[priceKey]) {
                totalPrice += parseFloat(selectedParts[priceKey]); //update total price by adding part price if exists
            }
        });

        return totalPrice.toFixed(2);  // 2 dec points for $
    }

    // final build handler
    document.querySelector("#complete-build").addEventListener("click", function () {
        const selectedParts = {};
        document.querySelectorAll(".part-selector").forEach(select => {
            const category = select.dataset.category;
            const selectedValue = select.value;
            if (selectedValue) {
                selectedParts[category] = selectedValue;


                // tried handling extra spec for cpu -- implement post proj most likely
                // how to make an effective table showing specs?? maybe just leabe in dropdowns
                if (category === 'cpu') {
                    const selectedOption = select.options[select.selectedIndex];
                    const cpuPrice = selectedOption.getAttribute("data-price");
                    const cpuCoreCount = selectedOption.getAttribute("data-core-count");
                    const cpuCoreClock = selectedOption.getAttribute("data-core-clock");
                    const cpuBoostClock = selectedOption.getAttribute("data-boost-clock");


                    selectedParts['cpu_price'] = cpuPrice;
                    selectedParts['cpu_core_count'] = cpuCoreCount;
                    selectedParts['cpu_core_clock'] = cpuCoreClock;
                    selectedParts['cpu_boost_clock'] = cpuBoostClock;
                }


                if (category === 'cpu_cooler') {
                    const selectedOption = select.options[select.selectedIndex];
                    const cpuCoolerPrice = selectedOption.getAttribute("data-price");

                    selectedParts['cpu_cooler_price'] = cpuCoolerPrice;
                }

                if (category === 'motherboard') {
                    const selectedOption = select.options[select.selectedIndex];
                    const moboPrice = selectedOption.getAttribute("data-price");

                    selectedParts['motherboard_price'] = moboPrice;
                }

                if (category === 'memory') {
                    const selectedOption = select.options[select.selectedIndex];
                    const memPrice = selectedOption.getAttribute("data-price");

                    selectedParts['memory_price'] = memPrice;
                }

                if (category === 'storage') {
                    const selectedOption = select.options[select.selectedIndex];
                    const storagePrice = selectedOption.getAttribute("data-price");

                    selectedParts['storage_price'] = storagePrice;
                }

                if (category === 'video_card') {
                    const selectedOption = select.options[select.selectedIndex];
                    const gpuPrice = selectedOption.getAttribute("data-price");

                    selectedParts['video_card_price'] = gpuPrice;
                }

                if (category === 'pc_case') {
                    const selectedOption = select.options[select.selectedIndex];
                    const casePrice = selectedOption.getAttribute("data-price");

                    selectedParts['pc_case_price'] = casePrice;
                }

                if (category === 'power_supply') {
                    const selectedOption = select.options[select.selectedIndex];
                    const psuPrice = selectedOption.getAttribute("data-price");

                    selectedParts['power_supply_price'] = psuPrice;
                }

                if (category === 'operating_system') {
                    const selectedOption = select.options[select.selectedIndex];
                    const osPrice = selectedOption.getAttribute("data-price");

                    selectedParts['operating_system_price'] = osPrice;
                }
            }
        });

        // need a total price for user
        const totalPrice = calculateTotalPrice(selectedParts);
        selectedParts['total_price'] = totalPrice;

        console.log("Selected Parts: ", selectedParts); // debug


        fetch("/save_build", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(selectedParts)
        })

        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = "/checkout";  // success! go to checkout
            } else {
                alert(data.error || "Something went wrong, please try again.");
            }
        })
        .catch(error => {
            console.error("Error saving build:", error);
            alert("An error occurred while saving the build. Please try again.");
        });
    });
    


    // reset button, quick start over
    document.querySelector("#reset-build").addEventListener("click", function () {
        // destruct selections ob
        Object.keys(selections).forEach(category => {
            delete selections[category];
        });

        // reset dropdowns
        document.querySelectorAll(".part-selector").forEach(select => {
            select.value = "";
        });

        // reset compatibility (no selections, no compatibility issues)
        document.querySelectorAll(".part-selector").forEach(select => {
            Array.from(select.options).forEach(option => {
                option.disabled = false;
            });
        });


        // reset specs display (dont show specs when no selections)
        document.querySelectorAll(".price-specs").forEach(info => {
            info.innerHTML = ""; //clears info
        });

        // update to the reset compatibility so all parts are available again
        fetchAndUpdateCompatibility();
    });



    // fetch compatibility on first load
    fetchAndUpdateCompatibility();
});
