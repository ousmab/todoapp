import './App.css';
import Menu from './components/base/Menu';
import React from 'react';
import Login from './components/Login';
import Register from './components/Register';
import ErrorPage from './components/ErrorPage';
import Home from './components/home';
import Dashboard from "./components/home/Dashboard"
import Profile from "./components/home/Profile"
import Todos from "./components/home/Todos"

import { BrowserRouter , Routes , Route } from 'react-router-dom';



function App() {

  return (
    
      <BrowserRouter>
          <Menu />
          <Routes>
              <Route path="/" element={<Login />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />

              <Route path="/home" element={<Home /> } >
                    <Route index element={ <Dashboard />  } />
                    <Route path="dashboard" element={ <Dashboard />  } />
                    <Route path="profile" element={ <Profile />  } />
                    <Route path="todos" element={ <Todos />  } />
              </Route>


              <Route path="*" element={<ErrorPage />} />

          </Routes>
      
      </BrowserRouter>
  );
}

export default App;

