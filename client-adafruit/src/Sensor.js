// src/Sensor.js

import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';

function Sensor({ label, value, loading }) {
  return (
    <Card sx={{ minWidth: 275, marginBottom: 3 }}>
      <CardContent>
        <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
          {label}
        </Typography>
        <Typography variant="h5" component="div">
          {loading ? <CircularProgress /> : value}
        </Typography>
      </CardContent>
    </Card>
  );
}

export default Sensor;
