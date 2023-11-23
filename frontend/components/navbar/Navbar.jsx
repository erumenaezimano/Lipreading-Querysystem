import React from "react";
import { GiHamburgerMenu } from "react-icons/gi";
import { GrFormClose } from "react-icons/gr";
import image from "../../constants/image";
import { Link, useNavigate } from "react-router-dom";
import "./navbar.css";

const Navbar = () => {
	const [toggleMenu, setToggleMenu] = React.useState(false);
	const token = localStorage.getItem("authToken");
	const navigate = useNavigate();

	const signOut = () => {
		localStorage.removeItem("authToken");
		navigate("/");
	};
	return (
		<nav className='app__navbar'>
			<div className='app__navbar-logo'>
				<img src={image.logo2} alt='app logo' />
			</div>
			<ul className='app__navbar-links'>
				<li className='p__opensans'>
					<Link to='/'>Home</Link>
				</li>
				<li className='p__opensans'>
					<Link to='/dashboard'>Dashboard</Link>
				</li>
				<li className='p__opensans'>
					<Link to='/search'>Search</Link>
				</li>
				<li className='p__opensans'>
					<Link to='/interactive'>Word Association</Link>
				</li>
			</ul>
			<div className='app__navbar-login'>
				{!token ? (
					<>
						<Link to='/login' className='p__opensans'>
							Login
						</Link>
						<Link to='/registeration' className='p__opensans'>
							{" "}
							Registration
						</Link>
					</>
				) : (
					<span className='p__opensans' onClick={signOut}>
						Logout
					</span>
				)}

				<div />
			</div>
			<div className='app__navbar-smallscreen'>
				<GiHamburgerMenu
					color='#fff'
					fontSize={27}
					onClick={() => setToggleMenu(true)}
				/>
				{toggleMenu && (
					<div className='app__navbar-smallscreen_overlay flex__center slide-bottom'>
						<GrFormClose
							fontSize={27}
							className='overlay__close'
							onClick={() => setToggleMenu(false)}
						/>
						<ul className='app__navbar-smallscreen_links'>
							<li>
								<a href='#home' onClick={() => setToggleMenu(false)}>
									Home
								</a>
							</li>
							<li>
								<a href='#dashboard' onClick={() => setToggleMenu(false)}>
									Dashboard
								</a>
							</li>
							<li>
								<a href='#searchpage' onClick={() => setToggleMenu(false)}>
									Search
								</a>
							</li>
							<li>
								<a href='#about' onClick={() => setToggleMenu(false)}>
									Contact
								</a>
							</li>
						</ul>
					</div>
				)}
			</div>
		</nav>
	);
};

export default Navbar;
