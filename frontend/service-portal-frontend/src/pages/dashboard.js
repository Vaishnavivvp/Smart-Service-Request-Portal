import Navbar from "../components/Navbar";
import RequestForm from "../components/RequestForm";
import RequestList from "../components/RequestList";

function Dashboard() {
    const role = localStorage.getItem("role");

  return (
    
    <>
      <Navbar />
      <div className="dashboard">
        {role!=="admin"&&<RequestForm />}
        <RequestList />
      </div>
    </>
  );
}

export default Dashboard;
