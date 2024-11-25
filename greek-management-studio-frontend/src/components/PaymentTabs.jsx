import React from "react";
import { useParams } from "react-router-dom";
import PaymentScreen from "./PaymentScreen";
import PaymentInfo from "./PaymentInfo";
import { Tabs, Tab } from "react-bootstrap";

const PaymentTabs = () => {
  const { id, amount, bill_name } = useParams();

  const billDetails = {
    id,
    amount,
    bill_name,
  };

  return (
    <div className="container mt-4">
      <Tabs defaultActiveKey="paymentScreen" id="payment-tabs" className="mb-3">
        <Tab eventKey="paymentScreen" title="Payment Screen">
          <PaymentScreen {...billDetails} />
        </Tab>
        <Tab eventKey="paymentInfo" title="Payment Info">
          <PaymentInfo />
        </Tab>
      </Tabs>
    </div>
  );
};

export default PaymentTabs;
