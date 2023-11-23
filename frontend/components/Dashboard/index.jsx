import axios from "axios";
import React, { useEffect, useState } from "react";
import baseUrl from "../../config";
import BarChart from "../BarCharts";
import Layout from "../layout/Layout";
import Loader from "../Loader";

const Dashboard = () => {
	const [data, setData] = useState([]);
	const [wordFrequency, setFrequency] = useState([]);
	const [videodata, setVideoData] = useState([]);
	const [partofSpeechData, setSpeechData] = useState([]);
	const [wordSpeedData, setWordSpeed] = useState([]);
	const [wordLength, setWordLength] = useState([]);
	const [negative, setNegative] = useState([]);
	const [loading, setLoading] = useState(false);

	useEffect(() => {
		const fetchData = async () => {
			try {
				//homophones
				const responseGet = await axios.get(`${baseUrl}/getHomephones`);
				setData(responseGet.data);

				//Word Frequency
				const FrequencyresponseGet = await axios.get(`${baseUrl}//wordFrequency`);
				setFrequency(FrequencyresponseGet.data);

				//video clips
				const videoresponseGet = await axios.get(`${baseUrl}/getVideoclips`);
				setVideoData(videoresponseGet.data);

				//part of speech
				const partofSpeechresponseGet = await axios.get(
					`${baseUrl}/partofspeech`
				);
				setSpeechData(partofSpeechresponseGet.data);

				//word speed
				const wordspeedresponseGet = await axios.get(`${baseUrl}/wordSpeed`);
				setWordSpeed(wordspeedresponseGet.data);

				//word length
				const wordLengthResponse = await axios.get(`${baseUrl}/wordLength`);
				setWordLength(wordLengthResponse.data);

				//word length
				const negativeResponse = await axios.get(`${baseUrl}/negative`);
        setNegative(negativeResponse.data);
        
        setLoading(true)
			} catch (error) {
				console.error("GET API error:", error);
			}
		};

		fetchData(); // Call fetchData inside useEffect
	}, []);

	return (
		<Layout>
			{!loading ? (
				<Loader />
			) : (
				<>
					<BarChart
						type='Linguistic Type Data'
						title='Words With Homophones'
						data={data}
						categoryKey='HH'
						valueKey='record_count'
					/>
					<hr />
					<BarChart
						type='Word Frequency'
						title='Frequency of Words with more than 5 Characters'
						data={wordFrequency}
						categoryKey='word'
						valueKey='record_count'
					/>
					<hr />
					<BarChart
						type='Video Clips Data'
						title='Video Speed'
						data={videodata}
						categoryKey='video_length'
						valueKey='record_count'
					/>
					<hr />
					<BarChart
						type=''
						title='Parts of Speech'
						data={partofSpeechData}
						categoryKey='part_of_speech'
						valueKey='record_count'
					/>
					<BarChart
						type=''
						title='Word Speed'
						data={wordSpeedData}
						categoryKey='word_speed'
						valueKey='record_count'
					/>
					<BarChart
						type='Duration Data'
						title='Word Length'
						data={wordLength}
						categoryKey='word_length'
						valueKey='record_count'
					/>
					<hr />
					<BarChart
						type='Negative Words Table'
						title='Negative Words'
						data={negative}
						categoryKey='word'
						valueKey='record_count'
					/>
				</>
			)}
		</Layout>
	);
};

export default Dashboard;
