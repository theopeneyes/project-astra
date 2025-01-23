import React ,{useEffect} from "react";
import { useAuth } from "../contexts/authContext";
import { useNavigate } from "react-router-dom";
import Cookies from "js-cookie"; // Optional: if you are using cookies for authentication
import { pageName } from "./common/pagesName";
import { useComponentName } from "./common/loadedComponentName";
import { goTo } from "./common/goTo";

const Dashboard = () => {
  const { isAuthenticated, logout } = useAuth();
  const { setComponentName } = useComponentName(pageName.dashboard);
  const navigate = useNavigate();

    useEffect(() => {
      setComponentName(pageName.dashboard);
    }, [])

  // const handelLogout = async () => {
  //   try {
  //     await logout(); 
  //     Cookies.remove("authData");
  //     navigate("/"); 
  //   } catch (error) {
  //     console.error("Error during logout:", error);
  //   }
  // };

  // const handelClick = (flag) => {
  //     if (flag == "/react-flow") {
  //       goTo(navigate, "/react-flow");
  //     }
  //   };

  return (
    <div>
      {/* <button onClick={() => handelClick("/react-flow")}> Go to ReactFlow</button> */}
      {/* <button onClick={handelLogout}>Logout</button> */}
      <h2>Dashboard</h2>
      {isAuthenticated ? (
        <p>Welcome to your dashboard, {isAuthenticated.email}</p>
      ) : (
        <p>You must be logged in to view this page.</p>
      )}
    </div>
  );
};

export default Dashboard;
