import { useEffect, useState } from "react";
import API from "../api";

function RequestList() {
  const [requests, setRequests] = useState([]);
  const role = localStorage.getItem("role");

  useEffect(() => {
    fetchRequests();
  }, []);

  const fetchRequests = async () => {
    const res = await API.get("/requests");
    setRequests(res.data);
  };

  const updateStatus = async (id, status) => {
    await API.put(`/requests/${id}/status`, null, {
      params: { new_status: status },
    });
    fetchRequests();
  };

  return (
    <div>
      <h2 style={{ color: "white" }}>All Requests</h2>
      {requests.map((req) => (
        <div key={req.id} className="request-card">
          <h4>{req.title}</h4>
          <p>{req.description}</p>
          <p>Status: {req.status}</p>

          {role === "admin" && (
            <div className="admin-buttons"> 
              <button onClick={() => updateStatus(req.id, "In Progress")}>In Progress</button>
              <button onClick={() => updateStatus(req.id, "Resolved")}>Resolved</button>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default RequestList;
