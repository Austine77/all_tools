function checkResume() {
    let file = document.getElementById("resume").files[0];
    let formData = new FormData();
    formData.append("resume", file);

    fetch("/resume-check", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("resumeResult").textContent =
            JSON.stringify(data, null, 2);
    });
}
