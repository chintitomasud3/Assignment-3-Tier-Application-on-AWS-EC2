const API = "/api"; // nginx route

// ---------------- CREATE USER ----------------
document.getElementById("userForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        age: document.getElementById("age").value
            ? Number(document.getElementById("age").value)
            : null
    };

    const res = await fetch(API + "/users", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await res.json();

    document.getElementById("result").innerHTML =
        "<pre>" + JSON.stringify(result, null, 2) + "</pre>";

    loadUsers();
});

// ---------------- LOAD USERS ----------------
async function loadUsers() {
    const res = await fetch(API + "/users");
    const users = await res.json();

    const list = document.getElementById("userList");
    list.innerHTML = "";

    users.forEach(u => {
        list.innerHTML += `
            <div class="user">
                <b>${u.name}</b> (${u.email})<br>
                Age: ${u.age ?? "N/A"}
            </div>
        `;
    });
}
