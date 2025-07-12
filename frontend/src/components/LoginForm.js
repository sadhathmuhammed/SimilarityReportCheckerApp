import React, { useState } from "react";
import API from "../api/axios";
import { useNavigate } from "react-router-dom";
import "./App.css";


const LoginForm = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();


    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await API.post("auth/login/", { username, password });
            console.log('response', response.data);
            const role = response.data.is_staff ? "faculty" : "student";

            localStorage.setItem("role", role);
            localStorage.setItem("access_token", response.data.access);
            localStorage.setItem("refresh_token", response.data.refresh);
            localStorage.setItem("username", response.data.username);

            if (role === "student") navigate("/student");
            else if (role === "faculty") navigate("/faculty");

        } catch (err) {
            setError("Invalid username or password");
        }
    };

    return (
        <div className="page-container">
            <form className="form-box" onSubmit={handleLogin}>
                <h1>Login <br></br> File Submission Portal</h1>
                {error && <p className="error">{error}</p>}
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    style={{
                        width: "100%",
                        padding: "10px",
                        marginBottom: "1rem",
                        borderRadius: "5px",
                        border: "1px solid #ccc"
                    }}
                    required
                />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={{
                        width: "100%",
                        padding: "10px",
                        marginBottom: "1rem",
                        borderRadius: "5px",
                        border: "1px solid #ccc"
                    }}
                    required
                />
                <button type="submit">Login</button>
                <div className="links">
                    <p>New user? <a href="/register/student">Student</a> | <a href="/register/faculty">Faculty</a></p>
                </div>
            </form>
        </div>
    );
};

export default LoginForm;