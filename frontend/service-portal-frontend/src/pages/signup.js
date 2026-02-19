import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../api";

function Signup() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSignup = async () => {
    try {
      await API.post("/signup", null, {
        params: { name, email, password },
      });
      alert("Registered Successfully!");
      navigate("/");
    } catch {
      alert("Signup failed");
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h2>Create Account</h2>

        <input placeholder="Name" onChange={(e) => setName(e.target.value)} />
        <input placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
        <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />

        <button onClick={handleSignup}>Signup</button>

        <p style={{ textAlign: "center", marginTop: "10px" }}>
          Already have account? <Link to="/" style={{ color: "white" }}>Login</Link>
        </p>
      </div>
    </div>
  );
}

export default Signup;
