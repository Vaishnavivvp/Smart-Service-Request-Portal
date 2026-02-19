import { useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.clear();
    navigate("/");
  };

  return (
    <div className="navbar">
      <h3>Smart Service Request Portal</h3>
      <button onClick={logout}>Logout</button>
    </div>
  );
}

export default Navbar;
