import React, { useState } from "react";
import { Form, Button, Container, Row, Col } from "react-bootstrap";
import { useUser } from "../context/user_context";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const MakeBills = () => {
  const [dueDate, setDueDate] = useState(new Date());
  const [billName, setBillName] = useState("");
  const [amount, setAmount] = useState("");
  const [invoicee, setInvoicee] = useState("");
  const user = useUser();

  const make_bill_request = async (e) => {
    e.preventDefault();

    const payload = {
      bill_name: billName,
      due_date: dueDate,
      invoicee_id: invoicee,
      amount: amount,
    };

    try {
      const response = await user.post_with_headers("/api/make-bill", payload);
      if (response.ok) {
        alert("Bill Made");
      }
    } catch (error) {
      console.error("Error logging in:", error);
      alert("An error occurred while logging in.");
    }
  };

  return (
    <Container className="mt-5">
      <Row className="justify-content-md-center">
        <Col xs={12} md={6}>
          <h2 className="text-center">Create a Bill</h2>
          <Form onSubmit={make_bill_request}>
            <Form.Group controlId="formBillName" className="mb-3">
              <Form.Label>Bill Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter bill name"
                value={billName}
                onChange={(e) => setBillName(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group controlId="formRecipientEmail" className="mb-3">
              <Form.Label>Invoicee</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter Recipient Email"
                value={invoicee}
                onChange={(e) => setInvoicee(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group controlId="formDueDate" className="mb-3">
              <Form.Label>Due Date</Form.Label>
              <Form.Control
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group controlId="formAmount" className="mb-3">
              <Form.Label>Amount</Form.Label>
              <Form.Control
                type="number"
                placeholder="Enter amount"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                required
              />
            </Form.Group>

            <Button variant="primary" type="submit" className="w-100">
              Submit
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default MakeBills;
