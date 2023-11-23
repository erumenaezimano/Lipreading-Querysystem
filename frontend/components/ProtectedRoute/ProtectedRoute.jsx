import React from "react";
import { Navigate } from "react-router-dom";

function ProtectedRoute({ component }) {
	const App = component;

	const token = localStorage.getItem("authToken");


	if (!token) {
		// Redirect to login if token is not present
		return <Navigate to='/login' />;
	}

	// Render the protected component if token is present
	return App ;
}

export default ProtectedRoute;
