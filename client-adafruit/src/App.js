// src/App.js
import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Charts from './pages/Charts';

import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { ThemeProvider } from '@mui/material/styles';
import theme from './theme';

function App() {
    return (
        <BrowserRouter>
            <ThemeProvider theme={theme}>
                <Box sx={{ flexGrow: 1 }}>
                    <AppBar position="static">
                        <Toolbar>
                            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                                Sensor Dashboard
                            </Typography>
                            <Button color="inherit" component={Link} to="/">
                                Home
                            </Button>
                            <Button color="inherit" component={Link} to="/charts">
                                Charts
                            </Button>
                        </Toolbar>
                    </AppBar>
                </Box>
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/charts" element={<Charts />} />
                </Routes>
            </ThemeProvider>
        </BrowserRouter>
    );
}

export default App;

