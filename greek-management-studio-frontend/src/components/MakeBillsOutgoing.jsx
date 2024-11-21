import React, { useState } from "react";
import { Form, Button, Container, Row, Col } from "react-bootstrap";
import { useUser } from "../context/user_context";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const MakeBills = () => {
  const [billName, setBillName] = useState("");
  const [chapterContact, setChapterContact] = useState("");
  const [payerName, setPayerName] = useState("");
  const [payerBillAddress, setPayerBillAddress] = useState("");
  const [payerEmail, setPayerEmail] = useState("");
  const [payerPhone, setPayerPhone] = useState("");
  const [dueDate, setDueDate] = useState(new Date());
  const [amount, setAmount] = useState("");

  const user = useUser();

  const make_bill_request = async (e) => {
    e.preventDefault();

    const payload = {
      bill_name: billName,
      chapter_contact: chapterContact,
      payer_name: payerName,
      payer_bill_address: payerBillAddress,
      payer_email: payerEmail,
      payer_phone: payerPhone,
      due_date: dueDate,
      amount: amount,
    };

    try {
      const response = await user.post_with_headers(
        "/api/make-external-bill",
        payload
      );
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
            <Form.Group controlId="setChapterContact" className="mb-3">
              <Form.Label>Chapter Contact Email</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter Chapter Contact Email"
                value={chapterContact}
                onChange={(e) => setChapterContact(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group controlId="setPayerName" className="mb-3">
              <Form.Label>Eneter Invoicee Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter Invoicee Name"
                value={payerName}
                onChange={(e) => setPayerName(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group controlId="setPayerBillAddress" className="mb-3">
              <Form.Label>Enter Invoicee Address</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter Invoicee Address"
                value={payerBillAddress}
                onChange={(e) => setPayerBillAddress(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group controlId="setPayerEmail" className="mb-3">
              <Form.Label>Invoicee Email</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter Invoicee Email"
                value={payerEmail}
                onChange={(e) => setPayerEmail(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group controlId="setPayerPhone" className="mb-3">
              <Form.Label>Invoicee Phone Number</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter Invoicee Phone Number"
                value={payerPhone}
                onChange={(e) => setPayerPhone(e.target.value)}
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
