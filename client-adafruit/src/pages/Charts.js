import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './Charts.css'; // Make sure to import your CSS
import { format, parseISO } from 'date-fns';



function Charts() {
    const [temperatureData, setTemperatureData] = useState([]);
    const [humidityData, setHumidityData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const tempResponse = await axios.get('http://localhost:8000/api/data/temperature/');
                const humidityResponse = await axios.get('http://localhost:8000/api/data/humidity/');
                setTemperatureData(formatData(tempResponse.data));
                setHumidityData(formatData(humidityResponse.data));
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
        const intervalId = setInterval(fetchData, 60000);
        return () => clearInterval(intervalId);
    }, []);

    const formatData = (data) => {
        return data.map(item => ({
            name: format(parseISO(item.created_at), 'MM/dd/yyyy HH:mm:ss'), // Using date-fns for formatting
            value: parseFloat(item.value)
        }));
    };

    return (
        <div style={{ width: '90%', display: 'flex', flexDirection: 'column', gap: '100px' }}>
            <div style={{ width: '100%', height: '600px' }}> {/* Ensure each container has enough height */}
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={temperatureData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" height={90} angle={-35} textAnchor="end"/>
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="value" stroke="#8884d8" activeDot={{ r: 8 }} />
                    </LineChart>
                </ResponsiveContainer>
            </div>
            <div style={{ width: '90%', height: '400px' }}> {/* Separate container for the second chart */}
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={humidityData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" height={60} angle={-45} textAnchor="end"/>
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="value" stroke="#82ca9d" activeDot={{ r: 8 }} />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}

export default Charts;




