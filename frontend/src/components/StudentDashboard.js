import React, { useState, useEffect } from "react";
import API from "../api/axios";
import "./App.css";

const StudentDashboard = () => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [docxFile, setDocxFile] = useState(null);
  const [pptxFile, setPptxFile] = useState(null);
  const [similarityReport, setSimilarityReport] = useState(null);

  const [backendResponse, setBackendResponse] = useState(null);
  const [finalResponse, setFinalResponse] = useState(null);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [canSubmit, setCanSubmit] = useState(false);

  const uploadSubmission = async () => {
    const formData = new FormData();
    formData.append("title", title || "Draft Title");
    formData.append("description", description || "Draft Description");
    formData.append("docx_file", docxFile);
    formData.append("ppt_file", pptxFile);
    formData.append("similarity_report", similarityReport);

    try {
      const res = await API.post("student/upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log("Backend Response:", res.data);
      setBackendResponse(res.data);

      if (res.data.status === "Success") {
        setCanSubmit(true);
        setError("");
      } else {
        setCanSubmit(false); 
        setError("Similarity exceeds limit. Please re-upload all documents.");
      }
    } catch (err) {
      console.error(err);
      setError("Failed to upload and check similarity.");
      setCanSubmit(false);
    }
  };

  useEffect(() => {
    if (docxFile && pptxFile && similarityReport) {
      console.log("All files selected. Uploading...");
      uploadSubmission();
    }
  }, [docxFile, pptxFile, similarityReport]);

  const handleFileChange = (setter) => (e) => {
    setter(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setFinalResponse(backendResponse);
    setIsSubmitting(false);
  };

  return (
    <div className="page-container">
      <div className="form-box">
        <h1>Submit Project Files</h1>
        {error && <p className="error">{error}</p>}
        <form className="space-y-4" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
          <textarea
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows="3"
          ></textarea>
          <div>
            <label>DOCX File:</label>
            <input
              type="file"
              accept=".docx"
              onChange={handleFileChange(setDocxFile)}
              required
            />
          </div>
          <div>
            <label>PPTX File:</label>
            <input
              type="file"
              accept=".pptx"
              onChange={handleFileChange(setPptxFile)}
              required
            />
          </div>
          <div>
            <label>Similarity Report (PDF/DOCX):</label>
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={handleFileChange(setSimilarityReport)}
              required
            />
          </div>
          <button
            type="submit"
            disabled={!canSubmit || isSubmitting}
            style={{
              backgroundColor: canSubmit ? "#007bff" : "#ccc",
              color: "white",
              padding: "10px 20px",
              border: "none",
              borderRadius: "5px",
              cursor: canSubmit ? "pointer" : "not-allowed",
            }}
          >
            {isSubmitting ? "Submitting..." : "Submit"}
          </button>
        </form>

        {finalResponse && (
          <div className="mt-4">
            <h2 className="text-xl font-semibold">Submission Status</h2>
            <p>
              <strong>Similarity %:</strong> {finalResponse.similarity_percentage}%
            </p>
            <p>
              <strong>Status:</strong> {finalResponse.status}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default StudentDashboard;
