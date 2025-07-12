import React, { useState, useEffect } from "react";
import API from "../api/axios";
import { useNavigate, useParams } from "react-router-dom";
import "./App.css";

const RegisterForm = () => {
    const [formData, setFormData] = useState({
        username: "",
        password: "",
        name: "",
        email: "",
        department: "", // for faculty
        faculty: "",    // For student
    });
    const [faculties, setFaculties] = useState([]);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const navigate = useNavigate();
    const { userType } = useParams();

    useEffect(() => {
        if (userType === "student") {
            API.get("faculty/list/")
                .then(response => setFaculties(response.data))
                .catch(error => console.error("Error fetching faculty list:", error));
        }
    }, [userType]);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        const endpoint = `auth/register/${userType}/`;

        try {
            const response = await API.post(endpoint, formData);
            console.log("Registration successful:", response.data);
            setSuccess("Registration successful! You can now login.");
            setTimeout(() => navigate("/"), 2000);
        } catch (err) {
            console.error("Registration failed:", err.response?.data);
            setError("Registration failed. Please check your details.");
        }
    };

    return (
        <div className="page-container">
            <form className="form-box" onSubmit={handleRegister}>
                <h1>{userType === "faculty" ? "Faculty" : "Student"} Registration</h1>
                {error && <p className="error">{error}</p>}
                {success && <p className="success">{success}</p>}

                <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                />

                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                />

                <input
                    type="text"
                    name="name"
                    placeholder="Full Name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                />

                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                />

                {userType === "faculty" && (
                    <input
                        type="text"
                        name="department"
                        placeholder="Department"
                        value={formData.department}
                        onChange={handleChange}
                        required
                    />
                )}

                {userType === "student" && (
                    <select
                        name="faculty"
                        value={formData.faculty}
                        onChange={handleChange}
                        required
                    >
                        <option value="">-- Select Faculty --</option>
                        {faculties.map((fac) => (
                            <option key={fac.id} value={fac.id}>
                                {fac.name} ({fac.department})
                            </option>
                        ))}
                    </select>
                )}

                <button type="submit">Register</button>
                <div className="links">
                    <p>Already have an account? <a href="/">Login</a></p>
                </div>
            </form>
        </div>
    );
};

export default RegisterForm;
