import React, { useState } from "react";

import { toast } from "react-toastify";
//import Button from "../../components/Button";

import axios, { AxiosError } from "axios";
import { Link, useNavigate } from "react-router-dom";
import baseUrl from "../../config";
import Layout from "../layout/Layout";
import "./login.css";

const Login = () => {
	const [formData, setFormData] = useState({
		email: "",
		password: "",
	});

	const navigate = useNavigate();
	const handleChange = (e) => {
		setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
	};

	const handleSubmit = async (e) => {
		e.preventDefault();

		try {
			const postData = {
				email: formData.email,
				password: formData.password,
			};

			const api = axios.create({
				baseURL: baseUrl,
				withCredentials: true,
			});
			const responsePost = await api.post(`${baseUrl}/login`, postData);
			if (responsePost.status === 200) {
				localStorage.setItem("authToken", responsePost.data.token);
				navigate("/search");
				toast.success("Successfully logged in");
			}
		} catch (e) {
			if (e instanceof AxiosError) {
				toast.error(e.response.data.message);
			} else {
				toast("An error occurred while trying to log you in");
			}
		}
	};

	return (
		<Layout>
			<div className='form'>
				<div className='form-header'>
					<h3>Login</h3>
					<p>
						Not a member?{" "}
						<Link to='/registeration' className='login-active'>
							Signup
						</Link>
					</p>
				</div>
				<div className='form-body'>
					<form>
						<div className='form-group '>
							<div>
								<label>Email</label>
								<input
									type='text'
									className='form-control'
									name='email'
									required
									value={formData.username}
									onChange={handleChange}
								/>
							</div>
						</div>

						<div className='form-group '>
							<div>
								<label>Password</label>
								<input
									type='password'
									className='form-control'
									name='password'
									required
									value={formData.password}
									onChange={handleChange}
								/>
							</div>
						</div>

						<div className='form-group btn'>
							<button className='form-button' onClick={handleSubmit}>
								Login
							</button>
						</div>
					</form>
				</div>
			</div>
		</Layout>
	);
};

export default Login;
