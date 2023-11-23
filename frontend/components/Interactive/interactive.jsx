"./iframe.css";
import React from "react";

//import Button from "../../components/Button";

import Layout from "../layout/Layout";

const Interactive = () => {
	return (
		<Layout>
			<div id='frame-container' style={{width:"1200px",margin:"20px auto"}}>
				<iframe
					src='https://erumenaezimano.github.io/Viz/'
					width='1200'
					title='Interactive data presentation'
					height='1000'
				></iframe>
			</div>
		</Layout>
	);
};

export default Interactive;