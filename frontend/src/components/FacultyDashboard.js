import React, { useEffect, useState } from "react";
import API from "../api/axios";
import "./FacultyDashboard.css";

const FacultyDashboard = () => {
    const [submissions, setSubmissions] = useState([]);
    const [search, setSearch] = useState("");

    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await API.get("faculty/dashboard/");
                console.log("API Response:", res.data);
                setSubmissions(res.data.data || []);
            } catch (err) {
                console.error("Error fetching dashboard:", err);
            }
        };
        fetchData();
    }, []);
    
    const filteredSubmissions = submissions.filter((item) =>
        (item.student_name || "Unknown").toLowerCase().includes(search.toLowerCase())
    );

    return (
        <div className="faculty-page">
            <div className="faculty-box">
                <h1>Faculty Dashboard</h1>
                <input
                    type="text"
                    placeholder="Search by Student Name or ID"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="search-box"
                />
                <div className="table-container">
                    <table className="dashboard-table">
                        <thead>
                            <tr>
                                <th>Student Name</th>
                                <th>Version</th>
                                <th>Similarity %</th>
                                <th>Uploaded At</th>
                                <th>Files</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredSubmissions.length ? (
                                filteredSubmissions.map((item) => (
                                    <tr key={item.id}>
                                        <td>{item.student_name || "Unknown"}</td>
                                        <td>{item.version}</td>
                                        <td>{item.similarity_percentage}%</td>
                                        <td>{new Date(item.upload_timestamp).toLocaleString()}</td>
                                        <td>
                                            <a href={item.docx_file} target="_blank" rel="noopener noreferrer">DOCX</a> |{" "}
                                            <a href={item.ppt_file} target="_blank" rel="noopener noreferrer">PPTX</a> |{" "}
                                            <a href={item.similarity_report} target="_blank" rel="noopener noreferrer">Report</a>
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="5" className="no-submissions">
                                        No submissions found
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default FacultyDashboard;
