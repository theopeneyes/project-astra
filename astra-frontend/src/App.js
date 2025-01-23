import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import "@progress/kendo-theme-default/dist/all.css";
import { AuthProvider, useAuth } from "./contexts/authContext";
import Login from "./components/login";
import Register from "./components/register";
import ForgotPassword from "./components/forgotPassword";
import ResetPassword from "./components/resetPassword";
import Profile from "./components/profile";
import ReactFlowPreview from "./components/reactFlow/reactFlowPreview";
import QuestionView from "./components/questionview";
import UserManage from "./components/userManage";
import UploadFile from "./components/uploadFile";
import Dashboard from "./components/dashboard";
import PageNotFound from "./components/pageNotFound";
import Sidebar from "./components/sidebar";
import Header from "./components/header";
import Footer from "./components/footer";
import { Link } from "react-router-dom";
import { useLocation } from "react-router-dom";
import { getLocation } from "./components/common/getLocation";

const AppContent = () => {
  const { isAuthenticated } = useAuth();
  const location = useLocation();
  const segments = getLocation(location.pathname, null);

  const getPath = (index) => {
    return (
      "/" +
      segments
        .slice(0, index + 1)
        .join("/")
        .toLowerCase()
    );
  };

  return (
    <>
      {isAuthenticated && <Header />}
      {isAuthenticated && <Sidebar />}
      <div className="main-wrapper">
      <Routes>
      <Route path="/question-view" element={<QuestionView />} />
      </Routes>
        {isAuthenticated && segments.length > 1 && (
          <div className="breadcrumb text-capitalize">
            {segments.map((segment, index) => (
              <React.Fragment key={index}>
                <Link
                  to={getPath(index)}
                  className={
                    index === segments.length - 1
                      ? "breadcrumb-current"
                      : "breadcrumb-link"
                  }
                >
                  {segment}
                </Link>
                {index < segments.length - 1 && (
                  <span className="breadcrumb-separator">/</span>
                )}
              </React.Fragment>
            ))}
          </div>
        )}
        <Routes>
          <Route path="/dashboard" element={isAuthenticated && <Dashboard />} />
          <Route
            path="/upload-file"
            element={isAuthenticated && <UploadFile />}
          />
          <Route
            path="/user-manage"
            element={isAuthenticated && <UserManage />}
          />
          <Route path="/profile" element={isAuthenticated && <Profile />} />
          <Route
            path="/react-flow"
            element={isAuthenticated && <ReactFlowPreview />}
          />
        </Routes>
      </div>
      {isAuthenticated && <Footer />}
    </>
  );
};

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/signup" element={<Register />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          
        </Routes>
        <AppContent />
      </Router>
    </AuthProvider>
  );
};

export default App;
