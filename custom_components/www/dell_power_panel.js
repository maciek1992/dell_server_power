class DellPowerPanel extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: "open" });
    }

    set hass(hass) {
        if (!this.content) {
            this.content = document.createElement("div");
            this.content.innerHTML = `
                <style>
                    .container { padding: 16px; }
                    h1 { font-size: 20px; }
                    .chart-container { width: 100%; height: 300px; }
                </style>
                <div class="container">
                    <h1>Zużycie Energii Serwera</h1>
                    <p><strong>Bieżące zużycie:</strong> <span id="currentPower">Ładowanie...</span></p>
                    <p><strong>Koszt dzienny:</strong> <span id="dailyCost">Ładowanie...</span> PLN</p>
                    <p><strong>Koszt miesięczny:</strong> <span id="monthlyCost">Ładowanie...</span> PLN</p>
                    <p><strong>Całkowite zużycie:</strong> <span id="totalEnergy">Ładowanie...</span> kWh</p>
                    <p><strong>Całkowity koszt:</strong> <span id="totalCost">Ładowanie...</span> PLN</p>
                    <canvas id="powerChart"></canvas>
                </div>
            `;
            this.shadowRoot.appendChild(this.content);
        }

        const powerEntity = hass.states["sensor.dell_server_power_usage"];
        if (!powerEntity) {
            return;
        }

        // Aktualizacja wartości w interfejsie
        this.shadowRoot.getElementById("currentPower").textContent = powerEntity.state + " W";
        this.shadowRoot.getElementById("dailyCost").textContent = powerEntity.attributes.daily_cost;
        this.shadowRoot.getElementById("monthlyCost").textContent = powerEntity.attributes.monthly_cost;
        this.shadowRoot.getElementById("totalEnergy").textContent = powerEntity.attributes.total_energy_kwh;
        this.shadowRoot.getElementById("totalCost").textContent = powerEntity.attributes.total_cost;

        // Aktualizacja wykresu
        this.drawChart(powerEntity);
    }

    drawChart(powerEntity) {
        setTimeout(() => {
            const ctx = this.shadowRoot.getElementById("powerChart").getContext("2d");
            new Chart(ctx, {
                type: "line",
                data: {
                    labels: ["24h", "Miesiąc", "Cały okres"],
                    datasets: [{
                        label: "Zużycie energii (kWh)",
                        data: [
                            powerEntity.attributes.daily_cost / powerEntity.attributes.price_per_kwh,
                            powerEntity.attributes.monthly_cost / powerEntity.attributes.price_per_kwh,
                            powerEntity.attributes.total_energy_kwh
                        ],
                        backgroundColor: "rgba(54, 162, 235, 0.2)",
                        borderColor: "rgba(54, 162, 235, 1)",
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }, 500);
    }
}

customElements.define("dell-power-panel", DellPowerPanel);