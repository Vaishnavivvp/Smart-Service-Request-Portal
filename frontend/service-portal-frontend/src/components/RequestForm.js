import { useState } from "react";
import API from "../api";

function RequestForm() {
  const [form, setForm] = useState({
    title: "",
    category: "",
    description: "",
    priority: "",
  });

  const handleSubmit = async () => {
    await API.post("/requests", null, { params: form });
    alert("Request Submitted!");
    window.location.reload();
  };

  return (
    <div className="white-card">

      <h2>Create Request</h2>

      <input placeholder="Title" onChange={(e) => setForm({...form, title: e.target.value})} />
      <input placeholder="Category" onChange={(e) => setForm({...form, category: e.target.value})} />
      <input placeholder="Description" onChange={(e) => setForm({...form, description: e.target.value})} />
      <select onChange={(e) => setForm({...form, priority: e.target.value})}>
        <option value="">Select Priority</option>
        <option>Low</option>
        <option>Medium</option>
        <option>High</option>
      </select>

      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}

export default RequestForm;
