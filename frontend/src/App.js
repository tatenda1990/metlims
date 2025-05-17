// src/App.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './App.css';

import TestApi from './test_api';


function App() {
  return (
    <div className="App">
      <TestApi />
    </div>
  );
}
export default App;