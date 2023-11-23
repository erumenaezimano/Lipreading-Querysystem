import React, { useState } from "react";
//import styles, { layout } from "../../constants/styles";
//import Button from "../../components/Button";

import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import "./registeration.css";
import Layout from "../layout/Layout";
import { Link, useNavigate } from "react-router-dom";
import axios, { AxiosError } from "axios";
import baseUrl from "../../config";

const Registeration = () => {
	const navigate = useNavigate();
	const [formData, setFormData] = useState({
		username: "",
		email: "",
		password: "",
		confirmPassword: "",
	});

	const handleChange = (e) => {
		setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
	};

	const handleSubmit = async (e) => {
		e.preventDefault();
		if (formData.password !== formData.confirmPassword)
			return toast.error("passwords do not match");

		try {
			const postData = {
				username: formData.username,
				email: formData.email,
				password: formData.password,
			};

			const api = axios.create({
				baseURL: baseUrl,
				withCredentials: true,
			});
			const responsePost = await api.post(`${baseUrl}/register`, postData);
			if (responsePost.status === 200) {
				localStorage.setItem("authToken", responsePost.data.token);
				navigate("/search");
				toast.success("Successfully registered");
			}
		} catch (e) {
			if (e instanceof AxiosError) {
				toast.error(e.response.data.error);
			} else {
				toast("An error occurred while trying to log you in");
			}
		}
	};

	return (
		<Layout>
			<div className='form'>
				<div className='form-header'>
					<h3>Sign Up</h3>
					<p>
						Already a member?{" "}
						<Link to='/login' className='login-active'>
							Log in
						</Link>
					</p>
				</div>
				<div className='form-body'>
					<form>
						<div className='form-group '>
							<div>
								<label>Username</label>
								<input
									type='text'
									className='form-control'
									name='username'
									required
									value={formData.username}
									onChange={handleChange}
								/>
							</div>
						</div>
						<div className='form-group'>
							<div>
								<label>Email</label>
								<input
									type='email'
									className='form-control form-email'
									name='email'
									required
									value={formData.email}
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
						<div className='form-group'>
							<div>
								<label>Confirm Password</label>
								<input
									type='password'
									className='form-control'
									name='confirmPassword'
									required
									value={formData.confirmPassword}
									onChange={handleChange}
								/>
							</div>
						</div>
						<div className='form-group btn'>
							<button className='form-button' onClick={handleSubmit}>
								Register{" "}
							</button>
						</div>
					</form>
				</div>
			</div>
		</Layout>
	);
};

export default Registeration;
