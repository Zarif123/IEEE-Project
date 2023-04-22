import DragDropFile from './components/DragDropFile';
import logo from './logo.svg';
import React, { useState, useEffect } from "react";
import Uploads from './components/uploads';

import './App.css';

function App() {
  const [data, setdata] = useState({
    name: "",
    age: 0,
    date: "",
    programming: "",
  });
  useEffect(() => {
    // Using fetch to fetch the api from 
    // flask server it will be redirected to proxy
    fetch("/data").then((res) =>
        res.json().then((data) => {
            // Setting a data from api
            setdata({
                name: data.Name,
                age: data.Age,
                date: data.Date,
                programming: data.programming,
            });
        })
    );
}, []);
  return (
    <div className="App">
        <header className="App-header">
            <h1>Img2Ing</h1>
        </header>
          
          <DragDropFile/>
    </div>
  );
}

export default App;
