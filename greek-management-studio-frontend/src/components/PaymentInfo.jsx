import React, { useState, useEffect } from "react";
import {
  Form,
  Button,
  Table,
  Container,
  Tabs,
  Tab,
  Modal,
} from "react-bootstrap";
import { useUser } from "../context/user_context";

const PaymentInfoComponent = () => {
  const user = useUser();
  const [nickname, setNickname] = useState("");
  const [paymentType, setPaymentType] = useState("card");
  const [details, setDetails] = useState({});
  const [paymentInfo, setPaymentInfo] = useState([]);
  const [bills, setBills] = useState([]);
  const [activeTab, setActiveTab] = useState("all");
  const [showPayModal, setShowPayModal] = useState(false);
  const [selectedBill, setSelectedBill] = useState(null);
  const [paymentAmount, setPaymentAmount] = useState("");

  const fetchPaymentInfo = async () => {
    try {
      const response = await user.get_with_headers(
        "/api/member/" + user.user.email + "/payment_info"
      );

      if (!response.ok) {
        throw new Error("Failed to fetch payment information.");
      }

      const data = await response.json();
      setPaymentInfo(data);
    } catch (error) {
      console.error(error);
      alert("Error fetching payment information.");
    }
  };

  const fetchBills = async () => {
    try {
      const response = await user.get_with_headers("/api/bills");

      if (!response.ok) {
        throw new Error("Failed to fetch bills.");
      }

      const data = await response.json();
      setBills(data);
    } catch (error) {
      console.error(error);
      alert("Error fetching bills.");
    }
  };

  const handleAddPaymentInfo = async (e) => {
    e.preventDefault();

    const newPaymentInfo = {
      member_email: user.user.email,
      nickname,
      ...details,
    };

    try {
      const response = await user.post_with_headers(
        "/api/payment_info",
        newPaymentInfo
      );

      if (!response.ok) {
        throw new Error("Failed to add payment information.");
      }

      alert("Payment information added successfully!");
      fetchPaymentInfo();
    } catch (error) {
      console.error(error);
      alert("Error adding payment information.");
    }
  };

  const handleDeletePaymentInfo = async (paymentId) => {
    try {
      const response = await user.post_with_headers(
        `/api/payment_info/${paymentId}`,
        {
          method: "DELETE",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to delete payment information.");
      }

      alert("Payment information deleted successfully!");
      fetchPaymentInfo();
    } catch (error) {
      console.error(error);
      alert("Error deleting payment information.");
    }
  };

  const handlePayBill = async () => {
    if (!selectedBill || !paymentAmount) {
      alert("Please select a bill and enter a payment amount.");
      return;
    }

    try {
      const response = await user.post_with_headers(
        `/bill/pay/${selectedBill.bill_id}`,
        { payment_amount: parseFloat(paymentAmount) },
        { headers: { Authorization: `Bearer ${user.authToken}` } }
      );

      if (!response.ok) {
        throw new Error("Failed to pay the bill.");
      }

      alert("Bill paid successfully!");
      fetchBills();
      setShowPayModal(false);
    } catch (error) {
      console.error(error);
      alert("Error paying the bill.");
    }
  };

  useEffect(() => {
    fetchPaymentInfo();
    fetchBills();
  }, []);

  return (
    <Container className="mt-5">
      <h2>Manage Payment Information and Pay Bills</h2>
      <Tabs
        activeKey={activeTab}
        onSelect={(k) => setActiveTab(k)}
        className="mb-4"
      >
        <Tab eventKey="all" title="All Payment Info">
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>Nickname</th>
                <th>Details</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {paymentInfo.map((info) => (
                <tr key={info.payment_id}>
                  <td>{info.nickname}</td>
                  <td>{JSON.stringify(info.details)}</td>
                  <td>
                    <Button
                      variant="danger"
                      onClick={() => handleDeletePaymentInfo(info.payment_id)}
                    >
                      Delete
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Tab>
        <Tab eventKey="add_payment" title="Add Payment Info">
          <Form onSubmit={handleAddPaymentInfo} className="mb-4">
            <Form.Group controlId="formNickname" className="mb-3">
              <Form.Label>Nickname</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter nickname"
                value={nickname}
                onChange={(e) => setNickname(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group controlId="formPaymentType" className="mb-3">
              <Form.Label>Payment Type</Form.Label>
              <Form.Control
                as="select"
                value={paymentType}
                onChange={(e) => setPaymentType(e.target.value)}
              >
                <option value="card">Card</option>
                <option value="bank_account">Bank Account</option>
              </Form.Control>
            </Form.Group>
            {paymentType === "card" && (
              <>
                <Form.Group controlId="formCardNumber" className="mb-3">
                  <Form.Label>Card Number</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="Enter card number"
                    onChange={(e) =>
                      setDetails({ ...details, card_num: e.target.value })
                    }
                    required
                  />
                </Form.Group>
                <Form.Group controlId="formExpDate" className="mb-3">
                  <Form.Label>Expiration Date</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="MM-YY"
                    onChange={(e) =>
                      setDetails({ ...details, exp_date: e.target.value })
                    }
                    required
                  />
                </Form.Group>
              </>
            )}
            <Button variant="success" type="submit">
              Add Payment Info
            </Button>
          </Form>
        </Tab>
        <Tab eventKey="bills" title="Pay Bills">
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>Bill ID</th>
                <th>Amount</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {bills.map((bill) => (
                <tr key={bill.bill_id}>
                  <td>{bill.bill_id}</td>
                  <td>{bill.amount}</td>
                  <td>{bill.status}</td>
                  <td>
                    <Button
                      variant="primary"
                      onClick={() => {
                        setSelectedBill(bill);
                        setShowPayModal(true);
                      }}
                    >
                      Pay
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Tab>
      </Tabs>

      {/* Pay Bill Modal */}
      <Modal show={showPayModal} onHide={() => setShowPayModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Pay Bill</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Group controlId="formPaymentAmount" className="mb-3">
            <Form.Label>Payment Amount</Form.Label>
            <Form.Control
              type="number"
              placeholder="Enter payment amount"
              value={paymentAmount}
              onChange={(e) => setPaymentAmount(e.target.value)}
              required
            />
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowPayModal(false)}>
            Cancel
          </Button>
          <Button variant="success" onClick={handlePayBill}>
            Pay
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default PaymentInfoComponent;
