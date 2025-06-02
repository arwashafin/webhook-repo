function formatEvent(event) {
    console.log("Event:", event); // <== Add this
    const ts = new Date(event.timestamp).toUTCString();
    if (event.type === "PUSH") {
        return `${event.author} pushed to ${event.to_branch} on ${ts}`;
    } else if (event.type === "PULL_REQUEST") {
        return `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${ts}`;
    } else if (event.type === "MERGE") {
        return `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${ts}`;
    }
}

function loadEvents() {
    fetch("/events")
        .then(res => res.json())
        .then(events => {
            const container = document.getElementById("events");
            container.innerHTML = "";
            events.forEach(e => {
                const div = document.createElement("div");
                div.className = "event";
                div.textContent = formatEvent(e);
                container.appendChild(div);
            });
        });
}

setInterval(loadEvents, 15000);
window.onload = loadEvents;
