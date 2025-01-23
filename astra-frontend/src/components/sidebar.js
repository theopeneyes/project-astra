import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../contexts/authContext";
import { useNavigate, useLocation } from "react-router-dom";
import { goTo } from "./common/goTo";
import { pageName } from "./common/pagesName";

const Sidebar = () => {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [isActive, setIsActive] = useState(location.pathname);

  const handelClick = (flag) => {
    if (flag === "/dashboard") {
      setIsActive(flag);
      goTo(navigate, "/dashboard");
    } else if (flag === "/profile") {
      goTo(navigate, "/profile");
      setIsActive(flag);
    } else if (flag === "/user-manage") {
      goTo(navigate, "/user-manage");
      setIsActive(flag);
    }
    else if (flag === "/upload-file") {
      goTo(navigate, "/upload-file");
      setIsActive(flag);
    }
  };

  useEffect(() => {
    setIsActive(location.pathname);
  }, [location.pathname]);

  return (
    <>
      <nav className="d-none">
        <ul>
          <li>
            <Link>Home</Link>
          </li>
          {isAuthenticated ? (
            <>
              <li>
                <Link to="/profile">Profile</Link>
              </li>
              <li>
                <Link to="/file-upload">File-upload</Link>
              </li>
              <li>
                <button onClick={logout}>Logout</button>
              </li>
            </>
          ) : (
            <>
              <li>
                <Link to="/login">Login</Link>
              </li>
              <li>
                <Link to="/signup">Register</Link>
              </li>
            </>
          )}
        </ul>
      </nav>
      <div className="nav-side-menu">
        <button
          className="btn btn-dark d-md-none"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#menu-content"
          aria-expanded="false"
          aria-controls="menu-content"
        >
          <i className="fa fa-bars fa-2x"></i>
        </button>

        <div className="menu-list collapse d-md-block" id="menu-content">
          <ul className="nav flex-column">
            <li className="nav-item" onClick={() => handelClick("/dashboard")}>
              <Link
                className={`nav-item ${
                  isActive === "/dashboard" ? "active" : ""
                }`}
              >
                <i className="fa fa-dashboard fa-lg"></i> Dashboard
              </Link>
            </li>
            <li className="nav-item" onClick={() => handelClick("/upload-file")}>
              <Link
                className={`nav-item ${
                  isActive === "/upload-file" ? "active" : ""
                }`}
              >
                <i className="fa-solid fa-upload"></i> Upload File
              </Link>
            </li>

            <li className="nav-item dropdown">
              <Link
                className="nav-link dropdown-toggle show"
                id="uiDropdown"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                <i className="fa fa-gift fa-lg"></i> UI Elements
              </Link>
              <ul className="dropdown-menu show" aria-labelledby="uiDropdown">
                <li>
                  <Link className="dropdown-item">CSS3 Animation</Link>
                </li>
                <li>
                  <Link className="dropdown-item">General</Link>
                </li>
                <li>
                  <Link className="dropdown-item">Buttons</Link>
                </li>
              </ul>
            </li>

            <li className="nav-item dropdown">
              <Link
                className="nav-link dropdown-toggle"
                id="servicesDropdown"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                <i className="fa fa-globe fa-lg"></i> Services
              </Link>
              <ul className="dropdown-menu" aria-labelledby="servicesDropdown">
                <li>
                  <Link className="dropdown-item">Service 1</Link>
                </li>
                <li>
                  <Link className="dropdown-item">Service 2</Link>
                </li>
                <li>
                  <Link className="dropdown-item">Service 3</Link>
                </li>
              </ul>
            </li>

            <li className="nav-item dropdown">
              <Link
                className="nav-link dropdown-toggle"
                id="newDropdown"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                <i className="fa fa-car fa-lg"></i> New
              </Link>
              <ul className="dropdown-menu" aria-labelledby="newDropdown">
                <li>
                  <Link className="dropdown-item">New 1</Link>
                </li>
                <li>
                  <Link className="dropdown-item">New 2</Link>
                </li>
                <li>
                  <Link className="dropdown-item">New 3</Link>
                </li>
              </ul>
            </li>

            <li className="nav-item" onClick={() => handelClick("/profile")}>
              <Link
                className={`nav-item ${
                  isActive === "/profile" ? "active" : ""
                }`}
              >
                <i className="fa fa-user fa-lg"></i> {pageName.profile}
              </Link>
            </li>

            <li
              className="nav-item"
              onClick={() => handelClick("/user-manage")}
            >
              <Link
                className={`nav-item ${
                  isActive === "/user-manage" ? "active" : ""
                }`}
              >
                <i className="fa fa-users fa-lg"></i> Users
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </>
  );
};

export default Sidebar;
