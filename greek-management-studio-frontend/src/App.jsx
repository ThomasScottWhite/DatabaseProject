import React from 'react';
import Login from './components/Login';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { UserProvider } from './context/user_context';

import 'bootstrap/dist/css/bootstrap.min.css';
import MainPage from './components/MainPage';
import PaymentScreen from './components/PaymentScreen';
import CreateAccount from './components/CreateAccount';
import CreateOrganization from './components/CreateOrganization';

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/mainpage/*" element={<MainPage />} />
          <Route path="/create-account" element={<CreateAccount />} />
          <Route path="/create-organization" element={<CreateOrganization />} />
          <Route path="/payment" element={<PaymentScreen />} />

        </Routes>
      </div>
    </Router>
  );
}
export default App;
