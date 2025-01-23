// src/components/Profile.js
import React from "react";
import { Link } from "react-router-dom";
import logo from "../assets/images/logo-white.png";
import profileImg from "../assets/images/profile.jpg";
// import { getLocation } from "./common/getLocation";
// import { useLocation } from "react-router-dom";
// import { pageName } from "./common/pagesName";
import { useComponentName } from "./common/loadedComponentName";
import { useAuth } from "../contexts/authContext";
import { useNavigate } from "react-router-dom";
import Cookies from "js-cookie";
const Header = () => {
  const { componentName } = useComponentName();
   const { isAuthenticated, logout } = useAuth();
   const navigate = useNavigate();


    const handelLogout = async () => {
      try {
        await logout(); 
        Cookies.remove("authData");
        navigate("/"); 
      } catch (error) {
        console.error("Error during logout:", error);
      }
    };

  return (
    <header>
      <div className="brand"><img src={logo} alt="Logo" /></div>
      <div className="header-inner">
        <h1 className="text-capitalize">{componentName}</h1>
        <div className="h-right">
          <div className="dropdown notification-dropdown">
            <button className="dropdown-toggle notif-toggle"  data-bs-toggle="dropdown" aria-expanded="false">
              <i className="fa-regular fa-bell"></i>
            </button>
            {/* <ul className="dropdown-menu dropdown-menu-end" aria-labelledby="notificationDropdown">
              <li><Link className="dropdown-item" to="/">Profile</Link></li>
              <li><Link className="dropdown-item" to="/">Settings</Link></li>
              <li><hr className="dropdown-divider" /></li>
              <li><Link className="dropdown-item" to="/">Logout</Link></li>
            </ul> */}
          </div>
          <div className="dropdown">
            <button className="dropdown-toggle profile-toggle" id="profileDropdown" data-bs-toggle="dropdown" aria-expanded="false">
              <div className="profile-name">
                <span className="d-block">Thomas Anree</span>
                <small>Main User</small>
              </div>
              <img src={profileImg} alt="Profile" className="rounded-circle ms-2" />
            </button>
            <ul className="dropdown-menu dropdown-menu-end" aria-labelledby="profileDropdown">
              <li><Link className="dropdown-item" to="/profile">Profile</Link></li>
              {/* <li><Link className="dropdown-item" to="/">Settings</Link></li> */}
              <li><hr className="dropdown-divider" /></li>
              <li><Link className="dropdown-item" onClick={handelLogout}>Logout</Link></li>
            </ul>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
