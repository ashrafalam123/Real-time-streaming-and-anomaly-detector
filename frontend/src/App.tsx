import { useEffect, useState } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [allData, setAllData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [latest10, setLatest10] = useState([]); 
  const [showHistory, setShowHistory] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/weather-data");
        console.log('Fetched data:', response.data); // Log the fetched data
        setAllData(response.data.history); // Ensure you're accessing the correct data
        setLatest10(response.data.history.slice(-10).reverse()); // Get the last 10 entries and reverse them
        setLoading(false); // Set loading to false after data is fetched
      } catch (error) {
        console.error('Error fetching data:', error); // Log any errors
      }
    };

    const interval = setInterval(() => {
      fetchData(); // Fetch data every second
    }, 1000);

    // Initial fetch before starting the interval
    fetchData();

    return () => clearInterval(interval); // Clear the interval on component unmount
  }, []); // Empty dependency array means this runs once on mount

  const toggleHistory = () => {
    setShowHistory(!showHistory); // Toggle the history view
  };

  return (
    <div>
      <div className='text-3xl font-bold underline'>
        Weather Data Dashboard
      </div>
      <button 
            onClick={toggleHistory} 
            className="mt-4 bg-blue-500 text-white py-2 px-4 rounded"
          >
            {showHistory ? 'Show Latest 10' : 'Show History'}
      </button>
      {loading ? (
        <div className='text-2xl'>
          Fetching data from server....
        </div>
      ) : (
        <div>
          <div>
          {!showHistory ? (
            <div className="text-2xl font-bold">Latest 10 Entries</div>) : <div></div>}
            {latest10.map((data : any, index) => (
              <div key={index} style={{ color: data.anomaly ? 'red' : 'green' }}>
                <p>Temperature: {data.temperature} °C</p>
                {/* <p>Mean: {data.mean} °C</p>
                <p>Variance: {data.variance}</p> */}
                <p>Anomaly: {data.anomaly ? 'Yes' : 'No'}</p>
                <p>Predicted: {data.predicted ? 'Correct' : 'Incorrect'}</p>
                <hr />
              </div>
            ))}
          </div>

          {showHistory && (
            <div className="mt-4">
              {allData.slice().reverse().map((data : any, index) => ( // Reverse historical data for display
                <div key={index} style={{ color: data.anomaly ? 'red' : 'green' }}>
                  <p>Temperature: {data.temperature} °C</p>
                  {/* <p>Mean: {data.mean} °C</p>
                  <p>Variance: {data.variance}</p> */}
                  <p>Anomaly: {data.anomaly ? 'Yes' : 'No'}</p>
                  <hr />
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
