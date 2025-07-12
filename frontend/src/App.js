import React from "react";
import { BrowserRouter as Router, Routes, Route} from "react-router-dom";
import LoginForm from "./components/LoginForm";
import StudentDashboard from "./components/StudentDashboard";
import FacultyDashboard from "./components/FacultyDashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import RegisterForm from "./components/RegisterForm";


const App = () => (
  <Router>
    <Routes>
      <Route path="/" element={<LoginForm />} />

      <Route path="/" element={<LoginForm />} />
                <Route path="/register/:userType" element={<RegisterForm />} />
      
      <Route element={<ProtectedRoute allowedRoles={["student"]} />}>
          <Route path="/student" element={<StudentDashboard />} />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={["faculty"]} />}>
          <Route path="/faculty" element={<FacultyDashboard />} />
        </Route>
      
    </Routes>
  </Router>
);

export default App;
