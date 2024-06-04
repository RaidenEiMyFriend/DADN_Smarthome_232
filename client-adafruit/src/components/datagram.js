// Example in App.js of your React app
import React, { useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
  const collectionName = "temperature";  // This can be dynamically set

//   useEffect(() => {
//     axios.get(`http://localhost:8000/api/dashboards/${collectionName}/`)
//          .then(response => {
//              console.log(`Data from Firestore collection "${collectionName}":`, response.data);
//          })
//          .catch(error => console.error('Error fetching data:', error));
//   }, [collectionName]); // Dependency array to re-run effect if collectionName changes

  return (
    <div>
      <h1>Welcome to My React and Django App</h1>
    </div>
  );
}

export default Dashboard;
