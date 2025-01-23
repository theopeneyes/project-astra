import React, { useState, useEffect } from "react";
import { ref, onValue } from "firebase/database";
import { database } from "../firebase/firebaseConfig";
import profileImg from "../assets/images/profile.jpg";
import { Input, Switch, Checkbox } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
import { DropDownList } from "@progress/kendo-react-dropdowns";
import eyeoff from "../assets/images/eye-off.svg";
import eyeon from "../assets/images/eye.svg";
import { pageName } from "./common/pagesName";
import { useComponentName } from "./common/loadedComponentName";
import { useAuth } from "../contexts/authContext";
import { useNavigate } from "react-router-dom";
import Cookies from "js-cookie";

const Profile = () => {
  const auth = useAuth();
  const navigate = useNavigate();
  const user = auth.isAuthenticated;
  const { updateUserData, logout, deleteAuthUser } = useAuth();
  const { setComponentName } = useComponentName(pageName.profile);
  const [loginUserData, setLoginUserData] = useState();
  const [personalFormData, setpersonalFormData] = useState({
    firstName: "",
    lastName: "",
    password: "",
    address1: "",
    address2: "",
  });

  useEffect(() => {
    if (loginUserData) {
      setpersonalFormData({
        firstName: loginUserData.firstName || "",
        lastName: loginUserData.lastName || "",
        email: loginUserData.email || "",
        address1: loginUserData.address1 || "",
        address2: loginUserData.address2 || "",
      });
      setEmailFormData({ email: loginUserData.email });
    }
  }, [loginUserData]);

  const [languages, setLanguages] = useState([]);
  const [timezones, setTimezones] = useState([]);
  const [preferencesFormData, setPreferencesFormData] = useState({
    language: "English",
    timezone: "USA (GMT-5)",
    emailNotifications: true,
  });
  // const [preferencesData, setpreferencesData] = useState();
  useEffect(() => {
    const userRef = ref(database, `settings`);
    onValue(userRef, (snapshot) => {
      const data = snapshot.val();
      setLanguages(data.languages);
      setTimezones(data.timezones);
    });
  }, []);

  const [errors, setErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const [showPassword2, setShowPassword2] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setpersonalFormData({ ...personalFormData, [name]: value });
  };

  const validate = () => {
    const newErrors = {};
    if (!personalFormData.firstName)
      newErrors.firstName = "First Name is required";
    if (!personalFormData.lastName)
      newErrors.lastName = "Last Name is required";
    if (!personalFormData.address1)
      newErrors.address1 = "Address 1 is required";

    return newErrors;
  };

  const handlePreferencesChange = (e, field) => {
    setPreferencesFormData({ ...preferencesFormData, [field]: e.value });
  };
  const validatePreferences = () => {
    const validationErrors = {};
    if (!preferencesFormData.language)
      validationErrors.language = "Language is required.";
    if (!preferencesFormData.timezone)
      validationErrors.timezone = "Time Zone is required.";
    return validationErrors;
  };
  const handlePreferencesSubmit = (e) => {
    e.preventDefault();
    const validationErrors = validatePreferences();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
    } else {
      setErrors({});
      console.log("Form submitted successfully:", preferencesFormData);
      // Handle form submission, e.g., save to Firebase
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
    } else {
      setErrors({});
      console.log("Form submitted successfully:", personalFormData);
      try {
        const updatedData = {
          email: emailFormData.email,
          password: loginUserData.password,
          firstName: loginUserData.firstName,
          lastName: loginUserData.lastName,
          address1: personalFormData.address1,
          address2: personalFormData.address2,
        };
        await updateUserData(user.uid, updatedData);
        alert("User data updated successfully.");
      } catch (error) {
        console.error("Error updating user data:", error);
        setErrors({ email: "Failed to update user data. Please try again." });
      }
      // Perform update action here
    }
  };

  useEffect(() => {
    if (user) {
      const userUid = user.uid;
      const userRef = ref(database, `register/users/${userUid}`);

      onValue(userRef, (snapshot) => {
        const data = snapshot.val();
        setLoginUserData(data);
      });
    } else {
      console.log("No user is logged in.");
    }
  }, []);

  useEffect(() => {
    setComponentName(pageName.profile);
  }, []);

  const [isEditable, setIsEditable] = useState(false);
  const [emailFormData, setEmailFormData] = useState({ email: "" });

  const handleEmailInputChange = (e) => {
    const { name, value } = e.target;
    setEmailFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
    setErrors((prevErrors) => ({
      ...prevErrors,
      [name]: "",
    }));
  };

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleCancel = () => {
    setEmailFormData({ email: loginUserData.email });
    setIsEditable(false); // Disable editing
    setErrors({ email: "" });
  };
  const handleEmailSubmit = async (e) => {
    e.preventDefault();

    if (validateEmail(emailFormData.email)) {
      try {
        const updatedData = {
          email: emailFormData.email,
          password: loginUserData.password,
          // firstName: loginUserData.firstName,
          // lastName: loginUserData.lastName,
        };
        await updateUserData(user.uid, updatedData);
        setLoginUserData((prevData) => ({
          ...prevData,
          email: emailFormData.email,
        }));

        setIsEditable(false);
      } catch (error) {
        console.error("Error updating user data:", error);
        setErrors({ email: "Failed to update user data. Please try again." });
      }
    } else {
      setErrors({ email: "Please enter a valid email address." });
    }
  };

  const [isChecked, setIsChecked] = useState(false);
  const [error, setError] = useState("");
  const handleCheckboxChange = (e) => {
    setIsChecked(e.target.checked);
    if (e.target.value) {
      setIsChecked(e.target.value);
      setError("");
    }
  };
  const handleDeleteClick = async (e) => {
    e.preventDefault();

    if (!isChecked) {
      setError("You must agree to delete your account.");
      return;
    }

    try {
      debugger;
      if (user) {
        await deleteAuthUser();
        await logout();
        Cookies.remove("authData");
        navigate("/");
        alert("You have successfully deleted your account.");
      } else {
        setError("No user is currently logged in.");
      }
    } catch (err) {
      setError(
        "An error occurred while deleting your account. Please try again."
      );
      console.error(err);
    }
  };

  return (
    <div className="profile-main">
      <h1>{setComponentName}</h1>
      <div className="row">
        <div className="col-4">
          <div className="default-box d-flex align-items-center">
            <div className="user-pro-inner">
              <div className="user-img">
                <img
                  src={profileImg}
                  alt="Profile"
                  className="rounded-circle"
                />
                <i className="fa-solid fa-camera"></i>
              </div>
              <div className="user-name">
                <span className="d-block">
                  {personalFormData
                    ? `${personalFormData.firstName} ${personalFormData.lastName}`
                    : ""}
                </span>
                <small>Main User</small>
              </div>
              <div className="user-email">
                {personalFormData ? `${personalFormData.email}` : ""}
              </div>
            </div>
          </div>
        </div>
        <div className="col-8">
          <div className="default-box top-head">
            <div className="default-head">
              <h3>Personal Details</h3>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="row row-cols-2">
                <div className="col">
                  <div className="form-group">
                    <label>First Name</label>
                    <Input
                      type="text"
                      name="firstName"
                      placeholder="Enter first name"
                      value={personalFormData.firstName}
                      onChange={handleChange}
                    />
                    {errors.firstName && (
                      <small className="k-form-error k-text-start">
                        {errors.firstName}
                      </small>
                    )}
                  </div>
                </div>
                <div className="col">
                  <div className="form-group">
                    <label>Last Name</label>
                    <Input
                      type="text"
                      name="lastName"
                      placeholder="Enter last name"
                      value={personalFormData.lastName}
                      onChange={handleChange}
                    />
                    {errors.lastName && (
                      <small className="k-form-error k-text-start">
                        {errors.lastName}
                      </small>
                    )}
                  </div>
                </div>
                <div className="col">
                  <div className="form-group">
                    <label>Address 1</label>
                    <Input
                      type="text"
                      name="address1"
                      placeholder="Enter address 1"
                      value={personalFormData.address1}
                      onChange={handleChange}
                    />
                    {errors.address1 && (
                      <small className="k-form-error k-text-start">
                        {errors.address1}
                      </small>
                    )}
                  </div>
                </div>
                <div className="col">
                  <div className="form-group">
                    <label>Address 2</label>
                    <Input
                      type="text"
                      name="address2"
                      placeholder="Enter address 2"
                      value={personalFormData.address2}
                      onChange={handleChange}
                    />
                  </div>
                </div>
              </div>
              <div className="form-group text-center mb-0 mt-4">
                <Button className="btn-design btn-1" type="submit">
                  Update
                </Button>
              </div>
            </form>
          </div>
        </div>
      </div>
      <div className="default-box top-head mt-30 d-none">
        <div className="default-head">
          <h3>Preferences</h3>
        </div>
        <form onSubmit={handlePreferencesSubmit}>
          <div className="row row-cols-3">
            <div className="col">
              <div className="form-group">
                <label>Language</label>
                <DropDownList
                  data={languages}
                  value={preferencesFormData.language}
                  onChange={(e) => handlePreferencesChange(e, "language")}
                />
                {errors.language && (
                  <small className="text-danger">{errors.language}</small>
                )}
              </div>
            </div>
            <div className="col">
              <div className="form-group">
                <label>Time Zone</label>
                <DropDownList
                  data={timezones}
                  value={preferencesFormData.timezone}
                  onChange={(e) => handlePreferencesChange(e, "timezone")}
                />
                {errors.timezone && (
                  <small className="text-danger">{errors.timezone}</small>
                )}
              </div>
            </div>
            <div className="col">
              <div className="form-group">
                <label className="w-100 mb-3">Email Notifications</label>
                <span className="switch-label me-2">True</span>
                <Switch
                  onLabel={""}
                  offLabel={""}
                  checked={preferencesFormData.emailNotifications}
                  onChange={(e) =>
                    handlePreferencesChange(e, "emailNotifications")
                  }
                />
                <span className="switch-label ms-2">False</span>
              </div>
            </div>
          </div>
          <div className="form-group text-center mb-0 mt-4">
            <Button className="btn-design btn-1">Update</Button>
          </div>
        </form>
      </div>
      <div className="default-box top-head mt-30 d-none">
        <div className="default-head">
          <h3>Account Settings</h3>
        </div>
        <form>
          <div className="mb-30">
            <div className="email-change">
              Your Email address is{" "}
              <Input
                type="text"
                name="email"
                value={emailFormData.email || ""}
                disabled={!isEditable}
                onChange={handleEmailInputChange}
                placeholder="Enter your new email address"
              />
              {errors.email && (
                <small className="text-danger">{errors.email}</small>
              )}
              <span
                className="link-text fw-medium"
                onClick={() =>
                  isEditable ? handleCancel() : setIsEditable(true)
                }
              >
                {isEditable ? "Cancel" : "Change"}
              </span>
              {isEditable && (
                <span
                  onClick={handleEmailSubmit}
                  className="link-text fw-medium"
                >
                  Save
                </span>
              )}
            </div>
          </div>
        </form>
        <h3>Change Password</h3>
        <form>
          <div className="gap-xl-0 gap-lg-4 row row-cols-xl-3 row-cols-lg-1">
            <div className="col">
              <div className="form-group mb-0">
                <label>
                  <span>*</span>New Password
                </label>
                <Input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  placeholder="Enter new password"
                />
                <div
                  className="password-icon"
                  onClick={() => setShowPassword((prev) => !prev)}
                >
                  {showPassword ? (
                    <img src={eyeoff} alt="Hide" />
                  ) : (
                    <img src={eyeon} alt="Show" />
                  )}
                </div>
              </div>
            </div>
            <div className="col">
              <div className="form-group mb-0">
                <label>
                  <span>*</span>Confirm New Password
                </label>
                <Input
                  type={showPassword2 ? "text" : "password"}
                  name="password"
                  placeholder="Enter new password"
                />
                <div
                  className="password-icon"
                  onClick={() => setShowPassword2((prev) => !prev)}
                >
                  {showPassword2 ? (
                    <img src={eyeoff} alt="Hide" />
                  ) : (
                    <img src={eyeon} alt="Show" />
                  )}
                </div>
              </div>
            </div>
            <div className="col">
              <div className="form-group mb-0 mt-4">
                <Button className="btn-design btn-1">Save Password</Button>
              </div>
            </div>
          </div>
        </form>
      </div>
      <div className="default-box top-head mt-30">
        <div className="default-head">
          <h3>Delete Account</h3>
        </div>
        <p>
          Would you like to delete your account?
          <br />
          This account has 1,388 uploaded files. Deleting your account will
          permanently remove all associated content.
        </p>
        <div>
          <form onSubmit={handleDeleteClick}>
            <div className="form-group">
              <Checkbox
                type="checkbox"
                id="agree"
                name="isChecked"
                checked={isChecked}
                onChange={handleCheckboxChange}
              >
                <label className="k-checkbox-label" htmlFor="agree">
                  I want to delete my account
                </label>
              </Checkbox>
              {error && (
                <small className="k-form-error k-text-start">{error}</small>
              )}
            </div>
            <div className="form-group text-center mb-0 mt-4">
              <Button className="btn-design btn-1" type="submit">
                Delete
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Profile;