import React from 'react';
import { Tabs, Tab, Container } from 'react-bootstrap';
import { Routes, Route } from 'react-router-dom';
import Members from './Members';
import MakeBills from './MakeBills';
import ViewBills from './ViewBills';
import PaymentScreen from './PaymentScreen';
import OutgoingBills from "./OutgoingBills"
const MainPage = () => {
    return (
        <Container className="mt-5">
            <Routes>
                <Route
                    path="/"
                    element={
                        <Tabs defaultActiveKey="members" id="uncontrolled-tab-example" className="mb-3">
                            <Tab eventKey="members" title="Members">
                                <Members />
                            </Tab>
                            <Tab eventKey="make-bills" title="Make Bills">
                                <MakeBills />
                            </Tab>
                            <Tab eventKey="outgoing-bills" title="Outgoing Bills">
                                <OutgoingBills />
                            </Tab>
                            <Tab eventKey="view-bills" title="View Your Bills">
                                <ViewBills />
                            </Tab>
                        </Tabs>
                    }
                />
            </Routes>
        </Container>
    );
};

export default MainPage;
