import React from "react";
import ApexCharts from "react-apexcharts";
import "./index.css";

const categoriesAndValues = (arrObj, categoryKey, valueKey) => {
	const categories = arrObj.map((obj) => obj[categoryKey]);
	const categoryValues = arrObj.map((obj) => obj[valueKey]);

	return [categories, categoryValues];
};
const colors=['#EF7C8E','#98D7C2','#EF7C8E','#638C80',"#F4B9B8"]
const BarChart = ({ data, categoryKey, valueKey, title, type }) => {
	const [categories, categoryValues] = categoriesAndValues(
		data,
		categoryKey,
		valueKey
	);
	const index = Math.floor(Math.random() * colors.length)
	const barChartOptions = {
		chart: {
			id: "bar",
		},
		fill: {
			colors: colors[index]
		  },
		xaxis: {
			categories: categories,
		},

		colors: ["#0066f5"],
		plotOptions: {
			bar: {
				horizontal: true,
			},
		},
	};

	const barChartSeries = [
		{
			name: "My Data",
			data: categoryValues.length === 0 ? [1, 1] : categoryValues,
		},
	];

	const chartSeries = categoryValues;
	const chartOptions = {
		labels: categories,
	};

	return (
		<>
			<div className='wrapper-bar'>
				<div className='bar-container'>
					<h2 className='chat-title'> {title}</h2>
					<div className='fig'>
						<ApexCharts
							width={500}
							options={chartOptions}
							series={chartSeries}
							type='pie'
							height={250}
						/>
					</div>
				</div>

				<div className='bar-container'>
					<h2 className='chat-title'> {title}</h2>
					<div className='fig'>
						<ApexCharts
							width={500}
							options={barChartOptions}
							series={barChartSeries}
							type={`${type === "Negative Words Table" ? 'area' : 'bar'}`}
							height={350}
						/>
					</div>
				</div>
			</div>
			<h3 className='img-title'>{type}</h3>
		</>
	);
};

export default BarChart;
