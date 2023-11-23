import React from "react";
import ReactDOM from "react-dom/client"; // Correct the import statement
import "./index.css";
import App from "./App";
import Search from "./components/search/Search";
import Getstarted from "./components/getstarted/Getstarted";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Registeration from "./components/Registeration/Registeration";
import Login from "./components/Login/Login.jsx";
import ProtectedRoute from "./components/ProtectedRoute/ProtectedRoute";
import Dashboard from "./components/Dashboard";
import Interactive from "./components/Interactive/interactive";

const router = createBrowserRouter([
	{
		path: "/",
		element: <App />,
	},
	{
		path: "search",
		element: <ProtectedRoute component={<Search />} />,
	},
	{
		path: "dashboard",
		element: <ProtectedRoute component={<Dashboard />} />,
	},
	{
		path: "interactive",
		element: <ProtectedRoute component={<Interactive />} />,
	},
	{
		path: "getstarted",
		element: <Getstarted />,
	},
	{
		path: "registeration",
		element: <Registeration />,
	},
	{
		path: "login",
		element: <Login />,
	},
]);

ReactDOM.createRoot(document.getElementById("root")).render(
	<React.StrictMode>
		<RouterProvider router={router} />
	</React.StrictMode>
);
