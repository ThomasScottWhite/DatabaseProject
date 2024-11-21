import React from "react";
import { Tabs, Tab, Container } from "react-bootstrap";
import { Routes, Route } from "react-router-dom";
import Members from "./Members";
import MakeBills from "./MakeBills";
import MakeBillsOutgoing from "./MakeBillsOutgoing";
import ViewBills from "./ViewBills";
import OutgoingBills from "./OutgoingBills";
import { useUser } from "../context/user_context";
const MainPage = () => {
  const user = useUser();
  console.log(user);
  if (!user) {
    return <div>Loading...</div>; // Adjust as needed
  }
  return (
    <Container className="mt-5">
      <Routes>
        <Route
          path="/"
          element={
            <Tabs
              defaultActiveKey="members"
              id="uncontrolled-tab-example"
              className="mb-3"
            >
              <Tab eventKey="members" title="Members">
                <Members />
              </Tab>
              <Tab eventKey="view-bills" title="View Your Bills">
                <ViewBills />
              </Tab>
              {user.user.is_admin && (
                <Tab eventKey="make-bills" title="Make Interal Bills">
                  <MakeBills />
                </Tab>
              )}
              {user.user.is_admin && (
                <Tab eventKey="make-external-bills" title="Make External Bills">
                  <MakeBillsOutgoing />
                </Tab>
              )}
              {user.user.is_admin && (
                <Tab eventKey="outgoing-bills" title="Outgoing Bills">
                  <OutgoingBills />
                </Tab>
              )}
            </Tabs>
          }
        />
      </Routes>
    </Container>
  );
};

export default MainPage;
