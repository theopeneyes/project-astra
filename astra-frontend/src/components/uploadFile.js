import React, { useState, useEffect } from "react";
import axios from "axios";
import { Input } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
import { Link } from "react-router-dom";
import viewIcon2 from "../assets/images/view-icon-2.svg";
import { useComponentName } from "./common/loadedComponentName";
import { pageName } from "./common/pagesName";
import { useAuth } from "../contexts/authContext";
import { goTo } from "./common/goTo";
import { useNavigate } from "react-router-dom";

const UploadFile = () => {
  const auth = useAuth();
  const navigate = useNavigate();
  const user = auth.isAuthenticated;
  const [folderName, setFolderName] = useState("");
  const { setComponentName } = useComponentName(pageName.fileUpload);
  const [fileNames, setFileNames] = useState([]);
  const [errors, setErrors] = useState(false);
  const [uploadedUrl, setUploadedUrl] = useState("");

  useEffect(() => {
    setComponentName(pageName.fileUpload);
  }, []);
  const statuses = ["Pending", "In Progress", "Completed", "Rejected"];

  const getRandomStatus = () => {
    const randomIndex = Math.floor(Math.random() * statuses.length);
    return statuses[randomIndex];
  };

  const getStatusClass = (status) => {
    switch (status) {
      case "Pending":
        return "pending"; // Custom CSS class for Pending
      case "In Progress":
        return "in-progress"; // Custom CSS class for In Progress
      case "Completed":
        return "completed"; // Custom CSS class for Completed
      case "Rejected":
        return "rejected"; // Custom CSS class for Rejected
      default:
        return "";
    }
  };

  // Function to get the current date and time in the desired format
  const getCurrentDateTime = () => {
    const now = new Date();
    const options = {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: true,
    };
    return now.toLocaleString("en-GB", options).replace(",", ""); // Format as "10 Jan, 2025 04:50 PM"
  };

  const handleFileSelect = async (event) => {
    const files = event.target.files;

    if (files.length === 0) {
      setFolderName("");
      setFileNames([]);
      setErrors("");
      return;
    }

    // Filter PDF files
    const pdfFiles = Array.from(files).filter((file) =>
      file.name.toLowerCase().endsWith(".pdf")
    );

    if (pdfFiles.length === 0) {
      setFolderName("");
      setFileNames([]);
      setErrors(
        "No PDF files found in the selected directory. Please choose a directory containing PDF files."
      );
      return;
    }

    // Extract folder name from the first file's relative path
    const folder = pdfFiles[0].webkitRelativePath.split("/")[0];
    setFolderName(folder);

    const pdfFileNames = pdfFiles.map((file) => file.name);
    debugger
    setFileNames(pdfFileNames);

    try {
      // Create form data for the whole set of files
      const formData = new FormData();
      formData.append("email_id", user.email);
      formData.append("filenames", JSON.stringify(pdfFileNames));

      // Handle individual file uploads concurrently
      const uploadPromises = pdfFiles.map((file) => {
        const fileFormData = new FormData();
        fileFormData.append("email_id", user.email);
        fileFormData.append("pdf", file);
        fileFormData.append("filename", file.name);

        return axios
          .post("http://127.0.0.1:8000/upload_pdfs", fileFormData, {
            headers: { "Content-Type": "multipart/form-data" },
          })
          .then((response) => {
            setUploadedUrl(response.data.url); // Assuming `url` is part of the response
          })
          .catch((err) => {
            const errorMessage =
              err.response?.data?.detail || "An error occurred during upload.";
            setErrors(errorMessage);
            console.error("Upload error for file:", file.name, err);
          });
      });

      // Wait for all uploads to complete
      await Promise.all(uploadPromises);
    } catch (err) {
      setErrors("An unexpected error occurred.");
      console.error("Error during file processing:", err);
    }
  };

  return (
    <div className="default-box">
      <div className="row">
        <div className="col-6 m-auto">
          <div className="form-group">
            <label>
              <span>*</span>Choose a directory
            </label>
            <div className="directory-path">
              <label htmlFor="abc" className="mb-0 w-100 d-flex">
                <Input type="button" value={"Choose a directory"} />
                <Button className="btn-design btn-1">Choose</Button>
              </label>
              <input
                id="abc"
                type="file"
                webkitdirectory="true"
                className="d-none"
                onChange={handleFileSelect}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="mt-5">
        <h3>PDF files in directory: {folderName}</h3>
        <p>
          <strong>Note:</strong>{" "}
          <small className="small text-muted">
            Complete the react flow to see the generated questions.{" "}
          </small>
        </p>
        {fileNames.length > 0 && (
          <div className="mt-4">
            <div className="file-list-main row row-cols-4 gy-4">
              {fileNames.map((fileName, index) => {
                const randomStatus = getRandomStatus(); // Get a random status including "Rejected"
                const statusClass = getStatusClass(randomStatus); // Get the corresponding class

                // Disable the "View Questions" button if status is not "Completed"
                const isButtonDisabled = randomStatus !== "Completed";

                return (
                  <div className="col" key={index}>
                    <div className="file-item">
                      <div className="fi-top">
                        <div className={`fi-status ${statusClass}`}>
                          {randomStatus}
                        </div>
                        <div className="fi-date">
                          <strong>Created on:</strong> {getCurrentDateTime()}
                        </div>
                      </div>
                      <div className="fi-middle">
                        <h3 className="fw-bold">{fileName}</h3>
                        <p className="mb-0">
                          <strong>React Flow: </strong>
                          {randomStatus === "Pending" ? (
                            <span>Link available after completion</span>
                          ) : (
                            <Link
                              to={'/react-flow'}
                              rel="noopener noreferrer"
                            >
                              https://dummyurl.com
                            </Link>
                          )}
                        </p>
                      </div>
                      <div className="fi-bottom">
                        <Button
                          title="View Questions"
                          className="view-btn"
                          disabled={isButtonDisabled} 
                          onClick={() => goTo(navigate, "/question-view")}
                        >
                          <img src={viewIcon2} alt="View"   /> View Questions
                        </Button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
        {errors && <p className="my-5 py-5 text-center w-100">{errors}</p>}
      </div>
    </div>
  );
};

export default UploadFile;
