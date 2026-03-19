
const API = "http://127.0.0.1:8001";

// -------- PREVIEW --------
function preview() {
  const file = document.getElementById("file").files[0];
  if (!file) return;

  const img = document.getElementById("previewImg");
  img.src = URL.createObjectURL(file);
  img.classList.remove("hidden");

  document.getElementById("output").innerHTML = "";
  document.getElementById("registerSection").classList.add("hidden");

  document.getElementById("uploadText").innerText = file.name;

  // clear form
  document.getElementById("name").value = "";
  document.getElementById("gender").value = "";
  document.getElementById("comments").value = "";
}

// -------- RECOGNIZE --------
async function recognize() {
  const file = document.getElementById("file").files[0];
  if (!file) return alert("Upload image");

  const btn = document.getElementById("recognizeBtn");

  btn.disabled = true;
  btn.innerText = "Processing...";
  document.getElementById("output").innerHTML = "Processing...";

  const form = new FormData();
  form.append("file", file);

  try {
    const res = await fetch(`${API}/recognize`, {
      method: "POST",
      body: form
    });

    const data = await res.json();
    display(data);

    if (data.status === "unknown") {
      document.getElementById("registerSection").classList.remove("hidden");
    } else {
      document.getElementById("registerSection").classList.add("hidden");
    }

  } catch (err) {
    alert("Error during recognition");
  }

  btn.disabled = false;
  btn.innerText = "Recognize";
}

// -------- REGISTER --------
async function register() {
  const file = document.getElementById("file").files[0];
  const name = document.getElementById("name").value;
  const gender = document.getElementById("gender").value;
  const comments = document.getElementById("comments").value;

  if (!file || !name) return alert("Missing fields");

  const btn = document.getElementById("registerBtn");

  btn.disabled = true;
  btn.innerText = "Processing...";

  const form = new FormData();
  form.append("file", file);
  form.append("name", name);
  form.append("gender", gender);
  form.append("comments", comments);

  try {
    const res = await fetch(`${API}/register`, {
      method: "POST",
      body: form
    });

    const data = await res.json();
    display(data);

    // clear form
    document.getElementById("name").value = "";
    document.getElementById("gender").value = "";
    document.getElementById("comments").value = "";

    document.getElementById("registerSection").classList.add("hidden");

  } catch (err) {
    alert("Error during registration");
  }

  btn.disabled = false;
  btn.innerText = "Register";
}

// -------- DISPLAY --------
function display(data) {
  let html = "";

  if (data.status === "recognized") {
    html = `
      <div class="title success">Recognized</div>

      <div class="row"><span>ID</span><span>${data.subject_id}</span></div>
      <div class="row"><span>Name</span><span>${data.name || "N/A"}</span></div>
      <div class="row"><span>Gender</span><span>${data.gender || "N/A"}</span></div>
      <div class="row"><span>Age</span><span>${data.age || "N/A"}</span></div>
      <div class="row"><span>Comments</span><span>${data.comments || "N/A"}</span></div>

      <div class="confidence">Confidence: ${(data.similarity * 100).toFixed(1)}%</div>
    `;
  } 
  else if (data.status === "unknown") {
    html = `
      <div class="title warning">Unknown Person</div>
      <div>Please fill details to register</div>
    `;
  } 
  else if (data.status === "registered_new_user") {
    html = `
      <div class="title success">User Registered</div>
      <div class="row"><span>Name</span><span>${data.name}</span></div>
      <div class="row"><span>ID</span><span>${data.subject_id}</span></div>
    `;
  }
  else if (data.status === "image_added_existing_user") {
    html = `
      <div class="title success">Image Added</div>
      <div class="row"><span>User</span><span>${data.name}</span></div>
    `;
  }
  else if (data.status === "duplicate_image") {
    html = `
      <div class="title warning">Duplicate Image</div>
      <div class="row"><span>User</span><span>${data.name}</span></div>
    `;
  }
  else {
    html = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
  }

  document.getElementById("output").innerHTML = html;
}
