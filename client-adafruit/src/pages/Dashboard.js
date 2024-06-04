// src/Dashboard.js
import React, { useState, useEffect } from 'react';
import { Container, Grid, Typography, Switch, FormControlLabel } from '@mui/material';
import Sensor from '../Sensor';
import useWebSocket from '../useWebSocket';
import axios from 'axios';



function Dashboard() {
    const [temperature, setTemperature] = useState(null);
    const [humidity, setHumidity] = useState(null);
    const [light, setLight] = useState(null);
    const [isLedOn, setIsLedOn] = useState(false);

    const handleMessage = (message) => {
        try {
            const data = JSON.parse(message);
            const topic = data["message"]["topic"];

            if (topic === "temperature"){
                setTemperature(data.message.msg);
            } else if (topic === "humidity") {
                setHumidity(data.message.msg); 
            } else if (topic === "light") {
                setLight(data.message.msg);
            } else if (topic === "led") {
                if (data.message.msg === "True" || data.message.msg === "true") {
                    setIsLedOn(true);
                }
                else {
                    setIsLedOn(false);
                }
            }


        } catch (error){
            console.error("Failed to parse message", message);
        }
    }

    // Start webSocket
    const socket = useWebSocket('ws://127.0.0.1:8000/ws/data/', handleMessage);

    const handleToggle = (event) => {
        
        const newState = event.target.checked;
        setIsLedOn(newState);
        axios.post('http://localhost:8000/api/toggle-led/', { value: newState ? "True" : "False" })
            .then(response => console.log(response.data))
            .catch(error => console.error('Error toggling LED:', error));
    };

    return (
        <Container>
            <Typography variant="h4" gutterBottom>
                Sensor Dashboard
            </Typography>
            <Grid container spacing={3}>
                <Grid item xs={12}>
                    <Sensor label="Temperature" value={`${temperature} °C`} loading={temperature === null} />
                </Grid>
                <Grid item xs={12}>
                    <Sensor label="Humidity" value={`${humidity} %`} loading={humidity === null} />
                </Grid>
                <Grid item xs={12}>
                    <Sensor label="Light" value={`${light} lux`} loading={light === null} />
                </Grid>
                <Grid item xs={12}>
                    <FormControlLabel
                        control={
                            <Switch
                                checked={isLedOn}
                                onChange={handleToggle}
                                color="secondary" 
                                sx={{
                                    '& .MuiSwitch-switchBase.Mui-checked': {
                                        color: '#ff5722', // Thumb color when on
                                        '&:hover': {
                                            backgroundColor: 'rgba(255,87,34,0.08)', // Ripple color when on
                                        },
                                    },
                                    '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
                                        backgroundColor: '#ff5722', // Track color when on
                                    },
                                }}
                            />
                        }
                        label="LED Control"
                    />

                </Grid>
            </Grid>
        </Container>
    );
}

export default Dashboard;
